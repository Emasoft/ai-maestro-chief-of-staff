# AMCOS Role Boundaries

**CRITICAL: This document defines the strict boundaries between agent roles. Violating these boundaries breaks the system architecture.**

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
| Orchestrator | EOA | `member` |
| Architect | EAA | `member` |
| Integrator | EIA | `member` |
| Programmer | EPA | `member` |

AMCOS itself maps to governance role `chief-of-staff`. EAMA maps to `manager`.

---

## Role Hierarchy (Per-Team Scope)

```
┌──────────────────────────────────────────────────────────────┐
│                           USER                               │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                EAMA (Manager)                                │
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
│  EOA    EAA    EIA       │       │  EOA    EAA    EPA       │
│  member member member    │       │  member member member    │
└─────────────────────────┘       └─────────────────────────┘
```

---

## AMCOS (Chief of Staff) - Responsibilities

**Scope: TEAM-SCOPED. One AMCOS per team. Manages agent lifecycle for its own team only.**

### AMCOS CAN:
- Create agents for its team (with EAMA approval)
- Terminate agents in its team (with EAMA approval)
- Hibernate/wake agents in its team (with EAMA approval)
- Configure agents with skills and plugins
- Assign agents to its team
- Handle handoff protocols between agents in its team
- Monitor agent health and availability within its team
- Replace failed agents in its team (with EAMA approval)
- Report agent performance to EAMA

### AMCOS CANNOT:
- Create projects (EAMA only)
- Assign tasks to agents (EOA only)
- Manage GitHub Project kanban (EOA only)
- Make architectural decisions (EAA only)
- Perform code review (EIA only)
- Communicate directly with user (EAMA only)
- Manage agents in OTHER teams
- Directly message members of other closed teams

---

## Communication Restrictions

AMCOS can send messages to:

| Target | Allowed |
|--------|---------|
| EAMA (Manager) | Yes |
| Other AMCOS agents (other teams' COS) | Yes |
| Own team members | Yes |
| Agents not in any closed team (unassigned) | Yes |
| Members of OTHER closed teams | **NO** |

Cross-team operations (e.g., borrowing an agent, sharing resources) require a `GovernanceRequest` with **dual-manager approval** (both teams' managers, or EAMA if EAMA manages both).

---

## EOA (Orchestrator) - Responsibilities

**Governance role: `member`. Plugin role: Orchestrator.**

### EOA CAN:
- Assign tasks to agents within its project
- Manage GitHub Project kanban for its project
- Track task progress
- Reassign tasks between agents in its project
- Generate handoff documents
- Coordinate agent work within its project
- Request AMCOS to create/replace agents for its project

### EOA CANNOT:
- Create agents directly (request via AMCOS)
- Configure agent skills/plugins (AMCOS only)
- Create projects (EAMA only)
- Manage agents outside its project

### EOA Scope:
- **Project-linked**: One EOA per project
- **Task-focused**: Manages what agents DO, not what agents EXIST
- **Kanban owner**: Owns the GitHub Project board for its project

---

## EAMA (Manager) - Responsibilities

**Governance role: `manager`.**

### EAMA CAN:
- Create projects and teams
- Approve/reject AMCOS requests (agent create/terminate/etc.)
- Approve cross-team GovernanceRequests
- Communicate with user
- Set strategic direction
- Override any agent decision
- Grant autonomous operation directives

### EAMA CANNOT:
- Create agents directly (delegates to AMCOS)
- Assign tasks directly (delegates to EOA)

### EAMA Scope:
- **Organization-wide**: Oversees all teams and projects
- **User-facing**: Only agent that talks to user
- **Decision authority**: Final approval on all significant operations

---

## Interaction Patterns

### Creating an Agent for a Team

```
EOA: "I need a frontend developer agent for Project X"
  │
  ▼
AMCOS (team): Receives request, prepares agent specification
  │
  ▼
AMCOS → EAMA: "Request approval to spawn frontend-dev for Team Alpha / Project X"
  │
  ▼
EAMA: Approves (or rejects with reason)
  │
  ▼
AMCOS: Creates agent, configures skills, assigns to team
  │
  ▼
AMCOS → EOA: "Agent frontend-dev ready, assigned to your team/project"
  │
  ▼
EOA: Assigns tasks from kanban to new agent
```

### Cross-Team Operation

```
AMCOS-alpha: Needs agent from Team Beta for temporary work
  │
  ▼
AMCOS-alpha → AMCOS-beta: "GovernanceRequest: borrow agent-X for 2 tasks"
  │
  ▼
AMCOS-beta → EAMA: "Cross-team request from Team Alpha, forward for approval"
AMCOS-alpha → EAMA: "Cross-team request, requesting dual approval"
  │
  ▼
EAMA: Approves both sides (dual-manager approval)
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
AMCOS → EAMA: "Request approval to replace agent-123"
  │
  ▼
EAMA: Approves
  │
  ▼
AMCOS: Creates replacement agent-456, configures it
  │
  ▼
AMCOS → EOA: "agent-123 replaced by agent-456, generate handoff"
  │
  ▼
EOA: Generates handoff document with task context
EOA: Reassigns kanban tasks from agent-123 to agent-456
EOA: Sends handoff to agent-456
```

---

## Summary Table

| Responsibility | EAMA (manager) | AMCOS (chief-of-staff) | EOA (member) | EIA (member) | EAA (member) | EPA (member) |
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
**Document Version**: 2.0.0
**Last Updated**: 2026-02-27
