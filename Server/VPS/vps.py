from __future__ import annotations
from typing import Final as const, TypeVar, Generic, Type

import requests
import json

from abstract import AbsVPS, ConohaAPIParam, IServerInfo, VPSCondition



class VPS(AbsVPS):
    """_summary_\n
    VPSの操作を行う実装クラス。\n
    """
    def __init__(self, conoha_api_param:ConohaAPIParam) -> None:
        
        super().__init__(conoha_api_param)
        print("Server API Init Success")
        
    
    
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
    
    
    def shutdown(self) -> None:
        url: const[str] = self.BASE_URL + self.conoha_api_param.tenantId + "/servers/" + self.server_config.id + "/action"

        api = requests.post(
            url, 
            headers= {
                "Accept": "application/json",
                "X-Auth-Token": self.token,
            },
            data='{"os-stop": null}',
        )
        
        if api.status_code != 202:
            #TODO:Logで情報出力する
            raise ConnectionError("サーバーの通常停止に失敗しました。code = " + str(api.status_code))
        
    
    def force_shutdown(self) -> None:
        url: const[str] = self.BASE_URL + self.conoha_api_param.tenantId + "/servers/" + self.server_config.id + "/action"
        
        api = requests.post(
            url, 
            headers= {
                "Accept": "application/json",
                "X-Auth-Token": self.token,
            },
            data='{"os-stop": {"force_shutdown": true}}',
        )
        
        if api.status_code != 202:
            #TODO:Logで情報出力する
            raise ConnectionError("サーバーの強制停止に失敗しました。code = " + str(api.status_code))
        
        
    def reboot(self, type:str) -> None:
        """_summary_\n
        リモートサーバーを再起動する。\n
        Args:\n
            type (str(char)): reboot type\n
            ・s: 通常終了→再起動\n
            ・h: 強制終了→再起動\n
        """
        if(type not in ("soft.")):
            raise TypeError("引数typeには文字「s」.または「h」.を指定してください。")
        
        reboot_type: const[dict[str, str]] = {"s": "SOFT", "h": "HARD"}
        
        url: const[str] = self.BASE_URL + self.conoha_api_param.tenantId + "/servers/" + self.server_config.id + "/action"
        
        api = requests.post(
            url, 
            headers= {
                "Accept": "application/json",
                "X-Auth-Token": self.token,
            },
            data='{"reboot": {"type": '+ reboot_type[type] +'"}}',
        )

        if api.status_code != 202:
            #TODO:Logで情報出力する
            raise ConnectionError("サーバーの再起動に失敗しました。code = " + str(api.status_code))
    
    def get_vps_condition(self):
        """_summary_\n
        VPSの状態を取得する。\n
        Returns:\n
            VPSCondition: VPSの状態
        """
        #Nope
        pass
    
    
    
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
    
    test = VPS(param)