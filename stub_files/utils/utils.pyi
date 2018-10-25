"""
    Talos utils stub file
"""

from typing import Dict, List
import discord.ext.commands as dcommands
import utils.element as el


fullwidth_transform: Dict[str, str] = ...
tz_map: Dict[str, float] = ...

def replace_escapes(text: str) -> str: ...

def safe_remove(*filenames: str) -> None: ...

def to_snake_case(text: str) -> str: ...

def to_camel_case(text: str, upper: bool = ...) -> str: ...

def zero_pad(text: str, length: int) -> str: ...

def to_dom(html: str) -> el.Document: ...

def to_nodes(html: str) -> List[el.Node]: ...
