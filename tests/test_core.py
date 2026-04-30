import math

import pytest

from calculator import CalculatorError, evaluate


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("1 + 1", 2),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("10 - 4 - 3", 3),
        ("2 ** 10", 1024),
        ("-5 + 2", -3),
        ("+7", 7),
        ("--3", 3),
        ("17 % 5", 2),
        ("17 // 5", 3),
        ("(1 + 2) ** 3", 27),
    ],
)
def test_integer_results(expr, expected):
    assert evaluate(expr) == expected


def test_float_division():
    assert math.isclose(evaluate("1 / 4"), 0.25)


def test_division_by_zero():
    with pytest.raises(CalculatorError, match="division by zero"):
        evaluate("1 / 0")


def test_floor_division_by_zero():
    with pytest.raises(CalculatorError, match="division by zero"):
        evaluate("1 // 0")


def test_empty_expression():
    with pytest.raises(CalculatorError, match="empty"):
        evaluate("   ")


def test_invalid_syntax():
    with pytest.raises(CalculatorError, match="invalid syntax"):
        evaluate("2 +")


@pytest.mark.parametrize(
    "expr",
    [
        "x + 1",
        "__import__('os')",
        "open('foo')",
        "2 + 'a'",
        "abs(-1)",
        "True + 1",
        "[1, 2]",
    ],
)
def test_rejects_unsafe_or_unsupported(expr):
    with pytest.raises(CalculatorError):
        evaluate(expr)
