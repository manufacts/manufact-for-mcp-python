"""Minimal `mcp` (official Python SDK) fixture exposing tools + an MCP App view.

Follows the recommended MCP Apps protocol pattern from the say-server example:
- ``@mcp.tool(meta={"ui": {"resourceUri": VIEW_URI}})`` on the widget tool
- ``@mcp.resource(uri, mime_type="text/html;profile=mcp-app")`` for the View
"""

from typing import TypedDict

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings


class GreetProps(TypedDict):
    """Structured payload sent to the View as ``structuredContent``."""

    name: str


VIEW_URI = "ui://mcp-detect-mcp-python/greet.html"
RESOURCE_MIME_TYPE = "text/html;profile=mcp-app"

# Self-contained MCP Apps view. Loads the ext-apps app-bridge from esm.sh and
# renders the latest tool result.
VIEW_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Greet</title>
  <style>
    :root { color-scheme: light dark; }
    body { font:16px/1.4 system-ui, sans-serif; padding: 24px; margin: 0; }
    h1 { margin: 0 0 8px; }
    .meta { color: #666; font-size: 13px; margin-top: 12px; }
  </style>
</head>
<body>
  <h1 id="greeting">Greeting view loaded.</h1>
  <p id="hint" class="meta">Call the <code>greet_widget</code> tool to populate this view.</p>
  <script type="module">
    import { App } from "https://esm.sh/@modelcontextprotocol/ext-apps@1";
    const app = new App({ name: "mcp-detect-mcp-python-greet", version: "0.1.0" });
    app.ontoolresult = (result) => {
      const text = (result?.content ?? []).find((c) => c.type === "text")?.text;
      const struct = result?.structuredContent;
      const heading = document.getElementById("greeting");
      const hint = document.getElementById("hint");
      if (text) heading.textContent = text;
      if (struct && struct.name) hint.textContent = "props.name = " + struct.name;
    };
    app.connect();
  </script>
</body>
</html>"""

server: FastMCP = FastMCP(
    "mcp-detect-mcp-python",
    instructions="Smoke-test fixture for official MCP Python SDK framework detection (MCP Apps).",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    stateless_http=True,
)


@server.tool(name="echo", description="Echo the input back as text.")
def echo(text: str) -> str:
    """Return the same text the caller sent."""
    return text


@server.tool(
    name="greet_widget",
    description="Greet someone and render an MCP App view.",
    meta={
        "ui": {"resourceUri": VIEW_URI},
        "ui/resourceUri": VIEW_URI,
    },
)
def greet_widget(name: str) -> GreetProps:
    """Return structuredContent the MCP Apps View renders."""
    return {"name": name}


@server.resource(
    VIEW_URI,
    name="Greet view",
    description="MCP Apps view for the greet_widget tool.",
    mime_type=RESOURCE_MIME_TYPE,
)
def greet_view() -> str:
    """Serve the View HTML at VIEW_URI."""
    return VIEW_HTML


# Streamable-HTTP ASGI app (mounted at /mcp by FastMCP).
app = server.streamable_http_app()
