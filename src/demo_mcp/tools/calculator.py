"""Dummy calculator tools."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from demo_mcp.server import mcp


@mcp.tool
def add(
    a: Annotated[float, Field(description="First number")],
    b: Annotated[float, Field(description="Second number")],
) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool
def calculate(
    a: Annotated[float, Field(description="Left operand")],
    b: Annotated[float, Field(description="Right operand")],
    op: Annotated[
        Literal["+", "-", "*", "/"],
        Field(description="Arithmetic operator"),
    ] = "+",
) -> float:
    """Run a basic arithmetic operation."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
