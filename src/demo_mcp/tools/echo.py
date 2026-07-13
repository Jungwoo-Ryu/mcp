"""Dummy echo / greeting tools."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from demo_mcp.server import mcp


@mcp.tool
def echo(
    message: Annotated[str, Field(description="Text to echo back")],
) -> str:
    """Echo the given message unchanged."""
    return message


@mcp.tool
def greet(
    name: Annotated[str, Field(description="Name to greet")] = "world",
) -> str:
    """Return a simple greeting string."""
    return f"Hello, {name}!"
