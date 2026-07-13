"""In-memory FastMCP Client tests for the dummy server."""

from __future__ import annotations

import json

import pytest
from fastmcp import Client

from demo_mcp.server import mcp


@pytest.fixture
async def client():
    async with Client(mcp) as c:
        yield c


async def test_list_tools(client: Client) -> None:
    tools = await client.list_tools()
    names = {t.name for t in tools}
    assert {"echo", "greet", "add", "calculate", "save_note", "get_note", "list_notes"} <= names


async def test_echo_and_add(client: Client) -> None:
    echo = await client.call_tool("echo", {"message": "ping"})
    assert echo.data == "ping"

    summed = await client.call_tool("add", {"a": 2, "b": 3})
    assert summed.data == 5.0


async def test_calculate_divide(client: Client) -> None:
    result = await client.call_tool("calculate", {"a": 10, "b": 4, "op": "/"})
    assert result.data == 2.5


async def test_notes_lifespan_store(client: Client) -> None:
    await client.call_tool("save_note", {"key": "topic", "value": "fastmcp"})
    got = await client.call_tool("get_note", {"key": "topic"})
    assert got.data == "fastmcp"

    listed = await client.call_tool("list_notes", {})
    assert listed.data["topic"] == "fastmcp"
    assert "greeting" in listed.data  # seeded by lifespan


async def test_resources(client: Client) -> None:
    resources = await client.list_resources()
    uris = {str(r.uri) for r in resources}
    assert "config://app" in uris

    raw = await client.read_resource("config://app")
    payload = json.loads(raw[0].text)
    assert payload["name"] == "demo-mcp"

    note = await client.read_resource("notes://greeting")
    assert "hello" in note[0].text.lower()


async def test_prompts(client: Client) -> None:
    prompts = await client.list_prompts()
    names = {p.name for p in prompts}
    assert {"summarize", "code_review"} <= names

    rendered = await client.get_prompt("summarize", {"text": "hello world"})
    assert "hello world" in rendered.messages[0].content.text
