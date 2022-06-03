from __future__ import annotations
from typing import Final as const, Any

from Abstract import AbsMinecraftServer, LoginParam, ServerCondition
class MinecraftServer(AbsMinecraftServer):
    """_summary_\n
    MinecraftServerを操作するクラス。
    """
    
    def __init__(self, remote_host_param:LoginParam, rcon_param:LoginParam) -> None:
        super().__init__(remote_host_param, rcon_param)
        
    
    def stop(self) -> None:
        self.server.stop()
        
    def send_message(self, message:str) -> None:
        self.server.say(message)
        
        
if __name__ == "__main__":
    #UNIT TEST CALL
    rcon_param = LoginParam(
        ip_address="163.44.255.138",
        port=25575,
        password="alienwarertx2070"
    )
    dummy = LoginParam(
        ip_address="",
        port=0,
        password="",
        user_name=""
    )
    
    MinecraftServer(dummy, rcon_param).stop()