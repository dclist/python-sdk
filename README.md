# DCList.net Python SDK

This module is official python sdk for dclist.net.

It's open-source and always open to prs and contributions.

## Installation

You can install package via [pip](https://www.pypi.org/dclist.py) or [github](https://github.com/dclist/python-sdk) with following commands :

**Recomended**:
```
pip install dclist.py
```

or

```sh
git clone https://github.com/dclist/python-sdk.git
cd python-sdk
python -m venv env
pip install .
```

## Gettings Started

### Posting botstats automaticly as a Cog:
```py
import dclist

from discord.ext import commands, tasks

class dclistpy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dclistapi = dclist.DCLClient(bot, "YOUR_TOKEN_HERE")
        # you can get the token from your bot's page on dclist.net
        # you have option to pass your token as environment variable as `DCLIST_TOKEN`
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        try:
            await self.dclistapi.postBotStats()
        except dclist.DCListException as e:
            print(e)
            # print sucs lol use logger instead :walter_the_dog:
        else:
            print('Posted stats to dclist.net successfully')

def setup(bot):
    bot.add_cog(dclistpy(bot))
```

### Getting bot or user info from api:
```py
    @commands.group(invoke_without_command=True)
    async def dclist(self, ctx):
        await ctx.send('available commands -> `dclist bot` `dclist user` `dclist voted`')

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
```
## More

You can use sdk to get more information like `getUserComment`.