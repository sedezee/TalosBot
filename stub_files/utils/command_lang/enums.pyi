
import enum


class Instruction(enum.IntEnum):
    RAW: int = ...
    IF: int = ...
    ELIF: int = ...
    ELSE: int = ...
    EXEC: int = ...
