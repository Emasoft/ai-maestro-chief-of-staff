---
operation: hibernate-agent
parent-skill: amcos-agent-hibernation
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
- The `amp-send`/`amp-inbox`/`amp-read`/`amp-reply` CLIs are available
- State storage directory is writable (`~/.ai-maestro/agent-states/`)
- Team registry is accessible

## Procedure

### Step 1: Confirm Agent Is Idle

Verify the agent has no active work before hibernating.

Send via the `amp-send` CLI: `amp-send <target-session> "Idle Status Check" "<message>" --type request --priority normal`
- **Recipient**: the target agent session name
- **Subject**: `Idle Status Check`
- **Priority**: `normal`
- **Content**: type `status-request`, asking the agent if it is currently working on any active tasks (reply with IDLE if no active work)

**Verify**: confirm message delivery via `amp-send`'s output (message id).

Wait for IDLE confirmation.

### Step 2: Send Hibernation Warning

Send via the `amp-send` CLI: `amp-send <target-session> "Hibernation Notice" "<message>" --type notification --priority high`
- **Recipient**: the target agent session name
- **Subject**: `Hibernation Notice`
- **Priority**: `high`
- **Content**: type `hibernation-warning`, informing the agent it will be hibernated in 30 seconds and should save any transient state

**Verify**: confirm message delivery via `amp-send`'s output (message id).

### Step 3: Request State Capture

Send via the `amp-send` CLI: `amp-send <target-session> "State Capture Request" "<message>" --type request --priority high`
- **Recipient**: the target agent session name
- **Subject**: `State Capture Request`
- **Priority**: `high`
- **Content**: type `request`, asking the agent to save its current state to `~/.ai-maestro/agent-states/<session-name>-hibernation.json`

**Verify**: confirm message delivery via `amp-send`'s output (message id).

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

`amcos_team_registry.py` has no `log` subcommand — note the hibernation event by
sending a team notification via `amp-send` instead.

## Checklist

Copy this checklist and track your progress:

- [ ] Verify agent is idle (no active tasks)
- [ ] Send hibernation warning (30 second notice) via `amp-send`
- [ ] Request state capture from agent via `amp-send`
- [ ] Wait for state capture confirmation
- [ ] Execute hibernation via `ai-maestro-agents-management` skill
- [ ] Verify agent status changed to "hibernated"
- [ ] Update team registry status
- [ ] Log hibernation event with timestamp
- [ ] Note expected wake time if scheduled

## Examples

### Example: Hibernating Idle Developer at End of Day

For agent `dev-frontend-bob`:

1. Send via the `amp-send` CLI: `amp-send dev-frontend-bob "Idle Status Check" "Are you currently working on any active tasks?" --type request --priority normal`
   - **Recipient**: `dev-frontend-bob`
   - **Subject**: `Idle Status Check`
   - **Priority**: `normal`
   - **Content**: type `status-request`, message: "Are you currently working on any active tasks?"
2. Wait for IDLE response
3. Send via the `amp-send` CLI: `amp-send dev-frontend-bob "Hibernation Notice" "End of day hibernation in 30 seconds." --type notification --priority high`
   - **Recipient**: `dev-frontend-bob`
   - **Subject**: `Hibernation Notice`
   - **Priority**: `high`
   - **Content**: type `hibernation-warning`, message: "End of day hibernation in 30 seconds."
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
   `amp-send` instead): "End of day - scheduled hibernation."

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
