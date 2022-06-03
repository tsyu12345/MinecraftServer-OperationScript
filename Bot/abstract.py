from __future__ import annotations
from pyexpat.errors import messages
from typing import Final as const, Type, TypeVar, Callable
from abc import ABCMeta, abstractmethod

import json
import discord

T: const[Type] = TypeVar('T')
CLIENT: const = discord.Client()

class AbsDiscordBot(object, metaclass=ABCMeta):
    """_summary_\n
    本BOTの基底抽出クラス。継承先の子クラスは以下のメソッドを持つことを保証するもの。
    """
    
    def __init__(self, token_path:str) -> None:
        """_summary_\n
        Args:
            token_path (str): tokenへのパス
        """
        self.TOKEN: const[str] = self.__load_token(token_path)
        #on_messageで呼ばれるイベントハンドラーを登録する辞書。{"コマンド名": [イベントハンドラー, 引数]}
        self.command_handlers: dict[str, EventHandler] = {}
    

    def __load_token(self, token_path:str) -> str:
        """_summary_\n
        APIトークンを読み込む。json->str
        Args:
            token_path (str): discordBotToken.jsonのパス
        Returns:
            str: APIトークンの文字列
        """
        with open(token_path) as token_file:
            json_file: const[dict[str, str]] = json.load(token_file)
            token: const[str] = json_file["token"]
        
        return token 
    
    def addCommandListener(self, command:str, handler:Callable, *args:tuple[T]) -> None:
        """_summary_\n
        on_messageで実行されるイベントハンドラーを登録する。\n
        ※1つのコマンド名に対し、1つのハンドラのみを登録可能。
        Args:\n
            command (str): コマンド名\n
            handler (Callable): コマンドに対応するイベントハンドラー\n
        """
        self.command_handlers[command] = EventHandler(command, handler, *args)
    
    def removeCommandListener(self, handler:EventHandler) -> None:
        """_summary_\n
        on_messageで実行されるイベントハンドラーを削除する。\n
        Args:\n
            handler (EventHandler): 削除するイベントハンドラー\n
        """
        self.command_handlers.pop(handler.event_key)
        
    @abstractmethod
    def on_message(self, message:discord.Message) -> None:
        """_summary_\n
        on_messageで実行されるイベントハンドラーを実行する。\n
        """
        pass
    
    
class EventHandler():
    """_summary_\n
    イベントハンドラーオブジェクト。
    """
    
    __COMMANDS: list = []
    
    def __init__(self, event_key:str, handler:Callable, args:tuple[T]) -> None:
        self.event_key: const[str] = event_key
        self.handler: const[Callable] = handler
        self.args:const[tuple[T]] = args
        
        self.__COMMANDS.append(self.event_key)
    
    @classmethod
    def commands(cls) -> list:
        """_summary_\n
        登録されたイベントハンドラーのコマンド名のリストを返す。
        Returns:\n
            list: コマンド名のリスト
        """
        return cls.__COMMANDS
    
    def exec(self) -> None:
        """_summary_\n
        ハンドラを実行する。
        """
        self.handler(*self.args)
    