from discord.ext import commands
import discord
from utils.clean import clean_escape
from utils import gamestats
from utils.config import invite
import aiohttp
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit

class GameStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aiohttpclient = aiohttp.ClientSession()

    @commands.command()
    async def croyale(self, ctx, type: str, usertag: str):
        if type == "player":
            try:
                data = await gamestats.clash_royale_fetch(self.aiohttpclient, usertag)
            except Forbidden:
                await ctx.send(f"Uh oh, something seems to be inproperly configured. Please contact the bot maintainer about this over at discord.gg/{invite}\nIf you're the bot maintainer please make sure your API keys are valid.")
                return
            except NotFound:
                await ctx.send("A player with that tag could not be found, **Note:** we are asking you for your player tag (excluding the #) **not** your username!")
                return
            except Unavailable:
                await ctx.send("It seems that Clash Royales API is having problems at the moment :(\nPlease try again in a few moments.")
                return
            except RateLimit:
                await ctx.send("Uh oh, a lot of users are using our service and while we love this **HYPE**, we are limited on how fast we can check your and everyones stats.\nPlease retry again in a few moments once this has calmed down.")
                return
            except Unknown:
                await ctx.send("Oh no :(, it seems like the API we use to get your game stats is having some issues at the moment, hopefully this will be resolved soon.")
                return
            embed = discord.Embed(title=f"Paperplane showing stats for Clash Royale player: {await clean_escape(data['name'])}")
            embed.set_author(name="paperplane", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_footer(text="This content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell’s Fan Content Policy: www.supercell.com/fan-content-policy.")

            embed.add_field(name="Arena", value=f"{await clean_escape(data['name'])} is on {data['arena']['name']} right now.", inline=True)
            embed.add_field(name="Level", value=f"{await clean_escape(data['name'])} is right now on level {data['expLevel']}.", inline=True)
            embed.add_field(name="Wins", value=f"{await clean_escape(data['name'])} has won {data['wins']} games.", inline=True)
            embed.add_field(name="Losses", value=f"{await clean_escape(data['name'])} has lost {data['losses']} games.", inline=True)
            embed.add_field(name="Clan", value=f"{await clean_escape(data['name'])} is a member of the clan: **{await clean_escape(data['clan']['name'])}** (``{await clean_escape(data['clan']['tag'])}``).", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Uh oh, the type you specified was not valid. Valid types are ``player``.")


def setup(bot):
    bot.add_cog(GameStats(bot))
