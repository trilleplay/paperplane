from discord.ext import commands
import yaml

with open("config.yml") as file:
    bot_config = yaml.load(file)

async def get_prefix(bot, message):
    prefix = ["yeet"]
    return commands.when_mentioned_or(*prefix)(bot, message)

bot = commands.Bot(command_prefix=get_prefix)

cogs = ["cogs.basic"]

for cog in cogs:
    bot.load_extension(cog)

bot.run(bot_config["bot"]["token"])
