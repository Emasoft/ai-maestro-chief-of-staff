# AI Maestro Chief of Staff (amcos-)

**Version**: 2.0.0 | **Minimum AI Maestro**: 0.26.0

> Derived from emasoft-chief-of-staff v1.3.9, adapted for AI Maestro governance v0.26.0

## Overview

AMCOS manages **per-team** agent lifecycle. One Chief of Staff instance exists per team -- it is NOT organization-wide. AMCOS handles staff planning, agent creation/termination, approval workflows, failure recovery, and coordinates with the team's Orchestrator (EOA), Architect (EAA), and Integrator (EIA).

## Key Differences from emasoft-chief-of-staff

| Aspect | emasoft-chief-of-staff | AMCOS (this plugin) |
|--------|----------------------|---------------------|
| Scope | Organization-wide (one COS for all) | **Per-team** (one COS per team) |
| Governance | Single-manager approval | **AI Maestro governance** (GovernanceRequests, dual-manager approval) |
| Communication | Direct HTTP | **AMP messaging protocol** |
| Role system | Flat roles | **3-role governance** (manager / chief-of-staff / member) |
| Agent registry | File-based JSON | **REST API** for team registry |
| Distribution | emasoft-plugins marketplace | **Bundled with AI Maestro v0.26.0+** |

## Communication Hierarchy

```
MANAGER (team manager)
    |
    | GovernanceRequests (approval/rejection via AMP)
    v
AMCOS (Chief of Staff) ---- one per team
    |
    |--- AMP messages --->  EOA (Orchestrator)
    |--- AMP messages --->  EAA (Architect)
    |--- AMP messages --->  EIA (Integrator)
    |--- AMP messages --->  team member agents
```

- MANAGER approves/rejects AMCOS lifecycle requests
- AMCOS notifies EOA/EAA/EIA after every agent lifecycle change
- All communication uses AMP (AI Maestro Protocol) messaging -- no direct HTTP

## Core Responsibilities

1. **Approval Workflows** -- Request dual-manager approval before agent spawn/terminate/replace
2. **Agent Lifecycle** -- Create, hibernate, wake, terminate agents within the team scope
3. **Notification Protocols** -- Notify team agents before/after operations, wait for acknowledgment
4. **Failure Recovery** -- Detect failures, classify severity, execute recovery strategies
5. **Team Assignment** -- Assign agents to the team roster (NOT task assignment -- that is EOA)
6. **Skill/Plugin Configuration** -- Configure agents with appropriate skills for their roles
7. **Performance Reporting** -- Report agent performance metrics to team manager

## What AMCOS Does NOT Do

- Create projects (manager only)
- Assign tasks to agents (EOA only)
- Manage GitHub Project kanban (EOA only)
- Make architectural decisions (EAA only)
- Perform code review (EIA only)
- Communicate directly with user (manager only)

## Components

### Agents (10)

| Agent | Purpose |
|-------|---------|
| `amcos-main` | Main COS coordinator |
| `amcos-staff-planner` | Analyze task requirements, determine staffing needs |
| `amcos-lifecycle-manager` | Agent create/terminate/hibernate/wake |
| `amcos-plugin-configurator` | Configure plugins for agents |
| `amcos-skill-validator` | Validate skill configurations |
| `amcos-resource-monitor` | Monitor system resources and limits |
| `amcos-performance-reporter` | Analyze and report agent performance |
| `amcos-recovery-coordinator` | Detect failures and coordinate recovery |
| `amcos-approval-coordinator` | Manage GovernanceRequest workflows with manager |
| `amcos-team-coordinator` | Intra-team coordination and task tracking |

### Commands (23)

#### Agent Lifecycle

| Command | Description |
|---------|-------------|
| `/amcos-staff-status` | List all team agents |
| `/amcos-spawn-agent` | Create new agent (requires governance approval) |
| `/amcos-terminate-agent` | Terminate agent (requires governance approval) |
| `/amcos-hibernate-agent` | Hibernate agent |
| `/amcos-wake-agent` | Wake hibernated agent |
| `/amcos-transfer-agent` | Transfer agent to another team (requires dual-manager approval) |

#### Plugin/Skill Management

| Command | Description |
|---------|-------------|
| `/amcos-configure-plugins` | Configure plugins for team agents |
| `/amcos-validate-skills` | Validate skill configurations |
| `/amcos-reindex-skills` | Reindex skill database |
| `/amcos-install-skill-notify` | Install skill with notification protocol |

#### Approval Workflows

| Command | Description |
|---------|-------------|
| `/amcos-request-approval` | Submit GovernanceRequest to manager |
| `/amcos-check-approval-status` | Check pending GovernanceRequest status |
| `/amcos-wait-for-approval` | Wait for governance approval response |
| `/amcos-notify-manager` | Notify manager about issues |

#### Notification Protocols

| Command | Description |
|---------|-------------|
| `/amcos-notify-agents` | Notify team agents before/after operations |
| `/amcos-wait-for-agent-ok` | Wait for agent acknowledgment |
| `/amcos-broadcast-notification` | Broadcast to multiple team agents |

#### Recovery & Health

| Command | Description |
|---------|-------------|
| `/amcos-health-check` | Check team agent health status |
| `/amcos-replace-agent` | Replace failed agent (requires governance approval) |
| `/amcos-transfer-work` | Transfer work between team agents |
| `/amcos-recovery-workflow` | Execute recovery workflow |

#### Reporting

| Command | Description |
|---------|-------------|
| `/amcos-resource-report` | Show team resource usage |
| `/amcos-performance-report` | Show team performance metrics |

### Skills (26)

| Skill | Purpose |
|-------|---------|
| `amcos-agent-spawning` | Agent spawn procedures |
| `amcos-agent-termination` | Agent terminate procedures |
| `amcos-agent-hibernation` | Agent hibernate and wake procedures |
| `amcos-agent-coordination` | Agent lifecycle coordination across team |
| `amcos-failure-detection` | Failure detection and classification |
| `amcos-recovery-execution` | Recovery strategy execution |
| `amcos-agent-replacement` | Failed agent replacement procedures |
| `amcos-emergency-handoff` | Emergency handoff during critical failures |
| `amcos-label-taxonomy` | Label taxonomy for team agent classification |
| `amcos-pre-op-notification` | Pre-operation notifications to team agents |
| `amcos-post-op-notification` | Post-operation notifications to team agents |
| `amcos-acknowledgment-protocol` | Acknowledgment collection and verification |
| `amcos-failure-notification` | Failure event notifications to team and manager |
| `amcos-onboarding` | Agent onboarding checklists and procedures |
| `amcos-performance-tracking` | Performance metrics and reporting |
| `amcos-permission-management` | GovernanceRequest approval/response workflows |
| `amcos-plugin-management` | Plugin configuration and installation |
| `amcos-resource-monitoring` | Resource limits and monitoring |
| `amcos-memory-initialization` | Session memory initialization and loading |
| `amcos-context-management` | Session context persistence and management |
| `amcos-progress-tracking` | Session progress tracking and checkpoints |
| `amcos-config-snapshot` | Configuration snapshot capture and restore |
| `amcos-skill-management` | Skill validation and reindexing |
| `amcos-staff-planning` | Staff planning and role assignment |
| `amcos-team-coordination` | Team AMP messaging and coordination |
| `amcos-transfer-management` | Cross-team agent transfer with dual-manager approval |

### Hooks (5)

| Hook | Event | Purpose |
|------|-------|---------|
| `amcos-session-start` | SessionStart | Load session memory, initialize agent tracking, check resources |
| `amcos-session-end` | SessionEnd | Save session memory and context on exit |
| `amcos-resource-check` | UserPromptSubmit | Check system resources before processing |
| `amcos-heartbeat-check` | UserPromptSubmit | Check heartbeat status of active agents |
| `amcos-stop-check` | Stop | Block exit until coordination work is complete |

## Installation

This plugin is distributed with AI Maestro v0.26.0+. No separate installation is needed.

```bash
# Start a session with the team's COS agent
claude --agent amcos-chief-of-staff-main-agent
```

### Development Only

```bash
claude --plugin-dir ./ai-maestro-chief-of-staff
```

## Cross-Plugin Coordination (AMP Messaging)

All cross-plugin communication uses AMP (AI Maestro Protocol). AMCOS never calls other plugins directly.

| Target | AMP Subject Pattern | Purpose |
|--------|-------------------|---------|
| **Manager** | `governance-request.*` | Request approval for lifecycle operations; report agent status and performance |
| **EOA** (Orchestrator) | `agent-lifecycle.*` | Notify when agent is ready for task assignment; request handoff doc generation; inform EOA to reassign kanban tasks |
| **EAA** (Architect) | `staffing-requirements.*` | Request architecture input for staffing decisions |
| **EIA** (Integrator) | `deployment-coordination.*` | Coordinate deployment readiness of team agents |

## 3-Role Governance System

| Role | Permissions | Example |
|------|------------|---------|
| **Manager** | Approve/reject GovernanceRequests, create projects, direct user communication | Team manager agent |
| **Chief of Staff** | Submit GovernanceRequests, manage agent lifecycle, configure skills/plugins | AMCOS (this plugin) |
| **Member** | Execute assigned tasks, report status | EOA, EAA, EIA, task agents |

Critical operations (spawn, terminate, replace) require a GovernanceRequest approved by the team manager. Dual-manager approval is required for cross-team agent transfers.

## Validation

```bash
cd ai-maestro-chief-of-staff
uv run python scripts/validate_plugin.py . --verbose
```
