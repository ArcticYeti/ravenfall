from dataclasses import dataclass, field

from .ast_types import BinaryExpression, Expression, FloatLiteral, Identifier, IntLiteral, Program, Statement, StringLiteral
from .lexer import Token, TokenType



@dataclass
class Parser:
    token_stream: list[Token] = field(default_factory=list)

    def produce_ast(self, token_stream: list[Token]) -> Program:
        self.token_stream = token_stream.copy()
        body = []

        while self._not_eof():
            body.append(self._parse_statement())

        return Program(body=body)

    def _parse_statement(self) -> Statement:
        return self._parse_expression()
    #     token_type = self._at().type

    #     if token_type == TokenType.LET:
    #         self._eat()

    #         # handle mut
    #         is_mutable = self._at().type == TokenType.MUT 
    #         if is_mutable:
    #             self._eat()

    #         return self._parse_var_declaration(is_mutable)
    #     else:
    #         return self._parse_expression()

    def _parse_expression(self) -> Expression:
        return self._parse_additive_expression()

    def _parse_additive_expression(self) -> Expression:
        left = self._parse_multiplicative_expression()

        while self._at().value in ['+', '-']:
            operator = self._eat().value
            right = self._parse_multiplicative_expression()
            left = BinaryExpression(left, right, operator)

        return left

    def _parse_multiplicative_expression(self) -> Expression:
        left = self._parse_primary_expression()

        while self._at().value in ['*', '/', '%']:
            operator = self._eat().value
            right = self._parse_primary_expression()
            left = BinaryExpression(left, right, operator)

        return left

    def _parse_primary_expression(self) -> Expression:  # type: ignore
        ast_literal_map = {
            TokenType.INT: IntLiteral,
            TokenType.FLOAT: FloatLiteral,
            TokenType.STRING: StringLiteral,
        }

        token = self._at()
        ast_literal = ast_literal_map.get(token.type)
        if ast_literal:
            return ast_literal(value=self._eat().value)
        if token.type == TokenType.OPEN_PAREN:
            self._eat()
            value = self._parse_expression()
            self._expect(TokenType.CLOSE_PAREN)  # eat closing paren
            return value

        raise Exception(f'Unrecognized token "{self._at()}"')

    def _not_eof(self):
        return self._at().type != TokenType.EOF

    def _at(self) -> Token:
        return self.token_stream[0]

    def _eat(self) -> Token:
        return self.token_stream.pop(0)
    
    def _skip(self, token_type: TokenType) -> Token | None:
        if self._at().type == token_type:
            return self._eat()
        return None

    def _expect(self, expected_type: TokenType) -> Token:
        token = self._eat()

        if not token or token.type != expected_type:
            raise SyntaxError(f'Expected token of type "{expected_type}". Got "{token}" instead')

        return token
