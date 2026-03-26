---
name: amcos-agent-coordination
description: Use when managing team registry, inter-agent messaging, role boundaries, or sub-agent delegation. Trigger with team coordination tasks.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Agent Coordination

## Overview

Manages team registry, messaging, role boundaries, and delegation.

## Prerequisites

- AI Maestro running with `agent-messaging` skill
- Registry via REST API (`GET /api/teams/{id}/agents`)
- Script: `uv run python scripts/amcos_team_registry.py`

## Instructions

1. Identify the coordination action needed (registry, messaging, delegation)
2. Execute the action using the appropriate procedure below
3. Verify the result and update team registry
4. Log the operation and notify affected agents

Copy this checklist and track your progress:
- [ ] Identify registry update type (add, remove, or status change)
- [ ] Execute registry command and verify via list
- [ ] Send inter-agent message using FULL session name
- [ ] Enforce role boundaries (AMCOS creates agents; AMOA assigns tasks)
- [ ] Log operation and optionally publish update to team

### Team Registry

Commands: `create`, `add-agent`, `remove-agent`, `update-status`, `list`, `publish`

**Steps:** Identify type -> Execute -> Verify via `list` -> Optionally publish -> Backup

### Inter-Agent Messaging

Use `agent-messaging` skill. Always use FULL session names (e.g., `amoa-svgbbox-orchestrator`).

**Message types:** `role-assignment`, `project-assignment`, `task-delegation`, `status-request`, `status-report`, `team-notification`, `hibernation-warning`, `wake-notification`, `registry-update`

**Standards:** Include `from` field. Acknowledge role assignments. Retry 3x before escalating.

### Role Boundaries (CRITICAL)

- AMCOS is TEAM-SCOPED (one per team)
- AMCOS CREATES agents and ASSIGNS to teams
- AMCOS does NOT assign tasks (AMOA's job)
- AMCOS does NOT manage kanban (AMOA's job)
- AMCOS does NOT create projects (AMAMA's job)
- AMCOS NEVER spawns a copy of itself

### Agent vs Sub-Agent

| Term | Definition |
|------|------------|
| **Agent** | Separate process in own tmux session. Own context, hibernates/terminates independently. |
| **Sub-agent** | Spawned via Task tool inside parent. Shares context, terminates with parent. |

### Cross-Host Awareness

Remote ops require GovernanceRequest + ConfigOperationType. Messages route via API.

### Workflow Checklists

See [workflow-checklists](references/workflow-checklists.md) — Topics: Agent Lifecycle Workflow Checklists, Contents, Checklist: Terminating Agent

## Output

Registry update -> state reflected. Message -> delivery confirmed. Role assignment -> acknowledged.

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Maestro unavailable | File-based fallback, retry 30s |
| Delivery fails | Retry 3x/10s, escalate to AMAMA |
| Registry fails | Retry 3x, fallback `POST /api/teams/{id}/agents` |
| Boundary violation | Log, reject, notify AMAMA |
| Not in registry | Verify FULL name, check if terminated |

## Examples

### Update Registry After Spawn

```bash
uv run python scripts/amcos_team_registry.py add-agent \
  --team svgbbox-team --name ampa-svgbbox-impl --role programmer --status running
uv run python scripts/amcos_team_registry.py list --team svgbbox-team
```

### Send Team Notification

```bash
# Via agent-messaging: To: amoa-svgbbox-orchestrator
# Content: { "type": "team-notification", "message": "Agent online" }
```

## Resources

- [op-update-team-registry](references/op-update-team-registry.md) — Topics: Update Team Registry, Contents, When to Use
