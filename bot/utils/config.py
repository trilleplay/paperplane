import yaml

with open("config.yml") as file:
    bot_config = yaml.load(file, Loader=yaml.FullLoader)

async def invite():
    return(bot_config["bot"]["support"])

async def clash_royale():
    return(bot_config["games"]["clash_royale"])

async def tracker_network():
    return(bot_config["games"]["tracker_network"])
