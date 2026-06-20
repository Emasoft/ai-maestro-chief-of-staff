# Full Project Workflow: From Requirements to Delivery

**Version**: 2.13.0
**Last Updated**: 2026-06-11

This document describes the complete workflow for how the AI Maestro agent system handles a project from initial requirements to delivery. AMCOS (AI Maestro Chief of Staff) is **team-scoped**: it manages agents within ONE team only and **guards the team boundary** (R6 v3). Cross-team operations require GovernanceRequests. All inter-agent messaging uses the AMP protocol.

> **Corrected fleet model (R6 v3).** Within a team, the ORCHESTRATOR (AMOA) talks **directly** to the ARCHITECT (AMAA), the MEMBER agents, and the INTEGRATOR (AMIA) — these are direct team-layer edges, NOT routed through the COS. The COS guards the **team boundary** only: it is the sole entry/exit point between the team and the governance layer, and the MANAGER reaches any team-internal agent **only via the COS**. The COS never relays the in-team dialog loops described below.

---

## Workflow Overview

Two layers, one boundary. The **governance layer** (USER → MANAGER) sets direction; the **team layer** (COS + ORCH + ARCH + INT + MEMBER) does the work. The COS is the SOLE bridge across the boundary — everything between MANAGER and a team-internal agent transits the COS. Inside the team, ORCH ↔ ARCH / MEMBER / INT are **direct** edges.

```
GOVERNANCE LAYER
  USER  <--->  AMAMA (Manager)
                  |  (1) creates project, sends requirements
                  |  (3) team-ready notice, (9) approved design,
                  |  completion reports  ── all transit the COS ──
                  v
================  TEAM BOUNDARY (guarded by COS)  ================
                  |
  AMCOS (Chief of Staff) [TEAM-SCOPED]  -- sole entry/exit point
   (2) MANAGER-created (COS + 5 base: COS+ARCH+ORCH+INT+MEMBER, R29.1); COS completes/customizes under mandate + guards boundary
                  |
   +--- direct team-layer edges (NOT routed through COS) ---+
   |                                                        |
   v                                                        v
  AMAA (Architect) <===========> AMOA (Orchestrator) <===> AMIA (Integrator)
   (7) design doc                  (10) splits design          (validates merged
   (15) design-change              into TRDDs, owns the         PR vs the TRDD,
        dialog with ORCH           in-team coordination         (Z) flips column
                  ^                       |                      -> completed)
                  |                       |  three ORCH-owned in-team dialog loops
                  |          +------------+------------------------------+
                  |          | (A) comprehension handshake  (before code)|
                  |          | (B) in-dev blocker dialog    (during code)|
                  |          | (C) pre-PR "done?" gate       (before PR) |
                  |          +------------+------------------------------+
                  |                       v
                  +-------------------- MEMBER agents (implementers)
                                          code -> (C cleared) -> open PR
                                                            |
                                                            v
                                          AMIA reviews & merges the PR,
                                          then flips the column to completed.
```

**Reading the loops (all ORCHESTRATOR-owned, never the COS):**

- **(A) Task-comprehension handshake** — before a MEMBER writes any code, ORCH and the MEMBER confirm the MEMBER understands the TRDD, acceptance criteria, and dependencies. ORCH↔MEMBER, direct.
- **(B) In-dev issue dialog** — on any blocker, ambiguity, or improvement idea found mid-implementation, the MEMBER raises it to ORCH; ORCH unblocks, clarifies, or (if it is a design issue) opens the design-change dialog with ARCH. MEMBER⇄ORCH (and ORCH⇄ARCH), direct.
- **(C) Pre-PR gate** — the MEMBER clears a "done?" check with ORCH BEFORE opening a PR or notifying the INTEGRATOR. Only after ORCH agrees the work satisfies the TRDD does the MEMBER open the PR. MEMBER⇄ORCH, direct.

The COS does **not** relay (A), (B), or (C). It guards the boundary: it forwards proposals/escalations UP to MANAGER and relays MANAGER verdicts DOWN to the team.

---

## Team Scope and Cross-Team Operations

> **Runtime governance**: These rules are a local reference. The authoritative source is the `team-governance` skill, consulted at runtime. Plugins MUST NOT hardcode governance rules, permission matrices, or role restrictions.

AMCOS operates strictly within **one team boundary**:

| Operation | Scope | Mechanism |
|-----------|-------|-----------|
| Create/remove agents | Own team only | Direct AMP messages |
| Reassign agents within team | Own team only | Direct AMP messages |
| Request agents from another team | Cross-team | GovernanceRequest to target AMCOS |
| Offer agents to another team | Cross-team | GovernanceRequest to requesting AMCOS |
| Query another team's status | Cross-team | GovernanceRequest via AMAMA |

All cross-team GovernanceRequests must be approved by both teams' managers (AMAMA).

---

## Kanban — the canonical TRDD `column:` pipeline

> **Runtime source of truth.** The authoritative task lifecycle is the TRDD
> v2 `column:` state machine (see `~/.claude/rules/trdd-design-tasks.md` and
> the universal `prrd-trdd-kanban` skill in `ai-maestro-plugin`). The
> per-team `amcos-prrd-trdd-kanban` skill defers to that universal skill. Do
> NOT hardcode a different column set in any plugin.

Each task is a TRDD whose `column:` field advances through the pipeline below. The COS owns **no** column directly — column ownership lives with the team-layer agents, and the COS only routes the proposals/escalations that authorize transitions.

### Canonical columns (TRDD `column:` field)

| Group | Column | A task lives here when… | Who advances it |
|-------|--------|-------------------------|-----------------|
| ENTRY | `backburner` | proto-TRDD parking lot | MANAGER (promotes) |
| | `todo` | promoted, awaiting design | ORCHESTRATOR |
| DESIGN | `design` | ARCHITECT shapes proto → full TRDD (may 1→N split / N→1 group) | ARCHITECT |
| | `dispatch` | full TRDD designed, awaiting assignment | ORCHESTRATOR |
| WORK | `dev` | MEMBER implementing (new code OR fixes) — after the (A) handshake | MEMBER (assignee) |
| | `testing` | tests + audits running; failures bounce back to `dev` | test runner / MEMBER |
| | `ai_review` | code review by AI agents | AI reviewer / INTEGRATOR |
| | `human_review` | human eyes required (`review-requirements:` includes human-review) | reviewer; verdict relayed via COS→MANAGER→USER |
| READY | `complete` | TRDD satisfied + merged; INTEGRATOR has validated the PR | **INTEGRATOR (owns the flip)** |
| SHIP (tools) | `publish` → `published` | publishing a Claude Code plugin / package | INTEGRATOR (via RELEASER) |
| SHIP (services) | `deploy` → `live` | deploying a service | INTEGRATOR (via DEPLOYER) |
| OPERATE | `live_auditing` | post-deploy soak window | INTEGRATOR |
| EXCEPTIONS | `blocked` | `blocked-by:` non-empty; restores to `pre-block-column:` when cleared | owner |
| | `failed` / `superseded` | terminal: abandoned w/ post-mortem, or replaced | MANAGER / ARCHITECT |

**Who flips to `complete` (critical).** Nobody self-marks a task completed. The **INTEGRATOR (AMIA)** owns the column→`complete` flip: it validates that the merged PR actually satisfies the TRDD (acceptance criteria, tests, design) and only then advances the column. The ORCHESTRATOR does **not** own the final flip — ORCH owns the in-team coordination and the three dialog loops, INT owns completion.

### GitHub-Projects board (the ratified 14-stage pipeline — no projection)

The team board **mirrors the 14-stage TRDD v2 pipeline above 1:1**, plus the `blocked`/`failed`/`superseded` exception lanes — there is **no projection**. An earlier 8-column model (v2.20.0) was **superseded** by the MANAGER's ai-maestro#2 decision (a) (COS#11): a 14→8 collapse hid the human gate and the publish/deploy tails, so the board carries every TRDD `column:` as its own lane. The two governance review gates (`ai_review`, `human_review`) stay DISTINCT and `blocked` stays first-class by construction. COS sets this column schema once at team creation (via the deployed `kanban-config` verb; the per-team column **backend** is gated on ai-maestro#2); the canonical column set is the single source of truth in the `amcos-prrd-trdd-kanban` skill.

The board lanes are exactly the TRDD `column:` values, in lifecycle order:

`backburner · todo · design · dispatch · dev · testing · ai_review · human_review · complete · publish · published · deploy · live · live_auditing` + exceptions `blocked · failed · superseded`

A TRDD's frontmatter `column:` IS its board lane (no mapping table); the publish/deploy tails follow each TRDD's `release-via:`, and INT validates acceptance before the `complete` flip. `blocked` is a first-class lane: a blocked task returns to its `pre-block-column:` when unblocked. The operational `status:*` GitHub-issue labels AMCOS sets (in `amcos-label-taxonomy`) are a **separate, coarser** layer — not 1:1 with these lanes; expanding the label set to match is a separate MANAGER decision.

---

## Detailed Procedure Steps

### Phase 1: Project Creation and Team Setup

#### Step 1: Manager Creates Project
**Actor**: AMAMA (Manager)
**Action**:
- Create a new project in a new GitHub repository (or in an existing repository)
- Send the requirements to the Chief of Staff (AMCOS) via AMP

**Communication**:
- GitHub: Create repository, create initial issue with requirements
- AMP: Message to AMCOS with project details and requirements

#### Step 2: Chief of Staff Evaluates Project
**Actor**: AMCOS (Chief of Staff)
**Action**:
- Evaluate the project requirements
- Analyze complexity, technologies involved, timeline
- Suggest an optimal team of agents (from own team roster) to the Manager
- If specialized agents are needed from other teams: prepare GovernanceRequest

**Communication**:
- AMP: Send team proposal to AMAMA with justification

#### Step 3: Team Discussion and Approval
**Actor**: AMAMA (Manager) + AMCOS (Chief of Staff)
**Action**:
- Manager discusses the team proposal with Chief of Staff
- Negotiate team composition if needed
- Manager ultimately approves a team proposal
- If cross-team agents needed: AMAMA initiates GovernanceRequests

**Communication**:
- AMP: Back-and-forth messages until agreement

#### Step 4: Team Creation + Completion
**Actor**: the **MANAGER** creates the team (+ the COS + the 5 base members — R29.1); then **AMCOS** (Chief of Staff) completes & customizes it under the MANAGER's mandate (R30). While any of the 5 base members is missing the team is **FROZEN** — only the COS is active, the rest hibernated, until the base is complete (R31).
**Action (COS, under mandate)**:
- Complete the 5-member base the MANAGER created (add/configure any missing ARCH/ORCH/INT/MEMBER)
- Add extra MEMBER-titled agents tailored to the project (on the member-agent role-plugin)
- OR reassign agents from other projects within the same team
- Configure each agent with appropriate `ai-maestro-*` skills and plugins for their role
- (Team `create`/`delete` itself is MANAGER-only — R29.1; the COS never creates/deletes the team)

**Communication**:
- AMP: Coordination messages during agent creation
- AMP: Onboarding messages to each new agent

#### Step 5: Team Ready Notification
**Actor**: AMCOS (Chief of Staff)
**Action**:
- Notify the Manager that the team is set up and ready to follow instructions
- Provide team roster with agent names and roles

**Communication**:
- AMP: Team ready notification to AMAMA

---

### Phase 2: Design and Planning

#### Step 6: Requirements to Architect
**Actor**: AMAMA (Manager)
**Action**:
- Send the requirements to the Architect agent (AMAA) via AMP
- Expand the requirements with more details
- Include the list of team member names in the requirements
- Assign to the Architect the task of developing the design document

**Communication**:
- GitHub: Create issue with requirements, assign label for AMAA
- AMP: Message to AMAA with full requirements and team roster

#### Step 7: Design Document Creation
**Actor**: AMAA (Architect)
**Action**:
- Receive the task (on the kanban) to convert requirements into a full design document
- Create design document with:
  - System architecture
  - Module specifications
  - Detailed technical specs
  - Interface definitions
  - Data models

**Communication**:
- GitHub: Update issue with progress
- AMP: Progress updates to AMAMA

#### Step 8: Design Submission
**Actor**: AMAA (Architect)
**Action**:
- Send the completed design document back to the Manager

**Communication**:
- GitHub: Attach design document to issue, mark ready for review
- AMP: Notification to AMAMA that design is ready

#### Step 9: Design Approval
**Actor**: AMAMA (Manager) + USER
**Action**:
- Manager examines the design document
- Manager asks for approval from the User
- If User approves: design is sent to the Orchestrator
- If User rejects: design goes back to Architect with feedback

**Communication**:
- GitHub: Issue comments with design and approval status
- AMP: Message to AMOA with approved design

---

### Phase 3: Task Planning and Assignment

#### Step 10: Design Decomposition
**Actor**: AMOA (Orchestrator)
**Action**:
- Split the design into actionable small steps
- Split each step into actionable tasks
- Tailor tasks for the current team members and their capabilities

#### Step 11: Task Requirements Documents
**Actor**: AMOA (Orchestrator)
**Action**:
- Produce the task-requirements-document for each agent
- Include in each document:
  - Task description
  - Acceptance criteria
  - Related design sections
  - Dependencies
  - Expected deliverables

#### Step 12: Task Plan Creation
**Actor**: AMOA (Orchestrator)
**Action**:
- Create a plan where task-requirements-documents are ordered and parallelized
- Ensure tasks can be assigned to the right agent at the right time
- Define task dependencies
- Identify tasks that can run in parallel

#### Step 13: Kanban Population
**Actor**: AMOA (Orchestrator)
**Action**:
- Add tasks to the GitHub Project kanban `pending` column
- For each task:
  - Set the "Assigned Agent" custom field
  - Attach the task-requirements-document
  - Specify task order and dependencies
  - Ensure task executes only when required previous tasks are completed

**Communication**:
- GitHub: Create issues, add to project, set fields
- AMP: Notification to each agent about their first assigned task

#### Step 14: Task-Comprehension Handshake — Loop (A)
**Actor**: AMOA (Orchestrator) ⇄ MEMBER agents (direct, NOT via COS)
**Action**:
- This is the FIRST of the three ORCHESTRATOR-owned in-team dialog loops, and it gates the start of coding.
- Send each MEMBER a notification via AMP that their first task (TRDD) has been assigned.
- The MEMBER reads the TRDD and confirms back to ORCH that they understand the task, the acceptance criteria, the related design sections, and the dependencies.
- ORCH answers clarification questions directly. A MEMBER does NOT begin coding until ORCH confirms the comprehension handshake is complete.
- The Orchestrator is the team lead with full project understanding (along with the Architect). The COS does NOT participate in or relay this loop.

**Communication**:
- AMP: Task assignment + comprehension confirmation, ORCH⇄MEMBER directly

#### Step 15: In-Dev Issue Dialog — Loop (B) (design-change branch)
**Actor**: MEMBER agents ⇄ AMOA ⇄ AMAA (all direct team-layer edges, NOT via COS)
**Action**:
- This is the design-affecting branch of the SECOND ORCHESTRATOR-owned loop (the in-dev issue dialog). It can fire at any point during implementation.
- If a MEMBER hits a problem or surfaces an improvement idea mid-implementation, they raise it to ORCH (loop (B)). ORCH evaluates:
  - If ORCH can unblock or clarify in-team, it does so directly (this stays inside loop (B); see Step 17).
  - If the issue requires a design change: ORCH ⇄ ARCH directly — ORCH sends a design-change-request to the Architect, the Architect produces a new design version and returns it to ORCH.
- The COS does NOT relay any of these edges; ORCH↔MEMBER and ORCH↔ARCH are direct.

**Communication**:
- AMP: MEMBER raises blocker/idea to AMOA (direct)
- AMP: Design-change request AMOA → AMAA (direct)
- AMP: Updated design AMAA → AMOA (direct)

#### Step 16: Task Updates from Design Changes
**Actor**: AMOA (Orchestrator)
**Action**:
- Evaluate the new version of the design document
- If approved:
  - Update all task-requirements-documents affected by changes
  - Update the attachments in project kanban tasks
  - Send updated documents to assigned agents
  - Explain the changes and motivations

**Communication**:
- GitHub: Update issue attachments
- AMP: Change notifications to affected agents

---

### Phase 4: Implementation

#### Step 17: Task Execution (with in-dev unblock — Loop (B))
**Actor**: MEMBER agents ⇄ AMOA (direct)
**Action**:
- After the (A) handshake clears, the MEMBER starts working on the assigned TRDD and reports "in development" to the Orchestrator. ORCH advances the TRDD `column:` to `dev`.
- Loop (B) stays open for the whole `dev` phase: on any blocker, ambiguity, or risk, the MEMBER raises it to ORCH, who unblocks in-team (reassign, clarify, provide a missing dependency) or escalates the design branch to ARCH (Step 15). A non-design blocker is resolved entirely inside loop (B).
- The COS is not in this loop.

**Communication**:
- AMP: Status + blocker dialog, MEMBER⇄AMOA directly

#### Step 18: Kanban Status Update
**Actor**: AMOA (Orchestrator)
**Action**:
- Advance the TRDD `column:` from `dispatch` to `dev` (board projection: Pending → In Progress).
- As tests run, the column moves `dev → testing → ai_review` per the canonical pipeline (still projected to the In Progress board column).

**Communication**:
- GitHub: Update project item status / TRDD `column:`

#### Step 19: Pre-PR "Done?" Gate — Loop (C)
**Actor**: MEMBER agents ⇄ AMOA (direct, NOT via COS)
**Action**:
- This is the THIRD ORCHESTRATOR-owned loop and it gates PR creation.
- When a MEMBER believes a task is finished, they do NOT open a PR or notify the INTEGRATOR yet. They first clear a "done?" check with ORCH: ORCH reviews against the TRDD acceptance criteria and asks whatever questions are needed to confirm the work is genuinely complete.
- ONLY after ORCH agrees the work satisfies the TRDD does the MEMBER open the PR (and the INTEGRATOR is brought in at Step 20).
- The COS does NOT relay this gate. ORCH does NOT flip the column to `complete` here — that is the INTEGRATOR's job after PR validation (Step 23).

**Communication**:
- AMP: "done?" dialog, MEMBER⇄AMOA directly
- GitHub: PR created only after ORCH clears the gate

---

### Phase 5: Integration and Review

#### Step 20: PR Review Request
**Actor**: AMOA (Orchestrator) → AMIA (Integrator) (direct)
**Action**:
- Reached ONLY after the MEMBER has cleared the (C) pre-PR gate (Step 19) and opened the PR.
- ORCH sends an AMP message to the Integrator (AMIA) to review the PR(s) of the cleared tasks and merge if they pass all checks. (A MEMBER may also notify the INTEGRATOR directly once the gate is cleared; either path is a direct team-layer edge.)

**Communication**:
- AMP: PR review request to AMIA (direct)
- GitHub: PR ready for review

#### Step 21: PR Evaluation and Merge
**Actor**: AMIA (Integrator)
**Action**:
- Examine the PR of each task; verify it satisfies the TRDD and design requirements.
- Run the project's tests, linting, and any required checks.
- If everything passes: merge to the target branch.
- If not: refuse the PR and report the specific issues to ORCH (which routes them into loop (B), Step 22).

**Communication**:
- GitHub: PR review comments, approval/rejection, merge
- AMP: Report to AMOA with pass/fail details

#### Step 22: Handling Failed PRs (back into Loop (B))
**Actor**: AMIA → AMOA → MEMBER agents (direct)
**Action**:
- ORCH evaluates the Integrator's report and communicates the issues to the MEMBER, re-opening loop (B).
- ORCH provides an extended/improved TRDD if needed and moves the task `column:` back to `dev` (board: Review → In Progress).
- ORCH asks the MEMBER if anything is needed; the MEMBER resumes work, and on completion re-clears the (C) gate before the next PR.

**Communication**:
- AMP: Feedback and instructions, AMIA→AMOA→MEMBER (direct)
- GitHub: Update task `column:` / status

---

### Phase 6: Completion, Release, and Continuation

#### Step 23: Completion Flip and Release (INTEGRATOR-owned)
**Actor**: AMIA (Integrator) owns the flip; AMOA continues coordination
**Action**:
- **The INTEGRATOR owns the column → `complete` flip.** After merging, AMIA validates that the merged PR actually satisfies the TRDD (acceptance criteria, tests, design). Only then does AMIA flip the TRDD `column:` to `complete`. **Nobody self-marks completed, and the ORCHESTRATOR does NOT own this flip.**
- If the TRDD requires `human_review` first, the verdict is escalated COS→MANAGER→USER and relayed back before the flip.
- **Release is PROJECT-TYPE-SPECIFIC and designed by the INTEGRATOR per project.** There is no single universal publish step. The INTEGRATOR designs the right pipeline for the project type:

  | Project type | Release pipeline (designed by INTEGRATOR) | Terminal columns |
  |--------------|-------------------------------------------|------------------|
  | Library / package | build → publish to the language registry (npm, PyPI, crates.io, …) | `publish` → `published` |
  | Application | build → code-sign / notarize → package → release (app store, installer, GitHub release) | `publish` → `published` |
  | Service | containerize → deploy to the target environment → soak | `deploy` → `live` → `live_auditing` |
  | Claude Code plugin | CPV `publish.py` to the marketplace — **a recommendation for plugins only**, not a universal default | `publish` → `published` |

  Entering the release pipeline (publish/deploy to production) is NON-EXEMPT: the INTEGRATOR routes the request UP via the COS to the MANAGER for approval before shipping.
- After completion, ORCH reports up via the COS to the MANAGER and assigns the next task to the MEMBER who finished. Keep MEMBER agents working, never idle.

**Communication**:
- GitHub: INTEGRATOR flips `column:` to `complete`; release per project type
- AMP: Completion report ORCH → COS → AMAMA
- AMP: New task assignment ORCH → MEMBER (direct)

#### Step 24: Iteration
**Action**:
- This cycle iterates until all tasks are complete
- Each successful merge triggers:
  - Report to Manager
  - New task assignment to available agent

---

## Communication Matrix

> **Runtime governance**: These communication rules are a local reference. The authoritative source is the `team-governance` skill, consulted at runtime. Plugins MUST NOT hardcode governance rules, permission matrices, or role restrictions.

All messaging uses the **AMP (Agent Messaging Protocol)**. Per R6 v3, every edge that crosses the team boundary transits the COS; team-internal edges are direct.

| From | To | Channel | Edge type | Purpose |
|------|-----|---------|-----------|---------|
| AMAMA | AMCOS | AMP | boundary | Requirements, team requests |
| AMCOS | AMAMA | AMP | boundary | Team proposals, escalations, status |
| AMCOS | Other AMCOS | AMP + GovernanceRequest | cross-team | Cross-team agent transfers |
| AMAMA | AMAA / AMOA / AMIA / MEMBER | AMP **via AMCOS** | boundary | All MANAGER↔team-internal contact transits the COS |
| AMOA | MEMBER agents | AMP | **direct** | Task assignment + the (A) handshake, (B) blocker dialog, (C) pre-PR gate |
| MEMBER agents | AMOA | AMP | **direct** | Comprehension confirmation, blockers, "done?" |
| AMOA | AMAA | AMP | **direct** | Design-change requests (loop B branch) |
| AMAA | AMOA | AMP | **direct** | Design documents / updated designs |
| AMOA | AMIA | AMP | **direct** | PR review requests |
| AMIA | AMOA | AMP | **direct** | PR review results, completion notice |
| AMOA | AMCOS → AMAMA | AMP | boundary | Completion reports / escalations (via COS) |

The COS never relays the in-team (A)/(B)/(C) dialog loops — those are direct ORCH⇄team edges. The COS guards the boundary: it forwards proposals/escalations up and relays MANAGER verdicts down.

---

## Role Boundaries Summary

> **Runtime governance**: These role boundaries are a local reference. The authoritative source is the `team-governance` skill, consulted at runtime. Plugins MUST NOT hardcode governance rules, permission matrices, or role restrictions.

| Role | Creates | Manages | Cannot Do |
|------|---------|---------|-----------|
| **AMAMA** | Projects | Approvals, user communication; reaches team-internal agents only via the COS | Task assignment; direct team-internal messaging (must transit COS) |
| **AMCOS** | Agents, teams (own team only) | Agent lifecycle within team; guards the team boundary | Task assignment, projects, cross-team ops without GovernanceRequest; relaying the in-team (A)/(B)/(C) loops |
| **AMAA** | Designs | Architecture; design-change dialog with ORCH (direct) | Task assignment; the completed flip |
| **AMOA** | TRDDs, plans | In-team coordination, the three dialog loops, kanban transitions up to `dev` re-bounces | Agent creation, projects; **flipping a task to `complete` (INTEGRATOR owns it)** |
| **AMIA** | Project-type-specific release pipelines | PR review + merge; **owns the column → `complete` flip**; release/deploy | Task assignment |
| **MEMBER** | Code, PRs | Their assigned TRDDs; must clear (A) before coding and (C) before a PR | Self-marking a task complete; everything else |

---

## GitHub Integration Points

| Step | GitHub Action | Actor |
|------|---------------|-------|
| 1 | Create repository | AMAMA |
| 6 | Create requirements issue | AMAMA |
| 7 | Update issue with progress | AMAA |
| 8 | Attach design document | AMAA |
| 13 | Create task issues / TRDDs, add to project | AMOA |
| 13 | Set "Assigned Agent" field | AMOA |
| 18 | Advance `column:` `dispatch`→`dev` (board: In Progress) | AMOA |
| 19 | Create PR (only after the (C) gate clears) | MEMBER |
| 21 | Review and merge/reject PR | AMIA |
| 23 | Flip `column:` to `complete` (board: Completed) | **AMIA** |
| 23 | Release per project type (publish/deploy) | **AMIA** |

---

## Document References

- **Requirements Document**: Created by AMAMA, sent to AMAA
- **Design Document**: Created by AMAA, approved by AMAMA/User
- **Task-Requirements-Document (TRDD)**: Created by AMOA for each task; its `column:` field is the canonical task lifecycle
- **Design-Change-Request**: Created by AMOA (direct to AMAA) when a MEMBER surfaces a design issue during loop (B)

