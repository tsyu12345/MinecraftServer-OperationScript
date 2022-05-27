from __future__ import annotations
from typing import Final as const
from abc import ABCMeta, abstractmethod

class AbsServer(object, metaclass=ABCMeta):
    """_summary_\n
    ServerAPIの抽象基底クラス定義。
    基本機能のまとめ。
    """
    
    @abstractmethod
    def start(self) -> None:
        """_summary_\n
        サーバーを起動する。
        """
        pass
    
    @abstractmethod
    def stop(self) -> str:
        """_summary_\n
        ワールドを保存し、サーバーを停止する。
        Returns:\n
            str: stopコマンド送信結果文字列。
        """
        pass
    
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
        
    
    
