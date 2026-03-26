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
agent: ai-maestro-chief-of-staff-main-agent
---

# Agent Spawning

## Overview

Creates new agent instances with pre-flight OAuth validation, plugin setup, and registry registration. Use when spawning agents for task execution, scaling, or specialization.

## Prerequisites

- AI Maestro running, `ai-maestro-agents-management` and `agent-messaging` skills available
- tmux installed, team registry accessible via REST API (`GET /api/teams`)

## Instructions

Copy this checklist and track your progress:
- [ ] Request GovernanceRequest approval from sourceManager via amcos-permission-management
- [ ] Validate OAuth scopes (repo, project, read:project)
- [ ] Select agent type and unique session name
- [ ] Setup plugin from cache to agent directory
- [ ] Create agent instance via ai-maestro-agents-management skill
- [ ] Verify agent online and register in team registry
- [ ] Send welcome message via agent-messaging skill

### Pre-Flight: Validate OAuth Scopes

```bash
gh auth status 2>&1 | grep -q "project" || echo "ERROR: Missing project scope"
```

Required: `repo`, `project`, `read:project`. If missing, request human to run `gh auth refresh -h github.com -s project,read:project`. Do NOT proceed if scopes are missing.

### Spawn Procedure (PROCEDURE 1)

1. **Request GovernanceRequest approval** - Submit spawn request to sourceManager via `amcos-permission-management` skill. BLOCK until approved.
2. **Select agent type** from roles (Orchestrator, Architect, Integrator, Programmer)
3. **Choose session name** - Format: `<role-prefix>-<project>-<descriptive>` (must be unique)
4. **Setup plugin** - Copy from `$HOME/.claude/plugins/cache/ai-maestro/<plugin>/<latest>/` to `$HOME/agents/<session>/.claude/plugins/<plugin>/`
5. **Create instance** via `ai-maestro-agents-management` skill with args: `--dangerously-skip-permissions --chrome --add-dir /tmp --plugin-dir <path> --agent <agent-name>`
6. **Verify** agent appears online in agent list
7. **Register** via `uv run python scripts/amcos_team_registry.py add-agent`
8. **Send welcome message** via `agent-messaging` skill

### The --agent Flag

| Role | --agent Flag Value |
|------|--------------------|
| Orchestrator | `ai-maestro-orchestrator-main-agent` |
| Architect | `ai-maestro-architect-main-agent` |
| Integrator | `ai-maestro-integrator-main-agent` |
| Programmer | `ai-maestro-programmer-main-agent` |

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
      ~/agents/ampa-svgbbox-impl/.claude/plugins/ai-maestro-programmer-agent/

# 3. Create via ai-maestro-agents-management skill:
#    Name: ampa-svgbbox-impl, Dir: ~/agents/ampa-svgbbox-impl/
#    Args: --agent ai-maestro-programmer-main-agent

# 4. Register + send welcome message
```

## Resources

