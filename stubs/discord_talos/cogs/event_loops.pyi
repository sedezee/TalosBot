"""
    Stub file for Talos event loops

    author: CraftSpider
"""

from typing import List, Dict, Union, Tuple, Any
from discord_talos.talos import Talos
import spidertools.command_lang as command_lang
import spidertools.discord as dutils
import logging
import argparse
import googleapiclient.discovery
import oauth2client.client
import datetime as dt

SCOPES: str = ...
CLIENT_SECRET_FILE: str = ...
APPLICATION_NAME: str = ...
log: logging.Logger = ...
runner: command_lang.CommandLang()

# class SpreadsheetService(googleapiclient.discovery.Resource):
#
#     def spreadsheets(self) -> None: ...

def get_credentials() -> oauth2client.client.Credentials: ...

def create_service() -> googleapiclient.discovery.Resource: ...

class EventLoops(dutils.TalosCog):

    __slots__ = ("service", "last_guild_count")

    service: Any
    last_guild_count: int

    # noinspection PyMissingConstructor
    def __init__(self, bot: Talos) -> None: ...

    def setup_prompts(self) -> None: ...

    def get_spreadsheet(self, sheet_id: str, sheet_range: str) -> List[List[str]]: ...

    def set_spreadsheet(self, sheet_id: str, values: List[List[str]], sheet_range: str = ...) -> Dict[str, Union[str, int]]: ...

    async def minute_task(self) -> None: ...

    async def hourly_task(self) -> None: ...

    async def daily_task(self) -> None: ...

    async def uptime_task(self) -> None: ...

    async def prompt_task(self) -> None: ...

def setup(bot: Talos) -> None: ...
