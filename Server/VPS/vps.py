from __future__ import annotations
from typing import Final as const, TypeVar, Generic, Type, Any

import requests
import json
from paramiko import SSHClient, AutoAddPolicy

from abstract import AbsVPS, ConohaAPIParam, IServerInfo, VPSCondition, ISSHParam



class VPS(AbsVPS):
    """_summary_\n
    VPSの操作を行う実装クラス。\n
    """
    
    SERVER_DIR:const[str] = "/opt/minecraft_server"
    SERVER_START_COMMAND: const[str] = "java -Xmx1500M -Xms1300M -jar minecraft_server.1.18.2.jar -nogui"
    
    def __init__(self, conoha_api_param:ConohaAPIParam, ssh_param:ISSHParam | None = None) -> None:
        """_summary_\n
        Args:\n
            conoha_api_param (ConohaAPIParam): VPS API のログインパラメータ\n
            ssh_param (Any): MinecraftServerのSSH接続パラメータ\n
        """
        super().__init__(conoha_api_param)
        print("Server API Init Success")
        self.ssh_param = ssh_param
        
    
    
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
        if(type not in ("s", "h")):
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
        ※リリース後に実装予定。\n
        Returns:\n
            VPSCondition: VPSの状態
        """
        #Nope
        pass
    
    def start_minecraft(self) -> None:
        """_summary_\n
        MinecraftServerを起動する。\n
        コマンド実行はSSHで行う。\n
        """
        client: const = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        
        cd_serevr_dir: const[str] = "cd " + self.SERVER_DIR
        start_world: const[str] = "screen " + self.SERVER_START_COMMAND
        
        if self.ssh_param is None:
            raise ConnectionError("SSH接続パラメータが設定されていません。")
        
        client.connect(
            self.ssh_param.ipv4, 
            self.ssh_param.port, 
            self.ssh_param.user,
            self.ssh_param.password,
            timeout=10
        )
        
        client.exec_command(cd_serevr_dir)
        client.exec_command(start_world)
        #TODO:ERRORハンドリング
        
    
    
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