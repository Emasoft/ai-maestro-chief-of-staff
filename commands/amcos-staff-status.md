---
name: amcos-staff-status
description: "View all remote agents with status, working directory, and tags using AI Maestro CLI"
argument-hint: "[--status online|offline|hibernated|all] [--format table|json|names]"
allowed-tools: ["Bash", "Task"]
user-invocable: true
---

# Staff Status Command

View all remote agents managed by AI Maestro.

## Usage

Use the `ai-maestro-agents-management` skill to list all agents with the provided arguments.

## What This Command Does

This command lists all registered agents. The operation queries:
1. Agent registry for registered agents
2. tmux session status for online/offline detection
3. Agent metadata (tags, working directory, task)

## What This Command Shows

1. **Agent Name**: Registered agent name
2. **Status**: online, offline, hibernated
3. **Working Directory**: Project folder for the agent
4. **Tags**: Role/project tags assigned to the agent

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--status <status>` | No | Filter by status: `online`, `offline`, `hibernated`, `all` |
| `--format <format>` | No | Output format: `table` (default), `json`, `names` |
| `-q` / `--quiet` | No | Same as `--format names` |
| `--json` | No | Same as `--format json` |

## Examples

```bash
# List all agents (default: excludes hibernated)
/amcos-staff-status

# List only online agents
/amcos-staff-status --status online

# List all agents including hibernated
/amcos-staff-status --status all

# Get agent names only (for scripting)
/amcos-staff-status -q
# or
/amcos-staff-status --format names

# JSON output for processing
/amcos-staff-status --json
```

## Output Format (Table)

```
┌────────────────────┬──────────┬─────────────────────────────────┬──────────────────┐
│ Agent              │ Status   │ Working Directory               │ Tags             │
├────────────────────┼──────────┼─────────────────────────────────┼──────────────────┤
│ backend-api        │ online   │ /Users/dev/projects/backend     │ api, implementer │
│ frontend-dev       │ online   │ /Users/dev/projects/frontend    │ ui, react        │
│ test-runner        │ offline  │ /Users/dev/projects/tests       │ tester           │
│ data-processor     │ hibernated│ /Users/dev/projects/data       │ worker           │
└────────────────────┴──────────┴─────────────────────────────────┴──────────────────┘
```

## Status Values

| Status | Description |
|--------|-------------|
| `online` | Agent is running in a tmux session |
| `offline` | Agent exists but session is not running |
| `hibernated` | Agent explicitly hibernated, awaiting wake |

## View Agent Details

For detailed information about a specific agent, use the `ai-maestro-agents-management` skill to show agent details:
- **Name**: the agent to inspect
- **Format**: `table` (default) or `json` for scripting

## Agent Details Output

```
═══════════════════════════════════════════════════════════════
  Agent: helper-python
═══════════════════════════════════════════════════════════════

  ID:           a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Name:         helper-python
  Status:       online
  Program:      claude-code
  Model:        claude-sonnet-4-20250514

  Working Dir:  /Users/dev/projects/backend

  Task:         Implement user authentication module

  Tags:         implementer, python, auth

  Sessions:
    [0] helper-python (online) - tmux session

═══════════════════════════════════════════════════════════════
```

## Related Commands

- `/amcos-spawn-agent` - Create a new remote agent
- `/amcos-terminate-agent` - Terminate a remote agent
- `/amcos-hibernate-agent` - Put an agent to sleep
- `/amcos-wake-agent` - Wake a hibernated agent

## CLI Reference

Full documentation: `ai-maestro-agents-management` skill
