---
name: amcos-agent-spawning
description: Use when creating new agents. Trigger with agent spawn requests, pre-flight validation, or new agent creation.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-main
---

# Agent Spawning

## Overview

Creates new agent instances with pre-flight OAuth validation, plugin setup, and registry registration. Use when spawning agents for task execution, scaling, or specialization.

## Prerequisites

- AI Maestro running, `ai-maestro-agents-management` and `agent-messaging` skills available
- tmux installed, team registry accessible via REST API (`GET /api/teams`)

## Instructions

### Pre-Flight: Validate OAuth Scopes

```bash
gh auth status 2>&1 | grep -q "project" || echo "ERROR: Missing project scope"
```

Required: `repo`, `project`, `read:project`. If missing, request human to run `gh auth refresh -h github.com -s project,read:project`. Do NOT proceed if scopes are missing.

### Spawn Procedure (PROCEDURE 1)

1. **Select agent type** from roles (Orchestrator, Architect, Integrator, Programmer)
2. **Choose session name** - Format: `<role-prefix>-<project>-<descriptive>` (must be unique)
3. **Setup plugin** - Copy from `$HOME/.claude/plugins/cache/ai-maestro/<plugin>/<latest>/` to `$HOME/agents/<session>/.claude/plugins/<plugin>/`
4. **Create instance** via `ai-maestro-agents-management` skill with args: `--dangerously-skip-permissions --chrome --add-dir /tmp --plugin-dir <path> --agent <agent-name>`
5. **Verify** agent appears online in agent list
6. **Register** via `uv run python scripts/amcos_team_registry.py add-agent`
7. **Send welcome message** via `agent-messaging` skill

### The --agent Flag

| Role | --agent Flag Value |
|------|--------------------|
| Orchestrator | `eoa-orchestrator-main-agent` |
| Architect | `eaa-architect-main-agent` |
| Integrator | `eia-integrator-main-agent` |
| Programmer | `epa-programmer-main-agent` |

Remote host spawning requires a GovernanceRequest; state replicated via GovernanceSyncMessage.

## Output

| Step | Expected Output |
|------|----------------|
| Pre-flight | OAuth scopes confirmed |
| Spawn | tmux session created, agent running |
| Registry | Agent registered as "running" |

## Error Handling

| Issue | Resolution |
|-------|-----------|
| OAuth scopes missing | Block spawn, request human `gh auth refresh` |
| Spawn failed | Retry once, report to EAMA. See [spawn-procedures.md](references/spawn-procedures.md) 1.7 |
| Plugin validation failed | Verify cache exists at source path |
| Session name collision | Choose different unique name |
| Resource limit exceeded | Queue request, hibernate oldest idle |

## Examples

### Spawn a Programmer Agent

```bash
# 1. Verify scopes
gh auth status 2>&1 | grep -q "project" && echo "OK"

# 2. Copy plugin
cp -r ~/.claude/plugins/cache/ai-maestro/ai-maestro-programmer-agent/latest/* \
      ~/agents/epa-svgbbox-impl/.claude/plugins/ai-maestro-programmer-agent/

# 3. Create via ai-maestro-agents-management skill:
#    Name: epa-svgbbox-impl, Dir: ~/agents/epa-svgbbox-impl/
#    Args: --agent epa-programmer-main-agent

# 4. Register + send welcome message
```

## Resources

- [Spawn Procedures](references/spawn-procedures.md)
  <!-- TOC: spawn-procedures.md -->
  - What is agent spawning - Understanding agent creation
  - Spawn procedure - Step-by-step agent creation
  - ...and 5 more sections
  <!-- /TOC -->
- [op-spawn-agent.md](references/op-spawn-agent.md)
  <!-- TOC: op-spawn-agent.md -->
  - Procedure (Steps 1-6)
  - Examples
  - Error Handling
  <!-- /TOC -->
- [Workflow Examples](references/workflow-examples.md)
  <!-- TOC: workflow-examples.md -->
  - Setting Up a Development Team
  - Hibernating Idle Agents
  - Skill Reindex After Plugin Update
  <!-- /TOC -->
- [CLI Examples](references/cli-examples.md)
  <!-- TOC: cli-examples.md -->
  - Creating a Code Implementer Agent
  - End of Day Hibernate All
  - Resume Work Next Day
  <!-- /TOC -->
- [CLI Reference](references/cli-reference.md)
  <!-- TOC: cli-reference.md -->
  - Quick Operations Reference
  - Creating new agents
  - Listing and filtering
  <!-- /TOC -->
