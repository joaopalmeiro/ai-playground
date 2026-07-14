# kiro-requests

Inspect requests from [Kiro](https://kiro.dev/) for learning purposes.

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (if necessary):

```bash
curl -LsSf https://astral.sh/uv/0.11.6/install.sh | sh
```

```bash
uv python install
```

```bash
uv run mitmweb --listen-port 8080 -s eventstream_view.py
```

```bash
HTTPS_PROXY=http://127.0.0.1:8080 kiro .
```

```bash
uv run ruff format
```

```bash
uv run ruff check --fix
```
