from discord.ext import commands
from database.models import GuildSettings
from tortoise.exceptions import DoesNotExist

async def get_prefix(bot, message):
    try:
        guild = await GuildSettings.get(guild_id=message.guild.id)
    except DoesNotExist:
        await GuildSettings.create(guild_id=message.guild.id, prefix="!")
        return commands.when_mentioned_or("!")(bot, message)
    return commands.when_mentioned_or(guild.prefix)(bot, message)
