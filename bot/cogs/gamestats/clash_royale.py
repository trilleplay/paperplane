from discord.ext import commands
import discord
from utils.clean import clean_escape
from utils.gamestats import clash_royale_fetch
from utils.config import invite
import aiohttp
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit

class ClashRoyale(commands.Cog, name="Clash Royale"):
    def __init__(self, bot):
        self.bot = bot
        self.aiohttpclient = aiohttp.ClientSession()

    @commands.group()
    async def croyale(self, ctx):
        """Base command for Clash Royale"""
        if ctx.invoked_subcommand is None:
            await ctx.send('No arguments specified, valid arguments are ``player``.')


    @croyale.command()
    async def player(self, ctx, usertag: str = None):
        """Provides stats about a Clash Royale player, syntax: (prefix)croyale player <usertag>"""
        if usertag is None:
            await ctx.send("Oops, it seems you forgot to specify what usertag you wanted to look up.\nYou get your usertag by simply start the game, and from there navigate into your player profile, and under your username you should see a # followed by a few letters, those letters is your usertag!")
            return
        async with ctx.typing():
            try:
                data = await clash_royale_fetch(self.aiohttpclient, usertag)
            except Forbidden:
                invite_key = await invite()
                await ctx.send(f"Uh oh, something seems to be inproperly configured. Please contact the bot maintainer about this over at discord.gg/{invite_key}\nIf you're the bot maintainer please make sure your API keys are valid.")
                return
            except NotFound:
                await ctx.send("A player with that tag could not be found, **Note:** we are asking you for your player tag (**excluding the #**) **not** your username!\nYou get your usertag by simply start the game, and from there navigate into your player profile, and under your username you should see a # followed by a few letters, those letters is your usertag!")
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
            embed = discord.Embed(title=f"{self.bot.user.name} showing stats for Clash Royale player: {await clean_escape(data['name'])}")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url_as(static_format='png', size=1024))
            embed.set_footer(text="This content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell’s Fan Content Policy: www.supercell.com/fan-content-policy.")

            embed.add_field(name="Arena", value=f"{await clean_escape(data['name'])} is on {data['arena']['name']} right now.", inline=True)
            embed.add_field(name="Level", value=f"{await clean_escape(data['name'])} is right now on level {data['expLevel']}.", inline=True)
            embed.add_field(name="Wins", value=f"{await clean_escape(data['name'])} has won {data['wins']} games.", inline=True)
            embed.add_field(name="Losses", value=f"{await clean_escape(data['name'])} has lost {data['losses']} games.", inline=True)
            embed.add_field(name="Clan", value=f"{await clean_escape(data['name'])} is a member of the clan: **{await clean_escape(data['clan']['name'])}** (``{await clean_escape(data['clan']['tag'])}``).", inline=True)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ClashRoyale(bot))
