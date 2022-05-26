from __future__ import annotations
from typing import Final as const, TypeVar, Generic, Type

import requests
import json


T:const[Type] = TypeVar('T') 

class ConohaAPIParam():
    """_summary_\n
    ConohaAPIを利用する際に使用する、承認パラメータインタフェース。
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
        
        
        self.header:dict[str, str] = {
            "Accept": "application/json",
        }
        
        self.user_name:const[str] = user_name
        self.tenantId:const[str] = tenantId


class IServerInfo(object):
    """_summary_\n
    API返却値の統合再利用のためのオブジェクト
    """
    def __init__(self, server_value:dict) -> None:
        
        self.id: const[str] = server_value["id"]
        self.links: const[list[dict]] = server_value["links"]
        self.name: const[str] = server_value["name"]
        

class RemoteServer():
    
    header:const[dict[str,str]] = {"Accept": "application/json"}
    
    def __init__(self, conoha_api_param:ConohaAPIParam) -> None:
        
        self.conoha_api_param = conoha_api_param
        
        self.token = self.__get_api_token()
        self.server_config: const[IServerInfo] = self.__config()
        
        print("Server API Init Success")
        
    
    
    def __get_api_token(self) -> str:
        """_summary_\n
        APIトークンを取得する。
        Returns:
            str: APIトークン
        """
        url:const[str] = "https://identity.tyo2.conoha.io/v2.0/tokens"
        
        api = requests.post(
            url,
            headers=self.header, 
            data=json.dumps(self.conoha_api_param.auth)
        )
        
        if api.status_code != 200:
            raise ConnectionError("APIトークンの取得に失敗しました。code = " + str(api.status_code))
        
        token:str = api.json()["access"]["token"]["id"]
        return token
    
    
    def login(self) -> None:
        pass
        
    
    def boot(self) -> None:
        """_summary_\n
        リモートサーバーを起動する。
        """
        url:const[str] = "https://compute.tyo2.conoha.io/v2/" + self.conoha_api_param.tenantId + "servers/" + self.server_config.id + "/action"
        api = requests.post(
            url, 
            headers={
                "Accept": "application/json",
                "X-Auth-Token": self.token, 
            },
            data='{"os-start": null}',
        )
        
        if api.status_code != 202:
            raise ConnectionError("サーバーの起動に失敗しました。code = " + str(api.status_code)) 
    
    def logout(self) -> None:
        pass
        
        
    def reboot(self, type:str) -> None:
        """_summary_\n
        リモートサーバーを再起動する。\n
        Args:\n
            type (str): reboot type\n
            ・soft: 通常終了→再起動\n
            ・hard: 強制終了→再起動\n
        """
        url:const[str] = "https://compute.tyo2.conoha.io/v2/" + self.conoha_api_param.tenantId + "servers/" + self.server_config.id + "/action"
        #TODO:typeの判定に応じて、引数のdata値を変更する
        #Nope
        pass
    
    
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
    
class ConnectionError(Exception):
    pass


if __name__ == "__main__":
    
    """_summary_
    UNIT TEST CALL
    """
    data = json.load(open("./Server/ServerConfig.json"))
    
    param = ConohaAPIParam(
        data["ConohaAPI"]["auth"]["passwordCredentials"]["username"],
        data["ConohaAPI"]["auth"]["passwordCredentials"]["password"],
        data["ConohaAPI"]["auth"]["tenantId"]
    )
    
    test = RemoteServer(param)