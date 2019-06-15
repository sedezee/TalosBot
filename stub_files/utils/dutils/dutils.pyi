
from typing import Dict, Pattern, Callable
from discord_talos.talos import Talos
import discord.ext.commands as commands


mention_patterns: Dict[str, Pattern]


def admin_local(self: Talos, ctx: commands.Context) -> bool: ...

def dev_local(self: Talos, ctx: commands.Context) -> bool: ...

def admin_check() -> Callable[[commands.Context], bool]: ...

def dev_check() -> Callable[[commands.Context], bool]: ...

def is_mention(text: str) -> bool: ...

def is_user_mention(text: str) -> bool: ...

def is_role_mention(text: str) -> bool: ...

def is_channel_mention(text: str) -> bool: ...

def get_id(mention: str) -> int: ...

async def _send_paginated(self: commands.Context, msg: str, prefix: str = ..., suffix: str = ...): ...
