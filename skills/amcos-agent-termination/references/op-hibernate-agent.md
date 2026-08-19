---
operation: hibernate-agent
parent-skill: amcos-agent-termination
---

# Hibernate Agent


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Confirm Agent Is Idle](#step-1-confirm-agent-is-idle)
  - [Step 2: Send Hibernation Warning](#step-2-send-hibernation-warning)
  - [Step 3: Request State Capture](#step-3-request-state-capture)
  - [Step 4: Execute Hibernation](#step-4-execute-hibernation)
  - [Step 5: Update Team Registry](#step-5-update-team-registry)
  - [Step 6: Log Hibernation Event](#step-6-log-hibernation-event)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Hibernating Idle Developer at End of Day](#example-hibernating-idle-developer-at-end-of-day)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- Agent is idle but may be needed later
- Conserving system resources during low-activity periods
- Scheduled pause (end of work day, weekends)
- Resource pressure requires reducing active agents
- Agent idle timeout threshold exceeded (default: 30 min)

## Prerequisites

- Agent exists and is in "running" state
- AI Maestro is running locally
- The `ai-maestro-agents-management` skill is available
- The `amp-send`/`amp-inbox` CLIs are available
- State storage directory is writable (`~/.ai-maestro/agent-states/`)
- Team registry is accessible

## Procedure

### Step 1: Confirm Agent Is Idle

Verify the agent has no active work before hibernating.

Send an idle check via the `amp-send` CLI:
`amp-send <agent-session-name> "Idle Status Check" "<asking whether it is currently working on any active tasks — reply with IDLE if no active work>" --type status-request --priority normal`

**Verify**: confirm delivery via the `amp-inbox` CLI.

Wait for IDLE confirmation.

### Step 2: Send Hibernation Warning

Send a hibernation notice via the `amp-send` CLI:
`amp-send <agent-session-name> "Hibernation Notice" "<informing the agent it will be hibernated in 30 seconds and should save any transient state>" --type hibernation-warning --priority high`

**Verify**: confirm delivery via the `amp-inbox` CLI.

### Step 3: Request State Capture

Request state capture via the `amp-send` CLI:
`amp-send <agent-session-name> "State Capture Request" "<asking the agent to save its current state to ~/.ai-maestro/agent-states/<session-name>-hibernation.json>" --type request --priority high`

**Verify**: confirm delivery via the `amp-inbox` CLI.

### Step 4: Execute Hibernation

Use the `ai-maestro-agents-management` skill to hibernate the agent.

This suspends the tmux session while preserving state.

### Step 5: Update Team Registry

```bash
uv run python scripts/amcos_team_registry.py update-status \
  --team "<team>" \
  --agent-name "<agent-session-name>" \
  --status "hibernated"
```

### Step 6: Log Hibernation Event

`amcos_team_registry.py` has no `log` subcommand — note the hibernation event in
the team's coordination channel via the `amp-send` CLI instead.

## Checklist

Copy this checklist and track your progress:

- [ ] Verify agent is idle (no active tasks)
- [ ] Send hibernation warning (30 second notice) via the `amp-send` CLI
- [ ] Request state capture from agent via the `amp-send` CLI
- [ ] Wait for state capture confirmation
- [ ] Execute hibernation via `ai-maestro-agents-management` skill
- [ ] Verify agent status changed to "hibernated"
- [ ] Update team registry status
- [ ] Log hibernation event with timestamp
- [ ] Note expected wake time if scheduled

## Examples

### Example: Hibernating Idle Developer at End of Day

For agent `dev-frontend-bob`:

1. Check idle status via the `amp-send` CLI:
   `amp-send dev-frontend-bob "Idle Status Check" "Are you currently working on any active tasks?" --type status-request --priority normal`
2. Wait for IDLE response
3. Send hibernation warning via the `amp-send` CLI:
   `amp-send dev-frontend-bob "Hibernation Notice" "End of day hibernation in 30 seconds." --type hibernation-warning --priority high`
4. Wait 30 seconds
5. Use the `ai-maestro-agents-management` skill to hibernate agent `dev-frontend-bob`
6. Update registry:
   ```bash
   uv run python scripts/amcos_team_registry.py update-status \
     --team "<team>" \
     --agent-name "dev-frontend-bob" \
     --status "hibernated"
   ```
7. Log the event (no `log` subcommand exists — send a team notification via
   the `amp-send` CLI instead): "End of day - scheduled hibernation."

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent reports active work | Premature hibernation attempt | Wait for task completion or reassign task first |
| State capture failed | Storage full or permissions | Free space or fix permissions on ~/.ai-maestro/agent-states/ |
| Hibernation command fails | tmux session issue | Check tmux status, try manual session suspend |
| Agent not responding | Agent crashed or hung | Force hibernation, check logs for errors |
| Registry update fails | AI Maestro API error | Retry, or use `aimaestro-teams.sh list` to verify state |

## Related Operations

- [op-wake-agent.md](op-wake-agent.md) - Wake hibernated agent
- [op-terminate-agent.md](op-terminate-agent.md) - Terminate instead of hibernate
- [op-update-team-registry.md](op-update-team-registry.md) - Update registry
