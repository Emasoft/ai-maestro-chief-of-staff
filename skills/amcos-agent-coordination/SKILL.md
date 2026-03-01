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
agent: amcos-main
---

# Agent Coordination

## Overview

Manages team registry, inter-agent messaging, role boundary enforcement, and agent vs sub-agent delegation. Use for registry updates, message routing, role assignment, and workflow orchestration.

## Prerequisites

- AI Maestro running, `agent-messaging` skill available
- Team registry accessible via REST API (`GET /api/teams/{id}/agents`)
- Registry script: `uv run python scripts/amcos_team_registry.py`

## Instructions

### Team Registry

Commands: `create`, `add-agent`, `remove-agent`, `update-status`, `list`, `publish`

**Update steps:**
1. Identify update type (add, remove, status change)
2. Execute command
3. Verify via `list`
4. Optionally publish update to team
5. Backup registry

### Inter-Agent Messaging

Use `agent-messaging` skill. Always use FULL session names (e.g., `eoa-svgbbox-orchestrator`).

**Message types:** `role-assignment`, `project-assignment`, `task-delegation`, `status-request`, `status-report`, `team-notification`, `hibernation-warning`, `wake-notification`, `registry-update`

**Standards:** All messages include `from` field. Role assignments must be acknowledged. Failed delivery retried 3x before escalating.

### Role Boundaries (CRITICAL)

- AMCOS is TEAM-SCOPED (one per team)
- AMCOS CREATES agents and ASSIGNS to teams
- AMCOS does NOT assign tasks (EOA's job)
- AMCOS does NOT manage kanban (EOA's job)
- AMCOS does NOT create projects (EAMA's job)
- AMCOS NEVER spawns a copy of itself

### Agent vs Sub-Agent

| Term | Definition |
|------|------------|
| **Agent** | Separate Claude Code process in own tmux session. Own context, can hibernate/terminate. Created via `ai-maestro-agents-management`. |
| **Sub-agent** | Spawned inside same instance via Task tool. Shares parent context, terminates with parent. |

### Cross-Host Awareness

Configure operations on remote hosts require GovernanceRequest + ConfigOperationType. Messages route automatically via AI Maestro API.

### Workflow Checklists

See [workflow-checklists.md](references/workflow-checklists.md) for structured checklists covering spawn, terminate, hibernate, wake, team formation, and registry updates.

## Output

| Operation | Expected Output |
|-----------|----------------|
| Registry update | Registry reflects new state |
| Message sent | Delivery confirmed |
| Role assignment | Target acknowledges via reply |

## Error Handling

| Issue | Resolution |
|-------|-----------|
| AI Maestro unavailable | Fallback file-based communication, retry after 30s |
| Message delivery fails | Retry 3x with 10s delay, escalate to EAMA |
| Registry update fails | Retry 3x, fallback to `POST /api/teams/{id}/agents` |
| Role boundary violation | Log, reject operation, notify EAMA |
| Agent not in registry | Verify FULL session name, check if terminated |

## Examples

### Update Registry After Spawn

```bash
uv run python scripts/amcos_team_registry.py add-agent \
  --team svgbbox-team --name epa-svgbbox-impl --role programmer --status running
# Verify
uv run python scripts/amcos_team_registry.py list --team svgbbox-team
# Notify team via agent-messaging: type=registry-update
```

### Send Team Notification

```bash
# Via agent-messaging skill:
#   To: eoa-svgbbox-orchestrator, Priority: normal
#   Content: { "type": "team-notification",
#     "message": "Agent epa-svgbbox-impl online and ready" }
```

## Resources

- [op-update-team-registry.md](references/op-update-team-registry.md)
  <!-- TOC: op-update-team-registry.md -->
  - Procedure (Steps 1-5)
  - Examples
  - Error Handling
  <!-- /TOC -->
- [op-send-maestro-message.md](references/op-send-maestro-message.md)
  <!-- TOC: op-send-maestro-message.md -->
  - Procedure (Steps 1-6)
  - Examples
  - Error Handling
  <!-- /TOC -->
- [Sub-Agent Role Boundaries](references/sub-agent-role-boundaries-template.md)
  <!-- TOC: sub-agent-role-boundaries-template.md -->
  - Agent File Structure
  - Core Responsibilities
  - Iron Rules
  <!-- /TOC -->
- [Workflow Checklists](references/workflow-checklists.md)
  <!-- TOC: workflow-checklists.md -->
  - Spawning New Agent Checklist
  - Terminating Agent Checklist
  - Forming Team Checklist
  <!-- /TOC -->
