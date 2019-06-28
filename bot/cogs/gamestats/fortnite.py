from discord.ext import commands
import discord
from utils.clean import clean_escape
from utils.gamestats import fortnite_fetch
from utils.config import invite
import aiohttp
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit, InvalidPlatform

class Fortnite(commands.Cog, name="Fortnite"):
    def __init__(self, bot):
        self.bot = bot
        self.aiohttpclient = aiohttp.ClientSession()

    @commands.command()
    async def fortnite(self, ctx, platform: str = None, *, username: str = None):
        if platform is None:
            await ctx.send("Oops, it seems you forgot to specify what platform you wanted to fetch stats from.")
            return
        if platform.lower() == "pc":
            request_platform = "pc"
        elif platform.lower() == "ps4":
            request_platform = "psn"
        elif platform.lower() == "xbox":
            request_platform = "xbl"
        else:
            await ctx.send("Platform specified is invalid, valid platforms are: ``pc``, ``ps4`` and ``xbox``.")
            return
        if username is None:
            await ctx.send("Oops, it seems you forgot to specify what username you wanted to look up.")
            return
        try:
            data = await fortnite_fetch(self.aiohttpclient, request_platform, username)
        except Forbidden:
            await ctx.send(f"Uh oh, something seems to be inproperly configured. Please contact the bot maintainer about this over at discord.gg/{await invite()}\nIf you're the bot maintainer please make sure your API keys are valid.")
            return
        except NotFound:
            await ctx.send("A player with that username could not be found, **Note:** we are asking you for your epic username, and its also important that the platform paramater is correct aswell.")
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
        embed = discord.Embed(title=f"Paperplane showing lifetime stats for Fortnite player: {await clean_escape(data['epicUserHandle'])}, on platform: {await clean_escape(data['platformNameLong'])}")
        embed.set_author(name="paperplane", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text="Portions of the materials used are trademarks and/or copyrighted works of Epic Games, Inc. All rights reserved by Epic. This material is not official and is not endorsed by Epic.")
        for stat in data["lifeTimeStats"]:
            embed.add_field(name=stat["key"], value=stat["value"], inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fortnite(bot))
