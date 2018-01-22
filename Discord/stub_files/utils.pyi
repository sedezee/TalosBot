"""
    Talos utils stub file
"""

from typing import Dict, Union, List, Tuple, Any, Iterable, Optional, overload
from Discord.talos import Talos
import logging
import aiohttp
import paginators
import discord
import discord.ext.commands as dcommands
import datetime as dt
import mysql.connector.cursor_cext as cursor_cext
import mysql.connector.abstracts as mysql_abstracts

log = ... # type: logging.Logger
_levels = ... # type: Dict[str, int]
fullwidth_transform = ... # type: Dict[str, str]
tz_map = ... # type: Dict[str, float]

class NotRegistered(dcommands.CommandError):

    def __init__(self, message: Union[discord.Member, discord.User, str], *args) -> None: ...

class CustomCommandError(dcommands.CommandError):
    pass

class EmbedPaginator:

    # noinspection PyDunderSlots
    __slots__ = ("_max_size", "_title", "_description", "_fields", "_footer", "_built_pages", "_colours", "_colour_pos",
                 "_closed", "_author", "_author_url", "_author_avatar", "repeat_title", "repeat_desc", "repeat_author",
                 "_timestamp", "_footer_url") # type: Tuple[str, ...]

    MAX_TOTAL = ... # type: int
    MAX_TITLE = ... # type: int
    MAX_DESCRIPTION = ... # type: int
    MAX_FIELDS = ... # type: int
    MAX_FIELD_NAME = ... # type: int
    MAX_FIELD_VALUE = ... # type: int
    MAX_FOOTER = ... # type: int
    MAX_AUTHOR = ... # type: int

    repeat_title = ... # type: bool
    repeat_desc = ... # type: bool
    repeat_author = ... # type: bool

    _max_size = ... # type: int
    _title = ... # type: str
    _description = ... # type: str
    _author = ... # type: str
    _author_url = ... # type: str
    _author_avatar = ... # type: str
    _fields = ... # type: List[Tuple[str, str, bool]]
    _timestamp = ... # type: dt.datetime
    _footer = ... # type: str
    _footer_url = ... # type: str
    _built_pages = ... # type: List[discord.Embed]
    _colour_pos = ... # type: int
    _colours = ... # type: List[discord.Colour]
    _closed = ... # type: bool

    def __init__(self, max_size: int = ..., colour: Union[discord.Colour, List[discord.Colour]] = ...) -> None: ...

    @staticmethod
    def _suffix(d: int) -> str: ...
    def _custom_strftime(self, strf: str, t: dt.datetime) -> str: ...

    @property
    def size(self) -> int: return ...
    @property
    def pages(self) -> int: return ...

    def _next_colour(self) -> discord.Colour: ...

    def configure(self, *, repeat_title: bool = ..., repeat_desc: bool = ..., repeat_author: bool = ...) -> None: ...

    def set_title(self, title: str) -> EmbedPaginator: ...

    def set_description(self, description: str) -> EmbedPaginator: ...

    def set_author(self, name: str, *, url: str = ..., avatar: str = ...) -> EmbedPaginator: ...

    def set_colour(self, colour: Union[discord.Colour, List[discord.Colour]]) -> EmbedPaginator: ...

    def set_timestamp(self, timestamp: dt.datetime) -> EmbedPaginator: ...

    def set_footer(self, text: str, icon_url: str = ...) -> EmbedPaginator: ...

    def add_field(self, name: str, value: str, inline: bool = ...) -> EmbedPaginator: ...

    def close_page(self) -> None: ...

    def close(self) -> None: ...

    def get_pages(self) -> List[discord.Embed]: ...

class TalosFormatter(dcommands.HelpFormatter):

    _paginator = ... # type: Union[dcommands.Paginator, paginators.PaginatedEmbed]

    def __init__(self) -> None: ...

    @property
    async def clean_prefix(self) -> str: return ...

    async def get_command_signature(self) -> str: ...

    async def get_ending_note(self) -> str: ...

    @staticmethod
    def capital_split(text: str) -> str: ...

    def embed_shorten(self, text: str) -> str: ...

    def _subcommands_field_value(self, commands: List[dcommands.Command]) -> str: ...

    def _add_subcommands_to_page(self, max_width: int, commands: List[dcommands.Command]) -> None: ...

    async def format(self) -> Union[List[str], List[discord.Embed]]: ...

    async def embed_format(self) -> List[discord.Embed]: ...

    async def string_format(self) -> List[str]: ...

class EmptyCursor(mysql_abstracts.MySQLCursorAbstract):

    DEFAULT_ONE = ... # type: None
    DEFAULT_ALL = ... # type: list

    def __init__(self) -> None: ...

    def __iter__(self) -> iter: ...

    @property
    def description(self) -> Tuple: return ...
    @property
    def rowcount(self) -> int: return ...
    @property
    def lastrowid(self) -> type(None): return ...

    def callproc(self, procname: str, args: Tuple[Any, ...] = ...) -> None: ...

    def close(self) -> None: ...

    def execute(self, query: str, params: Iterable = ..., multi: bool = ...) -> None: ...

    def executemany(self, operation: str, seqparams: Iterable[Iterable]) -> None: ...

    def fetchone(self) -> type(DEFAULT_ONE): ...

    def fetchmany(self, size: int = ...) -> type(DEFAULT_ALL): ...

    def fetchall(self) -> type(DEFAULT_ALL): ...

talos_create_schema = ... # type: str
talos_create_table = ... # type: str
talos_add_column = ... # type: str
talos_remove_column = ... # type: str
talos_modify_column = ... # type: str
talos_tables = ... # type: Dict[str, Dict[str, Union[List[str], str]]]

class TalosDatabase:

    _sql_conn = ... # type: Optional[mysql_abstracts.MySQLConnectionAbstract]
    _cursor = ... # type: Union[cursor_cext.CMySQLCursor, EmptyCursor]

    def __init__(self, sql_conn: Optional[mysql_abstracts.MySQLConnectionAbstract]) -> None: ...

    def verify_schema(self) -> None: ...

    def clean_guild(self, guild_id: int) -> None: ...

    def commit(self) -> None: ...

    def is_connected(self) -> bool: ...

    def raw_exec(self, statement: str) -> List: ...

    # Meta methods

    def get_column_type(self, table_name: str, column_name: str) -> str: ...

    def get_columns(self, table_name: str) -> List[Tuple[str, str]]: ...

    # Guild option methods

    def get_guild_default(self, option_name: str) -> Union[str, int]: ...

    def get_guild_defaults(self) -> List[Union[str, int]]: ...

    def get_guild_option(self, guild_id: int, option_name: str) -> Union[str, int]: ...

    def get_guild_options(self, guild_id: int) -> List[Union[str, int]]: ...

    def get_all_guild_options(self) -> List[Tuple[Union[str, int], ...]]: ...

    def set_guild_option(self, guild_id: int, option_name: str, value: Union[str, int]) -> None: ...

    def remove_guild_option(self, guild_id: int, option_name: str) -> None: ...

    # User option methods

    def get_user_default(self, option_name: str) -> Union[str, int]: ...

    def get_user_defaults(self) -> List[Union[str, int]]: ...

    def get_user_option(self, user_id: int, option_name: str) -> Union[str, int]: ...

    def get_user_options(self, user_id: int) -> List[Union[str, int]]: ...

    def get_all_user_options(self) -> List[Tuple[Union[str, int]]]: ...

    def set_user_option(self, user_id: int, option_name: str, value: Union[str, int]) -> None: ...

    def remove_user_option(self, user_id: int, option_name: str) -> None: ...

    # User profile methods

    def register_user(self, user_id: int) -> None: ...

    def deregister_user(self, user_id: int) -> None: ...

    def get_user(self, user_id: int) -> Optional[Tuple[Union[str, int], ...]]: ...

    def get_description(self, user_id: int) -> Optional[str]: ...

    def set_description(self, user_id: int, desc: str) -> None: ...

    def get_title(self, user_id: int) -> Optional[str]: ...

    def set_title(self, user_id: int, title: str) -> None: ...

    def user_invoked_command(self, user_id: int, command: str) -> None: ...

    def get_command_data(self, user_id: int) -> List[Tuple[str, int]]: ...

    def get_favorite_command(self, user_id: int) -> Tuple[str, int]: ...

    # Admins methods

    def get_all_admins(self) -> List[Tuple[int, int]]: ...

    def get_admins(self, guild_id: int) -> List[int]: ...

    def add_admin(self, guild_id: int, opname: str) -> None: ...

    def remove_admin(self, guild_id: int, opname: str) -> None: ...

    # Perms methods

    def get_perm_rule(self, guild_id: int, command: str, perm_type: str, target: str) -> Optional[Tuple[int, int]]: ...

    def get_perm_rules(self, guild_id: int = ..., command: str = ..., perm_type: str = ..., target: str = ...) -> List[Tuple[int, int]]: ...

    def get_all_perm_rules(self) -> List[Tuple[int, str, str, str, int, int]]: ...

    def set_perm_rule(self, guild_id: int, command: str, perm_type: str, allow: bool, priority: int = ..., target: str = ...) -> None: ...

    def remove_perm_rules(self, guild_id: int, command: Optional[str] = ..., perm_type: Optional[str] = ..., target: Optional[str] = ...) -> None: ...

    # Custom guild commands

    def set_guild_command(self, guild_id: int, name: str, text: str) -> None: ...

    def get_guild_command(self, guild_id: int, name: str) -> Optional[str]: ...

    def get_guild_commands(self, guild_id: int) -> List[Tuple[str, str]]: ...

    def remove_guild_command(self, guild_id: int, name: str) -> None: ...

    # Uptime methods

    def add_uptime(self, uptime: int) -> None: ...

    def get_uptime(self, start: int) -> List[Tuple[int]]: ...

    def remove_uptime(self, end: int) -> None: ...

class TalosHTTPClient(aiohttp.ClientSession):

    NANO_URL = ... # type: str
    BTN_URL = ... # type: str
    CAT_URL = ... # type: str

    username = ... # type: str
    password = ... # type: str
    btn_key = ... # type: str
    cat_key = ... # type: str

    def __init__(self, *args, **kwargs) -> None: ...

    async def get_site(self, url: str, **kwargs) -> str: ...

    async def btn_get_names(self, gender: str = ..., usage: str = ..., number: int = ..., surname: bool = ...) -> Optional[List[str]]: ...

    async def nano_get_user(self, username: str) -> Optional[str]: ...

    @overload
    async def nano_get_novel(self, username: str, novel_name: str = ...) -> Tuple[str, str]: ...
    @overload
    async def nano_get_novel(self, username: str, novel_name: str = ...) -> Tuple[None, None]: ...

    async def nano_login_client(self) -> int: ...

    async def get_cat_pic(self) -> discord.File: ...

def to_snake_case(text: str) -> str: ...

def _perms_check(ctx: dcommands.Context) -> bool: ...

class TalosCog:

    __slots__ = ... # type: Tuple[str, ...]
    bot = ... # type: Talos
    database = ... # type: TalosDatabase

    def __init__(self, bot: Talos): ...

class PW:

    __slots__ = ... # type: Tuple[str, ...]

    start = ... # type: dt.datetime
    end = ... # type: dt.datetime
    members = ... # type: List[PWMember]

    def __init__(self) -> None: ...

    def get_started(self) -> bool: ...

    def get_finished(self) -> bool: ...

    def begin(self, tz: dt.timezone) -> None: ...

    def finish(self, tz: dt.timezone) -> None: ...

    def join(self, member: discord.Member, tz: dt.timezone) -> bool: ...

    def leave(self, member: discord.Member, tz: dt.timezone) -> bool: ...

class PWMember:

    __slots__ = ... # type: Tuple[str, ...]

    user = ... # type: discord.Member
    start = ... # type: dt.datetime
    end = ... # type: dt.datetime

    def __init__(self, user: discord.Member) -> None: ...

    def __str__(self) -> str: ...

    def __eq__(self, other: Any) -> bool: ...

    def get_len(self) -> dt.timedelta: ...

    def get_started(self) -> bool: ...

    def get_finished(self) -> bool: ...

    def begin(self, time: Union[dt.datetime, dt.time]) -> None: ...

    def finish(self, time: Union[dt.datetime, dt.time]) -> None: ...