# ag-ui-agent

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (if necessary):

```bash
curl -LsSf https://astral.sh/uv/0.11.6/install.sh | sh
```

```bash
uv python install
```

```bash
uv audit --verbose
```

```bash
uv run python generate_request.py
```

```bash
uv run python main.py
```

```bash
curl -X POST http://localhost:8000/ \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  -d @request.json
```

```bash
uv run mypy
```

```bash
uv run ruff format
```

```bash
uv run ruff check --fix
```
