"""Runtime settings for the demo MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    service_name: str = "demo-mcp"
    version: str = "0.1.0"
    instructions: str = (
        "Dummy FastMCP server for local structure testing. "
        "Use echo/calc tools, config resources, and sample prompts."
    )
    # HTTP defaults — override with DEMO_MCP_HOST / DEMO_MCP_PORT / DEMO_MCP_PATH
    transport: str = "http"
    host: str = "127.0.0.1"
    port: int = 8000
    path: str = "/mcp"
    # Pretend shared state that lifespan would load in a real service.
    dummy_store: dict[str, str] = field(
        default_factory=lambda: {
            "greeting": "hello from demo-mcp",
            "environment": "local",
        }
    )

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}{self.path}"


def load_settings() -> Settings:
    return Settings(
        transport=os.getenv("DEMO_MCP_TRANSPORT", "http"),
        host=os.getenv("DEMO_MCP_HOST", "127.0.0.1"),
        port=int(os.getenv("DEMO_MCP_PORT", "8000")),
        path=os.getenv("DEMO_MCP_PATH", "/mcp"),
    )


settings = load_settings()
