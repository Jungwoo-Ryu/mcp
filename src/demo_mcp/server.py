"""FastMCP entry point: create the server, attach lifespan, register modules."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastmcp import FastMCP

from demo_mcp.config import settings


@dataclass
class AppContext:
    """Shared objects available for the lifetime of the server process."""

    store: dict[str, str]
    call_count: int = 0


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Bootstrap long-lived state once per process (DB clients, caches, etc.)."""
    ctx = AppContext(store=dict(settings.dummy_store))
    # In a real server you would connect here and close in the finally block.
    yield ctx


mcp = FastMCP(
    name=settings.service_name,
    instructions=settings.instructions,
    version=settings.version,
    lifespan=lifespan,
)


def _register_components() -> None:
    """Import tool/resource/prompt modules so decorators run at import time."""
    from demo_mcp import prompts, resources, tools  # noqa: F401


_register_components()


def main() -> None:
    """CLI entry: `demo-mcp` or `python -m demo_mcp.server`.

    Defaults to HTTP. Use DEMO_MCP_TRANSPORT=stdio for Cursor stdio mode.
    """
    transport = settings.transport
    if transport == "stdio":
        mcp.run(transport="stdio")
        return

    print(f"Starting demo-mcp on {settings.url}")
    mcp.run(
        transport="http",
        host=settings.host,
        port=settings.port,
        path=settings.path,
    )


if __name__ == "__main__":
    main()
