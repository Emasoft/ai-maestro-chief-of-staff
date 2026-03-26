---
name: amcos-agent-replacement
description: Use when replacing a failed agent with a new instance. Trigger with agent replacement or failover events.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AMCOS Agent Replacement

## Overview

Replace a failed agent when recovery has failed or failure is terminal. Covers failure confirmation, artifact preservation, manager approval, agent creation, orchestrator notification, and work handoff.

## Prerequisites

- Failure classified as Terminal, or all recovery strategies exhausted
- AI Maestro running locally with agent registry accessible
- Handoff directory at `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/`

## Instructions

### Phase 4: Agent Replacement Protocol

1. **Confirm failure** -- verify all recovery strategies attempted or failure is terminal
2. **Preserve artifacts** -- save recoverable work to `thoughts/shared/handoffs/AGENT_NAME/`
3. **Request approval** -- send `urgent` replacement request to AMAMA; wait for approval
4. **Create replacement** -- use `ai-maestro-agents-management` skill
5. **Notify AMOA** -- so it can generate handoff docs and update kanban
6. **Send handoff docs** to new agent (validate with checklist below)
7. **Verify acknowledgment** -- confirm new agent received handoff and began work
8. **Close incident** -- log resolution, notify AMAMA

### Replacement Protocol Summary

```
Terminal failure -> AMCOS notifies AMAMA -> AMAMA approves
  -> Create new agent -> Notify AMOA (handoff + kanban)
  -> Send handoff to new agent -> Agent acknowledges
```

### Key Consideration: Memory Loss

**CRITICAL**: The replacement agent has NO MEMORY of the old agent. Therefore:
- AMOA must generate handoff documentation
- AMOA must reassign tasks in GitHub Project kanban
- AMCOS must send handoff docs to new agent

**ROLE BOUNDARY**: AMCOS creates agents and sends context. AMOA owns task assignment.

### Handoff Validation Checklist

Copy this checklist and track your progress:

```markdown
- [ ] Required fields present (from/to/type/UUID/task/failed_agent/failure_reason)
- [ ] UUID is unique
- [ ] Target agent exists and is alive
- [ ] All referenced files exist
- [ ] No [TBD] placeholders
- [ ] Acceptance criteria defined
```

## Output

| Phase | Output |
|-------|--------|
| Artifact preservation | Files saved to handoff directory |
| Manager approval | Approval message from AMAMA |
| Agent creation | New agent online and registered |
| Work handoff | Docs sent and acknowledged |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Manager does not respond | Wait 15 min, reminder, escalate to user |
| New agent fails to register | Verify AI Maestro health and hooks |
| Handoff rejected | Queue and retry in 5 minutes |
| No artifacts recoverable | Document loss, notify AMOA to recreate |

## Examples

- **Request replacement approval**: Send an `urgent` AMP message to `amama-assistant-manager` with type `replacement-request`, including the failed agent name and failure summary. Use the `agent-messaging` skill.
- **Notify orchestrator of replacement**: Send a `high`-priority AMP message to `amoa-orchestrator` with type `replacement-notification`, including old and new agent names. Use the `agent-messaging` skill. The orchestrator will generate handoff docs and update the kanban.

## Resources

