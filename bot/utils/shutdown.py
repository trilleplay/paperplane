from database import database_init

def init_cleanup(bot):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cleanup(bot))

async def cleanup(bot):
    await database_init.close()
    await bot.logout()
