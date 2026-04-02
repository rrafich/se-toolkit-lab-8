# Lab 8 Report

## Task 1 — Connect the Agent to the LMS Backend

### Part A — Terminal agent with LMS tools

Created `nanobot/` directory with:
- `config.json` — nanobot configuration with custom LLM provider
- `workspace/` — agent workspace with skills

### Part B — MCP server for LMS backend

Created `mcp/mcp-lms/` with tools:
- `lms_health` — Check backend health
- `lms_labs` — List available labs
- `lms_learners` — List registered learners
- `lms_pass_rates` — Get lab pass rates
- `lms_timeline` — Get submission timeline
- `lms_groups` — Get group statistics
- `lms_top_learners` — Get top performers
- `lms_completion_rate` — Get completion rate
- `lms_sync_pipeline` — Trigger ETL sync

## Task 2 — Deploy the Agent and Add a Web Client

### Part A — Deploy nanobot as Docker service

- Created `nanobot/entrypoint.py` — resolves env vars into config at runtime
- Created `nanobot/Dockerfile` — multi-stage uv build
- Updated `docker-compose.yml` — nanobot service with workspace mount

### Part B — Add WebSocket channel and web client

- Installed `nanobot-webchat` channel plugin
- Installed `mcp-webchat` for structured UI messages
- Enabled `/ws/chat` route in Caddyfile
- Enabled `/flutter` route for web client

**Checkpoint verified:**
- WebSocket endpoint responds at `ws://localhost:42002/ws/chat`
- Flutter client accessible at `http://localhost:42002/flutter`
- Agent answers capability questions

## Task 3 — Give the Agent New Eyes (Observability)

### Task 3A — Explore structured logs

Backend emits structured log events via OpenTelemetry with fields:
- `service.name`: "Learning Management Service" or "Qwen Code API"
- `severity`: INFO, WARNING, ERROR
- `event`: request_started, auth_success, db_query, request_completed
- `trace_id`: for distributed tracing
- `span_id`: individual span identifier

**Example structured log entry from docker compose logs:**
```
2026-04-02 21:57:13,019 ERROR [lms_backend.db.items] [trace_id=024c5f70bc6f0563ab1aff555a4af9da] 
- db_query
error: "[Errno -2] Name or service not known"
```

**VictoriaLogs UI query:**
```
_time:10m service.name:"Learning Management Service" severity:ERROR
```

**VictoriaLogs UI screenshot evidence:**
- Accessed at: `http://localhost:42002/utils/victorialogs/select/vmui`
- Query returns JSON log entries with fields: `_msg`, `_time`, `severity`, `service.name`, `trace_id`, `error`

### Task 3B — Explore traces

**VictoriaTraces API endpoint:** `http://localhost:42011/select/jaeger/api/`

**Services traced:**
```json
{"data": ["Learning Management Service", "Qwen Code API"]}
```

**Sample trace data (trace ID: 024c5f70bc6f0563ab1aff555a4af9da):**

```json
{
  "processes": {
    "p1": {
      "serviceName": "Learning Management Service",
      "tags": [
        {"key": "telemetry.sdk.language", "value": "python"},
        {"key": "telemetry.sdk.name", "value": "opentelemetry"},
        {"key": "telemetry.sdk.version", "value": "1.40.0"}
      ]
    }
  },
  "spans": [
    {
      "traceID": "024c5f70bc6f0563ab1aff555a4af9da",
      "spanID": "99c5f2c5994af915",
      "operationName": "GET /items/",
      "duration": 46000,
      "startTime": 1775167033150477,
      "tags": [
        {"key": "http.method", "value": "GET"},
        {"key": "http.url", "value": "/items/"},
        {"key": "http.status_code", "value": "404"},
        {"key": "error", "value": "socket.gaierror: [Errno -2] Name or service not known"}
      ]
    },
    {
      "traceID": "024c5f70bc6f0563ab1aff555a4af9da",
      "spanID": "6f5be062db91e0bb",
      "operationName": "db_query",
      "duration": 208000,
      "tags": [
        {"key": "db.system", "value": "postgresql"},
        {"key": "db.operation", "value": "SELECT"},
        {"key": "db.table", "value": "item"},
        {"key": "error", "value": "socket.gaierror: [Errno -2] Name or service not known"}
      ]
    }
  ]
}
```

**Trace analysis:**
- Trace shows request flow: `GET /items/` → `db_query` → error
- Root cause: PostgreSQL hostname resolution failure
- Span hierarchy shows parent-child relationships via `references`

### Task 3C — Observability MCP tools

Created 4 MCP tools in `mcp/mcp-obs/`:

**1. logs_search**
```python
LogsSearchParams(query: str, limit: int = 100, time_window: str = "1h")
```

**2. logs_error_count**
```python
LogsErrorCountParams(service: str | None = None, time_window: str = "1h")
```

**3. traces_list**
```python
TracesListParams(service: str, limit: int = 20)
```

**4. traces_get**
```python
TracesGetParams(trace_id: str)
```

#### Agent Test: Normal Conditions

**Question:** "Any LMS backend errors in the last 10 minutes?"

**Agent tool calls (from nanobot logs):**
```
Tool call: mcp_observability_logs_error_count({"service": "Learning Management Service", "time_window": "10m"})
Tool call: mcp_observability_logs_search({"query": "service.name:\"Learning Management Service\" severity:ERROR", "time_window": "10m", "limit": 10})
```

**Agent response:**
```
Good news! **No LMS backend errors** in the last 10 minutes. The service has been running cleanly.
```

#### Agent Test: Failure Conditions (PostgreSQL stopped)

**Question:** "List recent traces for Learning Management Service"

**Agent tool calls:**
```
Tool call: mcp_observability_traces_list({"service": "Learning Management Service", "limit": 10})
```

**Agent response with raw trace data:**
```
Here are the recent traces for the **Learning Management Service**:

## Summary of Recent Traces

| Trace ID | Operation | Status | Duration | Issue |
|----------|-----------|--------|----------|-------|
| `024c5f70...` | GET /items/ | **404** | 46ms | 🔴 DB connection error |
| `0df6997d...` | GET /items/ | **404** | 56ms | 🔴 DB connection error |
| `b95ed19c...` | GET /items/ | **404** | 253ms | 🔴 DB connection error |
| `dda00ab0...` | GET /items/ | **401** | 217ms | Unauthorized |
| `8300d79c...` | GET /items/ | **200** | 641ms | ✅ Success |

## Key Findings

### 🔴 Recent Errors (Most Critical)
The **3 most recent traces** all show the same error pattern:
- **Error**: `socket.gaierror: [Errno -2] Name or service not known`
- **Cause**: Failed to connect to PostgreSQL database at `postgres:5432`
- **Impact**: All `/items/` requests returning 404

### Trace Span Details
- **span_id**: `99c5f2c5994af915`
- **operation**: `GET /items/`
- **http.status_code**: `404`
- **db.operation**: `SELECT` on table `item`
- **error**: Connection refused to postgres:5432
```

#### Raw Tool Output Evidence

**logs_error_count raw output:**
```json
{
  "service": "Learning Management Service",
  "error_count": 3,
  "time_window": "10m"
}
```

**logs_search raw output (sample entry):**
```json
{
  "_msg": "db_query",
  "_time": "2026-04-02T21:57:13.019Z",
  "severity": "ERROR",
  "service.name": "Learning Management Service",
  "event": "db_query",
  "error": "[Errno -2] Name or service not known",
  "trace_id": "024c5f70bc6f0563ab1aff555a4af9da",
  "span_id": "6f5be062db91e0bb",
  "operation": "select",
  "table": "item"
}
```

**traces_list raw output (summary):**
```json
{
  "traces": [
    {
      "traceID": "024c5f70bc6f0563ab1aff555a4af9da",
      "spans": [
        {"operationName": "GET /items/", "duration": 46000, "tags": {"http.status_code": "404"}}
      ]
    }
  ]
}
```

### Files Created/Modified

**MCP Observability Server:**
- `mcp/mcp-obs/pyproject.toml`
- `mcp/mcp-obs/src/mcp_obs/__init__.py`
- `mcp/mcp-obs/src/mcp_obs/__main__.py`
- `mcp/mcp-obs/src/mcp_obs/settings.py`
- `mcp/mcp-obs/src/mcp_obs/observability.py` — Tool implementations
- `mcp/mcp-obs/src/mcp_obs/server.py` — MCP server

**Nanobot Configuration:**
- `nanobot/workspace/skills/observability/SKILL.md` — Observability skill prompt
- `nanobot/config.json` — Added observability MCP server
- `nanobot/entrypoint.py` — Added observability env var injection
- `docker-compose.yml` — Already has NANOBOT_VICTORIALOGS_URL and NANOBOT_VICTORIATRACES_URL

### Acceptance Criteria

✅ Structured log events identified in docker compose logs output
✅ VictoriaLogs UI queries working (accessed at /utils/victorialogs)
✅ VictoriaTraces UI accessible (accessed at /utils/victoriatraces)
✅ 4 MCP tools registered (logs_search, logs_error_count, traces_list, traces_get)
✅ Observability skill created and loaded
✅ Agent answers scoped observability questions with raw data output
✅ Task 3B includes specific trace span descriptions
✅ Task 3C includes visible raw tool output in agent transcript

## Task 4 — Diagnose a Failure and Make the Agent Proactive

### Task 4A — Multi-step investigation

**Enhanced observability skill** to guide one-shot investigation:
- When user asks "What went wrong?" or "Check system health":
  1. Call `logs_error_count` to check for recent errors
  2. Call `logs_search` to get detailed error logs with trace_id
  3. Extract `trace_id` from log entries
  4. Call `traces_get` to fetch the full trace
  5. Summarize findings combining log + trace evidence

**Failure scenario:** PostgreSQL stopped

**Agent investigation flow (from nanobot logs):**
```
Tool call: mcp_observability_logs_search({"query": "service.name:\"Learning Management Service\" AND severity:ERROR", "time_window": "10m", "limit": 50})
Tool call: mcp_observability_traces_list({"service": "Learning Management Service", "limit": 20})
Tool call: mcp_observability_logs_search({"query": "service.name:\"Learning Management Service\" AND (436 OR \"Name or service not known\" OR \"gaierror\")", "time_window": "10m", "limit": 30})
```

**Agent response:**
```
## LMS Backend Failure Analysis

I found **two critical issues** affecting the Learning Management Service:

### 🔴 Issue 1: Database Connection Failure
- **Error**: `socket.gaierror: [Errno -2] Name or service not known`
- **Cause**: PostgreSQL hostname `postgres:5432` cannot be resolved
- **Impact**: All database queries failing

### 🔴 Issue 2: External API Failure  
- **Error**: `httpx.HTTPStatusError: Client error '436 status code 436'`
- **URL**: `https://auche.namaz.live/api/items`
- **Impact**: ETL sync pipeline failing

### Evidence Chain
1. **Logs** show `severity:ERROR` with `event:db_query` and connection errors
2. **Traces** show span hierarchy: `GET /items/` → `db_query` → error
3. **Root cause**: PostgreSQL service unavailable
```

### Task 4B — Scheduled health check via cron

**Created cron job from Flutter chat:**
```
Tool call: cron({"action": "add", "every_seconds": 120, "message": "LMS Health Check: Check LMS backend health, search for errors in logs from the last 2 minutes, inspect a trace if errors found, and post a short summary"})
Cron: added job 'LMS Health Check: Check LMS ba' (b37762b2)
```

**Cron job configuration:**
- Runs every 120 seconds (2 minutes)
- Checks LMS backend health
- Searches for errors in last 2 minutes
- Inspects traces if errors found
- Posts summary to chat

### Task 4C — Bug fix and recovery

#### Root Cause
**Planted bug location:** `backend/src/lms_backend/routers/items.py`

**Bug description:** The `get_items()` function caught all exceptions and returned `404 Not Found` instead of the actual database error. This masked the real PostgreSQL failure.

**Original code (buggy):**
```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    try:
        return await read_items(session)
    except Exception as exc:
        logger.warning("items_list_failed_as_not_found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Items not found",
        ) from exc
```

#### Fix Applied
**Changed to return 500 for database errors:**
```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    try:
        return await read_items(session)
    except SQLAlchemyError as exc:
        logger.error("items_list_database_error", extra={"error": str(exc)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(exc)}",
        ) from exc
    except Exception as exc:
        logger.error("items_list_unexpected_error", extra={"error": str(exc)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(exc)}",
        ) from exc
```

**Key changes:**
1. Import `SQLAlchemyError` from `sqlalchemy.exc`
2. Catch `SQLAlchemyError` separately with 500 status code
3. Log at ERROR level instead of WARNING
4. Include actual error message in response
5. Applied same fix to `get_item()` and `put_item()` endpoints

#### Post-fix failure check (PostgreSQL stopped)

**Backend logs after fix:**
```
2026-04-02 22:51:44,877 ERROR [lms_backend.routers.items] - items_list_unexpected_error
2026-04-02 22:51:44,878 ERROR [lms_backend.main] - request_completed
INFO: 172.20.0.9:53010 - "GET /items/ HTTP/1.1" 500 Internal Server Error
```

**Before fix:** Response was `404 Not Found` (misleading)
**After fix:** Response is `500 Internal Server Error` (accurate)

#### Healthy follow-up (PostgreSQL restarted)

After restarting PostgreSQL, the cron health check reports:
```
System looks healthy - no recent backend errors found in the last 2 minutes.
```

**Verification:**
- Backend health endpoint returns 200 OK
- LMS tools (labs, learners, etc.) work correctly
- No ERROR level logs in VictoriaLogs
- Traces show successful request completion

### Files Modified

**Task 4A:**
- `nanobot/workspace/skills/observability/SKILL.md` — Enhanced with investigation flow

**Task 4C:**
- `backend/src/lms_backend/routers/items.py` — Fixed exception handling to return 500 for database errors

### Acceptance Criteria

✅ Observability skill guides agent to chain log and trace tools
✅ Created recurring health check from Flutter chat via cron tool
✅ Proactive health report appears in chat while failure present
✅ Fixed planted bug in backend code (404 → 500 for DB errors)
✅ After fix, failure path reveals real underlying error
✅ After recovery, health report says system looks healthy
✅ REPORT.md contains evidence from Task 4A, 4B, and 4C
