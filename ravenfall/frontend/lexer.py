from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()

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
    value: str
    type: TokenType

def tokenize(source_code: str) -> list[Token]:
    token_map = {
        '=': TokenType.EQUALS,
        '+': TokenType.ADD,
        '-': TokenType.SUBTRACT,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '%': TokenType.MODULO,
        '.': TokenType.PERIOD,
        ',': TokenType.COMMA,
        ':': TokenType.COLON,
        '(': TokenType.OPEN_PAREN,
        ')': TokenType.CLOSE_PAREN,
        '{': TokenType.OPEN_BRACE,
        '}': TokenType.CLOSE_BRACE,
        '[': TokenType.OPEN_BRACKET,
        ']': TokenType.CLOSE_BRACKET,
    }

    any_bracket_level = 0       # this tracks whether we're currently in any bracket block or not
    last_indent_level = 0
    token_stream: list[Token] = []
    chars = [*source_code]

    while chars:
        if chars[0] == ' ':
            chars.pop(0)
        elif chars[0] == '\n':
            newline = chars.pop(0)

            # handles indentation
            indent_level = 0
            while chars[:4] == [' ',]*4:
                del chars[:4]
                indent_level += 1

            if any_bracket_level > 0:
                # ignores indentation and newlines when inside a ({[ block )}]
                continue

            token_stream.append(Token(newline, TokenType.NEWLINE))

            if indent_level > last_indent_level:
                too_much_indent = last_indent_level - indent_level != -1
                if too_much_indent:
                    raise IndentationError('Invalid indentation')

                last_indent_level = indent_level
                token_stream.append(Token('', TokenType.INDENT))

            while indent_level < last_indent_level:
                last_indent_level -= 1
                token_stream.append(Token('', TokenType.DEDENT))

        elif chars[0] in ['\'', '"']:
            # build strings
            quote_type = chars[0]
            chars.pop(0)    # del open quote
            full_string = []

            while chars[0] != quote_type:
                full_string.append(chars.pop(0))
            chars.pop(0)    # del close quote

            token_stream.append(Token(''.join(full_string), TokenType.STRING))
        elif chars[0] in token_map:
            if chars[0] in ['(', '{', '[']:
                any_bracket_level += 1
            elif chars[0] in [')', '}', ']']:
                any_bracket_level -= 1

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
            # this builds identifier, boolean and keyword tokens
            full_value = []
            while chars and (chars[0].isalnum() or chars[0] in '_'):
                full_value.append(chars.pop(0))

            value = ''.join(full_value)

            # check for booleans
            if value in ['true', 'false'] :
                token_stream.append(Token(value, TokenType.BOOLEAN))
                continue

            # check for keywords
            reserved = KEYWORDS.get(value)
            if reserved:
                token_stream.append(Token(value, reserved))
            else:
                token_stream.append(Token(value, TokenType.IDENTIFIER))            
        else:
            raise Exception(f'Unrecognized character "{chars[0]}" found during tokenization')

    token_stream.append(Token('', TokenType.EOF))
    return token_stream
