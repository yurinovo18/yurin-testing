# calculator

A small arithmetic calculator with a CLI. Zero runtime dependencies — uses only the Python standard library.

Supports:
- Arithmetic: `+`, `-`, `*`, `/`, `//`, `%`, `**`, unary `+`/`-`, and parentheses with normal precedence.
- Functions: `sqrt`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `log` (also `log(x, base)`), `log2`, `log10`, `exp`, `floor`, `ceil`, `abs`, `pow`.
- Constants: `pi`, `e`, `tau`.

## Install

```bash
pip install -e ".[dev]"






```

## Use

```bash
calc "2 + 3 * 4"        # 14
calc "(1 + 2) ** 3"     # 27
calc "sqrt(16)"         # 4.0
calc "log2(1024)"       # 10.0
calc "2 * pi"           # 6.283185307179586
calc "1 / 0"            # error: division by zero (exit 2)
```

You can also pass the expression as separate args (handy when there are no shell-special chars):

```bash
calc 2 + 3
```

## Tests

```bash
pytest -q
```

## Docker

```bash
docker build -t calc .
docker run --rm calc "2 + 3 * 4"
docker run --rm calc "(1 + 2) ** 3"
```

The image is multi-stage: a build stage produces the wheel, the runtime stage installs only the wheel on top of `python:3.12-slim`. No build tooling ships in the final image.
