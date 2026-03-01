---
name: amcos-agent-hibernation
description: Use when hibernating idle agents or waking hibernated agents. Trigger with hibernate, wake, or resource pressure events.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-main
---

# Agent Hibernation and Wake

## Overview

Suspends idle agents to conserve resources and resumes them when work is available. Hibernation preserves full state so agents resume exactly where they left off. Use for idle timeouts, resource pressure, scheduled pauses, and wake operations.

## Prerequisites

- AI Maestro running, `ai-maestro-agents-management` and `agent-messaging` skills available
- Target agent in RUNNING state (hibernate) or HIBERNATED state (wake)
- Team registry accessible via REST API

## Instructions

### Agent States

```
SPAWNING -> RUNNING <-> HIBERNATED
              |
              v
           TERMINATED
```

### Hibernate Procedure (PROCEDURE 3)

1. **Confirm idle** - Verify no active work via status request message
2. **Send warning** via `agent-messaging` with `hibernation-warning` type
3. **Request state capture** - Agent saves context and handoff to storage
4. **Execute hibernation** via `ai-maestro-agents-management` skill
5. **Update registry** - `uv run python scripts/amcos_team_registry.py update-status --name <agent> --status hibernated`
6. **Log event** in lifecycle log

### Wake Procedure

1. **Verify hibernated** - Check registry status
2. **Check resources** - Confirm slot available (max 5 concurrent)
3. **Execute wake** via `ai-maestro-agents-management` skill (uses `--continue`)
4. **Verify responsive** - Health check, expect response within 30s
5. **Restore state** - Agent reads saved handoff/context
6. **Update registry** - Mark as "running"
7. **Log event** in lifecycle log

### Resource Limits

| Resource | Limit | Action |
|----------|-------|--------|
| Max concurrent agents | 5 | Queue, hibernate oldest idle |
| Max memory per agent | 2GB | Terminate or hibernate |
| Idle timeout | 30 min | Hibernate agent |

Remote host operations require GovernanceRequest; state replicated via GovernanceSyncMessage.

## Output

| Operation | Expected Output |
|-----------|----------------|
| Hibernate | State saved, session suspended, registry "hibernated" |
| Wake | Session resumed, agent responsive, registry "running" |

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Active work during hibernate | Wait for task to complete or request checkpoint |
| State capture fails | Retry once, proceed with warning (state loss risk) |
| Wake fails | See [hibernation-procedures.md](references/hibernation-procedures.md) 3.7. Try force-wake, respawn if needed |
| Resource limit on wake | Hibernate another idle agent first |
| Unresponsive after wake | Wait 60s, retry. If still unresponsive, terminate and respawn |

## Examples

### Hibernate an Idle Agent

```bash
# 1. Warn via agent-messaging: type=hibernation-warning
# 2. Wait 2 min for state capture
# 3. Hibernate via ai-maestro-agents-management skill
# 4. Update registry
uv run python scripts/amcos_team_registry.py update-status \
  --name epa-svgbbox-impl --status hibernated
```

### Wake a Hibernated Agent

```bash
# 1. Wake via ai-maestro-agents-management skill (uses --continue)
# 2. Notify via agent-messaging: type=wake-notification
# 3. Update registry
uv run python scripts/amcos_team_registry.py update-status \
  --name epa-svgbbox-impl --status running
```

## Resources

- [Hibernation Procedures](references/hibernation-procedures.md)
  <!-- TOC: hibernation-procedures.md -->
  - What is agent hibernation - Understanding state suspension
  - Hibernation procedure - Step-by-step suspension
  - ...and 5 more sections
  <!-- /TOC -->
- [op-hibernate-agent.md](references/op-hibernate-agent.md)
  <!-- TOC: op-hibernate-agent.md -->
  - Procedure (Steps 1-6)
  - Examples
  - Error Handling
  <!-- /TOC -->
- [op-wake-agent.md](references/op-wake-agent.md)
  <!-- TOC: op-wake-agent.md -->
  - Procedure (Steps 1-7)
  - Examples
  - Error Handling
  <!-- /TOC -->
