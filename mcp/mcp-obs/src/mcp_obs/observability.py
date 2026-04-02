"""Observability tools for VictoriaLogs and VictoriaTraces."""

import httpx
from pydantic import BaseModel


class LogsSearchParams(BaseModel):
    """Parameters for searching logs."""
    query: str
    limit: int = 100
    time_window: str = "1h"


class LogsErrorCountParams(BaseModel):
    """Parameters for counting errors."""
    service: str | None = None
    time_window: str = "1h"


class TracesListParams(BaseModel):
    """Parameters for listing traces."""
    service: str
    limit: int = 20


class TracesGetParams(BaseModel):
    """Parameters for getting a specific trace."""
    trace_id: str


class LogsSearchResult(BaseModel):
    """Result from logs search."""
    entries: list[dict]
    total: int


class LogsErrorCountResult(BaseModel):
    """Result from error count query."""
    service: str
    error_count: int
    time_window: str


class TracesListResult(BaseModel):
    """Result from traces list."""
    traces: list[dict]


class TracesGetResult(BaseModel):
    """Result from getting a trace."""
    trace: dict | None


async def logs_search(
    settings, params: LogsSearchParams
) -> LogsSearchResult:
    """Search logs using VictoriaLogs LogsQL query."""
    url = f"{settings.victorialogs_url}/select/logsql/query"
    query = params.query
    if not query.startswith("_time:"):
        query = f"_time:{params.time_window} {query}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={"query": query, "limit": params.limit},
            timeout=30.0,
        )
        response.raise_for_status()
        entries = response.json() if response.text else []
    
    if isinstance(entries, list):
        return LogsSearchResult(entries=entries, total=len(entries))
    return LogsSearchResult(entries=[entries] if entries else [], total=len(entries) if entries else 0)


async def logs_error_count(
    settings, params: LogsErrorCountParams
) -> LogsErrorCountResult:
    """Count errors in logs for a service over a time window."""
    query = f"_time:{params.time_window} severity:ERROR"
    if params.service:
        query += f' service.name:"{params.service}"'
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.victorialogs_url}/select/logsql/query",
            params={"query": query, "limit": 1000},
            timeout=30.0,
        )
        response.raise_for_status()
        entries = response.json() if response.text else []
    
    if isinstance(entries, dict):
        entries = [entries]
    
    return LogsErrorCountResult(
        service=params.service or "all",
        error_count=len(entries),
        time_window=params.time_window,
    )


async def traces_list(
    settings, params: TracesListParams
) -> TracesListResult:
    """List recent traces for a service."""
    url = f"{settings.victoriatraces_url}/select/jaeger/api/traces"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={"service": params.service, "limit": params.limit},
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
    
    traces = data.get("data", []) if isinstance(data, dict) else []
    return TracesListResult(traces=traces)


async def traces_get(
    settings, params: TracesGetParams
) -> TracesGetResult:
    """Get a specific trace by ID."""
    url = f"{settings.victoriatraces_url}/select/jaeger/api/traces/{params.trace_id}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        if response.status_code == 404:
            return TracesGetResult(trace=None)
        response.raise_for_status()
        data = response.json()
    
    trace_data = data.get("data", []) if isinstance(data, dict) else []
    trace = trace_data[0] if trace_data else None
    return TracesGetResult(trace=trace)
