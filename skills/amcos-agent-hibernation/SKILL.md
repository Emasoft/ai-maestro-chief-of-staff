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
agent: ai-maestro-chief-of-staff-main-agent
---

# Agent Hibernation and Wake

## Overview

Suspends idle agents and resumes them when needed. Preserves full state so agents resume where they left off.

## Prerequisites

- AI Maestro running with `ai-maestro-agents-management` and `agent-messaging` skills
- Agent in RUNNING (hibernate) or HIBERNATED (wake) state
- Team registry accessible

## Instructions

Copy this checklist and track your progress:
- [ ] Request GovernanceRequest approval from sourceManager via amcos-permission-management
- [ ] Confirm agent idle with no active work
- [ ] Send hibernation warning via agent-messaging skill
- [ ] Request state capture and wait for confirmation
- [ ] Execute hibernation via ai-maestro-agents-management skill
- [ ] Update registry status to hibernated and log event

### Agent States

```
SPAWNING -> RUNNING <-> HIBERNATED
              |
              v
           TERMINATED
```

### Hibernate Procedure (PROCEDURE 3)

1. **Request approval** via `amcos-permission-management`. BLOCK until approved.
2. **Confirm idle** - Verify no active work
3. **Send warning** via `agent-messaging` (type: `hibernation-warning`)
4. **Request state capture** - Agent saves context/handoff
5. **Execute** via `ai-maestro-agents-management`
6. **Update registry** - `uv run python scripts/amcos_team_registry.py update-status --name <agent> --status hibernated`
7. **Log event**

### Wake Procedure

1. **Verify hibernated** - Check registry
2. **Check resources** - Confirm slot available (max 5)
3. **Execute wake** via `ai-maestro-agents-management` (`--continue`)
4. **Verify responsive** - Expect response within 30s
5. **Restore state** - Agent reads saved handoff/context
6. **Update registry** - Mark "running"
7. **Log event**

### Resource Limits

| Resource | Limit | Action |
|----------|-------|--------|
| Concurrent agents | 5 | Queue/hibernate oldest idle |
| Memory per agent | 2GB | Terminate/hibernate |
| Idle timeout | 30 min | Hibernate |

Remote host ops require GovernanceRequest; state replicated via GovernanceSyncMessage.

## Output

| Operation | Expected Output |
|-----------|----------------|
| Hibernate | State saved, session suspended, registry "hibernated" |
| Wake | Session resumed, agent responsive, registry "running" |

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Active work during hibernate | Wait for completion or checkpoint |
| State capture fails | Retry once, warn (state loss risk) |
| Wake fails | Force-wake, respawn if needed (see 3.7) |
| Resource limit on wake | Hibernate another idle agent first |
| Unresponsive after wake | Wait 60s, retry, then terminate/respawn |

## Examples

### Hibernate an Idle Agent

```bash
# Warn -> wait 2min -> hibernate -> update registry
uv run python scripts/amcos_team_registry.py update-status \
  --name epa-svgbbox-impl --status hibernated
```

### Wake a Hibernated Agent

```bash
# Wake (--continue) -> notify -> update registry
uv run python scripts/amcos_team_registry.py update-status \
  --name epa-svgbbox-impl --status running
```

## Resources

- `references/hibernation-procedures.md`
- `references/op-hibernate-agent.md`
- `references/op-wake-agent.md`
