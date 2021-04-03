"""
MIT License

Copyright (c) 2021 ilkergzlkkr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging, os
import typing as t

from . import errors
from .gqlhttp import GQLHTTPClient

log = logging.getLogger(__name__)

class DCLClient:
    """
    API wrapper for dclist.net
    --------------------------
    Parameters
    ----------
    bot: discord.Client
        An instance of a discord.py Client object.
    token: str
        Your bot's Dclist.Net API Token.

    **loop: Optional[event loop]
        An `event loop` to use for asynchronous operations.
        Defaults to ``bot.loop``.
    **transporter: Optional[gql.transport]
        A `gql.transport` to use for transporting graphql queries.
    """

    def __init__(self, bot, api_token: t.Optional[str]=None, *args, **kwargs):
        if api_token is None:
            log.warning("No Token Provided. DCLClient never gonna post bot stats.")
        self.bot = bot
        self.bot_id = None
        self.loop = kwargs.get("loop", bot.loop)
        self.http = GQLHTTPClient(api_token, loop=self.loop, transporter=kwargs.get('transporter'))

    async def __get_ready(self):
        await self.bot.wait_until_ready()
        if self.bot_id is None:
            self.bot_id = self.bot.user.id
    
    async def _get_app_info(self):
        await self.__get_ready()
        return self.bot_id, (await self.bot.application_info()).owner.id


    async def postBotStats(self, guild_count: t.Optional[int]=None,
            user_count: t.Optional[int]=None, shard_count: t.Optional[int]=None):
        """
        Post bot stats to the API
        Parameters
        ----------
            :param guild_count: Guild count (optional)
            :param user_count: User count (optional)
            :param shard_count: User count (optional)
        """
        await self.__get_ready()
        if guild_count is None:
            guild_count = len(self.bot.guilds)
        if user_count is None:
            user_count = len(list(self.bot.get_all_members()))
        data = await self.http.postBotStats(guild_count, user_count, shard_count)
        return data['postBotStats']

    async def getBotById(self, bot_id: t.Optional[int]) -> dict:
        """
        Get a bot listed on dclist.net
        Parameters
        ----------
            :param bot_id: Bot id to be fetched
        if bot_id is not given. self bot will be used for getting stats.
        Returns
        -------
            bot: Bot as a dict fetched from gql-api
        """
        if bot_id is None:
            bot_id, _ = await _get_app_info()

        data = await self.http.getBotById(bot_id)
        return data['getBot']

    async def getUserById(self, user_id: t.Optional[int]) -> dict:
        """
        Get a user from dclist.net.
        Parameters
        ----------
            :param user_id: User id to be fetched.
        if user_id is not given. self bot owner will be used for getting stats.
        Returns
        -------
            user: User as a dict fetched from gql-api.
        """
        if user_id is None:
            _, user_id = await _get_app_info()

        data = await self.http.getUserById(user_id)
        return data['getUser']

    async def isUserVoted(self, user_id: t.Optional[int]) -> bool:
        """
        Is user voted for my bot from dclist.net.
        Parameters
        ----------
            :param user_id: User id to be checked.
        if user_id is not given. self bot owner will be used for getting voted info.
        Returns
        -------
            :return bool: True or False is user voted.
        """
        if user_id is None:
            _, user_id = await _get_app_info()

        data = await self.http.isUserVoted(user_id)
        return data['isUserVoted']

    async def getUserComment(self, user_id: t.Optional[int]) -> dict:
        """
        Get a user comment from dclist.net from your bot page.
        Parameters
        ----------
            :param user_id: User id to be checked.
        if user_id is not given. self bot owner will be used for getting comment info.
        Returns
        -------
            :return Comment: Comment stats as a dict fetched from gql-api.
        given user must be commented to your any bots. if not so. return value will be None.
        """
        if user_id is None:
            _, user_id = await _get_app_info()

        data = await self.http.getUserComment(user_id)
        return data['getUserComment']
