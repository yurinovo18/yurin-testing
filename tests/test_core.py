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
        "True + 1",
        "[1, 2]",
        "math.sqrt(4)",
    ],
)
def test_rejects_unsafe_or_unsupported(expr):
    with pytest.raises(CalculatorError):
        evaluate(expr)


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("sqrt(16)", 4.0),
        ("sqrt(2) ** 2", 2.0),
        ("abs(-7)", 7),
        ("abs(-3.5)", 3.5),
        ("floor(3.7)", 3),
        ("ceil(3.2)", 4),
        ("log2(1024)", 10.0),
        ("log10(1000)", 3.0),
        ("log(8, 2)", 3.0),
        ("exp(0)", 1.0),
        ("pow(2, 10)", 1024),
    ],
)
def test_scientific_functions(expr, expected):
    assert math.isclose(evaluate(expr), expected)


def test_log_of_e():
    assert math.isclose(evaluate("log(e)"), 1.0)


def test_trig_with_pi():
    assert math.isclose(evaluate("sin(pi)"), 0.0, abs_tol=1e-9)
    assert math.isclose(evaluate("cos(0)"), 1.0)
    assert math.isclose(evaluate("tan(pi / 4)"), 1.0)


@pytest.mark.parametrize(
    "name, expected",
    [("pi", math.pi), ("e", math.e), ("tau", math.tau)],
)
def test_constants(name, expected):
    assert evaluate(name) == expected


def test_function_composition():
    assert math.isclose(evaluate("sqrt(sqrt(16))"), 2.0)
    assert evaluate("ceil(log2(1000))") == 10


def test_unknown_function():
    with pytest.raises(CalculatorError, match="unknown function"):
        evaluate("nope(1)")


def test_unknown_constant():
    with pytest.raises(CalculatorError, match="unknown name"):
        evaluate("unknown_var")


def test_function_domain_error():
    with pytest.raises(CalculatorError, match="sqrt"):
        evaluate("sqrt(-1)")


def test_function_keyword_args_rejected():
    with pytest.raises(CalculatorError, match="keyword"):
        evaluate("log(8, base=2)")
