# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### Question 1: "What is the agentic loop?"

**Response:**
The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks.
It's the core reasoning and action pattern that enables agents to work independently toward goals.

The Basic Loop:
1. **Perceive** — Gather information about the current state (read files, check outputs, observe environment)
2. **Reason** — Analyze the situation, plan next steps, make decisions based on goals and constraints
3. **Act** — Execute actions using available tools (run commands, write files, call APIs, send messages)
4. **Observe** — Collect feedback from the action's results (success, failure, output, errors)
5. **Repeat** — Continue the loop until the goal is achieved or a stopping condition is met

Key Characteristics:
- **Autonomy**: The agent decides what to do next without constant human direction
- **Iterative**: Progress happens through repeated cycles, not one-shot solutions
- **Feedback-driven**: Each action's outcome informs the next decision
- **Goal-oriented**: The loop continues until the objective is reached

### Question 2: "What labs are available in our LMS?"

**Response:**
The agent explored local workspace files and found Lab 8 (current) and Lab 1 (in wiki).
It did NOT return real backend data from the LMS - it only inspected local repo files.
The agent found:
- Lab 8 with 5 required tasks and 1 optional task
- Lab 1 located in /root/se-toolkit-lab-8/wiki/lab-1/

This confirms the bare agent has no live LMS backend access yet - it can only inspect local files.

## Task 1B — Agent with LMS tools

### Question 1: "What labs are available?"

**Response:**
The agent successfully called the MCP tool `mcp_lms_lms_labs` and returned real lab data from the backend:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08

### Question 2: "Is the LMS backend healthy?"

**Response:**
"Yes, the LMS backend is healthy! It's currently tracking 56 items."

The agent called the `mcp_lms_lms_health` tool and returned real health data from the backend.

### Complex Question: "Which lab has the lowest pass rate?"

**Response:**
The agent chained multiple tool calls:
1. First called `mcp_lms_lms_labs` to get the list of labs
2. Then called `mcp_lms_lms_completion_rate` for each lab (lab-01 through lab-08)
3. Analyzed the results and provided a comprehensive answer:
   - Lab 01: 93.9% (108 passed out of 115 total)
   - Lab 02-08: 0.0% (0 passed out of 0 total - no submissions yet)

## Task 1C — Skill prompt

### Question: "Show me the scores" (without specifying a lab)

**Response:**
The agent demonstrated the skill prompt behavior:

1. Recognized that "scores" requires a lab parameter
2. Called `lms_labs` to fetch the list of available labs
3. Presented the list and asked the user to choose:

"Here are the available labs. Which one would you like to see the scores for?

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08

Please let me know which lab you'd like to see the pass rates for, or I can show you scores for all of them."

This confirms the LMS skill is working - the agent now asks for lab selection when needed instead of guessing or failing.

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
