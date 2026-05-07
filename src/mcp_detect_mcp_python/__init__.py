from mcp.server.fastmcp import FastMCP

server = FastMCP("mcp-detect-mcp-python")


@server.tool()
def hello(name: str) -> str:
    return f"hello {name} from official MCP python sdk"


if __name__ == "__main__":
    server.run()
