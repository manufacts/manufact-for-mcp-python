"""Minimal `mcp` (official Python SDK) fixture exposed as an HTTP /mcp endpoint."""

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# Disable DNS-rebinding protection so the fixture is reachable behind any
# proxy host (Fly, Cloudflare, etc.). Keep this off only for public smoke-test
# fixtures — production servers should set explicit `allowed_hosts`.
server: FastMCP = FastMCP(
    "mcp-detect-mcp-python",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    stateless_http=True,
)


@server.tool()
def hello(name: str) -> str:
    return f"hello {name} from official MCP python sdk"


# Streamable-HTTP ASGI app (mounted at /mcp by FastMCP).
app = server.streamable_http_app()
