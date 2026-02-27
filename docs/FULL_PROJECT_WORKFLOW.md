# Full Project Workflow: From Requirements to Delivery

**Version**: 2.0.0
**Last Updated**: 2026-02-27

This document describes the complete workflow for how the AI Maestro agent system handles a project from initial requirements to delivery. AMCOS (AI Maestro Chief of Staff) is **team-scoped**: it manages agents within ONE team only. Cross-team operations require GovernanceRequests. All inter-agent messaging uses the AMP protocol.

---

## Workflow Overview

```
USER
  |
  v
EAMA (Manager) <--------------------------------------------+
  |                                                          |
  | 1. Creates project                                       |
  | 2. Sends requirements to AMCOS                           |
  v                                                          |
AMCOS (Chief of Staff) [TEAM-SCOPED]                         |
  |                                                          |
  | 3. Evaluates project, suggests team                      |
  | 4. Creates/assigns agents (within own team)              |
  | 5. Notifies EAMA: team ready                             |
  v                                                          |
EAMA ---->                                                   |
  |                                                          |
  | 6. Sends requirements to EAA                             |
  v                                                          |
EAA (Architect)                                              |
  |                                                          |
  | 7. Creates design document                               |
  | 8. Sends design to EAMA                                  |
  v                                                          |
EAMA <--- USER APPROVAL --->                                 |
  |                                                          |
  | 9. Sends approved design to EOA                          |
  v                                                          |
EOA (Orchestrator)                                           |
  |                                                          |
  | 10. Splits design into tasks                             |
  | 11. Creates task-requirements-documents                  |
  | 12. Adds tasks to kanban                                 |
  | 13. Assigns tasks to agents                              |
  v                                                          |
IMPLEMENTER AGENTS <------>                                  |
  |                                                          |
  | 14. Work on tasks                                        |
  | 15. Submit PRs                                           |
  v                                                          |
EIA (Integrator)                                             |
  |                                                          |
  | 16. Reviews PRs                                          |
  | 17. Merges or rejects                                    |
  v                                                          |
EOA <---->                                                   |
  |                                                          |
  | 18. Reports to EAMA                                      |
  | 19. Assigns next tasks                                   |
  +----------------------------------------------------------+
```

---

## Team Scope and Cross-Team Operations

AMCOS operates strictly within **one team boundary**:

| Operation | Scope | Mechanism |
|-----------|-------|-----------|
| Create/remove agents | Own team only | Direct AMP messages |
| Reassign agents within team | Own team only | Direct AMP messages |
| Request agents from another team | Cross-team | GovernanceRequest to target AMCOS |
| Offer agents to another team | Cross-team | GovernanceRequest to requesting AMCOS |
| Query another team's status | Cross-team | GovernanceRequest via EAMA |

All cross-team GovernanceRequests must be approved by both teams' managers (EAMA).

---

## Kanban Column System

All projects use an **8-column kanban system** on GitHub Projects. Every agent must understand these columns and use the canonical code format consistently.

### Canonical Columns

| # | Column | Code Format | Label | Description |
|---|--------|-------------|-------|-------------|
| 1 | Backlog | `backlog` | `status:backlog` | Entry point for all new issues |
| 2 | Todo | `todo` | `status:todo` | Ready to start, prioritized |
| 3 | In Progress | `in-progress` | `status:in-progress` | Active work by assigned agent |
| 4 | AI Review | `ai-review` | `status:ai-review` | Integrator (EIA) reviews the PR |
| 5 | Human Review | `human-review` | `status:human-review` | User reviews (big tasks only) |
| 6 | Merge/Release | `merge-release` | `status:merge-release` | Approved and ready to merge |
| 7 | Done | `done` | `status:done` | Completed and merged |
| 8 | Blocked | `blocked` | `status:blocked` | Blocked at any stage |

### Task Routing

- **Small tasks**: In Progress -> AI Review -> Merge/Release -> Done
- **Big tasks**: In Progress -> AI Review -> Human Review -> Merge/Release -> Done
- **Human Review** is requested via EAMA (Manager asks the user to test/review)
- **Blocked** can be set from any column; task returns to its previous column when unblocked

### Code Format Rules

- **Always use dashes**: `in-progress`, `ai-review`, `merge-release` (NOT underscores)
- **Labels use `status:` prefix**: `status:in-progress`, `status:ai-review`
- **Display names use title case**: "In Progress", "AI Review", "Merge/Release"

---

## Detailed Procedure Steps

### Phase 1: Project Creation and Team Setup

#### Step 1: Manager Creates Project
**Actor**: EAMA (Manager)
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
- AMP: Send team proposal to EAMA with justification

#### Step 3: Team Discussion and Approval
**Actor**: EAMA (Manager) + AMCOS (Chief of Staff)
**Action**:
- Manager discusses the team proposal with Chief of Staff
- Negotiate team composition if needed
- Manager ultimately approves a team proposal
- If cross-team agents needed: EAMA initiates GovernanceRequests

**Communication**:
- AMP: Back-and-forth messages until agreement

#### Step 4: Team Creation
**Actor**: AMCOS (Chief of Staff)
**Action**:
- Create the agents needed for the project team (within own team scope)
- OR reassign agents from other projects within the same team
- Configure each agent with appropriate `ai-maestro-*` skills and plugins for their role
- Assign agents to the project team

**Communication**:
- AMP: Coordination messages during agent creation
- AMP: Onboarding messages to each new agent

#### Step 5: Team Ready Notification
**Actor**: AMCOS (Chief of Staff)
**Action**:
- Notify the Manager that the team is set up and ready to follow instructions
- Provide team roster with agent names and roles

**Communication**:
- AMP: Team ready notification to EAMA

---

### Phase 2: Design and Planning

#### Step 6: Requirements to Architect
**Actor**: EAMA (Manager)
**Action**:
- Send the requirements to the Architect agent (EAA) via AMP
- Expand the requirements with more details
- Include the list of team member names in the requirements
- Assign to the Architect the task of developing the design document

**Communication**:
- GitHub: Create issue with requirements, assign label for EAA
- AMP: Message to EAA with full requirements and team roster

#### Step 7: Design Document Creation
**Actor**: EAA (Architect)
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
- AMP: Progress updates to EAMA

#### Step 8: Design Submission
**Actor**: EAA (Architect)
**Action**:
- Send the completed design document back to the Manager

**Communication**:
- GitHub: Attach design document to issue, mark ready for review
- AMP: Notification to EAMA that design is ready

#### Step 9: Design Approval
**Actor**: EAMA (Manager) + USER
**Action**:
- Manager examines the design document
- Manager asks for approval from the User
- If User approves: design is sent to the Orchestrator
- If User rejects: design goes back to Architect with feedback

**Communication**:
- GitHub: Issue comments with design and approval status
- AMP: Message to EOA with approved design

---

### Phase 3: Task Planning and Assignment

#### Step 10: Design Decomposition
**Actor**: EOA (Orchestrator)
**Action**:
- Split the design into actionable small steps
- Split each step into actionable tasks
- Tailor tasks for the current team members and their capabilities

#### Step 11: Task Requirements Documents
**Actor**: EOA (Orchestrator)
**Action**:
- Produce the task-requirements-document for each agent
- Include in each document:
  - Task description
  - Acceptance criteria
  - Related design sections
  - Dependencies
  - Expected deliverables

#### Step 12: Task Plan Creation
**Actor**: EOA (Orchestrator)
**Action**:
- Create a plan where task-requirements-documents are ordered and parallelized
- Ensure tasks can be assigned to the right agent at the right time
- Define task dependencies
- Identify tasks that can run in parallel

#### Step 13: Kanban Population
**Actor**: EOA (Orchestrator)
**Action**:
- Add tasks to the GitHub Project kanban `todo` column
- For each task:
  - Set the "Assigned Agent" custom field
  - Attach the task-requirements-document
  - Specify task order and dependencies
  - Ensure task executes only when required previous tasks are completed

**Communication**:
- GitHub: Create issues, add to project, set fields
- AMP: Notification to each agent about their first assigned task

#### Step 14: Agent Clarification
**Actor**: EOA (Orchestrator) + IMPLEMENTER AGENTS
**Action**:
- Send to each agent a notification via AMP that their first task has been assigned
- Ask each agent if they need clarifications
- The Orchestrator is the team lead with full project understanding (along with Architect)

**Communication**:
- AMP: Task assignment messages with clarification request

#### Step 15: Feedback and Design Updates (if needed)
**Actor**: IMPLEMENTER AGENTS -> EOA -> EAA
**Action**:
- If agents reply presenting problems or improvement suggestions:
  - Orchestrator evaluates the feedback
  - If feasible: Orchestrator sends design-change-request to Architect
  - Architect creates new version of design document
  - Architect sends updated design to Orchestrator

**Communication**:
- AMP: Feedback from agents to EOA
- AMP: Design change request from EOA to EAA
- AMP: Updated design from EAA to EOA

#### Step 16: Task Updates from Design Changes
**Actor**: EOA (Orchestrator)
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

#### Step 17: Task Execution
**Actor**: IMPLEMENTER AGENTS
**Action**:
- Start working on assigned tasks
- Report status of being "in development" to Orchestrator

**Communication**:
- AMP: Status update to EOA

#### Step 18: Kanban Status Update
**Actor**: EOA (Orchestrator)
**Action**:
- Move tasks on project kanban from `todo` column to `in-progress` column

**Communication**:
- GitHub: Update project item status

#### Step 19: Task Completion
**Actor**: IMPLEMENTER AGENTS -> EOA
**Action**:
- When an implementer agent finishes a task, notify the Orchestrator via AMP
- Orchestrator discusses and asks questions to ensure truly completed
- If OK: Orchestrator gives approval to do the pull-request
- Implementer creates PR

**Communication**:
- AMP: Completion notification from agent to EOA
- AMP: Approval to PR from EOA to agent
- GitHub: PR created

---

### Phase 5: Integration and Review

#### Step 20: PR Review Request
**Actor**: EOA (Orchestrator)
**Action**:
- Send AMP message to Integrator agent (EIA) to evaluate all PRs of completed tasks
- Request merge if they pass all checks

**Communication**:
- AMP: PR review request to EIA
- GitHub: PR ready for review

#### Step 21: PR Evaluation
**Actor**: EIA (Integrator)
**Action**:
- Examine the PR of each task
- Verify compliance with design requirements
- Run tests and linting
- If everything OK: merge to main
- If not OK: refuse PR, report issues to Orchestrator

**Communication**:
- GitHub: PR review comments, approval/rejection
- AMP: Report to EOA with pass/fail details

#### Step 22: Handling Failed PRs
**Actor**: EOA (Orchestrator) -> IMPLEMENTER AGENTS
**Action**:
- Evaluate Integrator report about each task PR
- Communicate to agents the issues and shortcomings
- Instruct agents to fix or improve the code
- Provide extended/improved task-requirements-document if needed
- Move task back to `in-progress` column
- Ask agent if they need anything to complete the task
- If OK: implementer agent resumes work on task

**Communication**:
- AMP: Feedback and instructions to agents
- GitHub: Update task status

---

### Phase 6: Completion and Continuation

#### Step 23: Successful PR Handling
**Actor**: EOA (Orchestrator)
**Action**:
- When Integrator reports successful PR merge, move task to `ai-review` column
  - If AI review passes for small tasks: move to `merge-release`, then `done`
  - If AI review passes for big tasks: move to `human-review` first, then `merge-release`, then `done`
  - Report to Manager (EAMA) for approval
  - If Manager approves: assign new task to the agent that finished
  - Keep implementer agents always working, never idle

**Communication**:
- GitHub: Update project item status through kanban columns
- AMP: Completion report to EAMA
- AMP: New task assignment to agent

#### Step 24: Iteration
**Action**:
- This cycle iterates until all tasks are complete
- Each successful merge triggers:
  - Report to Manager
  - New task assignment to available agent

---

## Communication Matrix

All messaging uses the **AMP (Agent Messaging Protocol)**.

| From | To | Channel | Purpose |
|------|-----|---------|---------|
| EAMA | AMCOS | AMP | Requirements, team requests |
| AMCOS | EAMA | AMP | Team proposals, status updates |
| AMCOS | Other AMCOS | AMP + GovernanceRequest | Cross-team agent transfers |
| EAMA | EAA | GitHub + AMP | Requirements, design requests |
| EAA | EAMA | GitHub + AMP | Design documents |
| EAMA | EOA | GitHub + AMP | Approved designs |
| EOA | Agents | GitHub + AMP | Task assignments |
| Agents | EOA | AMP | Status updates, questions |
| EOA | EAA | AMP | Design change requests |
| EOA | EIA | AMP | PR review requests |
| EIA | EOA | AMP | PR review results |
| EOA | EAMA | AMP | Completion reports |

---

## Role Boundaries Summary

| Role | Creates | Manages | Cannot Do |
|------|---------|---------|-----------|
| **EAMA** | Projects | Approvals, user communication | Task assignment |
| **AMCOS** | Agents, teams (own team only) | Agent lifecycle within team | Task assignment, projects, cross-team ops without GovernanceRequest |
| **EAA** | Designs | Architecture | Task assignment |
| **EOA** | Tasks, plans | Kanban, agent coordination | Agent creation, projects |
| **EIA** | Nothing | PR reviews, merges | Task assignment |
| **Agents** | Code, PRs | Their assigned tasks | Everything else |

---

## GitHub Integration Points

| Step | GitHub Action | Actor |
|------|---------------|-------|
| 1 | Create repository | EAMA |
| 6 | Create requirements issue | EAMA |
| 7 | Update issue with progress | EAA |
| 8 | Attach design document | EAA |
| 13 | Create task issues, add to project | EOA |
| 13 | Set "Assigned Agent" field | EOA |
| 18 | Move to "In Progress" column | EOA |
| 19 | Create PR | Agent |
| 21 | Review and merge/reject PR | EIA |
| 23 | Move to "Done" column | EOA |

---

## Document References

- **Requirements Document**: Created by EAMA, sent to EAA
- **Design Document**: Created by EAA, approved by EAMA/User
- **Task-Requirements-Document**: Created by EOA for each task
- **Design-Change-Request**: Created by EOA when agents suggest improvements
- **PR Review Report**: Created by EIA for each PR
- **GovernanceRequest**: Created by AMCOS for cross-team agent operations

---

**This workflow must be followed by all agents. Deviations require Manager approval.**
