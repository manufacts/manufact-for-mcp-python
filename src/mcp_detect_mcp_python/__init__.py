"""Minimal `mcp` (official Python SDK) fixture exposed as an HTTP /mcp endpoint."""

from mcp.server.fastmcp import FastMCP

server: FastMCP = FastMCP("mcp-detect-mcp-python")


@server.tool()
def hello(name: str) -> str:
    return f"hello {name} from official MCP python sdk"


# Streamable-HTTP ASGI app (mounted at /mcp by FastMCP).
app = server.streamable_http_app()
