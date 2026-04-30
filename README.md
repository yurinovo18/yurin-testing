# calculator

A small arithmetic calculator with a CLI. Zero runtime dependencies — uses only the Python standard library.

Supports `+`, `-`, `*`, `/`, `//`, `%`, `**`, unary `+`/`-`, and parentheses with normal operator precedence.

## Install

```bash
pip install -e ".[dev]"
```

## Use

```bash
calc "2 + 3 * 4"        # 14
calc "(1 + 2) ** 3"     # 27
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
