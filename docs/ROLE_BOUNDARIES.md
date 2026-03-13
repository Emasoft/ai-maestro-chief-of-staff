# AMCOS Role Boundaries

**CRITICAL: This document defines the strict boundaries between agent roles. Violating these boundaries breaks the system architecture.**

> **Authoritative source**: The `team-governance` skill is the runtime authority for governance rules. This document is a local reference copy.

---

## Governance Roles vs Plugin Roles

AI Maestro governance defines three roles at the team level:

| Governance Role | Description |
|-----------------|-------------|
| `manager` | Team owner. Approves requests, creates projects, talks to user. |
| `chief-of-staff` | Team-scoped staff agent. Manages agent lifecycle for ONE team. |
| `member` | Any agent performing work within a team. |

The AMCOS plugin defines four specializations that all map to governance role `member`:

| Plugin Role | Abbreviation | Governance Role |
|-------------|-------------|-----------------|
| Orchestrator | AMOA | `member` |
| Architect | AMAA | `member` |
| Integrator | AMIA | `member` |
| Programmer | AMPA | `member` |

AMCOS itself maps to governance role `chief-of-staff`. AMA maps to `manager`.

---

## Role Hierarchy (Per-Team Scope)

```
┌──────────────────────────────────────────────────────────────┐
│                           USER                               │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                AMA (Manager)                                │
│                governance role: manager                       │
│                - User's sole interlocutor                     │
│                - Creates projects / teams                     │
│                - Approves AMCOS requests                      │
│                - Supervises all teams                         │
└────────────────────────────┬─────────────────────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                                   │
           ▼                                   ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│      Team Alpha         │       │      Team Beta          │
│                         │       │                         │
│  ┌───────────────────┐  │       │  ┌───────────────────┐  │
│  │ AMCOS-alpha       │  │       │  │ AMCOS-beta        │  │
│  │ chief-of-staff    │  │       │  │ chief-of-staff    │  │
│  │ (one per team)    │  │       │  │ (one per team)    │  │
│  └────────┬──────────┘  │       │  └────────┬──────────┘  │
│           │              │       │           │              │
│    ┌──────┼──────┐       │       │    ┌──────┼──────┐       │
│    ▼      ▼      ▼       │       │    ▼      ▼      ▼       │
│  AMOA    AMAA    AMIA       │       │  AMOA    AMAA    AMPA       │
│  member member member    │       │  member member member    │
└─────────────────────────┘       └─────────────────────────┘
```

---

## AMCOS (Chief of Staff) - Responsibilities

**Scope: TEAM-SCOPED. One AMCOS per team. Manages agent lifecycle for its own team only.**

### AMCOS CAN:
- Create agents for its team (with AMA approval)
- Terminate agents in its team (with AMA approval)
- Hibernate/wake agents in its team (with AMA approval)
- Configure agents with skills and plugins
- Assign agents to its team
- Handle handoff protocols between agents in its team
- Monitor agent health and availability within its team
- Replace failed agents in its team (with AMA approval)
- Report agent performance to AMA

### AMCOS CANNOT:
- Create projects (AMA only)
- Assign tasks to agents (AMOA only)
- Manage GitHub Project kanban (AMOA only)
- Make architectural decisions (AMAA only)
- Perform code review (AMIA only)
- Communicate directly with user (AMA only)
- Manage agents in OTHER teams
- Directly message members of other closed teams

---

## Communication Restrictions

AMCOS can send messages to:

| Target | Allowed |
|--------|---------|
| AMA (Manager) | Yes |
| Other AMCOS agents (other teams' COS) | Yes |
| Own team members | Yes |
| Agents not in any closed team (unassigned) | Yes |
| Members of OTHER closed teams | **NO** |

Cross-team operations (e.g., borrowing an agent, sharing resources) require a `GovernanceRequest` with **dual-manager approval** (both teams' managers, or AMA if AMA manages both).

---

## AMOA (Orchestrator) - Responsibilities

**Governance role: `member`. Plugin role: Orchestrator.**

### AMOA CAN:
- Assign tasks to agents within its project
- Manage GitHub Project kanban for its project
- Track task progress
- Reassign tasks between agents in its project
- Generate handoff documents
- Coordinate agent work within its project
- Request AMCOS to create/replace agents for its project

### AMOA CANNOT:
- Create agents directly (request via AMCOS)
- Configure agent skills/plugins (AMCOS only)
- Create projects (AMA only)
- Manage agents outside its project

### AMOA Scope:
- **Project-linked**: One AMOA per project
- **Task-focused**: Manages what agents DO, not what agents EXIST
- **Kanban owner**: Owns the GitHub Project board for its project

---

## AMA (Manager) - Responsibilities

**Governance role: `manager`.**

### AMA CAN:
- Create projects and teams
- Approve/reject AMCOS requests (agent create/terminate/etc.)
- Approve cross-team GovernanceRequests
- Communicate with user
- Set strategic direction
- Override any agent decision
- Grant autonomous operation directives

### AMA CANNOT:
- Create agents directly (delegates to AMCOS)
- Assign tasks directly (delegates to AMOA)

### AMA Scope:
- **Organization-wide**: Oversees all teams and projects
- **User-facing**: Only agent that talks to user
- **Decision authority**: Final approval on all significant operations

---

## Interaction Patterns

### Creating an Agent for a Team

```
AMOA: "I need a frontend developer agent for Project X"
  │
  ▼
AMCOS (team): Receives request, prepares agent specification
  │
  ▼
AMCOS → AMA: "Request approval to spawn frontend-dev for Team Alpha / Project X"
  │
  ▼
AMA: Approves (or rejects with reason)
  │
  ▼
AMCOS: Creates agent, configures skills, assigns to team
  │
  ▼
AMCOS → AMOA: "Agent frontend-dev ready, assigned to your team/project"
  │
  ▼
AMOA: Assigns tasks from kanban to new agent
```

### Cross-Team Operation

```
AMCOS-alpha: Needs agent from Team Beta for temporary work
  │
  ▼
AMCOS-alpha → AMCOS-beta: "GovernanceRequest: borrow agent-X for 2 tasks"
  │
  ▼
AMCOS-beta → AMA: "Cross-team request from Team Alpha, forward for approval"
AMCOS-alpha → AMA: "Cross-team request, requesting dual approval"
  │
  ▼
AMA: Approves both sides (dual-manager approval)
  │
  ▼
AMCOS-beta: Temporarily reassigns agent-X
AMCOS-alpha: Receives agent-X into team scope
```

### Agent Replacement

```
AMCOS: Detects agent-123 is unresponsive (terminal failure)
  │
  ▼
AMCOS → AMA: "Request approval to replace agent-123"
  │
  ▼
AMA: Approves
  │
  ▼
AMCOS: Creates replacement agent-456, configures it
  │
  ▼
AMCOS → AMOA: "agent-123 replaced by agent-456, generate handoff"
  │
  ▼
AMOA: Generates handoff document with task context
AMOA: Reassigns kanban tasks from agent-123 to agent-456
AMOA: Sends handoff to agent-456
```

---

## Summary Table

| Responsibility | AMA (manager) | AMCOS (chief-of-staff) | AMOA (member) | AMIA (member) | AMAA (member) | AMPA (member) |
|----------------|:-:|:-:|:-:|:-:|:-:|:-:|
| Create projects/teams | Yes | -- | -- | -- | -- | -- |
| Create agents | Approves | Yes | Requests | -- | -- | -- |
| Configure agents | -- | Yes | -- | -- | -- | -- |
| Assign agents to team | -- | Yes | -- | -- | -- | -- |
| Assign tasks | -- | -- | Yes | -- | -- | -- |
| Manage kanban | -- | -- | Yes | -- | -- | -- |
| Code review | -- | -- | -- | Yes | -- | -- |
| Architecture | -- | -- | -- | -- | Yes | -- |
| Implementation | -- | -- | -- | -- | -- | Yes |
| Talk to user | Yes | -- | -- | -- | -- | -- |
| Cross-team governance | Approves | Requests | -- | -- | -- | -- |
| Message other teams' members | Yes | **No** | **No** | **No** | **No** | **No** |

---

**Plugin**: `ai-maestro-chief-of-staff`
**Document Version**: 2.11.0
**Last Updated**: 2026-03-13
