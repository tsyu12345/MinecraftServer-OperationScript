from __future__ import annotations
from ipaddress import ip_address
from typing import Final as const, Any
from mcipc.rcon.je import Biome, Client
from mcipc.server import server
from Abstract import AbsServer, ServerCondition
from function import load_json

class MinecraftServer(AbsServer):
    
    
    def __init__(self, ip_address: str, port: str, password: str) -> None:
        
        self.ip_address = ip_address
        self.port = port
        self.password = password
        
        self.client = Client(ip_address, int(port), passwd=password)
        self.players: list[str] = []
        
    def start(self) -> None: #NOTE:mcipcで起動できるか不明。subprocess経由かも
        pass
    
    def stop(self) -> None:
        pass
    
    def get_server_condition(self) -> ServerCondition:
        
        server_response: bytes = server.get_response("hello")
        print(server_response)
        
if __name__ == "__main__":
    #TEST CALL
    MCserver = MinecraftServer