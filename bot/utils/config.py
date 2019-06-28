import yaml

with open("config.yml") as file:
    bot_config = yaml.load(file, Loader=yaml.FullLoader)

async def invite():
    return(bot_config["bot"]["support"])

async def clash_royale():
    return(bot_config["games"]["clash_royale"])

async def tracker_network():
    return(bot_config["games"]["tracker_network"])

async def riot_games():
    return(bot_config["games"]["riot_games"])

async def destiny():
    return(bot_config["games"]["destiny"])

async def destiny_user_agent():
    return(bot_config["games"]["destiny_user_agent"])

async def postgres():
    return(f"postgres://{bot_config['postgres']['username']}:{bot_config['postgres']['password']}@{bot_config['postgres']['server']}:{bot_config['postgres']['port']}/{bot_config['postgres']['database']}")
