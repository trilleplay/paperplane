from discord.ext import commands
import yaml

with open("config.yml") as file:
    bot_config = yaml.load(file, Loader=yaml.FullLoader)

async def get_prefix(bot, message):
    prefix = ["yeet"]
    return commands.when_mentioned_or(*prefix)(bot, message)

bot = commands.Bot(command_prefix=get_prefix)

cogs = ["cogs.basic", "cogs.gamestats"]

for cog in cogs:
    bot.load_extension(cog)

bot.run(bot_config["bot"]["token"])
