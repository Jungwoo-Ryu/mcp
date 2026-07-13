"""Import tool modules so @mcp.tool registrations attach to the server."""

from demo_mcp.tools import calculator, echo, notes

__all__ = ["calculator", "echo", "notes"]
