import yaml
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit, InvalidPlatform
from utils.config import clash_royale, tracker_network
import urllib.parse

with open("config.yml") as file:
    bot_config = yaml.load(file, Loader=yaml.FullLoader)

async def clash_royale_fetch(client, usertag: str):
    headers = {
    'Authorization': f"Bearer {await clash_royale()}",
    'cache-control': "no-cache"
    }
    async with client.get(f"https://api.clashroyale.com/v1/players/%23{urllib.parse.quote(usertag)}", headers=headers) as resp:
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

async def fortnite_fetch(client, platform: str, username: str):
    if platform == "pc":
        pass
    elif platform == "psn":
        pass
    elif platform == "xbl":
        pass
    else:
        raise InvalidPlatform("Platform is not: pc, psn or xbl.")
    headers = {
    'TRN-Api-Key': await tracker_network(),
    'cache-control': "no-cache"
    }
    async with client.get(f"https://api.fortnitetracker.com/v1/profile/{platform}/{urllib.parse.quote(username)}", headers=headers) as resp:
        # here it is
        json = await resp.json()
        try:
            if json["error"] == "Player Not Found":
                raise NotFound()
        except KeyError:
            pass
        if resp.status == 401:
            raise Forbidden("Invalid Authorization.")
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
