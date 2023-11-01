from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()

    EQUALS = auto()     # =
    ADD = auto()        # +
    SUBTRACT = auto()   # -
    MULTIPLY = auto()   # *
    DIVIDE = auto()     # /
    MODULO = auto()     # %

    OPEN_PAREN = auto()     # (
    CLOSE_PAREN = auto()    # )
    OPEN_BRACE = auto()     # {
    CLOSE_BRACE = auto()    # }
    OPEN_BRACKET = auto()   # [
    CLOSE_BRACKET = auto()  # ]

    PERIOD = auto()     # .
    COMMA = auto()      # ,
    COLON = auto()      # :

    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()

    IDENTIFIER = auto()
    LET = auto()
    MUT = auto()
    EOF = auto()

KEYWORDS: dict[str, TokenType] = {
    'let': TokenType.LET,
    'mut': TokenType.MUT,
}

@dataclass
class Token:
    value: str | None
    type: TokenType

def tokenize(source_code: str) -> list[Token]:
    token_map = {
        '=': TokenType.EQUALS,
        '+': TokenType.ADD,
        '-': TokenType.SUBTRACT,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '%': TokenType.MODULO,
        '(': TokenType.OPEN_PAREN,
        ')': TokenType.CLOSE_PAREN,
        '{': TokenType.OPEN_BRACE,
        '}': TokenType.CLOSE_BRACE,
        '[': TokenType.OPEN_BRACKET,
        ']': TokenType.CLOSE_BRACKET,
        '.': TokenType.PERIOD,
        ',': TokenType.COMMA,
        ':': TokenType.COLON,
    }

    in_block = False
    last_indent_level = 0
    token_stream: list[Token] = []
    chars = [*source_code]

    while chars:
        if chars[0] == ' ':
            chars.pop(0)
        elif chars[0] == '\n':
            token_stream.append(Token(chars.pop(0), TokenType.NEWLINE))

            # handles indentation
            indent_level = 0
            while chars[:4] == [' ',]*4:
                del chars[:4]
                indent_level += 1

            if in_block:
                # ignore indentation when inside a ({[ block )}]
                continue

            if indent_level > last_indent_level:
                too_much_indent = last_indent_level - indent_level != -1
                if too_much_indent:
                    raise IndentationError('Invalid indentation')

                last_indent_level = indent_level
                token_stream.append(Token(None, TokenType.INDENT))

            while indent_level < last_indent_level:
                last_indent_level -= 1
                token_stream.append(Token(None, TokenType.DEDENT))

        elif chars[0] in '\'"':
            # build strings
            quote_type = chars[0]
            chars.pop(0)    # del open quote
            full_string = []

            while chars[0] != quote_type:
                full_string.append(chars.pop(0))
            chars.pop(0)    # del close quote

            token_stream.append(Token(''.join(full_string), TokenType.STRING))
        elif chars[0] in token_map:
            in_block = chars[0] in '({['
            token_stream.append(Token(chars[0], token_map[chars.pop(0)]))
        elif chars[0].isnumeric():
            # this builds float and int tokens
            full_number = []
            period_found = False
            while chars and (chars[0].isnumeric() or chars[0] == '.'):
                if period_found and not chars[0].isnumeric():
                    break
                if chars[0] == '.':
                    period_found = True
                full_number.append(chars.pop(0))
            if period_found:
                token_stream.append(Token(''.join(full_number), TokenType.FLOAT))
            else:
                token_stream.append(Token(''.join(full_number), TokenType.INT))
        elif chars[0].isalpha():
            # this builds identifier and keyword tokens
            full_value = []
            while chars and (chars[0].isalnum() or chars[0] in '_'):
                full_value.append(chars.pop(0))

            value = ''.join(full_value)

            # check for keywords
            reserved = KEYWORDS.get(value)
            if reserved:
                token_stream.append(Token(value, reserved))
            else:
                token_stream.append(Token(value, TokenType.IDENTIFIER))
        else:
            raise Exception(f'Unrecognized character "{chars[0]}" found during tokenization')

    token_stream.append(Token(None, TokenType.EOF))
    return token_stream
