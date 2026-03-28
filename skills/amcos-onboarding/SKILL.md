---
name: amcos-onboarding
description: Use when onboarding new agents to the team, providing role briefings, conducting project handoffs, bootstrapping a new project pipeline (Architect → Orchestrator → team), and ensuring agents are ready to contribute effectively. Trigger with new agent, new project setup, or project bootstrap.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro messaging API access, project documentation access, and role definition documents. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff Onboarding Skill

## Overview

Agent onboarding integrates new AI agents into a coordinated team. The Chief of Staff ensures each new agent understands their role, project context, key procedures, and communication channels.

## Prerequisites

1. Agent to be onboarded is created and running
2. Project documentation is available
3. Team registry is accessible

## Instructions

1. Identify what needs onboarding (agent or project)
2. Gather required context and documentation
3. Send onboarding materials to target
4. Verify understanding and readiness

### Checklist

Copy this checklist and track your progress:

- [ ] Agent session is active and responsive
- [ ] Role briefing delivered with responsibilities and reporting chain
- [ ] Project context and conventions shared
- [ ] Agent confirmed understanding of assigned tasks
- [ ] (Project bootstrap) Team/project config verified via `amp-project-info.sh`
- [ ] (Project bootstrap) Architect created via `aimaestro-agent.sh` and given requirements via `amp-send.sh`
- [ ] (Project bootstrap) Orchestrator created via `aimaestro-agent.sh` and given design doc via `amp-send.sh`
- [ ] (Project bootstrap) All requested agents created and onboarded
- [ ] (Project bootstrap) MANAGER notified "Team of N agents ready" via `amp-send.sh`

## Output

| Onboarding Type | Output |
|-----------------|--------|
| New agent | Agent understands role and context |
| New project | Project registered, team assigned |
| Role change | Agent updated with new responsibilities |
| Project bootstrap | Full pipeline created (Architect → Orchestrator → team), MANAGER notified |

## Core Procedures

### PROCEDURE 1: Execute Onboarding Checklist

**When/Steps:** Initiate session, verify identity, work through checklist items, confirm completion, document.

See `references/onboarding-checklist.md` and `references/op-execute-onboarding-checklist.md`.

### PROCEDURE 2: Deliver Role Briefing

**When/Steps:** Retrieve role definition, explain responsibilities, clarify reporting, set expectations, confirm understanding.

See `references/role-briefing.md` and `references/op-deliver-role-briefing.md`.

### PROCEDURE 3: Conduct Project Handoff

**When/Steps:** Provide project overview, share current state, explain conventions, transfer knowledge, verify comprehension.

See `references/project-handoff.md` and `references/op-conduct-project-handoff.md`.

### Validate Handoff Document

Validate handoff documents before sending using the validation checklist and scripts.

See `references/op-validate-handoff.md`.

## Examples

**Input:** "Onboard new agent libs-svg-renderer for SVG rendering tasks on project svg-player"

**Output:**
```
Onboarding libs-svg-renderer:
1. Role briefing sent: SVG renderer, reports to apps-svgplayer-development
2. Project handoff: svg-player repo, conventions, current sprint context
3. Agent confirmed ready. Registry updated.
[DONE] libs-svg-renderer onboarded successfully.
```

See `references/onboarding-overview-and-examples.md` for full examples.

### PROCEDURE 4: Project Bootstrap Pipeline

**When:** MANAGER assigns a new project to the team, or a new team is created for a project. The COS bootstraps the full agent pipeline from scratch.

**Scripts Used:**
- `amp-project-info.sh` — Verify team/project configuration before proceeding
- `aimaestro-agent.sh create <name>` — Create agents (Architect, Orchestrator, team members)
- `amp-send.sh <agent> <subject> <message>` — Deliver requirements, design docs, and task assignments

**Steps:**

1. **Verify project config:**
   ```bash
   amp-project-info.sh --team <team-id>
   ```
   Confirm the team exists, the project is registered, and the MANAGER has provided requirements.

2. **Create the Architect agent** (if not already auto-created by the team setup):
   ```bash
   aimaestro-agent.sh create <architect-name> -d <project-dir> -t "Architecture design for <project>"
   ```
   Assign the `ai-maestro-architect-agent` role-plugin and the MEMBER title.
   Ensure the agent folder has proper multi-repo structure: `~/agents/<architect-name>/repos/`, `~/agents/<architect-name>/reports/`, etc.
   Clone project repos via `amp-clone-repo.sh <url>` into `~/agents/<architect-name>/repos/<repo-name>/`.

3. **Send project requirements to the Architect:**
   ```bash
   amp-send.sh <architect-agent> "Project Requirements" "Here are the requirements from MANAGER: <requirements summary>. Please produce a design document. Target repo: ~/agents/<architect-name>/repos/<repo-name>"
   ```

4. **Wait for the Architect's design document.** Monitor inbox for the Architect's reply containing the design doc or a path to it.

5. **Create the Orchestrator agent** (if not already auto-created by the team setup):
   ```bash
   aimaestro-agent.sh create <orchestrator-name> -d ~/agents/<orchestrator-name> -t "Task orchestration for <project>"
   ```
   Assign the `ai-maestro-orchestrator-agent` role-plugin and the **ORCHESTRATOR** title (governance v3).
   Create multi-repo folder structure and clone project repos into `~/agents/<orchestrator-name>/repos/`.

6. **Hand the Orchestrator the design document:**
   ```bash
   amp-send.sh <orchestrator-agent> "Design Document Ready" "Architect has completed the design. Document: <path-or-content>. Begin task breakdown and request agents as needed."
   ```

7. **Create remaining agents as the Orchestrator requests them.** The Orchestrator will send messages via `amp-send.sh` requesting specific agent roles. For each request:
   ```bash
   aimaestro-agent.sh create <agent-name> -d ~/agents/<agent-name> -t "<task description>"
   ```
   Create multi-repo folder structure (`repos/`, `reports/`, `tmp/`, `teams/`, `db/`) and clone project repos via `amp-clone-repo.sh`.
   Then onboard each new agent using PROCEDURE 1 (Execute Onboarding Checklist).

8. **Report to MANAGER when the team is ready:**
   ```bash
   amp-send.sh <manager-agent> "Team Ready" "Team of N agents assembled and onboarded for <project>. Architect, Orchestrator, and N-2 team members are active."
   ```

**Success criteria:** All agents created, onboarded, and confirmed ready. MANAGER notified.

## Error Handling

| Issue | Resolution |
|-------|------------|
| Agent does not respond | Verify session active, retry with higher priority, escalate if persistent |
| Agent confused by briefing | Provide specific examples, break down responsibilities, have agent repeat back |
| Handoff incomplete | Review checklist, identify gaps, send supplementary information |

## Resources

- `references/onboarding-checklist.md`
- `references/role-briefing.md`
- `references/project-handoff.md`
- `references/onboarding-overview-and-examples.md`
- `references/op-execute-onboarding-checklist.md`
- `references/op-deliver-role-briefing.md`
- `references/op-conduct-project-handoff.md`
- `references/op-validate-handoff.md`

