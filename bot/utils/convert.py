from discord.ext import commands
import re

class LeagueRegionConverter(commands.Converter):
    async def convert(self, ctx, argument):
        region_list = {
            "BR": {"api": "BR1", "name": "Brazil"},
            "EUNE": {"api": "EUN1", "name": "EU Noric & East"},
            "EUW": {"api": "EUW1", "name": "EU West"},
            "JP": {"api": "JP1", "name": "Japan"},
            "KR": {"api": "KR", "name": "Korea"},
            "LAN": {"api": "LA1", "name": "Latin America North"},
            "LAS": {"api": "LA2", "name": "Latin America South"},
            "NA": {"api": "NA1", "name": "North America"},
            "OCE": {"api": "OC1", "name": "Oceania"},
            "TR": {"api": "TR1", "name": "Turkey"},
            "RU": {"api": "RU", "name": "Russia"}
        }
        try:
            return(region_list[f"{argument.upper()}"])
        except KeyError:
            return("invalid")

class LeagueUserConverter(commands.Converter):
    async def convert(self, ctx, argument):
        username_valid = re.search("^[0-9\[A-z\] _\\.]+$", argument)
        if (username_valid):
            return(argument)
        else:
            return False

class BungieMembershipTypeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        BungieMembershipType_list = {
            "XBOX": {"value": 1, "name": "Xbox"},
            "PSN": {"value": 2, "name": "PSN"},
            "BLIZZARD": {"value": 4, "name": "Blizzard"}
        }
        try:
            return(BungieMembershipType_list[f"{argument.upper()}"])
        except KeyError:
            return("invalid")
