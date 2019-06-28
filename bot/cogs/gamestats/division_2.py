from discord.ext import commands
import discord
from utils.convert import Division_2PlatformConverter
from utils.clean import clean_escape
from utils.gamestats import division_2_fetch
from utils.config import invite
import aiohttp
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit, InvalidPlatform

class Division_2(commands.Cog, name="The Division 2"):
    def __init__(self, bot):
        self.bot = bot
        self.aiohttpclient = aiohttp.ClientSession()

    @commands.command()
    async def division(self, ctx, platform: Division_2PlatformConverter = None, *, username: str = None):
        """Provides stats about a The Division 2 player, valid platforms are Uplay, PS4 and Xbox. syntax: (prefix)division <platform> <username>"""
        if platform is None:
            await ctx.send("Oops, it seems you forgot to specify what platform you wanted to fetch stats from. Valid platforms are: ``uplay``, ``ps4`` and ``xbox``.")
            return
        if platform == "invalid":
            await ctx.send("Platform specified is invalid, valid platforms are: ``uplay``, ``ps4`` and ``xbox``.")
            return
        if username is None:
            await ctx.send("Oops, it seems you forgot to specify what username you wanted to look up.")
            return
        async with ctx.typing():
            try:
                data = await division_2_fetch(self.aiohttpclient, platform["value"], username)
            except Forbidden:
                await ctx.send(f"Uh oh, something seems to be inproperly configured. Please contact the bot maintainer about this over at discord.gg/{await invite()}\nIf you're the bot maintainer please make sure your API keys are valid.")
                return
            except NotFound:
                await ctx.send("A player with that username could not be found, **Note:** make sure your username is 100% correct, and its also important that the platform paramater is correct aswell. Otherwise we cant find it :(")
                return
            except Unavailable:
                await ctx.send("It seems that Tracker Networks API is having problems at the moment :(\nPlease try again in a few moments.")
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
            embed = discord.Embed(title=f"{self.bot.user.name} showing lifetime stats for Division 2 player: {await clean_escape(data['data']['metadata']['platformUserHandle'])}, on platform: {await clean_escape(platform['name'])}")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url_as(static_format='png', size=1024))
            embed.set_thumbnail(url=data['data']['metadata']['avatarUrl'])
            embed.set_footer(text=f"{self.bot.user.name} is in no way endorsed by Ubisoft. Ubisoft are the trademark holders of the Division 2, and is in no way responsible for {self.bot.user.name} or the content it provides.")
            for stat in data['data']['stats']:
                embed.add_field(name=stat["metadata"]["name"], value=stat["displayValue"], inline=True)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Division_2(bot))
