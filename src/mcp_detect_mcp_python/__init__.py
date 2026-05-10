"""Minimal `mcp` (official Python SDK) fixture exposing tools + a widget tool."""

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import EmbeddedResource, TextContent, TextResourceContents
from pydantic import AnyUrl

# Disable DNS-rebinding protection so the fixture is reachable behind any
# proxy host (Fly, Cloudflare, etc.).
server: FastMCP = FastMCP(
    "mcp-detect-mcp-python",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    stateless_http=True,
)


@server.tool(name="echo", description="Echo the input back as text.")
def echo(text: str) -> str:
    """Return the same text the caller sent."""
    return text


@server.tool(
    name="greet_widget",
    description="Greet someone and return an HTML widget rendered by the MCP client.",
)
def greet_widget(name: str) -> list[TextContent | EmbeddedResource]:
    """Return a textual greeting plus an embedded HTML UI resource."""
    html = (
        '<!doctype html><html><body style="font:16px/1.4 system-ui;padding:24px">'
        f'<h1 style="margin:0 0 8px">Hello, {name}!</h1>'
        '<p style="color:#555">Greeting widget served by mcp-detect-mcp-python.</p>'
        '</body></html>'
    )
    return [
        TextContent(type="text", text=f"Hello, {name}!"),
        EmbeddedResource(
            type="resource",
            resource=TextResourceContents(
                uri=AnyUrl(f"ui://greet/{name}"),
                mimeType="text/html",
                text=html,
            ),
        ),
    ]


# Streamable-HTTP ASGI app (mounted at /mcp by FastMCP).
app = server.streamable_http_app()
