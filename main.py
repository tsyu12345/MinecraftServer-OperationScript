from __future__ import annotations
from typing import Final as const

import json

from Bot.discord_bot import DiscordBot
from Server.VPS.vps import VPS
from Server.MinecraftServer.MinecraftServer import MinecraftServer, LoginParam
from Server.VPS.abstract import ConohaAPIParam
from commands import Commands

def main() -> None:
    
    #initilize objects
    bot = DiscordBot("token_path")
    
    vps_param = get_VPS_param()
    vps = VPS(vps_param)
    
    
    mc_server = MinecraftServer() #TODO:インスタンスパラメータの調整
    
    Commands(vps, mc_server)
    
    #add commandEvents below
    bot.addCommandListener("boot", vps.boot)
    bot.addCommandListener("shutdown", vps.shutdown)
    bot.addCommandListener("force_shutdown", vps.force_shutdown)
    bot.addCommandListener("start", Commands.start)
    #starting bot
    bot.run()


def get_rcon_param() -> LoginParam:
    
    with json.load(open("./Server/ServerConfig.json")) as config_file:
        param = LoginParam(
        config_file["rcon"]["ipv4"],
        config_file["rcon"]["port"],
        config_file["rcon"]["password"]
        )
        
        return param
    
    
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