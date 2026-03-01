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
agent: amcos-main
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
3. **Request approval** -- send `urgent` replacement request to EAMA; wait for approval
4. **Create replacement** -- use `ai-maestro-agents-management` skill
5. **Notify EOA** -- so it can generate handoff docs and update kanban
6. **Send handoff docs** to new agent (validate with checklist below)
7. **Verify acknowledgment** -- confirm new agent received handoff and began work
8. **Close incident** -- log resolution, notify EAMA

See [references/agent-replacement-protocol.md](references/agent-replacement-protocol.md) and [references/op-replace-agent.md](references/op-replace-agent.md).
  <!-- TOC: agent-replacement-protocol.md -->
  - Phase 1: Failure confirmation and artifact preservation
  - Phase 2: Manager notification and approval
  - ...and 8 more sections
  <!-- /TOC -->

### Replacement Protocol Summary

```
Terminal failure -> AMCOS notifies EAMA -> EAMA approves
  -> Create new agent -> Notify EOA (handoff + kanban)
  -> Send handoff to new agent -> Agent acknowledges
```

### Key Consideration: Memory Loss

**CRITICAL**: The replacement agent has NO MEMORY of the old agent. Therefore:
- EOA must generate handoff documentation
- EOA must reassign tasks in GitHub Project kanban
- AMCOS must send handoff docs to new agent

**ROLE BOUNDARY**: AMCOS creates agents and sends context. EOA owns task assignment.

### Handoff Validation Checklist

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
| Manager approval | Approval message from EAMA |
| Agent creation | New agent online and registered |
| Work handoff | Docs sent and acknowledged |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Manager does not respond | Wait 15 min, reminder, escalate to user |
| New agent fails to register | Verify AI Maestro health and hooks |
| Handoff rejected | Queue and retry in 5 minutes |
| No artifacts recoverable | Document loss, notify EOA to recreate |

## Examples

```bash
# Request replacement approval
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to":"eama-assistant-manager","subject":"URGENT: Replace libs-svg-svgbbox","priority":"urgent","content":{"type":"replacement-request","message":"Terminal failure (3 crashes). Requesting replacement approval.","failed_agent":"libs-svg-svgbbox"}}'

# Notify orchestrator of replacement
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to":"eoa-orchestrator","subject":"Agent replaced: libs-svg-svgbbox","priority":"high","content":{"type":"replacement-notification","message":"Please generate handoff docs and update kanban.","old_agent":"libs-svg-svgbbox","new_agent":"libs-svg-svgbbox-v2"}}'
```

## Resources

- [references/agent-replacement-protocol.md](references/agent-replacement-protocol.md) - Full replacement protocol
- [references/op-replace-agent.md](references/op-replace-agent.md) - Replace agent runbook
