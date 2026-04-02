# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### Question 1: "What is the agentic loop?"

**Response:**
```
The **agentic loop** is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It's the core reasoning and action pattern that enables agents to work independently toward goals.

## The Basic Loop

The typical agentic loop consists of these stages:

1. **Perceive** — Gather information about the current state (read files, check outputs, observe environment)

2. **Reason** — Analyze the situation, plan next steps, make decisions based on goals and constraints

3. **Act** — Execute actions using available tools (run commands, write files, call APIs, send messages)

4. **Observe** — Collect feedback from the action's results (success, failure, output, errors)

5. **Repeat** — Continue the loop until the goal is achieved or a stopping condition is met

## Key Characteristics

- **Autonomy**: The agent decides what to do next without constant human direction
- **Iterative**: Progress happens through repeated cycles, not one-shot solutions
- **Feedback-driven**: Each action's outcome informs the next decision
- **Goal-oriented**: The loop continues until the objective is reached

## Example

For a task like "fix the bug in this code":
1. *Perceive*: Read the code file and error logs
2. *Reason*: Identify the likely cause of the bug
3. *Act*: Edit the file to fix the issue
4. *Observe*: Run tests to verify the fix works
5. *Repeat*: If tests fail, analyze why and try again

This loop is what distinguishes **agents** from simple chatbots—agents can take multi-step actions and adapt based on results rather than just responding to queries.
```

### Question 2: "What labs are available in our LMS?"

**Response:**
```
I'll explore the workspace to find information about available labs in the LMS.

Based on my exploration of the workspace, here are the available labs in your LMS:

## Available Labs

**Lab 8** (Current - `se-toolkit-lab-8`)
- **Required Tasks:**
  - Task 1
  - Task 2
  - Task 3
  - Task 4
  - Task 5

- **Optional Tasks:**
  - Task 1

**Lab 1** (Also available in wiki)
- Located at `/root/se-toolkit-lab-8/wiki/lab-1/`

The current lab environment is **Lab 8**, which appears to be a Software Engineering toolkit lab with 5 required tasks and 1 optional task. The lab includes:
- Setup scripts (`lab/setup/`)
- Task definitions (`lab/tasks/required/` and `lab/tasks/optional/`)
- Documentation in the wiki

Would you like me to show you the details of any specific task or help you get started with a particular lab?
```

This confirms the bare agent has no live LMS backend access - it only inspected local repo files and found Lab 8 and Lab 1 from the wiki documentation.

---

## Task 1B — Agent with LMS tools

### Question 1: "What labs are available?"

**Response:**
```
Here are the available labs:

1. **Lab 01** – Products, Architecture & Roles
2. **Lab 02** — Run, Fix, and Deploy a Backend Service
3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy
4. **Lab 04** — Testing, Front-end, and AI Agents
5. **Lab 05** — Data Pipeline and Analytics Dashboard
6. **Lab 06** — Build Your Own Agent
7. **Lab 07** — Build a Client with an AI Coding Agent
8. **Lab 08** — lab-08

Is there a specific lab you'd like to explore or get more information about?
```

The agent successfully called the MCP tool `mcp_lms_lms_labs` and returned real lab data from the backend.

### Question 2: "Is the LMS backend healthy?"

**Response:**
```
Yes, the LMS backend is healthy! It's currently tracking 56 items.
```

The agent called the `mcp_lms_lms_health` tool and returned real health data from the backend: `{"status": "healthy", "item_count": 56, "error": ""}`.

### Complex Question: "Which lab has the lowest pass rate?"

**Response:**
```
I'll help you find which lab has the lowest pass rate. Let me first get the list of available labs, then check their pass rates.

Now let me check the completion rate for each lab to find the lowest one:

Based on the completion rates:

- **Lab 01**: 93.9% (108 passed out of 115 total)
- **Lab 02-08**: 0.0% (0 passed out of 0 total - no submissions yet)

**Lab 01** has the lowest pass rate among labs that actually have submissions (93.9%). However, Labs 02-08 all show 0% completion rate because they have no submissions yet (0 total students).

If we're considering only labs with actual student activity, **Lab 01** has the lowest pass rate at 93.9%. If we include labs with no submissions, then Labs 02-08 all tie at 0%.
```

The agent chained multiple tool calls: first `mcp_lms_lms_labs` to get the list of labs, then `mcp_lms_lms_completion_rate` for each lab (lab-01 through lab-08).

---

## Task 1C — Skill prompt

### Question: "Show me the scores" (without specifying a lab)

**Response:**
```
I'll help you view the scores. First, let me fetch the list of available labs so you can choose which one you'd like to see.

Here are the available labs. Which one would you like to see the scores for?

1. **Lab 01** – Products, Architecture & Roles
2. **Lab 02** — Run, Fix, and Deploy a Backend Service
3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy
4. **Lab 04** — Testing, Front-end, and AI Agents
5. **Lab 05** — Data Pipeline and Analytics Dashboard
6. **Lab 06** — Build Your Own Agent
7. **Lab 07** — Build a Client with an AI Coding Agent
8. **Lab 08** — lab-08

Please let me know which lab you'd like to see the pass rates for, or I can show you scores for all of them.
```

This confirms the LMS skill is working - the agent now asks for lab selection when needed instead of guessing or failing.

---

## Task 2A — Deploy nanobot as Docker service

### Files Created

1. **`nanobot/entrypoint.py`** — Python entrypoint that resolves environment variables into config at runtime
2. **`nanobot/Dockerfile`** — Multi-stage Docker build using uv package manager

### Startup Log Excerpt

```terminal
nanobot-1  | Using config: /tmp/config.resolved.json
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | 2026-04-02 14:00:24.582 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-04-02 14:00:26.615 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'webchat': connected, 1 tools registered
nanobot-1  | 2026-04-02 14:00:26.615 | INFO     | nanobot.agent.loop:run:280 - Agent loop started
```

### Configuration Changes

- **`docker-compose.yml`**: Uncommented and configured `nanobot` service with:
  - Build context pointing to `./nanobot`
  - Volume mounts for nanobot, mcp, nanobot-websocket-channel, wiki, lab, contributing
  - Environment variables for LLM API, LMS backend, webchat channel, and OpenTelemetry
  - Dependencies on backend, qwen-code-api, and otel-collector

- **`caddy/Caddyfile`**: Uncommented `/ws/chat` route:
  ```
  handle /ws/chat {
      reverse_proxy http://nanobot:{$NANOBOT_WEBCHAT_CONTAINER_PORT}
  }
  ```

- **`nanobot/config.json`**: Added webchat channel configuration

---

## Task 2B — Add Flutter web client

### Files Modified

- **`docker-compose.yml`**: 
  - Uncommented `client-web-flutter` service building from `./nanobot-websocket-channel/client-web-flutter`
  - Added `client-web-flutter` to caddy's `depends_on`
  - Added `client-web-flutter:/srv/flutter:ro` volume mount to caddy service
  - Added `NANOBOT_WEBCHAT_CONTAINER_PORT` environment variable to caddy

- **`caddy/Caddyfile`**: Uncommented `/flutter` route:
  ```
  handle_path /flutter* {
      root * /srv/flutter
      try_files {path} /index.html
      file_server
  }
  ```

### Submodule Added

- **`nanobot-websocket-channel/`** — Git submodule containing:
  - `client-web-flutter/` — Flutter web chat client
  - `nanobot-webchat/` — WebSocket channel implementation
  - `mcp-webchat/` — MCP webchat server for agent communication

### Full Stack Verification

#### 1. Flutter Web Client Accessible

```terminal
$ curl -s http://localhost:42002/flutter/ | head -20
<!DOCTYPE html>
<html>
<head>
  <base href="/flutter/">
  <meta charset="UTF-8">
  <title>Nanobot</title>
  ...
```

#### 2. WebSocket Connection Working

The nanobot gateway is listening on the WebSocket endpoint and processing messages:

```terminal
$ docker compose logs nanobot | grep "Processing message"
nanobot-1  | 2026-04-02 15:47:42.919 | INFO | nanobot.agent.loop:_process_message:425 - Processing message from webchat:2214ad19-3d6b-46f8-ab68-713758825a88: hello
nanobot-1  | 2026-04-02 16:04:21.430 | INFO | nanobot.agent.loop:_process_message:425 - Processing message from webchat:f05981ca-4920-49dd-92fc-db8e0ea97b32: hello
```

#### 3. Agent Responds via WebSocket

```terminal
$ docker compose logs nanobot | grep "Response to"
nanobot-1  | 2026-04-02 15:47:48.310 | INFO | nanobot.agent.loop:_process_message:479 - Response to webchat:2214ad19-3d6b-46f8-ab68-713758825a88: Hello! 👋 I'm nanobot, your AI assistant. How can I help you today?
nanobot-1  | 2026-04-02 16:04:26.584 | INFO | nanobot.agent.loop:_process_message:479 - Response to webchat:f05981ca-4920-49dd-92fc-db8e0ea97b32: Hello! 👋 I'm nanobot, your AI assistant. How can I help you today?
```

### Architecture Flow

```
browser -> caddy (port 42002) -> nanobot webchat channel (port 8765) -> nanobot gateway -> mcp_lms -> backend
nanobot gateway -> qwen-code-api -> Qwen LLM
nanobot gateway -> mcp_webchat -> nanobot webchat UI relay -> browser
```

All components are running and communicating successfully:
- ✅ Flutter web client served at `/flutter/`
- ✅ WebSocket accepts connections at `/ws/chat`
- ✅ Agent processes messages and responds
- ✅ Full stack working end-to-end

### Flutter Conversation Transcript

Below is a real conversation captured from the Flutter web client session:

**User:** "How is the backend doing?"

**Agent:** "The backend is doing well! ✅

- **Status**: Healthy
- **Item count**: 56 items in the database

Everything looks good and..."

This conversation demonstrates:
1. Flutter web client successfully sends messages via WebSocket
2. nanobot gateway receives and processes the message
3. Agent calls the `mcp_lms_lms_health` tool to check backend status
4. Response is sent back through the WebSocket to the Flutter client

---

## Task 2 Fix Applied

### Issue Found and Fixed

**Problem:** The autochecker test was failing with "FAIL: could not reach LLM — Connection refused"

**Root Cause:** Port mismatch in `.env.docker.secret`:
- `QWEN_CODE_API_HOST_PORT` was set to `42005`
- But the qwen-code-api container was actually mapped to port `42006`

**Fix Applied:** Updated `.env.docker.secret` to use correct port:
```bash
QWEN_CODE_API_HOST_PORT=42006  # Was 42005
```

**Verification:**
```terminal
$ curl -H "Authorization: Bearer my-secret-qwen-key" http://localhost:42006/v1/models
{"object":"list","data":[
  {"id":"qwen3-coder-plus"},
  {"id":"qwen3-coder-flash"},
  {"id":"coder-model"},
  {"id":"vision-model"}
]}
```

The LLM API is now reachable from the VM shell using the environment variables in `.env.docker.secret`.

---
