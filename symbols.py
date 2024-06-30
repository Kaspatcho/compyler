from enum import Enum, auto

class Symbol(Enum):
    Plus = auto(), 1
    Minus = auto(), 1
    Star = auto(), 2
    Slash = auto(), 2
    Percent = auto(), 2
    DoubleSlash = auto(), 2
    DoubleStar = auto(), 3
    OpenParen = auto(), 0
    CloseParen = auto(), 0
    Equal = auto(), 0
    GreaterThan = auto(), 0
    LessThan = auto(), 0
    GreaterThanEqual = auto(), 0
    LessThanEqual = auto(), 0
    Bang = auto(), 0
    BangEqual = auto(), 0
    DoubleEqual = auto(), 0
    If = auto(), 0
    OpenBracket = auto(), 0
    CloseBracket = auto(), 0
    SemiColon = auto(), 0
    Else = auto(), 0
    Comma = auto(), 0

class BuiltinFunction(Enum):
    Print = auto()
    Read = auto()
