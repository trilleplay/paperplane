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

@bot.listen()
async def on_guild_join(guild):
    if guild.system_channel:
        await guild.system_channel.send(f"Heya!\nThanks for adding me, to get a list of all commands run ``!help``. Don't like the current prefix? No problem you can change it by sending ``!set_pefix NEW_AND_AWESOME_PREFIX_HERE``, or if you forget your prefix: ``@{str(bot.user)} set_pefix NEW_AND_AWESOME_PREFIX_HERE``")


cogs = ["cogs.basic", "cogs.config", "cogs.gamestats.clash_royale", "cogs.gamestats.fortnite", "cogs.gamestats.League_of_Legends", "cogs.gamestats.Destiny", "cogs.gamestats.apex", "cogs.gamestats.division_2"]


for cog in cogs:
    bot.load_extension(cog)

try:
    bot.run(bot_config["bot"]["token"])
except KeyboardInterrupt:
    init_cleanup(bot)
