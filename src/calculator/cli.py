import argparse
import sys
from typing import Optional, Sequence

from calculator import __version__
from calculator.core import CalculatorError, evaluate


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="calc",
        description="Evaluate an arithmetic expression.",
    )
    parser.add_argument("--version", action="version", version=f"calc {__version__}")
    parser.add_argument(
        "expression",
        nargs="+",
        help='Expression to evaluate, e.g. "2 + 3 * 4".',
    )
    args = parser.parse_args(argv)
    expr = " ".join(args.expression)

    try:
        result = evaluate(expr)
    except CalculatorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
