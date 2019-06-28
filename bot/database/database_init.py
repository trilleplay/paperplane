from tortoise import Tortoise
from utils.config import postgres

async def init():
    await Tortoise.init(db_url=await postgres(), modules={'models': ['database.models']})
    await Tortoise.generate_schemas()

async def close():
    await Tortoise.close_connections()
