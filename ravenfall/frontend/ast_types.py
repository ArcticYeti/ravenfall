from dataclasses import dataclass

@dataclass
class Statement:
    ...

@dataclass
class Program(Statement):
    body: list[Statement]

@dataclass
class Expression(Statement):
    ...

@dataclass
class BinaryExpression(Expression):
    left: Expression
    right: Expression
    operator: str

@dataclass
class Identifier(Expression):
    symbol: str

@dataclass
class IntLiteral(Expression):
    value: int

@dataclass
class FloatLiteral(Expression):
    value: float

@dataclass
class StringLiteral(Expression):
    value: str

@dataclass
class BooleanLiteral(Expression):
    value: bool
