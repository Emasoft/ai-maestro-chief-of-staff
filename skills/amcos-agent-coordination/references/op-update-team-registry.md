---
operation: update-team-registry
parent-skill: amcos-agent-coordination
parent-plugin: ai-maestro-chief-of-staff
version: 1.0.0
---

# Update Team Registry


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Identify Update Type](#step-1-identify-update-type)
  - [Step 2: Execute Registry Update](#step-2-execute-registry-update)
  - [Step 3: Verify Update](#step-3-verify-update)
  - [Step 4: Publish Update to Team (Optional)](#step-4-publish-update-to-team-optional)
  - [Step 5: Backup Registry (Recommended)](#step-5-backup-registry-recommended)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Complete Agent Addition Flow](#example-complete-agent-addition-flow)
  - [Example: Status Change After Hibernation](#example-status-change-after-hibernation)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- After spawning a new agent
- After terminating an agent
- After hibernating or waking an agent
- When agent role or project assignment changes
- When publishing registry updates to teammates
- During team audit or reconciliation

## Prerequisites

- AI Maestro is running (registry managed via REST API)
- `amcos_team_registry.py` script is available (wraps REST API)
- Team exists in AI Maestro (verify with `aimaestro-teams.sh list`)

## Procedure

### Step 1: Identify Update Type

Determine which registry operation is needed:

| Event | Command |
|-------|---------|
| New agent | `add-agent` |
| Agent removed | `remove-agent` |
| Status change | `update-status` |

`amcos_team_registry.py` has no `update-role` and no `log` subcommand — a role
change or event log is not tracked by this script; use the `amp-send` CLI to
notify the team instead.

### Step 2: Execute Registry Update

**Add new agent:**
```bash
uv run python scripts/amcos_team_registry.py add-agent \
  --team "<team>" \
  --agent-name "<agent-session-name>" \
  --role "<role>" \
  --plugin "<plugin>" \
  --host "$(hostname)"
```

**Remove agent:**
```bash
uv run python scripts/amcos_team_registry.py remove-agent \
  --team "<team>" \
  --agent-name "<agent-session-name>"
```

**Update status:**
```bash
uv run python scripts/amcos_team_registry.py update-status \
  --team "<team>" \
  --agent-name "<agent-session-name>" \
  --status "<running|hibernated|terminated>"
```

### Step 3: Verify Update

```bash
# View the team's registry (list only supports --team, no per-agent filter)
uv run python scripts/amcos_team_registry.py list --team "<team>"
```

### Step 4: Publish Update to Team (Optional)

`amcos_team_registry.py` has no `publish` subcommand — if teammates need to
know about the change, notify them via the `amp-send` CLI instead.

### Step 5: Verify Registry State (Recommended)

After significant changes, confirm via REST API:

```bash
# Uses AI Maestro REST API (not file-based)
# Verify current team registry state
aimaestro-teams.sh list | jq '.[] | {name: .name, members: (.members | length)}'
```

## Checklist

Copy this checklist and track your progress:

- [ ] Identify the registry operation needed
- [ ] Prepare all required parameters
- [ ] Execute the registry command
- [ ] Verify update was applied correctly
- [ ] Publish update to team if needed
- [ ] Create backup after significant changes
- [ ] Log the registry operation

## Examples

### Example: Complete Agent Addition Flow

```bash
SESSION_NAME="dev-api-charlie"
TEAM_NAME="backend-api-team"

# Add to registry
uv run python scripts/amcos_team_registry.py add-agent \
  --team "$TEAM_NAME" \
  --agent-name "$SESSION_NAME" \
  --role "developer" \
  --plugin "ai-maestro-programmer-agent" \
  --host "$(hostname)"

# Verify
uv run python scripts/amcos_team_registry.py list --team "$TEAM_NAME"
# Read dev-api-charlie's entry from the output

# Log the addition / notify team — no log or publish subcommand exists;
# use the amp-send CLI instead: "New team member: $SESSION_NAME (developer on backend-api)"
```

### Example: Status Change After Hibernation

```bash
SESSION_NAME="dev-frontend-bob"
TEAM_NAME="webapp-team"

# Update status
uv run python scripts/amcos_team_registry.py update-status \
  --team "$TEAM_NAME" \
  --agent-name "$SESSION_NAME" \
  --status "hibernated"

# Log hibernation — no log subcommand exists; use the amp-send CLI instead:
# "Idle timeout exceeded (30 min)"

# Verify
uv run python scripts/amcos_team_registry.py list --team "$TEAM_NAME"
# Read dev-frontend-bob's entry from the output
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Registry file not found | First run or file deleted | Run `create` command to initialize registry |
| Agent already exists | Duplicate add-agent call | Use update-status instead or remove first |
| Agent not found | Wrong name or already removed | Check agent name with `list` command |
| Permission denied | File permissions issue | Check write permissions on .ai-maestro directory |
| JSON parse error | Corrupt registry file | Restore from backup or recreate |
| Broadcast failed | AI Maestro not running | Start AI Maestro or skip broadcast |

## Related Operations

- [op-spawn-agent.md](op-spawn-agent.md) - Spawn agent (calls add-agent)
- [op-terminate-agent.md](op-terminate-agent.md) - Terminate agent (calls remove-agent)
- [op-hibernate-agent.md](op-hibernate-agent.md) - Hibernate agent (calls update-status)
- [op-wake-agent.md](op-wake-agent.md) - Wake agent (calls update-status)
