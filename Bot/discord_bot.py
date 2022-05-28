from __future__ import annotations
from typing import Final as const

from abstract import AbsDiscordBot, CLIENT, T
import discord

class DiscordBot(AbsDiscordBot):
    """_summary_\n
    本Botの実装クラス。
    """
    
    def __init__(self, token_path:str):
        super().__init__(token_path)
        
    
