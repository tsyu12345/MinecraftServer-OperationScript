from __future__ import annotations
from typing import Final as const
from abc import ABCMeta, abstractmethod

from mcipc.rcon.je import Client
class AbsMinecraftServer(object, metaclass=ABCMeta):
    """_summary_\n
    MinecraftServerAPIの抽象基底クラス定義。
    基本機能のまとめ。
    """
    
    def __init__(self, remote_host_param:LoginParam, rcon_param:LoginParam) -> None:
        """_summary_\n
        Args:
            remote_host_param (LoginParam): サーバーの本体のログイン情報。
            rcon_param (LoginParam): サーバーのRCON情報。
        """
        self.remote_host_param = remote_host_param
        self.rcon_param = rcon_param
        
        self.server:Client = self.__config()
    
    @abstractmethod
    def start(self) -> None:
        """_summary_\n
        サーバーを起動する。
        """
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """_summary_\n
        ワールドを保存し、サーバーを停止する。
        Returns:\n
            str: stopコマンド送信結果文字列。
        """
        pass
    
    @abstractmethod
    def reboot(self) -> None:
        """_summary_\n
        サーバーを再起動する。
        """
        pass
    
    @abstractmethod
    def get_server_condition(self) -> ServerCondition:
        """_summary_\n
        サーバーの状態を取得する。
        """
        pass
    
    def __config(self) -> Client:
        """_summary_\n
        MinecraftServerにRCON接続を行う。\n
        Returns:\n
            Client: RCON接続クラス。
        """
        rcon_client = Client(self.rcon_param.ip_address, self.rcon_param.port, passwd=self.rcon_param.password)
        rcon_client.connect(True)
        #TODO:リリーステストで外す↓
        rcon_client.say("This is RCON test. connect success.")
        
        return rcon_client
        
class ServerCondition():
    """"_summary_\n
    サーバーの稼働状態を表すクラス。（inteface）
    """
    OPERATING: const[str] = "In Operating" # サーバーが起動中
    STOPPING: const[str] = "In Stopping" # サーバーが停止中
    AVAILABLE: const[str] = "Available" #サーバーは停止中だが、起動可能
    SHUTDOWN: const[str] = "Shutdown" # サーバーPCの電源が切れている
    

class LoginParam():
    """_summary_\n
    Jsonで読み込まれるサーバー情報の型定義。
    Arguments:\n
        ip_address {str} -- サーバーのIPアドレス。
        port {int} -- サーバーのポート番号。
        password {str} -- サーバーのパスワード。
        user_name {str} -- サーバーのユーザー名。初期値はroot。
    """
    def __init__(self, ip_address: str, port: int, password: str, user_name:str="root") -> None:
        self.ip_address = ip_address
        self.port = port
        self.password = password
        self.user_name = user_name
        
    
    
