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

1. **User asks about errors** → Start with `logs_error_count` to check if errors exist
2. **User wants details** → Use `logs_search` with relevant filters
3. **Found a trace_id in logs** → Use `traces_get` to fetch the full trace
4. **Investigating a service** → Use `traces_list` to see recent traces

## Response Guidelines

- **Summarize findings** — don't dump raw JSON
- **Highlight errors** — point out severity:ERROR entries
- **Extract trace_id** — if found, offer to fetch the full trace
- **Be concise** — focus on what matters to the user

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

## Reasoning Flow

1. User asks "Any errors?" → Call `logs_error_count` first
2. If errors found → Call `logs_search` to get details
3. If trace_id found in logs → Call `traces_get` for full picture
4. Summarize: "Found X errors in the last Y minutes. The main issue was Z."
