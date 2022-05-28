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
        self.on_message_event_handler: dict[str, list[Callable | tuple]] = {} 
    

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
    
    def addEventListener(self, command:str, handler:Callable, *args:tuple[T]) -> None:
        """_summary_\n
        on_messageで実行されるイベントハンドラーを登録する。\n
        ※1つのコマンド名に対し、1つのハンドラのみを登録可能。
        Args:\n
            command (str): コマンド名\n
            handler (Callable): コマンドに対応するイベントハンドラー\n
        """
        self.on_message_event_handler[command][0] = handler
        self.on_message_event_handler[command][1] = args
    
    
    @CLIENT.event
    async def on_message(self, message:discord.Message) -> T:
        """_summary_\n
        既定のメッセージが撃ち込まれたときに呼ばれる。イベントリスナ-
        """
        if message.content in self.on_message_event_handler.keys():
            command:const[str] = message.content
            callback = self.on_message_event_handler[command][0]
            args:tuple[T] = self.on_message_event_handler[command][1]
            callback(args)
    
    
    