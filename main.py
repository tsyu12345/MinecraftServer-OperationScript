from __future__ import annotations
from typing import Final as const

import json

from Bot.discord_bot import DiscordBot
from Server.VPS.vps import VPS
from Server.VPS.abstract import ConohaAPIParam

def main() -> None:
    
    #initilize objects
    bot = DiscordBot("token_path")
    
    vps_param = get_VPS_param()
    vps = VPS(vps_param)
    
    #add commandEvents below
    bot.addCommandListener("boot", vps.boot)
    bot.addCommandListener("shutdown", vps.shutdown)
    bot.addCommandListener("force_shutdown", vps.force_shutdown)
    
    #starting bot
    bot.run()


def get_VPS_param() -> ConohaAPIParam:
    
    with json.load(open("./Server/ServerConfig.json")) as config_file:
        param = ConohaAPIParam(
        config_file["ConohaAPI"]["auth"]["passwordCredentials"]["username"],
        config_file["ConohaAPI"]["auth"]["passwordCredentials"]["password"],
        config_file["ConohaAPI"]["auth"]["tenantId"]
        )
        
        return param
    



if __name__ == '__main__':
    main()