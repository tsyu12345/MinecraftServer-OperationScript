from __future__ import annotations
from typing import Final as const, TypeVar, Generic, Type
from abc import ABCMeta, abstractmethod

import requests
import json

T:const[Type] = TypeVar('T') 
class AbsVPS(object, metaclass=ABCMeta):
    """_summary_\n
    Conoha VPS API を利用したVPS制御の基底クラス。
    """
    BASE_URL:const[str] = "https://compute.tyo2.conoha.io/v2/"
    
    
    def __init__(self, param:ConohaAPIParam) -> None:
        """_summary_\n
        Args:
            param (ConohaAPIParam): JSONから読み取るAPI情報
        """
        self.conoha_api_param = param
        self.token = self.__get_api_token()
        self.server_config: const[IServerInfo] = self.__config()
    
    
    def __get_api_token(self) -> str:
        """_summary_\n
        APIトークンを取得する。
        Returns:
            str: APIトークン
        """
        url:const[str] = "https://identity.tyo2.conoha.io/v2.0/tokens"
        
        api = requests.post(
            url,
            headers=self.conoha_api_param.header, 
            data=json.dumps(self.conoha_api_param.auth)
        )
        
        if api.status_code != 200:
            raise ConnectionError("APIトークンの取得に失敗しました。code = " + str(api.status_code))
        
        token:str = api.json()["access"]["token"]["id"]
        return token
    
    
    def __config(self) -> IServerInfo:
        """_summary_\n
        serverIDを取得する。
        """
        url:const[str] = "https://compute.tyo2.conoha.io/v2/"+ self.conoha_api_param.tenantId +"/servers"
        
        api = requests.get(
            url, 
            headers={
                "X-Auth-Token": self.token, 
                "Accept": "application/json"
            }
        )
        
        if api.status_code != 200:
            raise ConnectionError("サーバー情報の取得に失敗しました。code = " + str(api.status_code))
        
        response_dict:const[dict[str, list[dict]]] = api.json()
        server_value:const[dict[str, T]] = response_dict["servers"][0]
        
        
        return IServerInfo(server_value)
    
    
    @abstractmethod
    def boot(self) -> None:
        """_summary_\n
        VPSを起動する。
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """_summary_\n
        VPSをシャットダウンする。(通常終了)
        """
        pass
    
    @abstractmethod
    def force_shutdown(self) -> None:
        """_summary_\n
        VPSを強制終了する。
        """
        pass
    
    @abstractmethod
    def reboot(self) -> None:
        """_summary_\n
        VPSを再起動する。
        """
        pass
    
    @abstractmethod
    def start_minecraft(self) -> None:
        """_summary_\n
        Minecraftを起動する。\n
        java -Xmx1024M -Xms1024M -jar minecraft_server.1.18.2.jar -noguiの実行
        """
        pass
    
    @abstractmethod
    def get_vps_condition(self) -> VPSCondition:
        """_summary_\n
        VPSの状態を取得する。
        """
        pass


class VPSCondition(object):
    """_summary_\n
    VPSの稼働状態を表す固定値クラス。（interface）
    """
    BOOTING: const[str] = "Booting" # VPSが稼働中
    SHUTDOWN: const[str] = "Shutdown" # VPSが停止中
    ERROR: const[str] = "Error" # VPSでエラーが発生した
    

class ConohaAPIParam(object):
    """_summary_\n
    ConohaAPIを利用する際に使用する、承認パラメータオブジェクトの生成。
    """
    
    def __init__(self, user_name:str, api_password:str, tenantId:str) -> None:
        self.auth:dict[str, dict[str, dict|str]] = {
            "auth": {
                "passwordCredentials": {
                "username": user_name,
                "password": api_password
                },
                "tenantId": tenantId
            }
        }
        
        
        self.header:dict[str, str] = {"Accept": "application/json"}
        
        self.user_name:const[str] = user_name
        self.tenantId:const[str] = tenantId

class ISSHParam():
    """_summary_\n
    VPSのSSH接続情報を表すインターフェース。
    """
    def __init__(self, ipv4:str, user:str, port:int, password:str) -> None:
        """_summary_\n
        Args:
            ipv4 (str): VPSのIPアドレス(IPv4)
            user (str): ログインユーザー名
            port (int): ポート番号
            password (str): ログインパスワード
        """
        self.ipv4:const[str] = ipv4
        self.user:const[str] = user
        self.port:const[int] = port
        self.password:const[str] = password

class IServerInfo(object):
    """_summary_\n
    Server config API返却値の統合再利用のためのオブジェクト
    """
    def __init__(self, server_value:dict) -> None:
        
        self.id: const[str] = server_value["id"]
        self.links: const[list[dict]] = server_value["links"]
        self.name: const[str] = server_value["name"]