from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="Calculator Server")


@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b
@mcp.tool
def remainder(a: float, b: float) -> float:
    """Return remainder of a divided by b."""
    return a % b

# Start server
if __name__ == "__main__":
    mcp.run(transport="stdio")