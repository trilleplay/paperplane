from discord.ext import commands
from utils.clean import clean_escape
from database.models import GuildSettings

class Config(commands.Cog, name="Configure"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_prefix(self, ctx, prefix: str = None):
        guild = await GuildSettings.get(guild_id=ctx.guild.id)
        if prefix is None:
            frick_strings = await clean_escape(guild.prefix)
            await ctx.send(f"Since you did not provide your new prefix, here is your current prefix: ``{frick_strings}``")
        elif len(prefix) > 5:
            await ctx.send("A prefix can't be longer then five characters, sorry :(")
        else:
            guild.prefix = prefix
            await guild.save()
            frick_strings = await clean_escape(guild.prefix)
            await ctx.send(f"🎉 Alright, your prefix has now been changed to: ``{frick_strings}``")

def setup(bot):
    bot.add_cog(Config(bot))
