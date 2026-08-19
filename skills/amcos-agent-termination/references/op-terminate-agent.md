---
operation: terminate-agent
parent-skill: amcos-agent-termination
parent-plugin: ai-maestro-chief-of-staff
version: 1.0.0
---

# Terminate Agent


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Verify Work Is Complete](#step-1-verify-work-is-complete)
  - [Step 2: Save Final State (Optional but Recommended)](#step-2-save-final-state-optional-but-recommended)
  - [Step 3: Send Termination Warning](#step-3-send-termination-warning)
  - [Step 4: Execute Termination](#step-4-execute-termination)
  - [Step 5: Update Team Registry](#step-5-update-team-registry)
  - [Step 6: Cleanup Resources](#step-6-cleanup-resources)
  - [Step 7: Log Termination](#step-7-log-termination)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Terminating a Completed Developer Agent](#example-terminating-a-completed-developer-agent)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- Agent task is complete and no further work expected
- Agent is no longer needed for the project
- Cleanup operations during project closure
- User explicitly requests agent termination
- Unrecoverable error condition requires agent replacement

## Prerequisites

- Agent exists and is registered in team registry
- AI Maestro is running locally
- The `ai-maestro-agents-management` skill is available
- The `amp-send`/`amp-inbox` CLIs are available
- Team registry is accessible

## Procedure

### Step 1: Verify Work Is Complete

Before terminating, confirm the agent has no pending work.

Send a status request via the `amp-send` CLI:
`amp-send <agent-session-name> "Pre-Termination Status Check" "<asking the agent to confirm all tasks are complete before termination>" --type status-request --priority high`

**Verify**: confirm delivery via the `amp-inbox` CLI.

Wait for confirmation response.

### Step 2: Save Final State (Optional but Recommended)

If state preservation is needed for audit or handoff:

Request a state dump via the `amp-send` CLI:
`amp-send <agent-session-name> "State Dump Request" "<asking the agent to save its current state to ~/.ai-maestro/agent-states/<session-name>-final.json before termination>" --type request --priority high`

**Verify**: confirm delivery via the `amp-inbox` CLI.

### Step 3: Send Termination Warning

Send a termination notice via the `amp-send` CLI:
`amp-send <agent-session-name> "Termination Notice" "<informing the agent it will be terminated in 60 seconds and should complete any final cleanup>" --type hibernation-warning --priority urgent`

**Verify**: confirm delivery via the `amp-inbox` CLI.

### Step 4: Execute Termination

Use the `ai-maestro-agents-management` skill to terminate the agent with confirmation.

If graceful termination fails, use the force option if available.

### Step 5: Update Team Registry

```bash
uv run python scripts/amcos_team_registry.py remove-agent \
  --team "<team>" \
  --agent-name "<agent-session-name>"
```

### Step 6: Cleanup Resources

Optionally remove the agent's working directory and local plugin cache. Keep the directory if audit trail is needed.

### Step 7: Log Termination

`amcos_team_registry.py` has no `log` subcommand — note the termination event in
the team's coordination channel via the `amp-send` CLI instead.

## Checklist

Copy this checklist and track your progress:

- [ ] Verify agent has no pending work
- [ ] Request status confirmation from agent
- [ ] Save final state if needed
- [ ] Send termination warning (60 second notice)
- [ ] Wait for agent acknowledgment or timeout
- [ ] Execute termination via `ai-maestro-agents-management` skill with confirmation
- [ ] Verify agent status is "terminated" or session gone
- [ ] Update team registry to remove agent
- [ ] Log termination event
- [ ] Notify relevant teammates if needed

## Examples

### Example: Terminating a Completed Developer Agent

For agent `dev-backend-alice`:

1. Send a pre-termination status check via the `amp-send` CLI:
   `amp-send dev-backend-alice "Pre-Termination Status Check" "Please confirm all tasks are complete." --type status-request --priority high`
2. Wait for response confirming work is done
3. Send a termination warning via the `amp-send` CLI:
   `amp-send dev-backend-alice "Termination Notice" "Termination in 60 seconds." --type hibernation-warning --priority urgent`
4. Wait 60 seconds
5. Use the `ai-maestro-agents-management` skill to terminate agent `dev-backend-alice` with confirmation
6. Update registry:
   ```bash
   uv run python scripts/amcos_team_registry.py remove-agent --team "<team>" --agent-name "dev-backend-alice"
   ```
7. Log the event (no `log` subcommand exists — send a team notification via
   the `amp-send` CLI instead): "Task completed - backend API implementation finished."

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not responding to status check | Agent hung or crashed | Proceed with forced termination |
| Termination command fails | tmux session stuck | Kill tmux session manually: `tmux kill-session -t <name>` |
| Agent still appears in registry | Registry not updated | Manually remove entry or run remove-agent again |
| Work not complete | Premature termination request | Delay termination, assign work to another agent |
| Cannot find agent session | Wrong session name | Use the `ai-maestro-agents-management` skill to list agents for correct name |

## Related Operations

- [op-spawn-agent.md](op-spawn-agent.md) - Spawn new agent
- [op-hibernate-agent.md](op-hibernate-agent.md) - Hibernate instead of terminate
- [op-update-team-registry.md](op-update-team-registry.md) - Update registry
