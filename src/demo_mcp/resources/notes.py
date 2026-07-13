"""Templated note resources."""

from __future__ import annotations

from demo_mcp.config import settings
from demo_mcp.server import mcp


@mcp.resource("notes://{key}")
def note_by_key(key: str) -> str:
    """Read a seed note by key (static seed data only — not lifespan store)."""
    value = settings.dummy_store.get(key)
    if value is None:
        return f"(missing) {key}"
    return value
