from discord.ext import commands
from database import database_init
from utils.fetch_prefix import get_prefix
from utils.shutdown import init_cleanup
import yaml

with open("config.yml") as file:
    bot_config = yaml.load(file, Loader=yaml.FullLoader)

bot = commands.Bot(command_prefix=get_prefix)
startup = False

@bot.listen()
async def on_connect():
    global startup
    if startup is False:
        await database_init.init()
        startup = True

@bot.listen()
async def on_ready():
    print("Bot is READY.")


cogs = ["cogs.basic", "cogs.config", "cogs.gamestats.clash_royale", "cogs.gamestats.fortnite", "cogs.gamestats.League_of_Legends"]


for cog in cogs:
    bot.load_extension(cog)

try:
    bot.run(bot_config["bot"]["token"])
except KeyboardInterrupt:
    init_cleanup(bot)
