from discord.ext import commands
import discord
from utils.convert import LeagueRegionConverter, LeagueUserConverter
from utils.clean import clean_escape
from utils.gamestats import league_fetch
from utils.config import invite
import aiohttp
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit, InvalidPlatform

class League_of_Legends(commands.Cog, name="League of Legends"):
    def __init__(self, bot):
        self.bot = bot
        self.aiohttpclient = aiohttp.ClientSession()

    @commands.command()
    async def league(self, ctx, region: LeagueRegionConverter = None, *, username: LeagueUserConverter = None):
        if region is None:
            await ctx.send("Oops, it seems you forgot to specify what region you wanted to fetch stats from.")
            return
        if region == "invalid":
            await ctx.send("Oops, the region you specified seems to be invalid.")
            return
        if username is None:
            await ctx.send("Oops, it seems you forgot to specify what username you wanted to look up.")
            return
        if username is False:
            await ctx.send("Oops, your username doesnt seem to be valid :(")
            return
        async with ctx.typing():
            try:
                data = await league_fetch(self.aiohttpclient, region["api"], username)
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
            embed = discord.Embed(title=f"{self.bot.user.name} showing stats for League of Legends player: {await clean_escape(data['username'])}, on region: {await clean_escape(region['name'])}")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url_as(static_format='png', size=1024))
            embed.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/9.13.1/img/profileicon/{data['profile_image']}.png")
            embed.set_footer(text=f"{self.bot.user.name} isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.")
            embed.add_field(name="Username", value=await clean_escape(data["username"]), inline=True)
            embed.add_field(name="Summoner Level", value=data["level"], inline=True)
            if data["league_entries"] == []:
                embed.add_field(name="Oops", value="No activity can be detected for your account :(", inline=True)
            else:
                for league_entry in data["league_entries"]:
                    if league_entry["queueType"] == "RANKED_SOLO_5x5":
                        embed.add_field(name="Ranked tier", value=league_entry["tier"], inline=True)
                        embed.add_field(name="Ranked wins", value=league_entry["wins"], inline=True)
                        embed.add_field(name="Ranked losses", value=league_entry["losses"], inline=True)
                        embed.add_field(name="Ranked league points", value=league_entry["leaguePoints"], inline=True)
                        embed.add_field(name="Ranked rank", value=f"**{league_entry['rank']}**", inline=True)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(League_of_Legends(bot))
