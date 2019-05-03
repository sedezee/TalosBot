
from typing import Tuple, Dict, List, Union, Optional, Any, Iterable, TypeVar, Type
from utils.data import *
import mysql.connector.cursor_cext as cursor_cext
import mysql.connector.abstracts as mysql_abstracts

T = TypeVar("T", bound=Row)
V = TypeVar("V")

levels: Dict[str, int]

class EmptyCursor(mysql_abstracts.MySQLCursorAbstract):

    __slots__ = ()

    DEFAULT_ONE: None = ...
    DEFAULT_ALL: list = ...

    # noinspection PyMissingConstructor
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

talos_create_schema: str = ...
talos_create_table: str = ...
talos_add_column: str = ...
talos_remove_column: str = ...
talos_modify_column: str = ...
talos_create_trigger: str = ...

talos_tables: Dict[str, Dict[str, Union[List[str], List[Tuple[str, int, ...]], str]]] = ...
talos_triggers: Dict[str, Dict[str, str]]

class TalosDatabase:

    __slots__ = ("_sql_conn", "_cursor", "_username", "_password", "_schema", "_host", "_port", "_cache")

    _sql_conn: Optional[mysql_abstracts.MySQLConnectionAbstract]
    _cursor: Union[cursor_cext.CMySQLCursor, EmptyCursor]
    _username: str
    _password: str
    _schema: str
    _host: str
    _port: int

    def __init__(self, address: str, port: int, username: str, password: str, schema: str) -> None: ...

    def verify_schema(self) -> None: ...

    def clean_guild(self, guild_id: int) -> None: ...

    def commit(self) -> bool: ...

    def is_connected(self) -> bool: ...

    def reset_connection(self) -> None: ...

    def raw_exec(self, statement: str) -> List: ...

    # Meta methods

    def get_tables(self) -> List[Table]: ...

    def has_table(self, table: str) -> bool: ...

    def get_columns(self, table_name: str) -> List[Column]: ...

    def has_column(self, table: str, column: str) -> bool: ...

    # Generic methods

    def get_item(self, type: Type[T], *, order: str = ..., default: V = ..., **kwargs: Any) -> Union[T, V]: ...

    def get_items(self, type: Type[T], *, limit: Union[int, Tuple[int, int]] = ..., order: str = ..., **kwargs: Any) -> List[T]: ...

    def get_count(self, type: Type[T], **kwargs: Any) -> int: ...

    def save_item(self, item: Union[type(Row), type(MultiRow)]) -> None: ...

    def remove_item(self, item: Union[type(Row), type(MultiRow)], general: bool = ...) -> None: ...

    def remove_items(self, type: Type[T], *, limit: Union[int, Tuple[int, int]] = ..., order: str = ..., **kwargs: Any) -> None: ...

    # Guild option methods

    def get_guild_defaults(self) -> GuildOptions: ...

    def get_guild_options(self, guild_id: int) -> GuildOptions: ...

    def get_all_guild_options(self) -> List[GuildOptions]: ...

    # User option methods

    def get_user_defaults(self) -> UserOptions: ...

    def get_user_options(self, user_id: int) -> UserOptions: ...

    def get_all_user_options(self) -> List[UserOptions]: ...

    # User profile methods

    def register_user(self, user_id: int) -> None: ...

    def get_user(self, user_id: int) -> Optional[TalosUser]: ...

    def user_invoked_command(self, user_id: int, command: str) -> None: ...

    # Admins methods

    def get_admins(self, guild_id: int) -> List[TalosAdmin]: ...

    def get_all_admins(self) -> List[TalosAdmin]: ...

    # Perms methods

    def get_perm_rule(self, guild_id: int, command: str, perm_type: str, target: str) -> PermissionRule: ...

    def get_perm_rules(self, guild_id: int = ..., command: str = ..., perm_type: str = ..., target: str = ...) -> List[PermissionRule]: ...

    def get_all_perm_rules(self) -> List[PermissionRule]: ...

    # Custom guild commands

    def get_guild_command(self, guild_id: int, name: str) -> Optional[GuildCommand]: ...

    def get_guild_commands(self, guild_id: int) -> List[GuildCommand]: ...

    # Custom guild events

    def get_guild_event(self, guild_id: int, name: str) -> Optional[GuildEvent]: ...

    def get_guild_events(self, guild_id: int) -> List[GuildEvent]: ...

    # Quote methods

    def get_quote(self, guild_id: int, qid: int): ...

    def get_random_quote(self, guild_id: int): ...

    # Uptime methods

    def add_uptime(self, uptime: int) -> None: ...

    def get_uptime(self, start: int) -> List[Tuple[int]]: ...

    def remove_uptime(self, end: int) -> None: ...