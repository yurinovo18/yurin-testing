import ast
import math
import operator
from typing import Union

Number = Union[int, float]


class CalculatorError(ValueError):
    pass


_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log,
    "log2": math.log2,
    "log10": math.log10,
    "exp": math.exp,
    "floor": math.floor,
    "ceil": math.ceil,
    "abs": abs,
    "pow": pow,
}

_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}


def evaluate(expr: str) -> Number:
    if not expr or not expr.strip():
        raise CalculatorError("empty expression")
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise CalculatorError(f"invalid syntax: {exc.msg}") from exc
    try:
        return _eval(tree.body)
    except ZeroDivisionError as exc:
        raise CalculatorError("division by zero") from exc


def _eval(node: ast.AST) -> Number:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculatorError(f"unsupported constant: {node.value!r}")
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in _CONSTANTS:
            raise CalculatorError(f"unknown name: {node.id}")
        return _CONSTANTS[node.id]
    if isinstance(node, ast.BinOp):
        op = _BIN_OPS.get(type(node.op))
        if op is None:
            raise CalculatorError(f"unsupported operator: {type(node.op).__name__}")
        return op(_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        op = _UNARY_OPS.get(type(node.op))
        if op is None:
            raise CalculatorError(f"unsupported unary operator: {type(node.op).__name__}")
        return op(_eval(node.operand))
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise CalculatorError("only direct function calls are allowed")
        name = node.func.id
        if name not in _FUNCTIONS:
            raise CalculatorError(f"unknown function: {name}")
        if node.keywords:
            raise CalculatorError(f"{name}: keyword arguments are not supported")
        args = [_eval(a) for a in node.args]
        try:
            result = _FUNCTIONS[name](*args)
        except (ValueError, OverflowError, TypeError) as exc:
            raise CalculatorError(f"{name}: {exc}") from exc
        if isinstance(result, bool) or not isinstance(result, (int, float)):
            raise CalculatorError(f"{name}: non-numeric result")
        return result
    raise CalculatorError(f"unsupported expression: {type(node).__name__}")
