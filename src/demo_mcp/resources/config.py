"""Static config resources."""

from __future__ import annotations

import json

from demo_mcp.config import settings
from demo_mcp.server import mcp


@mcp.resource("config://app")
def app_config() -> str:
    """Expose basic service metadata as a resource."""
    return json.dumps(
        {
            "name": settings.service_name,
            "version": settings.version,
            "environment": settings.dummy_store["environment"],
        },
        indent=2,
    )
