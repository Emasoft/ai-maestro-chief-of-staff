---
name: amcos-emergency-handoff
description: Use when handling emergency work handoff from failed agents. Trigger with agent failure handoff or task blocker routing.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AMCOS Emergency Handoff

## Overview

Transfer critical work when deadlines cannot wait. Routes task blocker escalations to AMA.

## Prerequisites

- Deadline-critical failure OR task blocker escalation from AMOA
- AI Maestro running locally
- Handoff dir: `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/emergency/`

## Instructions

### Phase 5: Emergency Work Handoff

1. Identify critical tasks at risk
2. Notify AMOA of emergency handoff initiation
3. Find an available receiving agent
4. Create minimum-viable handoff doc (task, state, files, deadline)
5. Send handoff via AI Maestro
6. Verify receiving agent acknowledges
7. Notify AMA (notification only, no approval needed)
8. Monitor deadline compliance

| Aspect | Regular | Emergency |
|---|---|---|
| Timing | After replacement | Immediately |
| Completeness | Full context | Minimum viable |
| Recipient | Replacement | Any available |
| Duration | Permanent | Temporary |

### Task Blockers vs Agent Failures

**Agent Failures** -- resolve via failure recovery workflow.

**Task Blockers** -- blocked by missing info/access/user decision:
1. Receive escalation from AMOA
2. AMCOS can resolve? (reassignment, permission) -> handle directly
3. Needs user input? -> route to AMA via `blocker-escalation`
4. Track; route AMA response back to AMOA

### Decision Tree

```
Escalation -> Agent failure? -> recovery workflow
           -> Blocker AMCOS resolves? -> handle
           -> Needs user input? -> route to AMA
```

### Handoff Validation Checklist

Copy this checklist and track your progress:

- [ ] Required fields: from/to/type/UUID/task/failed_agent/failure_reason
- [ ] UUID unique, target alive, files exist
- [ ] No [TBD] placeholders, deadline and acceptance criteria set

## Output

| Result | Output |
|---|---|
| Handoff sent | Work transferred to available agent |
| Blocker routed | Awaiting AMA user decision |
| Blocker resolved | Agent reassigned directly |

## Error Handling

| Issue | Resolution |
|---|---|
| No available agent | Notify AMA for manual intervention |
| Handoff rejected | Try next available agent |
| Deadline missed | Document, notify, post-mortem |
| AMA unresponsive | 15 min wait, reminder, escalate |

## Examples

### Emergency handoff

```bash
amp-send.sh apps-svgplayer-development "EMERGENCY: SVG fix (2h)" urgent \
  '{"type":"emergency-handoff","message":"svgbbox crashed. Fix by 18:00 UTC.","task":"Fix SVG rendering","failed_agent":"libs-svg-svgbbox","deadline":"2025-02-05T18:00:00Z"}'
```

### Task blocker routing

```bash
amp-send.sh ama-assistant-manager "BLOCKER: API key needed" high \
  '{"type":"blocker-escalation","message":"API key needed, user must provide.","blocker_type":"user-decision","impact":"Deploy blocked","escalated_from":"amoa-deployment"}'
```

## Resources

- `references/work-handoff-during-failure.md` - Handoff procedures
- `references/op-emergency-handoff.md` - Handoff runbook
- `references/op-route-task-blocker.md` - Blocker routing runbook
