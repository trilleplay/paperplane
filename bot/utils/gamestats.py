import yaml
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit

with open("config.yml") as file:
    bot_config = yaml.load(file, Loader=yaml.FullLoader)

async def clash_royale_fetch(client, usertag: str):
    headers = {
    'Authorization': f"Bearer {bot_config['games']['clash_royale']}",
    'cache-control': "no-cache"
    }
    async with client.get(f"https://api.clashroyale.com/v1/players/%23{usertag}", headers=headers) as resp:
        # here it is
        if resp.status == 403:
            raise Forbidden("Invalid Authorization.")
        if resp.status == 404:
            raise NotFound("Player not found.")
        if resp.status == 500:
            raise Unknown()
        if resp.status == 503:
            raise Unavailable()
        if resp.status == 429:
            raise RateLimit()
        if resp.status == 200:
            return await resp.json()
        else:
            raise Unknown()
