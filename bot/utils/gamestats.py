import yaml
from utils.exceptions import Forbidden, Unknown, NotFound, Unavailable, RateLimit, InvalidPlatform
from utils.config import clash_royale, tracker_network, riot_games, destiny, destiny_user_agent
from utils.clean import clean_escape
import urllib.parse
import discord
import asyncio
import datetime

with open("config.yml") as file:
    bot_config = yaml.load(file, Loader=yaml.FullLoader)

async def destiny_fetch(client, botname, membershipType, username: str):
    headers = {
    'X-API-Key': await destiny(),
    'User-Agent': await destiny_user_agent(),
    'cache-control': "no-cache"
    }
    async with client.get(f'https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/{membershipType["value"]}/{urllib.parse.quote(username)}/', headers=headers) as resp:
        if resp.status == 500:
            json = resp.json()
            try:
                if json["ErrorStatus"] is not None:
                    if json["ErrorStatus"] == "ApiKeyMissingFromRequest":
                        raise Forbidden("No api key.")
                    elif json["ErrorStatus"] == "ApiInvalidOrExpiredKey":
                        raise Forbidden("Invalid Authorization.")
                    elif json["ErrorStatus"] == "ParameterParseFailure":
                        raise Unknown()
                    raise NotFound()
            except KeyError:
                pass
            raise Unknown()
        elif resp.status == 503:
            raise Unavailable()
        elif resp.status == 429:
            raise RateLimit()
        elif resp.status == 200:
            json = await resp.json()
            if json["Response"] == []:
                raise NotFound("Player not found.")
            else:
                pass
        else:
            raise Unknown()
        await asyncio.sleep(2)
        async with client.get(f'https://www.bungie.net/Platform/Destiny2/{membershipType["value"]}/Profile/{json["Response"][0]["membershipId"]}/?components=100', headers=headers) as resp:
            if resp.status == 500:
                try:
                    json = await resp.json()
                except:
                    raise Unknown()
                try:
                    if json["ErrorStatus"] is not None:
                        if json["ErrorStatus"] == "ApiKeyMissingFromRequest":
                            raise Forbidden("No api key.")
                        elif json["ErrorStatus"] == "ApiInvalidOrExpiredKey":
                            raise Forbidden("Invalid Authorization.")
                        elif json["ErrorStatus"] == "ParameterParseFailure":
                            raise Unknown()
                        raise NotFound()
                except KeyError:
                    pass
                raise Unknown()
            elif resp.status == 503:
                raise Unavailable()
            elif resp.status == 429:
                raise RateLimit()
            elif resp.status == 200:
                profile_json = await resp.json()
            else:
                raise Unknown()
        escaped_player_handle = await clean_escape(username)
        embed = discord.Embed(title=f'{botname} showing stats for Destiny 2 player: {escaped_player_handle}, on platform: {membershipType["name"]}')
        embed.set_footer(text="© Bungie, Inc. All rights reserved. Destiny, the Destiny Logo, Bungie and the Bungie logo are among the trademarks of Bungie, Inc.")
        embed.add_field(name="Last time played", value=profile_json["Response"]["profile"]["data"]["dateLastPlayed"])
        minutesplayed = 0
        total_light = 0
        is_first = False
        await asyncio.sleep(1)
        for characterId in profile_json["Response"]["profile"]["data"]["characterIds"]:
            async with client.get(f'https://www.bungie.net/Platform/Destiny2/{membershipType["value"]}/Profile/{json["Response"][0]["membershipId"]}/Character/{characterId}/?components=200', headers=headers) as resp:
                if resp.status == 500:
                    try:
                        json = await resp.json()
                    except:
                        raise Unknown()
                    try:
                        if json["ErrorStatus"] is not None:
                            if json["ErrorStatus"] == "ApiKeyMissingFromRequest":
                                raise Forbidden("No api key.")
                            elif json["ErrorStatus"] == "ApiInvalidOrExpiredKey":
                                raise Forbidden("Invalid Authorization.")
                            elif json["ErrorStatus"] == "ParameterParseFailure":
                                raise Unknown()
                            raise NotFound()
                    except KeyError:
                        pass
                    raise Unknown()
                elif resp.status == 503:
                    raise Unavailable()
                elif resp.status == 429:
                    raise RateLimit()
                elif resp.status == 200:
                    json_character = await resp.json()
                else:
                    raise Unknown()
                if is_first is False:
                    is_first = True
                    embed.set_thumbnail(url=f'https://www.bungie.net{json_character["Response"]["character"]["data"]["emblemPath"]}')
                minutesplayed = minutesplayed + int(json_character["Response"]["character"]["data"]["minutesPlayedTotal"])
                total_light = total_light + int(json_character["Response"]["character"]["data"]["light"])
            await asyncio.sleep(1)
        embed.add_field(name="Total time played", value=str(datetime.timedelta(seconds=minutesplayed*60)))
        embed.add_field(name="Total light amount", value=total_light)

        return(embed)

async def clash_royale_fetch(client, usertag: str):
    stupid_f_strings = await clash_royale()
    headers = {
    'Authorization': f"Bearer {stupid_f_strings}",
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

async def apex_fetch(client, platform: str, username: str):
    if platform in ('origin', 'xbl', 'psn'):
        pass
    else:
        raise InvalidPlatform("Platform is not: origin, xbl or psn.")
    headers = {
        'TRN-Api-Key': await tracker_network(),
        'cache-control': "no-cache"
    }
    async with client.get(f"https://public-api.tracker.gg/v1/apex/standard/profile/{platform}/{urllib.parse.quote(username)}", headers=headers) as resp:
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
            error = json["errors"]
            if error[0]["code"] == "CollectorResultStatus::NotFound":
                raise NotFound()
        except KeyError:
            pass
        if resp.status == 200:
            return await resp.json()
        else:
            raise Unknown()

async def division_2_fetch(client, platform: str, username: str):
    if platform in ('uplay', 'xbl', 'psn'):
        pass
    else:
        raise InvalidPlatform("Platform is not: origin, xbl or psn.")
    headers = {
        'TRN-Api-Key': await tracker_network(),
        'cache-control': "no-cache"
    }
    async with client.get(f"https://public-api.tracker.gg/v1/division-2/standard/profile/{platform}/{urllib.parse.quote(username)}", headers=headers) as resp:
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
            error = json["errors"]
            if error[0]["code"] == "CollectorResultStatus::NotFound":
                raise NotFound()
        except KeyError:
            pass
        if resp.status == 200:
            return await resp.json()
        else:
            raise Unknown()
