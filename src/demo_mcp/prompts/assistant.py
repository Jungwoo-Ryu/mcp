"""Dummy prompt templates."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from demo_mcp.server import mcp


@mcp.prompt
def summarize(
    text: Annotated[str, Field(description="Text to summarize")],
) -> str:
    """Ask the model to summarize the given text."""
    return f"Summarize the following text in 2-3 sentences:\n\n{text}"


@mcp.prompt
def code_review(
    code: Annotated[str, Field(description="Source code to review")],
    focus: Annotated[
        Literal["bugs", "style", "performance"],
        Field(description="Review focus area"),
    ] = "bugs",
) -> str:
    """Ask the model to review code with a specific focus."""
    return (
        f"Review the following code focusing on {focus}. "
        "List findings as short bullet points.\n\n"
        f"```\n{code}\n```"
    )
