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
