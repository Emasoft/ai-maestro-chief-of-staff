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
agent: ai-maestro-chief-of-staff-main-agent
---

# Agent Termination

## Overview

Handles clean shutdown of agent instances including work verification, state preservation, termination execution, and registry cleanup. Use when an agent's work is complete, when reclaiming resources, or during cleanup.

## Prerequisites

- AI Maestro running, `ai-maestro-agents-management` and `agent-messaging` skills available
- Target agent in RUNNING or HIBERNATED state
- Team registry accessible via REST API

## Instructions

Copy this checklist and track your progress:
- [ ] Request GovernanceRequest approval from sourceManager (REQUIRED before any termination)
- [ ] Verify work complete and no pending uncommitted tasks
- [ ] Save final state and request agent context handoff
- [ ] Send termination warning via agent-messaging skill
- [ ] Execute termination via ai-maestro-agents-management skill
- [ ] Remove agent from team registry
- [ ] Cleanup resources and log termination event

### Termination Procedure (PROCEDURE 2)

1. **Request GovernanceRequest approval** - Submit termination request to sourceManager via `amcos-permission-management` skill. BLOCK until approved. Do NOT proceed without approval.
2. **Verify work complete** - Confirm no pending tasks or uncommitted work
3. **Save final state** - Request agent to save context/progress to handoff file
4. **Send termination warning** via `agent-messaging` with `hibernation-warning` type
5. **Execute termination** via `ai-maestro-agents-management` skill (requires confirmation)
6. **Update registry** - `uv run python scripts/amcos_team_registry.py remove-agent`
7. **Cleanup resources** - Verify tmux session gone, temp directories cleaned
8. **Log termination** - Record timestamp, reason, outcome in lifecycle log

### Graceful vs Forced

| Type | When | Procedure |
|------|------|-----------|
| Graceful | Agent responsive, work done | Full 8-step procedure |
| Forced | Unresponsive 5+ min | Skip steps 2-4, force-terminate tmux |

Always attempt graceful first.

### Quality Standards

- Terminated agents MUST be cleaned from registry
- ALWAYS hibernate instead of terminate when agent may be needed again
- ALWAYS save state before termination
- Log every termination per `references/record-keeping.md`

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
| Unresponsive to warning | Wait 2 min, retry. After 5 min, force-terminate. See `references/termination-procedures.md` 2.7 |
| tmux persists | `tmux kill-session -t <name>` |
| Registry update fails | Retry 3x, then remove via `ai-maestro-agents-management` skill |

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

- `references/termination-procedures.md`
- `references/op-terminate-agent.md`
- `references/success-criteria.md`
- `references/record-keeping.md`
