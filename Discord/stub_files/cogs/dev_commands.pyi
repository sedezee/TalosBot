"""
    Stub for Talos dev commands

    author: CraftSpider
"""

from typing import Callable
from Discord.talos import Talos
import logging
import utils
import discord
import discord.ext.commands as commands

log: logging.Logger = ...

class DevCommands(utils.TalosCog):

    __local_check: Callable[Talos, commands.Context] = ...

    async def playing(self, ctx: commands.Context, *, playing: str) -> None: ...

    async def streaming(self, ctx: commands.Context, *, streaming: str) -> None: ...

    async def listening(self, ctx: commands.Context, *, listening: str) -> None: ...

    async def watching(self, ctx: commands.Context, *, watching: str) -> None: ...

    async def stop(self, ctx: commands.Context) -> None: ...

    async def master_nick(self, ctx: commands.Context, nick: str) -> None: ...

    async def idlist(self, ctx: commands.Context) -> None: ...

    async def verifysql(self, ctx: commands.Context) -> None: ...

    async def grant_title(self, ctx: commands.Context, user: discord.User, *, title: str) -> None: ...

    async def reload(self, ctx: commands.Context, name: str) -> None: ...

    async def eval(self, ctx: commands.Context, *, program: str) -> None: ...

    async def exec(self, ctx: commands.Context, *, program: str) -> None: ...

    async def sql(self, ctx: commands.Context, *, statement: str) -> None: ...

    async def resetsql(self, ctx: commands.Context) -> None: ...

    async def image(self, ctx: commands.Context, red: int = ..., green: int = ..., blue: int = ...) -> None: ...

def dev_check(self: DevCommands, ctx: commands.Context) -> bool: ...

def setup(bot: Talos) -> None: ...
