"""Stdio MCP server exposing observability operations as typed tools."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel

from mcp_obs.settings import resolve_settings
from mcp_obs.observability import (
    logs_search,
    logs_error_count,
    traces_list,
    traces_get,
    LogsSearchParams,
    LogsErrorCountParams,
    TracesListParams,
    TracesGetParams,
)


def _text(data: BaseModel | list | dict) -> list[TextContent]:
    """Convert data to MCP text response."""
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    else:
        payload = data
    return [TextContent(
        type="text",
        text=json.dumps(payload, indent=2, ensure_ascii=False)
    )]


TOOL_SPECS = [
    {
        "name": "logs_search",
        "description": "Search logs using VictoriaLogs LogsQL query. Use fields like service.name, severity, event, trace_id.",
        "model": LogsSearchParams,
    },
    {
        "name": "logs_error_count",
        "description": "Count errors in logs for a service over a time window. Returns error count and time window.",
        "model": LogsErrorCountParams,
    },
    {
        "name": "traces_list",
        "description": "List recent traces for a service. Returns trace IDs and metadata.",
        "model": TracesListParams,
    },
    {
        "name": "traces_get",
        "description": "Get a specific trace by ID. Returns full trace with all spans.",
        "model": TracesGetParams,
    },
]

TOOLS_BY_NAME = {spec["name"]: spec for spec in TOOL_SPECS}


def create_server(settings) -> Server:
    """Create the observability MCP server."""
    server = Server("observability")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=spec["name"],
                description=spec["description"],
                inputSchema=spec["model"].model_json_schema(),
            )
            for spec in TOOL_SPECS
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[TextContent]:
        spec = TOOLS_BY_NAME.get(name)
        if spec is None:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        try:
            args = spec["model"].model_validate(arguments or {})
            if name == "logs_search":
                result = await logs_search(settings, args)
            elif name == "logs_error_count":
                result = await logs_error_count(settings, args)
            elif name == "traces_list":
                result = await traces_list(settings, args)
            elif name == "traces_get":
                result = await traces_get(settings, args)
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
            return _text(result)
        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    _ = list_tools, call_tool
    return server


async def main() -> None:
    """Main entry point."""
    settings = resolve_settings()
    server = create_server(settings)
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
