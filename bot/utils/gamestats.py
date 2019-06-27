import yaml
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit, InvalidPlatform
from utils.config import clash_royale, tracker_network, riot_games
import urllib.parse
import asyncio

with open("config.yml") as file:
    bot_config = yaml.load(file, Loader=yaml.FullLoader)

async def clash_royale_fetch(client, usertag: str):
    headers = {
    'Authorization': f"Bearer {await clash_royale()}",
    'cache-control': "no-cache"
    }
    async with client.get(f"https://api.clashroyale.com/v1/players/%23{urllib.parse.quote(usertag)}", headers=headers) as resp:
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

async def league_fetch(client, region: str, username: str):
    headers = {
    'X-Riot-Token': await riot_games(),
    'cache-control': "no-cache"
    }
    async with client.get(f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{urllib.parse.quote(username)}", headers=headers) as resp:
        if resp.status == 401:
            raise Forbidden("No api key.")
        elif resp.status == 403:
            raise Forbidden("Invalid Authorization.")
        elif resp.status == 404:
            raise NotFound("Player not found.")
        elif resp.status == 500:
            raise Unknown("Internal server error")
        elif resp.status == 502:
            raise Unknown("Bad gateway")
        elif resp.status == 504:
            raise Unknown("Gateway timeout")
        elif resp.status == 503:
            raise Unavailable("Service unavailable")
        elif resp.status == 429:
            raise RateLimit("Rate limit exceeded")
        elif resp.status == 200:
            summoner_lookup = await resp.json()
        else:
            raise Unknown()
        await asyncio.sleep(1)
        async with client.get(f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{urllib.parse.quote(summoner_lookup['id'])}", headers=headers) as resp:
            if resp.status == 401:
                raise Forbidden("No api key.")
            elif resp.status == 403:
                raise Forbidden("Invalid Authorization.")
            elif resp.status == 404:
                raise NotFound("Player not found.")
            elif resp.status == 500:
                raise Unknown("Internal server error")
            elif resp.status == 502:
                raise Unknown("Bad gateway")
            elif resp.status == 504:
                raise Unknown("Gateway timeout")
            elif resp.status == 503:
                raise Unavailable("Service unavailable")
            elif resp.status == 429:
                raise RateLimit("Rate limit exceeded")
            elif resp.status == 200:
                league_entries = await resp.json()
            else:
                raise Unknown()
        summoner = {
            "username": summoner_lookup["name"],
            "level": summoner_lookup["summonerLevel"],
            "profile_image": summoner_lookup["profileIconId"],
            "league_entries": league_entries
        }
        return(summoner)

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
        if resp.status == 401:
            raise Forbidden("Invalid Authorization.")
        if resp.status == 500:
            raise Unknown()
        if resp.status == 503:
            raise Unavailable()
        if resp.status == 429:
            raise RateLimit()
        # Why can't you just return 404 here API and make my life easier.
        json = await resp.json()
        try:
            if json["error"] == "Player Not Found":
                raise NotFound()
        except KeyError:
            pass
        if resp.status == 200:
            return await resp.json()
        else:
            raise Unknown()
