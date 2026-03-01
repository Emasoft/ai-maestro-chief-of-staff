---
name: amcos-emergency-handoff
description: Use when performing emergency work handoff from a failed agent or routing task blockers. Trigger with deadline-critical failures or task blocker escalations.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-main
---

# AMCOS Emergency Handoff

## Overview

Transfer critical work immediately when deadlines cannot wait for full replacement. Also covers routing task blocker escalations to EAMA for user decisions.

## Prerequisites

- A deadline-critical failure has occurred, OR a task blocker escalation received from EOA
- AI Maestro running locally
- Emergency handoff dir at `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/emergency/`

## Instructions

### Phase 5: Emergency Work Handoff

1. Identify critical tasks at risk
2. Notify EOA of emergency handoff initiation
3. Find an available receiving agent
4. Create minimum-viable handoff doc (task, state, files, deadline)
5. Send handoff via AI Maestro
6. Verify receiving agent acknowledges
7. Notify EAMA (notification only, no approval needed)
8. Monitor deadline compliance

| Aspect | Regular | Emergency |
|--------|---------|-----------|
| Timing | After replacement | Immediately |
| Completeness | Full context | Minimum viable |
| Recipient | Replacement agent | Any available |
| Duration | Permanent | Temporary |

See [references/work-handoff-during-failure.md](references/work-handoff-during-failure.md) and [references/op-emergency-handoff.md](references/op-emergency-handoff.md).
  <!-- TOC: work-handoff-during-failure.md -->
  - Triggering emergency handoff
  - Creating emergency handoff documentation
  - ...and 6 more sections
  <!-- /TOC -->

### Task Blockers vs Agent Failures

**Agent Failures** -- AMCOS resolves directly via failure recovery workflow.

**Task Blockers** -- work blocked by missing info/access/user decision. Routing steps:
1. Receive escalation from EOA
2. Can AMCOS resolve? (agent reassignment, permission) -> handle directly
3. Needs user input? -> route to EAMA with `blocker-escalation` message
4. Track blocker; when EAMA responds, route resolution back to EOA

See [references/op-route-task-blocker.md](references/op-route-task-blocker.md).
  <!-- TOC: op-route-task-blocker.md -->
  - Decision Tree
  - Step 1: Receive and Classify Escalation
  - ...and 6 more sections
  <!-- /TOC -->

### Decision Tree

```
AMCOS receives escalation
  +- Agent failure? -> failure recovery workflow
  +- Blocker AMCOS can resolve? -> handle directly
  +- Blocker needs user input? -> route to EAMA
```

### Handoff Validation Checklist

```markdown
- [ ] Required fields: from/to/type/UUID/task/failed_agent/failure_reason
- [ ] UUID unique, target agent alive, referenced files exist
- [ ] No [TBD] placeholders, deadline stated, acceptance criteria defined
```

## Output

| Result | Output |
|--------|--------|
| Emergency handoff sent | Work transferred to available agent |
| Blocker routed to EAMA | Awaiting user decision |
| Blocker resolved by AMCOS | Agent reassigned directly |

## Error Handling

| Issue | Resolution |
|-------|------------|
| No available agent | Notify EAMA urgently for manual intervention |
| Handoff rejected | Try next available agent |
| Deadline missed | Document, notify stakeholders, post-mortem |
| EAMA does not respond | Wait 15 min, reminder, escalate to user |

## Examples

### Emergency handoff with deadline

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to":"apps-svgplayer-development","subject":"EMERGENCY: SVG fix (2h deadline)","priority":"urgent","content":{"type":"emergency-handoff","message":"libs-svg-svgbbox crashed. Fix needed by 18:00 UTC.","task":"Fix SVG rendering bug","failed_agent":"libs-svg-svgbbox","deadline":"2025-02-05T18:00:00Z"}}'
```

### Routing a task blocker

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to":"eama-assistant-manager","subject":"BLOCKER: API key required","priority":"high","content":{"type":"blocker-escalation","message":"Production API key needed, only user can provide.","blocker_type":"user-decision","impact":"Deployment blocked, 3 tasks waiting","escalated_from":"eoa-deployment"}}'
```

## Resources

- [references/work-handoff-during-failure.md](references/work-handoff-during-failure.md) - Emergency handoff procedures
- [references/op-emergency-handoff.md](references/op-emergency-handoff.md) - Emergency handoff runbook
- [references/op-route-task-blocker.md](references/op-route-task-blocker.md) - Task blocker routing runbook
