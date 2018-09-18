"""
    Stub file for Talos commands

    author: CraftSpider
"""
from typing import Tuple, List, Dict, Optional
import logging
import asyncio
import discord.ext.commands as commands
import datetime as dt
import utils
from discord_talos.talos import Talos

active_pw: Dict[int, utils.PW] = ...
log: logging.Logger = ...

def sort_mem(member: utils.PWMember) -> dt.timedelta: ...

def strfdelta(time_delta: dt.timedelta, fmt: str) -> str: ...

def html_to_markdown(html_text: str) -> str: ...

class Commands(utils.TalosCog):

    noun: List[str] = ...
    adjective: List[str] = ...
    goal: List[str] = ...
    obstacle: List[str] = ...
    place: List[str] = ...
    place_adjective: List[str] = ...
    action: List[str] = ...
    phrases: List[str] = ...
    active_wws: Dict[int, asyncio.Task] = ...

    def get_uptime_days(self) -> str: ...

    def get_uptime_percent(self) -> Tuple[float, float, float]: ...

    async def information(self, ctx: commands.Context) -> None: ...

    async def tos(self, ctx: commands.Context) -> None: ...

    async def version(self, ctx: commands.Context) -> None: ...

    async def roll(self, ctx: commands.Context, dice: str) -> None: ...

    async def choose(self, ctx: commands.Context, *, choices: str) -> None: ...

    async def time(self, ctx: commands.Context, timezone: Optional[str] = ...) -> None: ...

    async def wordwar(self, ctx: commands.Context, length: str, start: str = ..., name: str = ..., wpm: int = ...) -> None: ...

    async def credits(self, ctx: commands.Context) -> None: ...

    async def uptime(self, ctx: commands.Context) -> None: ...

    async def ping(self, ctx: commands.Context) -> None: ...

    nanowrimo: commands.Group = ...

    async def _novel(self, ctx: commands.Context, username: str, novel_name: str = ...) -> None: ...

    async def _profile(self, ctx: commands.Context, username: str) -> None: ...

    generate: commands.Group = ...

    async def _crawl(self, ctx: commands.Context) -> None: ...

    async def _prompt(self, ctx:commands.Context) -> None: ...

    async def _name(self, ctx: commands.Context, number: int = ...) -> None: ...

    productivitywar: commands.Group = ...

    async def _create(self, ctx: commands.Context) -> None: ...

    async def _join(self, ctx: commands.Context) -> None: ...

    async def _start(self, ctx: commands.Context, time: str = ...) -> None: ...

    async def _leave(self, ctx: commands.Context) -> None: ...

    async def _end(self, ctx: commands.Context) -> None: ...

    async def _dump(self, ctx: commands.Context) -> None: ...

def setup(bot: Talos) -> None: ...
