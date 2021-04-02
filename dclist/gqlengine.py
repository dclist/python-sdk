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
import json
import asyncio
from gql import Client, gql
try:
    from gql.transport.aiohttp import AIOHTTPTransport
    from gql.transport.websockets import WebsocketsTransport
except ModuleNotFoundError:
    raise DeprecationWarning('please uninstall gql and install with "pip install --pre gql[aiohttp,websockets]"')
from gql.transport import exceptions

from .helpers.queries import Queries
from . import errors

log = logging.getLogger(__name__)

def json_or_text(response, *, retry=False):
    try:
        return json.loads(response)
    except Exception as e:
        if retry:
            response = response.replace("'", '"')
            return json_or_text(response)
        return response
 

class GQLEngine:

    BASE = 'https://api.dclist.net/graphql'
    WSS = 'wss://api.dclist.net/subscribe'
    # we're using gql-aiohttp/wss api but this sdk can provide rest api ? :thinking:

    def __init__(self, api_token, *args, **kwargs):
        self.loop = kwargs.get('loop') or asyncio.get_event_loop()
        self.token_provided = api_token is not None
        self.__auth = 'Sdk '+ (api_token or os.getenv('DCLIST_TOKEN') or '')

        self.force_ws = kwargs.get('always_use_websockets', True) is True

        headers = {"Authorization": self.__auth}
        self._ws_transporter = kwargs.get('ws_transporter') or WebsocketsTransport(url=self.WSS, headers=headers, init_payload={"headers": headers})
        self._transporter = kwargs.get('transporter') or AIOHTTPTransport(url=self.BASE, headers=headers)


    async def subscribe(self, query, variable_values: t.Optional[dict]=None):
        async with Client(transport=self._ws_transporter) as session:
            exc = None
            try:
                log.debug('SUBSCRIBING TO WS :: %s', query)
                async for notif in session.transport.subscribe(gql(query), variable_values=variable_values): #geneartor object to be subscribed.
                    log.debug('WS RAW RESPONSE :: %s', notif)
                    response = json_or_text(notif.data)
                    log.debug('WS RESPONSE :: %s', response)
                    yield response
            except (exceptions.TransportQueryError, 
                exceptions.TransportServerError) as e:
                exc = e
            self.handle_exc(exc)


    async def execute(self, query, variable_values: t.Optional[dict]=None):
        t = self._ws_transporter if self.force_ws else self._transporter
        async with Client(transport=t) as session:
            exc = None
            try:
                raw_response = await session.execute(gql(query), variable_values=variable_values)
                log.debug('RAW_RESPONSE :: %s', raw_response)
                response = json_or_text(raw_response)
                log.debug('json payload :: %s', response)
                return response
            except (exceptions.TransportQueryError, 
                exceptions.TransportServerError) as e:
                exc = e
            self.handle_exc(exc)

    def handle_exc(self, e):
        if e is None:
            return
        data = json_or_text(str(e), retry=True)
        exc = errors.HTTPException(e.__repr__(), data)
        code = getattr(exc, 'code', '') 
        log.debug('raised exc. code=%s, message=%s', code, exc.text)
        if 'rate limit' in exc.text or code == 'RATE_LIMIT':
            log.warning('we are being ratelimited from dclist.net gql-api')
        elif code == 'BAD_USER_INPUT':
            raise errors.ClientException(exc.text, code)
        elif code == 'UNAUTHORIZED':
            raise errors.Unauthorized
        elif code == 'INTERNAL_SERVER_ERROR':
            log.warning('ugh dclist.net internal error occured while executing.')
        raise exc

    async def subscribe_to_events(self):
        raw_query = Queries.SDKUpdateSubcription
        query = Queries.fields(raw_query, '')
        params = {'topics': ['SDK_NEW_COMMENT', 'SDK_NEW_VOTE']}
        subscription = self.subscribe(query, params)
        async for n in subscription:
            yield n['sdkUpdates']

    async def postBotStats(self, guild_count, user_count, shard_count):
        query = Queries.postBotStats
        params = {"stats": {
            "guildCount": guild_count,
            "userCount": user_count,
            "shardCount": shard_count or 1}}
        if self.token_provided or os.getenv('DCLIST_TOKEN'):
            log.debug('posted bot stats, guild_count=%s, user_count=%s, shard_count=%s', guild_count, user_count, (shard_count or 1))
            return await self.execute(query, params)
            # {'postBotStats': True}

        return {'postBotStats': False}

    async def getBotById(self, bot_id):
        raw_query = Queries.getBotById
        fields = Queries.bot_fields()
        query = Queries.fields(raw_query, fields)
        params = {"botId": str(bot_id)}
        return await self.execute(query, params)
        # {'getBot': {'id': '297343587538960384', 'username': 'Eevnxxbot', 'website': 'https://eevnxx.tk' ...}}

    async def getUserById(self, user_id):
        raw_query = Queries.getUser
        fields = Queries.user_fields()
        query = Queries.fields(raw_query, fields)
        params = {"userId": str(user_id)}
        return await self.execute(query, params)
        # {'getUser': {'id': '223071656510357504', 'username': 'Eevnxx', 'discriminator': '4378', 'github': https://github.com/ilkergzlkkr ...}}

    async def isUserVoted(self, user_id):
        query = Queries.isUserVoted
        params = {"userId": str(user_id)}
        return await self.execute(query, params)
        # {'isUserVoted': False}

    async def getUserComment(self, user_id):
        raw_query = Queries.getUserComment
        fields = Queries.comment_fields()
        query = Queries.fields(raw_query, fields)
        params = {"userId": str(user_id)}
        return await self.execute(query, params)
        # {'getUserComment': None}
