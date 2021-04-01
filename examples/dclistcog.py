import dclist
import logging

log = logging.getLogger(__name__)

from discord.ext import commands, tasks

class dclistpy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dclistapi = dclist.DCLClient(bot)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=120.0)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        try:
            await self.dclistapi.postBotStats()
        except dclist.DCListException as e:
            log.warning(e)
        else:
            log.info('Posted stats to dclist.net successfully')
    
    @commands.group(invoke_without_command=True)
    async def dclist(self, ctx):
        await ctx.send('available commands -> `dclist bot $botId` `dclist user $userId` `dclist voted $userId`')

    @dclist.command(name="bot")
    async def get_dclist_bot(self, ctx, bot_id):
        bot = await self.dclistapi.getBotById(bot_id)
        to_send = f"found bot {bot['username']} using this github {bot['github']} and vote_count is {bot['stats']['voteCount']}"
        await ctx.send(to_send)

    @dclist.command(name="me")
    async def get_dclist_user(self, ctx):
        user = await self.dclistapi.getUserById(ctx.author.id)
        to_send = f"found user {user['username']} using this website {user['website']} and discriminator is {user['discriminator']}"
        await ctx.send(to_send)

    @dclist.command(name="voted")
    async def get_dclist_user(self, ctx, user_id):
        is_voted = await self.dclistapi.isUserVoted(user_id)
        if is_voted:
            await ctx.send('yessir, i did voted from this dude.')
        else:
            await ctx.send('this user is not voted :(')

def setup(bot):
    bot.add_cog(dclistpy(bot))