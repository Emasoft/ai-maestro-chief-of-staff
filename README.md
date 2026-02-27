# AI Maestro Chief of Staff (amcos-)

**Version**: 1.2.0

## Overview

The AI Maestro Chief of Staff (AMCOS) manages **remote agents** across multiple projects. It handles staff planning, agent lifecycle, approval workflows, failure recovery, and coordinates with the Assistant Manager (EAMA) and Orchestrator (EOA).

**Key Role**: AMCOS is responsible for keeping agents ready and correctly configured. It must notify the manager (EAMA) after every change, and request approval for critical operations.

## CRITICAL: Role Boundaries

**See [docs/ROLE_BOUNDARIES.md](docs/ROLE_BOUNDARIES.md) for complete role definitions.**

### AMCOS Scope: PROJECT-INDEPENDENT

AMCOS is **organization-wide** - there is ONE Chief of Staff managing agents across ALL projects.

### What AMCOS Does:
- ✅ Creates/terminates/hibernates/wakes agents (with EAMA approval)
- ✅ Configures agents with skills and plugins for their roles
- ✅ Assigns agents to project teams
- ✅ Handles handoff protocols when agents are replaced
- ✅ Monitors agent health and availability
- ✅ Reports agent performance to EAMA

### What AMCOS Does NOT Do:
- ❌ **Create projects** (EAMA only)
- ❌ **Assign tasks to agents** (EOA only)
- ❌ **Manage GitHub Project kanban** (EOA only)
- ❌ **Make architectural decisions** (EAA only)
- ❌ **Perform code review** (EIA only)
- ❌ **Communicate directly with user** (EAMA only)

### Key Distinction: AMCOS vs EOA

| Aspect | AMCOS (Chief of Staff) | EOA (Orchestrator) |
|--------|----------------------|-------------------|
| Scope | Organization-wide (ONE) | Project-linked (ONE per project) |
| Manages | Agent EXISTENCE | Agent WORK |
| Creates | Agents, teams | Task assignments |
| Owns | Agent registry | GitHub Project kanban |
| Question answered | "Who exists?" | "Who does what?" |

## Agent Management Integration

This plugin uses two skills for agent and messaging operations:

- **`ai-maestro-agents-management` skill** - For all agent lifecycle operations (create, terminate, hibernate, wake, install plugins, list agents, check health)
- **`agent-messaging` skill** - For all inter-agent communication (send messages, check inbox, broadcast notifications, approval requests)

### Required Claude Code Arguments

**IMPORTANT**: When spawning agents, always include the standard Claude Code flags as program arguments:

| Argument | Purpose |
|----------|---------|
| `continue` | Resume previous session context |
| `--dangerously-skip-permissions` | Skip permission dialogs for automation |
| `--chrome` | Enable Chrome DevTools integration |
| `--add-dir <TEMP>` | Add temp directory access |

**Platform-specific temp directories:**
- **macOS/Linux**: `/tmp`
- **Windows**: `%TEMP%` or `C:\Users\<user>\AppData\Local\Temp`

## Communication Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER                                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│      EAMA (Assistant Manager)                                    │
│   - User's right hand, sole interlocutor                         │
│   - Approves/rejects AMCOS requests                               │
└──────┬──────────────────────────────────────────────────────────┘
       │ requests approval, reports status
       ▼
┌─────────────────────────────────────────────────────────────────┐
│      AMCOS (Chief of Staff)                                       │
│   - Manages agent lifecycle                                      │
│   - Coordinates approvals and notifications                      │
│   - Handles failure recovery                                     │
└──────┬─────────────────────┬─────────────────────┬──────────────┘
       │                     │                     │
       ▼                     ▼                     ▼
   ARCHITECT           ORCHESTRATOR           INTEGRATOR
   (EAA)                (EOA)                   (EIA)
```

## Core Responsibilities

1. **Approval Workflows**: Request manager approval before agent spawn/terminate/replace
2. **Agent Lifecycle**: Create, hibernate, wake, terminate agents via AI Maestro CLI
3. **Notification Protocols**: Notify agents before/after operations, wait for acknowledgment
4. **Failure Recovery**: Detect failures, classify severity, execute recovery strategies
5. **Team Assignment**: Assign agents to project teams (NOT task assignment - that's EOA)
6. **Skill/Plugin Configuration**: Configure agents with appropriate skills for their roles
7. **Performance Reporting**: Report agent strengths/weaknesses to manager

**Note**: AMCOS does NOT manage tasks or kanban boards. When a new agent is created or an agent is replaced, AMCOS notifies EOA so that EOA can handle task (re)assignment.

## Components

### Agents (10)

| Agent | Description |
|-------|-------------|
| `amcos-main` | Main Chief of Staff coordinator |
| `amcos-staff-planner` | Analyzes task requirements, determines staffing needs |
| `amcos-lifecycle-manager` | Manages agent create/terminate/hibernate/wake |
| `amcos-project-coordinator` | Tracks multi-project assignments |
| `amcos-plugin-configurator` | Configures plugins for agents |
| `amcos-skill-validator` | Validates skill configurations |
| `amcos-resource-monitor` | Monitors system resources and limits |
| `amcos-performance-reporter` | Analyzes and reports agent performance |
| `amcos-recovery-coordinator` | Detects failures and coordinates recovery |
| `amcos-approval-coordinator` | Manages approval workflows with manager |

### Commands (26)

#### Agent Lifecycle
| Command | Description |
|---------|-------------|
| `/amcos-staff-status` | List all agents |
| `/amcos-spawn-agent` | Create new agent |
| `/amcos-terminate-agent` | Delete agent |
| `/amcos-hibernate-agent` | Hibernate agent |
| `/amcos-wake-agent` | Wake hibernated agent |

#### Project Management
| Command | Description |
|---------|-------------|
| `/amcos-list-projects` | List managed projects |
| `/amcos-add-project` | Add project to management |
| `/amcos-remove-project` | Remove project from management |
| `/amcos-assign-project` | Assign agent to project |

#### Plugin/Skill Management
| Command | Description |
|---------|-------------|
| `/amcos-configure-plugins` | Configure plugins for agents |
| `/amcos-validate-skills` | Validate skill configurations |
| `/amcos-reindex-skills` | Reindex skill database |
| `/amcos-install-skill-notify` | Install skill with notification protocol |

#### Approval Workflows
| Command | Description |
|---------|-------------|
| `/amcos-request-approval` | Request approval from manager |
| `/amcos-check-approval-status` | Check pending approval status |
| `/amcos-wait-for-approval` | Wait for approval response |
| `/amcos-notify-manager` | Notify manager about issues |

#### Notification Protocols
| Command | Description |
|---------|-------------|
| `/amcos-notify-agents` | Notify agents before/after operations |
| `/amcos-wait-for-agent-ok` | Wait for agent acknowledgment |
| `/amcos-broadcast-notification` | Send notification to multiple agents |

#### Recovery & Health
| Command | Description |
|---------|-------------|
| `/amcos-health-check` | Check agent health status |
| `/amcos-replace-agent` | Replace failed agent with new one |
| `/amcos-transfer-work` | Transfer work between agents |
| `/amcos-recovery-workflow` | Execute recovery workflow |

#### Reporting
| Command | Description |
|---------|-------------|
| `/amcos-resource-report` | Show resource usage report |
| `/amcos-performance-report` | Show performance metrics |

### Skills (13)

| Skill | Description |
|-------|-------------|
| `amcos-agent-lifecycle` | Agent spawn, terminate, hibernate, wake procedures |
| `amcos-failure-recovery` | Failure detection, classification, recovery strategies |
| `amcos-multi-project` | Multi-project tracking and coordination |
| `amcos-notification-protocols` | Pre/post operation notifications, acknowledgment |
| `amcos-onboarding` | Agent onboarding checklists and procedures |
| `amcos-performance-tracking` | Performance metrics and reporting |
| `amcos-permission-management` | Approval request/response workflows |
| `amcos-plugin-management` | Plugin configuration and installation |
| `amcos-resource-monitoring` | Resource limits and monitoring |
| `amcos-session-memory-library` | Session memory persistence and management |
| `amcos-skill-management` | Skill validation and reindexing |
| `amcos-staff-planning` | Staff planning and role assignment |
| `amcos-team-coordination` | Team messaging and coordination |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `amcos-memory-load` | SessionStart | Load session memory at startup |
| `amcos-memory-save` | SessionEnd | Save session memory on exit |
| `amcos-heartbeat` | UserPromptSubmit | Check agent health |
| `amcos-stop-check` | Stop | Verify all work complete before exit |

## Key Protocols

### Approval Protocol

1. AMCOS sends approval request to EAMA via AI Maestro
2. AMCOS waits up to 2 minutes for response (reminders at 30s, 60s, 90s)
3. If approved: AMCOS executes operation
4. If rejected: AMCOS aborts and notifies requester
5. If timeout: AMCOS may proceed but logs this and notifies EAMA

### Skill Installation Protocol

1. AMCOS notifies agent about upcoming skill install (will hibernate/wake)
2. AMCOS asks agent to finish current work and send "ok"
3. AMCOS waits up to 2 minutes for acknowledgment
4. AMCOS uses the `ai-maestro-agents-management` skill to install the plugin on the agent
5. After wake, AMCOS asks agent to verify skill is active

### Agent Replacement Protocol

1. AMCOS detects agent cannot be recovered
2. AMCOS requests approval from EAMA
3. If approved: AMCOS creates new agent on local host
4. AMCOS notifies EOA to generate handoff document
5. AMCOS notifies EOA to update GitHub Project kanban
6. AMCOS sends handoff docs to new agent
7. New agent acknowledges and begins work

## Communication Methods

1. **AI Maestro messages** - for approval requests, notifications, status updates
2. **Handoff .md files** with UUIDs - for detailed specifications
3. **GitHub Issues** - as permanent record

## Installation (Production)

Install from the AI Maestro marketplace. Use `--scope local` to install only for this agent's directory only, or `--scope global` for all projects.

Role plugins are installed with `--scope local` inside the specific agent's working directory (`~/agents/<agent-name>/`). This ensures the plugin is only available to that agent.

```bash
# Add AI Maestro marketplace (first time only)
claude plugin marketplace add ai-maestro-plugins --url https://github.com/Emasoft/ai-maestro-plugins

# Install plugin (--scope local = this agent's directory only, recommended)
claude plugin install ai-maestro-chief-of-staff@ai-maestro-plugins --scope local

# RESTART Claude Code after installing (required!)
```

Once installed, start a session with the main agent:

```bash
claude --agent amcos-chief-of-staff-main-agent
```

## Development Only (--plugin-dir)

`--plugin-dir` loads a plugin directly from a local directory without marketplace installation. Use only during plugin development.

```bash
claude --plugin-dir ./OUTPUT_SKILLS/ai-maestro-chief-of-staff
```

## Validation

```bash
cd OUTPUT_SKILLS/ai-maestro-chief-of-staff
uv run python scripts/validate_plugin.py . --verbose
```

## Cross-Plugin Coordination

AMCOS coordinates with:
- **EAMA** (ai-maestro-assistant-manager-agent):
  - Requests approval for agent lifecycle operations
  - Reports agent status and performance
  - Receives autonomous operation directives
- **EOA** (ai-maestro-orchestrator-agent):
  - Notifies when new agent is ready for task assignment
  - Requests handoff document generation when replacing agents
  - Informs EOA to reassign kanban tasks from failed to replacement agents
  - **Note**: EOA owns task assignment and kanban management
- **EIA** (ai-maestro-integrator-agent): Code review and deployment coordination
- **EAA** (ai-maestro-architect-agent): Architecture decisions for staffing requirements
