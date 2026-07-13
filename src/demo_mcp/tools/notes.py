"""Dummy in-memory notes tools that use lifespan context."""

from __future__ import annotations

from typing import Annotated

from fastmcp import Context
from pydantic import Field

from demo_mcp.server import AppContext, mcp


@mcp.tool
async def save_note(
    key: Annotated[str, Field(description="Note key")],
    value: Annotated[str, Field(description="Note value")],
    ctx: Context,
) -> dict[str, str | int]:
    """Save a note into the process-local store (lifespan context)."""
    app: AppContext = ctx.lifespan_context
    app.store[key] = value
    app.call_count += 1
    return {"key": key, "value": value, "calls": app.call_count}


@mcp.tool
async def get_note(
    key: Annotated[str, Field(description="Note key to read")],
    ctx: Context,
) -> str:
    """Read a note from the process-local store."""
    app: AppContext = ctx.lifespan_context
    if key not in app.store:
        return f"(missing) {key}"
    return app.store[key]


@mcp.tool
async def list_notes(ctx: Context) -> dict[str, str]:
    """List all notes currently held in lifespan store."""
    app: AppContext = ctx.lifespan_context
    return dict(app.store)
