from fastmcp import FastMCP

# Initialize the FastMCP Server
mcp = FastMCP("budget-tools")

@mcp.tool()
def estimate_budget(destination: str, days: int) -> float:
    """Estimate travel budget in USD."""
    base_cost = 100
    if "paris" in destination.lower():
        base_cost = 200
    elif "barcelona" in destination.lower():
        base_cost = 150
    return float(base_cost * days)

if __name__ == "__main__":
    # This automatically runs on port 3333 with SSE enabled if configured,
    # but for explicit port control matching your Agent:
    print("Starting Budget MCP Server on port 3333...")
    mcp.run(transport="sse", port=3333)