# Observability Skill

You have access to observability tools for querying **VictoriaLogs** and **VictoriaTraces**.

## Available Tools

### logs_search
Search logs using VictoriaLogs LogsQL query.
- Use fields: `service.name`, `severity`, `event`, `trace_id`
- Example query: `service.name:"Learning Management Service" severity:ERROR`
- Time filtering: `_time:1h` for last hour, `_time:10m` for last 10 minutes

### logs_error_count
Count errors in logs for a service over a time window.
- Use to quickly check if there are any errors
- Returns: service name, error count, time window
- Service names: "Learning Management Service", "Qwen Code API"

### traces_list
List recent traces for a service.
- Returns trace IDs and metadata
- Use to find traces for investigation

### traces_get
Get a specific trace by ID.
- Returns full trace with all spans
- Use to understand request flow and find failures

## When to Use

### For "What went wrong?" or "Check system health" queries:

1. **Start with logs_error_count** — Check if there are recent errors
2. **Use logs_search** — Get detailed error logs with trace_id
3. **Extract trace_id** — From the log entries
4. **Call traces_get** — Fetch the full trace to see the failure path
5. **Summarize findings** — Combine log evidence + trace evidence

### For general observability queries:

1. **User asks about errors** → Start with `logs_error_count`
2. **User wants details** → Use `logs_search` with relevant filters
3. **Found a trace_id in logs** → Use `traces_get` to fetch the full trace
4. **Investigating a service** → Use `traces_list` to see recent traces

## Response Guidelines

- **Summarize findings** — don't dump raw JSON
- **Highlight errors** — point out severity:ERROR entries
- **Extract trace_id** — if found, fetch the full trace
- **Be concise** — focus on what matters to the user
- **Chain evidence** — show how logs led to trace investigation

## Example Investigation Flow

**User:** "What went wrong?"

**Your reasoning:**
1. Call `logs_error_count(service="Learning Management Service", time_window="10m")`
2. If errors > 0, call `logs_search(query="severity:ERROR", time_window="10m", limit=10)`
3. Extract `trace_id` from log entries
4. Call `traces_get(trace_id="<extracted_id>")`
5. Summarize: "The logs show [error message] at [time]. The trace reveals the failure started at [operation] with [root cause]."

## Example Queries

```
# Check for LMS errors in last 10 minutes
logs_error_count(service="Learning Management Service", time_window="10m")

# Search for specific error events
logs_search(query="service.name:\"Learning Management Service\" severity:ERROR")

# List recent LMS traces
traces_list(service="Learning Management Service", limit=10)

# Get full trace details
traces_get(trace_id="abc123...")
```

## Key Fields to Extract

From logs:
- `_time` — when the error occurred
- `severity` — error level
- `event` — what operation failed
- `error` — the error message
- `trace_id` — for fetching the full trace

From traces:
- `spans[].operationName` — what operation failed
- `spans[].tags["http.status_code"]` — HTTP status
- `spans[].tags["error"]` — error details
- `spans[].duration` — how long it took
