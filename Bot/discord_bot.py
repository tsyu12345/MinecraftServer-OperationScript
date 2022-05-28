from __future__ import annotations
from typing import Final as const

from abstract import AbsDiscordBot, CLIENT, EventHandler
import discord

class DiscordBot(AbsDiscordBot):
    """_summary_\n
    本Botの実装クラス。
    """
    
    def __init__(self, token_path:str):
        super().__init__(token_path)
    
    
    @CLIENT.event
    async def on_message(self, message:discord.Message) -> None:
        """_summary_\n
        既定のメッセージが撃ち込まれたときに呼ばれる。イベントリスナ-.
        
        """
        text: const[str] = message.content
        
        if text[0] == "/" and text in EventHandler.commands():
            cmd:const[str] = text.replace("/", "")
            self.command_handlers[cmd].exec()


