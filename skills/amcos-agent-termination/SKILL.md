---
name: amcos-agent-termination
description: Use when terminating agents or performing clean shutdown. Trigger with agent termination or stop requests.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-main
---

# Agent Termination

## Overview

Handles clean shutdown of agent instances including work verification, state preservation, termination execution, and registry cleanup. Use when an agent's work is complete, when reclaiming resources, or during cleanup.

## Prerequisites

- AI Maestro running, `ai-maestro-agents-management` and `agent-messaging` skills available
- Target agent in RUNNING or HIBERNATED state
- Team registry accessible via REST API

## Instructions

### Termination Procedure (PROCEDURE 2)

1. **Verify work complete** - Confirm no pending tasks or uncommitted work
2. **Save final state** - Request agent to save context/progress to handoff file
3. **Send termination warning** via `agent-messaging` with `hibernation-warning` type
4. **Execute termination** via `ai-maestro-agents-management` skill (requires confirmation)
5. **Update registry** - `uv run python scripts/amcos_team_registry.py remove-agent`
6. **Cleanup resources** - Verify tmux session gone, temp directories cleaned
7. **Log termination** - Record timestamp, reason, outcome in lifecycle log

### Graceful vs Forced

| Type | When | Procedure |
|------|------|-----------|
| Graceful | Agent responsive, work done | Full 7-step procedure |
| Forced | Unresponsive 5+ min | Skip steps 1-3, force-terminate tmux |

Always attempt graceful first.

### Quality Standards

- Terminated agents MUST be cleaned from registry
- Session names MUST follow `<role-prefix>-<project>-<descriptive>` convention
- ALWAYS hibernate instead of terminate when agent may be needed again
- ALWAYS save state before termination

### Record-Keeping

Log every termination: timestamp (ISO 8601), session name, type (graceful/forced), reason, state saved (y/n), registry updated (y/n). See [record-keeping.md](references/record-keeping.md) for format.
<!-- TOC: record-keeping.md -->
- Lifecycle Log
- Operation Audit Trail
- ...and 20 more sections
<!-- /TOC -->

## Output

| Step | Expected Output |
|------|----------------|
| Termination | tmux session destroyed, process stopped |
| Registry | Agent removed, status "terminated" |
| Cleanup | Resources freed, log entry written |

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Uncommitted work | Request commit/push first. Do NOT proceed until confirmed |
| Unresponsive to warning | Wait 2 min, retry. After 5 min, force-terminate. See [termination-procedures.md](references/termination-procedures.md) 2.7 |
| tmux persists | `tmux kill-session -t <name>` |
| Registry update fails | Retry 3x, then `DELETE /api/agents/{id}` |

## Examples

### Graceful Termination

```bash
# 1. Send status request via agent-messaging
# 2. After confirmation, terminate via ai-maestro-agents-management skill
# 3. Update registry
uv run python scripts/amcos_team_registry.py remove-agent --name epa-svgbbox-impl
# 4. Verify
tmux has-session -t epa-svgbbox-impl 2>/dev/null && echo "RUNNING" || echo "TERMINATED"
```

### Forced Termination

```bash
# After 5 min no response:
tmux kill-session -t epa-stuck-agent
uv run python scripts/amcos_team_registry.py remove-agent --name epa-stuck-agent
```

## Resources

- [Termination Procedures](references/termination-procedures.md)
  <!-- TOC: termination-procedures.md -->
  - What is agent termination - Understanding clean shutdown
  - Termination procedure - Step-by-step shutdown
  - ...and 5 more sections
  <!-- /TOC -->
- [op-terminate-agent.md](references/op-terminate-agent.md)
  <!-- TOC: op-terminate-agent.md -->
  - Procedure (Steps 1-7)
  - Examples
  - Error Handling
  <!-- /TOC -->
- [Success Criteria](references/success-criteria.md)
  <!-- TOC: success-criteria.md -->
  - Agent Terminated Cleanly
  - Common Self-Check Failures
  - Completion Criteria Summary
  <!-- /TOC -->
- [Record-Keeping](references/record-keeping.md)
  <!-- TOC: record-keeping.md -->
  - Lifecycle Log
  - Operation Audit Trail
  - Log Query Examples
  <!-- /TOC -->
