from __future__ import annotations
from typing import Final as const
from abc import ABCMeta, abstractmethod

class AbsServer(object, metaclass=ABCMeta):
    """_summary_\n
    ServerAPIの抽象基底クラス定義。
    基本機能のまとめ。
    """
    
    ip_address: str
    port: str
    password: str
    
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def start(self) -> None:
        """_summary_\n
        サーバーを起動する。
        """
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """_summary_\n
        サーバーを停止する。
        """
        pass
    
    @abstractmethod
    def get_server_condition(self) -> ServerCondition:
        """_summary_\n
        サーバーの状態を取得する。
        """
        pass
    

class ServerCondition():
    
    in_operating: const[str] = "In Operating" # サーバーが起動中
    in_stopping: const[str] = "In Stopping" # サーバーが停止中
    available: const[str] = "Available" #サーバーは停止中だが、起動可能
    shutdown: const[str] = "Shutdown" # サーバーPCの電源が切れている
    
