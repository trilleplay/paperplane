import yaml

with open("config.yml") as file:
    bot_config = yaml.load(file, Loader=yaml.FullLoader)

async def invite():
    return(bot_config["bot"]["support"])
