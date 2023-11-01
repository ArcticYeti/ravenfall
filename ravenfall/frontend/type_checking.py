from .ast_types import BinaryExpression

def type_check_binary_expression(expr):
    if isinstance(expr, BinaryExpression):
        left_type = type_check_binary_expression(expr.left)
        right_type = type_check_binary_expression(expr.right)
        operator = expr.operator

        if left_type == right_type:
            return left_type
        else:
            return None

    return expr.__class__
