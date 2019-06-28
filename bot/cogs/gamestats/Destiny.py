from discord.ext import commands
import discord
from utils.convert import BungieMembershipTypeConverter
from utils.clean import clean_escape
from utils.gamestats import destiny_fetch
from utils.config import invite
import aiohttp
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit, InvalidPlatform

class Destiny_2(commands.Cog, name="Destiny 2"):
    def __init__(self, bot):
        self.bot = bot
        self.aiohttpclient = aiohttp.ClientSession()

    @commands.command()
    async def destiny(self, ctx, platform: BungieMembershipTypeConverter = None, *, username: str = None):
        if platform is None:
            await ctx.send("Oops, it seems you forgot to specify what platform you wanted to fetch stats from.")
            return
        if platform == "invalid":
            await ctx.send("Oops, the platform you specified seems to be invalid, valid platforms are: ``Blizzard``, ``Xbox`` and ``PSN``.")
            return
        if username is None:
            await ctx.send("Oops, it seems you forgot to specify what username you wanted to look up.")
            return
        async with ctx.typing():
            try:
                embed = await destiny_fetch(self.aiohttpclient, self.bot.user.name, platform, username)
            except Forbidden:
                await ctx.send(f"Uh oh, something seems to be inproperly configured. Please contact the bot maintainer about this over at discord.gg/{await invite()}\nIf you're the bot maintainer please make sure your API keys are valid.")
                return
            except NotFound:
                await ctx.send("A player with that username could not be found, make sure you spellt everything correctly, its also important that the platform paramater is correct aswell.")
                return
            except Unavailable:
                await ctx.send("It seems that Riot Games API is having problems at the moment :(\nYou can track its issues over at: <https://developer.riotgames.com/api-status/>.")
                return
            except RateLimit:
                await ctx.send("Uh oh, a lot of users are using our service and while we love this **HYPE**, we are limited on how fast we can check your and everyones stats.\nPlease retry again in a few moments once this has calmed down.")
                return
            except Unknown:
                await ctx.send("Oh no :(, it seems like the API we use to get your game stats is having some issues at the moment, hopefully this will be resolved soon.")
                return
            except InvalidPlatform:
                await ctx.send("Shit, something just happend that there are checks in place for how did this happen, please open an issue here: <https://github.com/trilleplay/paperplane/issues>.")
                return
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Destiny_2(bot))
