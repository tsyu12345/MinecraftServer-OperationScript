from __future__ import annotations
from typing import Final as const, Any

from mcipc.rcon.je import Biome, Client
from mcipc.server import server
from paramiko import SSHClient, AutoAddPolicy, SFTPClient
from setuptools import Command

from Abstract import AbsServer, ServerCondition, LoginParam
class MinecraftServer(AbsServer):
    """_summary_\n
    MinecraftServerを操作するクラス。
    """
    
    SERVER_DIR:const[str] = "/opt/minecraft_server"
    SERVER_START_COMMAND: const[str] = "java -Xmx1024M -Xms1024M -jar minecraft_server.1.18.2.jar -nogui"
    
    def __init__(self, remote_host_param:LoginParam, rcon_param:LoginParam) -> None:
        """_summary_\n
        Args:
            remote_host_param (LoginParam): サーバーの本体のログイン情報。
            rcon_param (LoginParam): サーバーのRCON情報。
        """
        self.remote_host_param = remote_host_param
        self.rcon_param = rcon_param
        
        self.server:SSHClient = SSHClient()
        self.command: SFTPClient
        self.rcon_client:Client
        
        
        
    def ssh_connection(self) -> bool:
        """_summary_\n
        サーバーにssh接続する。
        """
        try:
            self.server.set_missing_host_key_policy(AutoAddPolicy())
            self.server.connect(
                self.remote_host_param.ip_address, 
                port=self.remote_host_param.port, 
                username=self.remote_host_param.user_name, 
                password=self.remote_host_param.password
            )
        except:
            return False
        else:
            self.command = self.server.open_sftp()
            return True
        
    def rcon_connection(self) -> bool:
        """_summary_\n
        RCONプロトコルでMinecraftServerに接続する。
        """
        try:
            self.rcon_client = Client(self.rcon_param.ip_address, self.rcon_param.port, passwd=self.rcon_param.password)
            self.rcon_client.connect(True)
            self.rcon_client.say("This is RCON test. connect success.")
        except:
            return False
        else:
            return True
        
        
    def start(self) -> None: #NOTE:RCONが/stopと同時に切れるため、subprocessとかつかってsshする方法が良いかも
        self.command.chdir(self.SERVER_DIR)
        self.server.exec_command(self.SERVER_START_COMMAND)
        
    
    def stop(self) -> str:
        result: str = self.rcon_client.stop()
        return result
    
    
        
    
    def get_server_condition(self) -> ServerCondition:
        pass
        
if __name__ == "__main__":
    #TEST CALL
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
    
    rcon = MinecraftServer(dummy, rcon_param)
    rcon.rcon_connection()