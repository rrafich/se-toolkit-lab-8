---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use LMS MCP tools to fetch live data from the Learning Management System backend.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `lms_health` | Check if LMS backend is healthy | None |
| `lms_labs` | List all available labs | None |
| `lms_learners` | List all registered learners | None |
| `lms_pass_rates` | Get pass rates for a lab | `lab` (required) |
| `lms_timeline` | Get submission timeline for a lab | `lab` (required) |
| `lms_groups` | Get group performance for a lab | `lab` (required) |
| `lms_top_learners` | Get top learners for a lab | `lab` (required), `limit` (optional, default 5) |
| `lms_completion_rate` | Get completion rate for a lab | `lab` (required) |
| `lms_sync_pipeline` | Trigger ETL sync pipeline | None |

## Strategy

### When lab parameter is needed but not provided

If the user asks for scores, pass rates, completion, groups, timeline, or top learners **without naming a lab**:

1. First call `lms_labs` to get the list of available labs
2. Use the `mcp_webchat_ui_message` tool (via the `structured-ui` skill) to present a choice
3. Use each lab's `title` field as the user-facing label
4. Use the lab's `id` field as the value to pass to subsequent tool calls

Example flow for "Show me the scores":
1. Call `lms_labs` → get list of labs
2. Present choice UI with lab titles as labels
3. Wait for user selection
4. Call `lms_pass_rates` with selected lab id

### Formatting numeric results

- **Percentages**: Format as `XX.X%` (one decimal place)
- **Counts**: Use plain integers with comma separators for thousands
- **Scores**: Show as `X.X / Y.Y` or percentage based on context
- **Dates**: Use human-readable format (e.g., "Apr 2, 2026")

### Response style

- Keep responses concise and focused on the data requested
- Use bullet points or tables for structured data
- Highlight key insights (e.g., highest/lowest values)
- When multiple tool calls are needed, explain the process briefly

### Handling "what can you do?"

When the user asks about capabilities, explain:

"I can help you explore data from the Learning Management System:

- **Lab overview**: List available labs, check backend health
- **Performance metrics**: Pass rates, completion rates, group performance
- **Learner insights**: Top performers, all registered learners
- **Timeline analysis**: Submission patterns over time
- **Data sync**: Trigger pipeline to fetch latest data from autochecker

Just ask about a specific lab or metric, and I'll fetch the live data for you."

## Integration with structured-ui

This skill works together with the `structured-ui` skill for interactive choices:

- When a lab selection is needed, delegate to `structured-ui` for the choice presentation
- Pass the lab `title` as the label and `id` as the value
- Let `structured-ui` handle the channel-specific rendering (WebSocket UI, plain text fallback)
