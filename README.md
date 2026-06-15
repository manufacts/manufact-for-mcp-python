[![Deploy to mcp-use](https://cdn.mcp-use.com/deploy.svg)](https://mcp-use.com/deploy/start?repository-url=https%3A%2F%2Fgithub.com%2Fmanufacts%2Fmanufact-for-mcp-python&branch=main&project-name=manufact-for-mcp-python&port=8000&start-command=uvicorn+%27mcp_detect_mcp_python%3Aapp%27+--host+0.0.0.0+--port+8000&runtime=python&base-image=python%3A3.12)

<div align="center">

# MCP Python SDK MCP Apps example

**Reference server for the [MCP Python SDK deploy guide](https://mcp-use.com/blog/mcp-app-with-mcp-python-sdk)** — same `echo` + `greet_widget` example used in our [seven-framework comparison](https://mcp-use.com/blog/deploying-seven-mcp-frameworks).

Built with the official [`mcp`](https://github.com/modelcontextprotocol/python-sdk) Python SDK (`FastMCP`).

**Live demo:** [`wild-pulse-opk28.run.mcp-use.com/mcp`](https://wild-pulse-opk28.run.mcp-use.com/mcp)

</div>

---

## Deploy to Manufact Cloud

Click the badge above, or open the [one-click deploy flow](https://mcp-use.com/deploy/start?repository-url=https%3A%2F%2Fgithub.com%2Fmanufacts%2Fmanufact-for-mcp-python&branch=main&project-name=manufact-for-mcp-python&port=8000&start-command=uvicorn+%27mcp_detect_mcp_python%3Aapp%27+--host+0.0.0.0+--port+8000&runtime=python&base-image=python%3A3.12). Sign in, connect GitHub, and Manufact clones this repo into your account and deploys it.

If you deploy manually from the dashboard instead:

| Setting | Value |
| --- | --- |
| **Port** | `8000` |
| **Build command** | *(leave empty — this repo has no `uv.lock`, so Manufact runs `pip install .`; with a committed `uv.lock` it uses `uv sync --frozen` instead)* |
| **Start command** | `uvicorn 'mcp_detect_mcp_python:app' --host 0.0.0.0 --port 8000` |

Manufact detects `mcp` in `pyproject.toml` and labels the repo **mcp-python**. DNS-rebinding protection is disabled for proxy compatibility — see the [deploy guide](https://mcp-use.com/blog/mcp-app-with-mcp-python-sdk) for production hardening.

---

## What's in this repo

- An `echo` tool (text-only)
- A `greet_widget` tool using the say-server MCP Apps pattern (`@server.tool` + `@server.resource`)
- Streamable HTTP at `/mcp` via `server.streamable_http_app()`

---

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn mcp_detect_mcp_python:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000/mcp`.

---

## Project layout

```
src/mcp_detect_mcp_python/
  __init__.py   # FastMCP server, tools, view HTML, and ASGI app export
```

See the [deploy guide](https://mcp-use.com/blog/mcp-app-with-mcp-python-sdk) for the full reference server walkthrough.
