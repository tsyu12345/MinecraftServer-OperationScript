from __future__ import annotations
from typing import Final as const

from Server.MinecraftServer.MinecraftServer import MinecraftServer
from Server.VPS.vps import VPS

class Commands():
    """_summary_\n
    本BOTで実行されるコマンドの集合。
    """
    VPS: VPS
    MC_SERVER: MinecraftServer
    
    def __init__(self, vps: VPS, mc_server: MinecraftServer) -> None:
        """_summary_\n
        Arguments:\n
            bot {DiscordBot} -- DiscordBotのインスタンス。
        """
        self.VPS = vps
        self.MC_SERVER = mc_server
        
    @classmethod
    def shutdown(cls) -> None:
        """_summary_\n
        worldを閉じてサーバーを停止する。
        """
        cls.MC_SERVER.stop()
        cls.VPS.shutdown()
    
    @classmethod
    def start(cls) -> None:
        """_summary_\n
        VPSを起動し、worldを開く。
        """
        cls.VPS.boot()
        cls.VPS.start_minecraft()
    