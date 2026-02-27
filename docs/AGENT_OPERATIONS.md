# AGENT_OPERATIONS.md - AMCOS Chief of Staff

**SINGLE SOURCE OF TRUTH** for AMCOS (AI Maestro Chief of Staff) agent operations.
**SCOPE**: TEAM-SCOPED. Each AMCOS instance manages exactly ONE team.
**Distribution**: Bundled with AI Maestro v0.26.0+.

---

## 1. Session Naming Convention

**Format**: `<role-prefix>-<descriptive>[-number]`

**AMCOS prefix**: `amcos-`

**Examples**:
- `amcos-chief-of-staff-one`
- `amcos-project-alpha`
- `amcos-orch-svgbbox`

**Critical Rules**:
- Session name = AI Maestro registry identity (how agents message each other)
- Must be unique across all running agents
- Session name is used when creating an agent via the `ai-maestro-agents-management` skill
- Session name determines the tmux session name
- Session name must be valid for both tmux and AI Maestro (alphanumeric, hyphens, underscores only)

**Role Prefixes**:
| Role | Prefix | Example Session Name |
|------|--------|---------------------|
| Chief of Staff | `amcos-` | `amcos-chief-of-staff-one` |
| Orchestrator | `amcos-orch-` | `amcos-orch-svgbbox` |
| Architect | `amcos-arch-` | `amcos-arch-project-alpha` |
| Integrator | `amcos-intg-` | `amcos-intg-feature-reviewer` |
| Manager | `amcos-mgr-` | `amcos-mgr-user-interface` |
| Programmer | `amcos-prog-` | `amcos-prog-svgbbox-001` |

---

## 2. AI Maestro Governance

### 2.1 Team Scope

AMCOS is a **per-team** Chief of Staff. Each AMCOS instance:
- Manages exactly ONE team
- Has authority only over agents assigned to its team
- Cannot spawn, hibernate, or terminate agents belonging to other teams
- Cannot reassign agents to other teams without a GovernanceRequest

### 2.2 Communication Restrictions

AMCOS can only send messages to:

| Target | Allowed | Example |
|--------|---------|---------|
| MANAGER (parent) | Yes | `amcos-mgr-user-interface` |
| Other COS agents | Yes | `amcos-chief-of-staff-two` |
| Own team members | Yes | `amcos-orch-svgbbox`, `amcos-prog-svgbbox-001` |
| Unassigned agents | Yes | Agents not yet assigned to any team |
| Other teams' agents | **No** | Must use GovernanceRequest |

### 2.3 GovernanceRequest

Cross-team operations require a GovernanceRequest sent to the MANAGER:

| Operation | Requires GovernanceRequest |
|-----------|---------------------------|
| Message agent in another team | Yes |
| Borrow agent from another team | Yes |
| Share resources across teams | Yes |
| Spawn agent for own team | No |
| Message own team members | No |

**GovernanceRequest format** (sent via `agent-messaging` skill):
- **Recipient**: MANAGER session name
- **Subject**: `GovernanceRequest: <operation>`
- **Content type**: `request`
- **Priority**: `high`
- **Body**: operation description, justification, target team/agent

---

## 3. Plugin Paths

**Environment Variables**:
- `${CLAUDE_PLUGIN_ROOT}` - Set by Claude Code when plugin loaded via `--plugin-dir`
- `${CLAUDE_PROJECT_DIR}` - Working directory of the Claude Code session
- AI Maestro API endpoint is configured automatically by AI Maestro and accessed via the `agent-messaging` skill

**Path Resolution**:
```bash
# Current plugin (loaded by this agent)
${CLAUDE_PLUGIN_ROOT}
# Example: ~/agents/amcos-chief-of-staff-one/.claude/plugins/ai-maestro-chief-of-staff

# Sibling plugins (in same parent directory)
${CLAUDE_PLUGIN_ROOT}/../<plugin-name>
# Example: ~/agents/amcos-chief-of-staff-one/.claude/plugins/ai-maestro-orchestrator-agent

# Agent local plugins directory
~/agents/<session-name>/.claude/plugins/<plugin-name>/
```

**Plugin Sources**:
| Context | Plugin Source |
|---------|--------------|
| **AI Maestro Distribution** | `~/.claude/plugins/cache/ai-maestro/<plugin-name>/<version>/` |
| **Agent Local** | `~/agents/<session-name>/.claude/plugins/<plugin-name>/` |

**CRITICAL**: AMCOS installs plugins from the AI Maestro distribution cache (`~/.claude/plugins/cache/ai-maestro/`) to the agent's local `.claude/plugins/` folder.

---

## 4. Agent Directory Structure (FLAT)

**Architecture**: FLAT (no nesting, all agents at same level)

```
~/agents/
├── amcos-chief-of-staff-one/
│   └── .claude/
│       └── plugins/
│           └── ai-maestro-chief-of-staff/
│               ├── .claude-plugin/
│               │   └── plugin.json
│               ├── agents/
│               ├── skills/
│               ├── commands/
│               └── hooks/
├── amcos-orch-svgbbox/
│   └── .claude/
│       └── plugins/
│           └── ai-maestro-orchestrator-agent/
│               ├── .claude-plugin/
│               │   └── plugin.json
│               ├── agents/
│               ├── skills/
│               ├── commands/
│               └── hooks/
├── amcos-arch-project-alpha/
│   └── .claude/
│       └── plugins/
│           └── ai-maestro-architect-agent/
│               └── ...
├── amcos-intg-feature-reviewer/
│   └── .claude/
│       └── plugins/
│           └── ai-maestro-integrator-agent/
│               └── ...
├── amcos-prog-svgbbox-001/
│   └── .claude/
│       └── plugins/
│           └── ai-maestro-programmer-agent/
│               └── ...
└── amcos-mgr-user-interface/
    └── .claude/
        └── plugins/
            └── ai-maestro-assistant-manager-agent/
                └── ...
```

**Why FLAT?**:
- Each agent is an independent Claude Code session
- No parent-child relationship in file system
- Communication happens via AI Maestro messaging, not file system
- Easier to manage, monitor, and terminate individual agents

---

## 5. Spawn Procedure

### 5.1 Copy Plugin First

**CRITICAL**: Always copy plugin to agent's local directory before spawning!

The plugin must be copied from the AI Maestro distribution cache to the agent's local `.claude/plugins/` directory:
- **Source**: `$HOME/.claude/plugins/cache/ai-maestro/<plugin-name>/<latest-version>/`
- **Destination**: `$HOME/agents/<session-name>/.claude/plugins/<plugin-name>/`

**Verify**: the copied plugin contains `.claude-plugin/plugin.json`.

### 5.2 Spawn Command

Use the `ai-maestro-agents-management` skill to create a new agent:
- **Name**: `<role-prefix>-<descriptive>` (the session name)
- **Directory**: `$HOME/agents/<session-name>` (the working directory)
- **Task**: task description for the agent
- **Program args**: include standard Claude Code flags plus `--plugin-dir` and `--agent`

**Required parameters**:
| Parameter | Purpose |
|-----------|---------|
| Name | Session name (also AI Maestro registry identity) |
| Directory | Agent's working directory |
| Task | Initial task prompt |
| `--dangerously-skip-permissions` | Auto-approve file operations |
| `--chrome` | Enable Chrome DevTools MCP |
| `--add-dir /tmp` | Add /tmp to accessible directories |
| `--plugin-dir` | Path to the plugin to load |
| `--agent` | Agent definition file to use |

**Verify**: the new agent appears in the agent list with "online" status.

### 5.3 Role to Plugin/Agent Mapping

| Role | Plugin | --agent Flag | Prefix |
|------|--------|--------------|--------|
| Chief of Staff | `ai-maestro-chief-of-staff` | `amcos-chief-of-staff-main-agent` | `amcos-` |
| Orchestrator | `ai-maestro-orchestrator-agent` | `amcos-orchestrator-main-agent` | `amcos-orch-` |
| Architect | `ai-maestro-architect-agent` | `amcos-architect-main-agent` | `amcos-arch-` |
| Integrator | `ai-maestro-integrator-agent` | `amcos-integrator-main-agent` | `amcos-intg-` |
| Manager | `ai-maestro-assistant-manager-agent` | `amcos-assistant-manager-main-agent` | `amcos-mgr-` |
| Programmer | `ai-maestro-programmer-agent` | `amcos-programmer-main-agent` | `amcos-prog-` |

### 5.4 Example: Spawn Orchestrator

1. Copy `ai-maestro-orchestrator-agent` plugin from AI Maestro distribution cache to `$HOME/agents/amcos-orch-svgbbox/.claude/plugins/ai-maestro-orchestrator-agent/`
2. Use the `ai-maestro-agents-management` skill to create a new agent:
   - **Name**: `amcos-orch-svgbbox`
   - **Directory**: `$HOME/agents/amcos-orch-svgbbox`
   - **Task**: "Orchestrate development of svgbbox library features"
   - **Plugin**: `ai-maestro-orchestrator-agent`
   - **Agent**: `amcos-orchestrator-main-agent`

**Verify**: agent `amcos-orch-svgbbox` appears online in the agent list.

### 5.5 Example: Spawn Programmer

1. Copy `ai-maestro-programmer-agent` plugin from AI Maestro distribution cache to `$HOME/agents/amcos-prog-svgbbox-001/.claude/plugins/ai-maestro-programmer-agent/`
2. Use the `ai-maestro-agents-management` skill to create a new agent:
   - **Name**: `amcos-prog-svgbbox-001`
   - **Directory**: `$HOME/agents/amcos-prog-svgbbox-001`
   - **Task**: "Implement authentication module for svgbbox library"
   - **Plugin**: `ai-maestro-programmer-agent`
   - **Agent**: `amcos-programmer-main-agent`

**Verify**: agent `amcos-prog-svgbbox-001` appears online in the agent list.

---

## 6. Wake Procedure (Hibernated Agent)

**When to use**: Agent was hibernated (tmux session exists but detached)

Use the `ai-maestro-agents-management` skill to wake the agent:
- **Name**: the session name of the hibernated agent

**What happens**:
- The `--continue` flag is internally added to Claude Code
- Reattaches to existing tmux session
- Claude Code resumes from last state
- Agent reconnects to the agent registry

**Verify**: agent status shows "online" in the agent list, and tmux session is running.

---

## 7. Hibernate Procedure

**When to use**: Temporarily pause agent, preserve state

Use the `ai-maestro-agents-management` skill to hibernate the agent:
- **Name**: the session name of the agent to hibernate

**What happens**:
- Detaches from tmux session (session continues running)
- Agent remains registered in the agent registry
- Can be woken later

**Difference from Terminate**:
| Action | Tmux Session | Registry | State |
|--------|--------------|----------|-------|
| **Hibernate** | Detached | Registered | Preserved |
| **Terminate** | Killed | Unregistered | Lost |

---

## 8. Terminate Procedure

**When to use**: Permanently stop agent, clean up resources

Use the `ai-maestro-agents-management` skill to terminate (delete) the agent:
- **Name**: the session name of the agent to terminate
- **Confirm**: required to prevent accidental termination
- **Force**: optional, forcefully kill tmux session if graceful stop fails

**What happens**:
- Claude Code session stopped
- Tmux session killed
- Agent unregistered from the agent registry
- Working directory preserved (not deleted)

**CRITICAL**: Always terminate agents when work is complete to avoid:
- Resource leaks (CPU, memory)
- Agent registry clutter
- Orphaned tmux sessions

---

## 9. Plugin Mutual Exclusivity

**CRITICAL RULE**: Each Claude Code instance can only have ONE role plugin loaded at a time!

**Why?**:
- Plugin hooks can conflict (duplicate PreToolUse, PostToolUse, etc.)
- Skill namespaces can collide
- Command namespaces can collide
- Agent definitions can conflict

**Implications**:
- CANNOT load `ai-maestro-chief-of-staff` + `ai-maestro-orchestrator-agent` in same session
- CANNOT reference skills from other plugins (e.g., Integrator skill in Orchestrator session)
- MUST spawn separate agent with correct plugin for cross-role operations
- MUST use AI Maestro messaging for cross-plugin communication

**Self-Contained Plugins**:
Each plugin must include all skills, commands, agents, and hooks needed for that role.

**Cross-Plugin Communication**: AI Maestro messages ONLY!

---

## 10. Inter-Agent Messaging

All messaging operations use the `agent-messaging` skill. Never use explicit API calls or command-line tools directly.

### 10.1 Send Message

Use the `agent-messaging` skill to send a message:
- **Recipient**: the target agent session name
- **Subject**: descriptive subject line
- **Content**: structured message with type and body
- **Priority**: `normal`, `high`, or `urgent`
- **Type**: `request`, `response`, or `notification`

**Priority Levels**:
| Priority | Use Case | Example |
|----------|----------|---------|
| `normal` | Regular updates, progress reports | "Task completed successfully" |
| `high` | Action required, important info | "Need input on architecture decision" |
| `urgent` | Blocking issue, immediate attention | "Critical bug found in production" |

**Content Types**:
| Type | Use Case | Example |
|------|----------|---------|
| `request` | Ask agent to do something | "Please review PR #42" |
| `response` | Reply to a request | "PR #42 approved" |
| `notification` | Inform about event | "Tests completed, 3 failures" |

### 10.2 Check Inbox / Mark Read

Use the `agent-messaging` skill to check for unread messages or mark a message as read.

### 10.3 Message Workflow Example

1. **AMCOS sends task to Orchestrator** via `agent-messaging`:
   - Recipient: `amcos-orch-svgbbox` | Subject: "Implement Feature X" | Priority: `high`

2. **Orchestrator acknowledges** via `agent-messaging`:
   - Recipient: `amcos-chief-of-staff-one` | Subject: "Re: Implement Feature X" | Priority: `normal`

3. **Orchestrator reports completion** via `agent-messaging`:
   - Recipient: `amcos-chief-of-staff-one` | Subject: "Re: Implement Feature X" | Priority: `normal`

---

## 11. Skill References

### 11.1 Correct Format

Reference skills by folder name only:
```
See skill: amcos-agent-lifecycle
```

In commands/agents, use just the skill name:
```yaml
skills:
  - amcos-agent-lifecycle
  - amcos-task-delegation
```

### 11.2 Rules

- NEVER use file paths to reference skills
- NEVER reference other plugins' skills from an AMCOS session
- Claude Code resolves skill names using the plugin's `skills/` directory and folder names

---

## 12. AMCOS-Specific Responsibilities

### 12.1 Creation

**AMCOS is created by the MANAGER only!**

- User interacts with MANAGER first
- MANAGER assesses if task requires orchestration
- MANAGER spawns AMCOS for complex multi-agent coordination within a team

### 12.2 Agent Creation Authority

**AMCOS creates** (within its team only):
| Role | Prefix |
|------|--------|
| Orchestrator | `amcos-orch-` |
| Architect | `amcos-arch-` |
| Integrator | `amcos-intg-` |
| Programmer | `amcos-prog-` |

**AMCOS does NOT create**:
- Manager - Only user creates Manager
- Other AMCOS instances - Only Manager creates AMCOS

**Implementer Category**: "Implementer" is an umbrella term for all agents that produce concrete deliverables. The Programmer is the first implementer role. Future implementer roles (each with its own plugin) may include: Documenter, 2D Artist, 3D Artist, Video Maker, Sound FX Artist, Music Maker, UI Designer, Copywriter, Interactive Storytelling, Marketing, App Store Optimization, SEO, and Financial agents.

### 12.3 Session Naming Responsibility

**AMCOS chooses unique session names** for all agents it creates:
```bash
# Format: amcos-<role-short>-<project>[-number]
amcos-orch-svgbbox
amcos-arch-svgbbox
amcos-intg-svgbbox
amcos-prog-svgbbox-001
amcos-prog-svgbbox-002
```

**Uniqueness Check**: Before spawning, use the `ai-maestro-agents-management` skill to list all agents and verify the chosen session name is not already in use. If the name exists, append a number suffix.

### 12.4 Lifecycle Management

- **Monitor agent health**: Check agent status, heartbeat, message backlog, last activity (every 5 min)
- **Hibernate idle agents**: If idle for 30+ minutes with no pending tasks
- **Terminate completed agents**: After work is done and verified

All operations use the `ai-maestro-agents-management` skill.

### 12.5 Task Delegation Flow

```
User Request
     |
   MANAGER
     | (spawns if complex)
   AMCOS (Chief of Staff) -- TEAM-SCOPED
     |
     +---> Orchestrator (amcos-orch-*) ---> Implementation agents
     +---> Architect (amcos-arch-*) ---> Design agents
     +---> Integrator (amcos-intg-*) ---> Review agents
```

**AMCOS coordination responsibilities**:
1. Assess task complexity and requirements
2. Choose which agents to spawn
3. Assign unique session names with `amcos-` prefix
4. Copy plugins from AI Maestro distribution cache to agent directories
5. Spawn agents with appropriate flags
6. Send initial task prompts via AI Maestro messaging
7. Monitor agent progress and health
8. Coordinate cross-agent communication (within team scope)
9. Hibernate idle agents
10. Terminate completed agents
11. Report final results back to MANAGER

---

## 13. Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| Agent won't spawn | Session name exists? Plugin at path? Claude binary accessible? | Use unique name; verify `.claude-plugin/plugin.json` exists |
| Agent can't find skills | Skill folder exists in plugin? Folder name matches reference? | Use skill folder name only, no paths |
| Cross-plugin skill fails | Referencing another plugin's skill | Spawn separate agent with correct plugin; use messaging |
| Hook conflicts | Multiple `--plugin-dir` flags | Load only ONE role plugin per agent |
| Messages not received | Agent registered? Messaging hook in `hooks.json`? | Verify registration; check hook configuration |
| Cross-team message blocked | Recipient in another team | Submit GovernanceRequest to MANAGER |

---

## 14. Quick Reference

All operations use intent-based skill references:

| Operation | Skill | Intent |
|-----------|-------|--------|
| **Spawn agent** | `ai-maestro-agents-management` | Create a new agent with name, directory, task, and plugin |
| **Wake agent** | `ai-maestro-agents-management` | Wake a hibernated agent by name |
| **Hibernate agent** | `ai-maestro-agents-management` | Hibernate an agent by name |
| **Terminate agent** | `ai-maestro-agents-management` | Delete an agent by name (with confirmation) |
| **List agents** | `ai-maestro-agents-management` | List all registered agents with status |
| **Check agent health** | `ai-maestro-agents-management` | Check health status for an agent |
| **Send message** | `agent-messaging` | Send message to a recipient with subject, content, and priority |
| **Check inbox** | `agent-messaging` | Check for unread messages |
| **Mark read** | `agent-messaging` | Mark a message as read |

---

## 15. Kanban Column System

All projects use the canonical **8-column kanban system** on GitHub Projects:

| Column | Code | Label |
|--------|------|-------|
| Backlog | `backlog` | `status:backlog` |
| Todo | `todo` | `status:todo` |
| In Progress | `in-progress` | `status:in-progress` |
| AI Review | `ai-review` | `status:ai-review` |
| Human Review | `human-review` | `status:human-review` |
| Merge/Release | `merge-release` | `status:merge-release` |
| Done | `done` | `status:done` |
| Blocked | `blocked` | `status:blocked` |

**Task routing**:
- Small tasks: In Progress -> AI Review -> Merge/Release -> Done
- Big tasks: In Progress -> AI Review -> Human Review -> Merge/Release -> Done

---

## 16. Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/amcos_pre_push_hook.py` | Pre-push validation (manifest, hooks, lint, Unicode compliance) |
| `scripts/amcos_resource_check.py` | Resource availability checking |
| `scripts/amcos_heartbeat_check.py` | Agent heartbeat monitoring |
| `scripts/amcos_team_registry.py` | Team registry management |
| `scripts/amcos_download.py` | Plugin download utility |

---

**END OF DOCUMENT**
