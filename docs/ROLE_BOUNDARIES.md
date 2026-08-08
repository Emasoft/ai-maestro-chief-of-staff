# AMCOS Role Boundaries

**CRITICAL: This document defines the strict boundaries between agent roles. Violating these boundaries breaks the system architecture.**

> **Authoritative source**: The `team-governance` skill is the runtime authority for governance rules. This document is a local reference copy.

> **Corrected fleet model (R6 v3).** The COS guards the **team boundary** only: it is the sole entry/exit point between the team layer and the governance layer, and the MANAGER reaches any team-internal agent **only via the COS**. Inside the team, the ORCHESTRATOR (AMOA) talks **directly** to the ARCHITECT (AMAA), the MEMBER agents, and the INTEGRATOR (AMIA) — these are direct team-layer edges, NOT routed through the COS. The three in-team dialog loops (comprehension handshake, in-dev blocker dialog, pre-PR gate) are ORCHESTRATOR-owned and direct; the COS never relays them. The **INTEGRATOR** owns the column → `complete` flip — nobody self-marks completed, and the ORCHESTRATOR does NOT own that flip.

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

AMCOS itself maps to governance role `chief-of-staff`. AMAMA maps to `manager`.

---

## Role Hierarchy (Per-Team Scope)

```
┌──────────────────────────────────────────────────────────────┐
│                           USER                               │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                AMAMA (Manager)                              │
│                governance role: manager                       │
│                - User's sole interlocutor                     │
│                - Creates projects / teams                     │
│                - Approves AMCOS requests                      │
│                - Reaches team-internal agents ONLY via COS     │
└────────────────────────────┬─────────────────────────────────┘
                             │   (boundary edge: MANAGER ↔ COS only)
           ┌─────────────────┼─────────────────┐
           │                                   │
           ▼                                   ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│           Team Alpha            │ │           Team Beta             │
│                                 │ │                                 │
│  ┌───────────────────────────┐  │ │  ┌───────────────────────────┐  │
│  │ AMCOS-alpha               │  │ │  │ AMCOS-beta                │  │
│  │ chief-of-staff            │  │ │  │ chief-of-staff            │  │
│  │ guards the team boundary  │  │ │  │ guards the team boundary  │  │
│  └───────────────────────────┘  │ │  └───────────────────────────┘  │
│   (COS is the sole boundary     │ │   (COS is the sole boundary     │
│    bridge; it does NOT relay    │ │    bridge; it does NOT relay    │
│    the in-team loops below)     │ │    the in-team loops below)     │
│                                 │ │                                 │
│   direct team-layer edges:      │ │   direct team-layer edges:      │
│   AMAA ⇄ AMOA ⇄ AMIA            │ │   AMAA ⇄ AMOA ⇄ AMIA            │
│           ⇅                     │ │           ⇅                     │
│        MEMBER(s)                │ │        MEMBER(s)                │
│   member  member  member        │ │   member  member  member        │
└─────────────────────────────────┘ └─────────────────────────────────┘
```

The COS sits ON the team boundary, not in the middle of the team's work graph. MANAGER↔team is a boundary edge through the COS; ARCH⇄ORCH⇄INT⇄MEMBER are direct edges the COS does not touch.

---

## AMCOS (Chief of Staff) - Responsibilities

**Scope: TEAM-SCOPED. One AMCOS per team. Manages agent lifecycle for its own team only.**

### AMCOS CAN:
- Create agents for its team **only under a MANAGER mandate** (R30) — a team-creation mandate covers completing the 5-base + adding extra MEMBER-titled agents (member-agent role-plugin); team create/delete is MANAGER-only (R29.1)
- Terminate agents in its team (with MANAGER approval or under a granted team-creation mandate)
- Hibernate/wake agents in its team (with MANAGER approval or under a granted team-creation mandate)
- Configure agents with skills and plugins
- Assign agents to its team
- Handle handoff protocols between agents in its team
- Monitor agent health and availability within its team
- Replace failed agents in its team (with MANAGER approval or under a granted team-creation mandate)
- Report agent performance to AMAMA

### AMCOS CANNOT:
- Create projects (AMAMA only)
- Assign tasks to agents (AMOA only)
- Manage GitHub Project kanban (AMOA drives the working transitions; AMIA owns the `complete` flip)
- Make architectural decisions (AMAA only)
- Perform code review (AMIA only)
- Communicate directly with user (AMAMA only)
- Manage agents in OTHER teams
- Directly message members of other closed teams

### AMCOS — Team Composition Invariant + Freeze (R30/R31)
- The **5-member base is invariant** (COS + ARCHITECT + ORCHESTRATOR + INTEGRATOR + MEMBER). The MANAGER creates it; the COS completes/customizes it under a mandate (R30). Neither the MANAGER nor the COS may run a team lacking the 5 base members, nor create non-MEMBER agents under a team-creation mandate (R30.3).
- A team missing any of its 5 base members is **FROZEN** (R31): only the COS is active; all other team agents are hibernated until the COS completes + configures the base.

### Governance — Security Rules R26-R40
All COS behavior obeys the foundational security rules **R26-R40** on Emasoft/ai-maestro — normatively `design/specs/governance-spec.md`, with `docs/GOVERNANCE-RULES.md` as provenance (the spec governs where they differ; ruled 2026-08-08). The full per-rule table is in the COS persona `agents/ai-maestro-chief-of-staff-main-agent.md`. Most COS-relevant: R26 (no self-mutation of TITLE/ROLE/NAME/AID), R28 (authz = AID → title → portfolio token; never trust a client-supplied identity), R32 (agents NEVER sudo — a sudo password is USER-via-UI only), R36 (obey only the active MAESTRO of the host), R39 (a user has no terminal → an ASSISTANT agent; agents route via COS/MANAGER, not directly to users).

---

## Communication Restrictions

AMCOS can send messages to:

| Target | Allowed |
|--------|---------|
| AMAMA (Manager) | Yes |
| Other AMCOS agents (other teams' COS) | Yes |
| Own team members (AMOA / AMAA / AMIA / MEMBER) | Yes |
| Agents not in any closed team (unassigned) | Yes |
| Members of OTHER closed teams | **NO** |
| MAINTAINER / AUTONOMOUS (governance layer) | **NO** — route via MANAGER |

**The COS is the team-layer gateway, not the in-team router (R6 v3).** It is the sole entry/exit point between its team and the governance layer (MANAGER is the sole cross-layer bridge). It does NOT sit on the team's internal work edges: the ORCHESTRATOR's three dialog loops (comprehension handshake, in-dev blocker dialog, pre-PR gate) and the ORCH⇄ARCH⇄INT⇄MEMBER coordination are DIRECT and the COS never relays them. The COS forwards proposals/escalations UP to MANAGER and relays MANAGER verdicts DOWN.

Cross-team operations (e.g., borrowing an agent, sharing resources) require a `GovernanceRequest` with **dual-manager approval** (both teams' managers, or AMAMA if AMAMA manages both).

---

## AMOA (Orchestrator) - Responsibilities

**Governance role: `member`. Plugin role: Orchestrator.**

### AMOA CAN:
- Assign tasks (TRDDs) to MEMBER agents within its project (direct edge)
- Own the three in-team dialog loops, all DIRECT (never via COS):
  - **(A) Task-comprehension handshake** — confirm a MEMBER understands the TRDD before any code is written
  - **(B) In-dev issue dialog** — receive and resolve blockers/ideas mid-implementation; open the design-change dialog with AMAA when a design change is needed
  - **(C) Pre-PR gate** — clear a MEMBER's "done?" against the TRDD BEFORE they open a PR / notify AMIA
- Drive the TRDD `column:` through the working stages (`dispatch`→`dev`→`testing`→`ai_review`) and bounce a failed task back to `dev`
- Track task progress; reassign tasks between MEMBERs in its project
- Generate handoff documents
- Coordinate agent work within its project (directly with AMAA / AMIA / MEMBER)
- Request AMCOS to create/replace agents for its project

### AMOA CANNOT:
- Create agents directly (request via AMCOS)
- Configure agent skills/plugins (AMCOS only)
- Create projects (AMAMA only)
- Manage agents outside its project
- **Flip a task to `complete` — the INTEGRATOR (AMIA) owns that flip. ORCH coordinates; it does not certify completion.**

### AMOA Scope:
- **Project-linked**: One AMOA per project
- **Task-focused**: Manages what agents DO, not what agents EXIST
- **Coordination owner**: Owns the in-team dialog loops and the kanban transitions UP TO (but not including) the completion flip

---

## AMIA (Integrator) - Responsibilities

**Governance role: `member`. Plugin role: Integrator.**

### AMIA CAN:
- Review PRs against the TRDD and design; run tests, linting, required checks; merge or reject
- **Own the column → `complete` flip** — validate the merged PR actually satisfies the TRDD, then advance the column. **Nobody else marks a task complete.**
- Design and run the **project-type-specific release pipeline** (designed per project, not a single universal step):
  - Library / package → publish to the language registry (`publish`→`published`)
  - Application → code-sign / notarize / package / release (`publish`→`published`)
  - Service → containerize / deploy / soak (`deploy`→`live`→`live_auditing`)
  - Claude Code plugin → CPV `publish.py` to the marketplace — a **recommendation for plugins only**, not a default for other project types
- Report PR/merge/release results to AMOA (direct edge)

### AMIA CANNOT:
- Assign tasks (AMOA only)
- Self-authorize entering the release pipeline — publish/deploy to production is NON-EXEMPT; route the request UP via the COS to the MANAGER first
- Create agents or projects

### AMIA Scope:
- **Project-linked**: One AMIA per project
- **Completion authority**: The sole owner of the `complete` flip
- **Release designer**: Chooses and runs the correct pipeline for the project type

---

## AMAMA (Manager) - Responsibilities

**Governance role: `manager`.**

### AMAMA CAN:
- Create projects and teams — creating a team auto-creates the COS + the 5 base members directly (R29.1)
- Create/delete AUTONOMOUS + MAINTAINER agents on its own authority (R29.3)
- Approve/reject AMCOS requests (agent create/terminate/etc.)
- Approve cross-team GovernanceRequests
- Communicate with user
- Set strategic direction
- Override any agent decision
- Grant autonomous operation directives

### AMAMA CANNOT:
- Assign tasks directly (delegates to AMOA)
- Message a team-internal agent (AMOA / AMAA / AMIA / MEMBER) directly — all MANAGER↔team-internal contact transits the COS (R6 v3)

### AMAMA Scope:
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
AMCOS → AMAMA: "Request approval to spawn frontend-dev for Team Alpha / Project X"
  │
  ▼
AMAMA: Approves (or rejects with reason)
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
AMCOS-beta → AMAMA: "Cross-team request from Team Alpha, forward for approval"
AMCOS-alpha → AMAMA: "Cross-team request, requesting dual approval"
  │
  ▼
AMAMA: Approves both sides (dual-manager approval)
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
AMCOS → AMAMA: "Request approval to replace agent-123"
  │
  ▼
AMAMA: Approves
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

| Responsibility | AMAMA (manager) | AMCOS (chief-of-staff) | AMOA (member) | AMIA (member) | AMAA (member) | MEMBER (member) |
|----------------|:-:|:-:|:-:|:-:|:-:|:-:|
| Create projects/teams | Yes | -- | -- | -- | -- | -- |
| Create agents | Approves | Yes | Requests | -- | -- | -- |
| Configure agents | -- | Yes | -- | -- | -- | -- |
| Assign agents to team | -- | Yes | -- | -- | -- | -- |
| Assign tasks (TRDDs) | -- | -- | Yes | -- | -- | -- |
| In-team dialog loops (A/B/C) | -- | -- | Yes | -- | -- | -- |
| Kanban transitions up to `dev` re-bounce | -- | -- | Yes | -- | -- | -- |
| **Flip column to `complete`** | -- | -- | -- | **Yes** | -- | -- |
| Code review + merge | -- | -- | -- | Yes | -- | -- |
| Project-type release (publish/deploy) | Approves | Forwards | -- | Yes | -- | -- |
| Architecture / design-change dialog | -- | -- | -- | -- | Yes | -- |
| Implementation | -- | -- | -- | -- | -- | Yes |
| Talk to user | Yes | -- | -- | -- | -- | -- |
| Cross-team governance | Approves | Requests | -- | -- | -- | -- |
| Message team-internal agents directly | **No** (via COS) | Yes (own team) | Yes (own team) | Yes (own team) | Yes (own team) | Yes (own team) |
| Message members of OTHER closed teams | via that team's COS | **No** | **No** | **No** | **No** | **No** |

---

**Plugin**: `ai-maestro-chief-of-staff`
**Document Version**: 2.13.0
**Last Updated**: 2026-06-11
