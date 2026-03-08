---
name: amcos-onboarding
description: Use when onboarding new agents to the team, providing role briefings, conducting project handoffs, and ensuring agents are ready to contribute effectively. Trigger with new agent or new project setup.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro messaging API access, project documentation access, and role definition documents. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-chief-of-staff-main-agent
workflow-instruction: "Step 4"
procedure: "proc-create-team"
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

## Output

| Onboarding Type | Output |
|-----------------|--------|
| New agent | Agent understands role and context |
| New project | Project registered, team assigned |
| Role change | Agent updated with new responsibilities |

## Core Procedures

### PROCEDURE 1: Execute Onboarding Checklist

**When/Steps:** Initiate session, verify identity, work through checklist items, confirm completion, document.

See [references/onboarding-checklist.md](references/onboarding-checklist.md) and [references/op-execute-onboarding-checklist.md](references/op-execute-onboarding-checklist.md).

### PROCEDURE 2: Deliver Role Briefing

**When/Steps:** Retrieve role definition, explain responsibilities, clarify reporting, set expectations, confirm understanding.

See [references/role-briefing.md](references/role-briefing.md) and [references/op-deliver-role-briefing.md](references/op-deliver-role-briefing.md).

### PROCEDURE 3: Conduct Project Handoff

**When/Steps:** Provide project overview, share current state, explain conventions, transfer knowledge, verify comprehension.

See [references/project-handoff.md](references/project-handoff.md) and [references/op-conduct-project-handoff.md](references/op-conduct-project-handoff.md).

### Validate Handoff Document

Validate handoff documents before sending using the validation checklist and scripts.

See [references/op-validate-handoff.md](references/op-validate-handoff.md).

## Examples

See [references/onboarding-overview-and-examples.md](references/onboarding-overview-and-examples.md) for full examples including onboarding initiation, role briefings, project handoffs, and validation checklists.
- What Is Agent Onboarding
- Onboarding Components
- Examples: Initiating Onboarding for New Developer
- Examples: Role Briefing Message
- Examples: Project Handoff Summary
- Handoff Validation Checklist
- Handoff Required Fields
- Key Takeaways
- Task Checklist

## Error Handling

| Issue | Resolution |
|-------|------------|
| Agent does not respond | Verify session active, retry with higher priority, escalate if persistent |
| Agent confused by briefing | Provide specific examples, break down responsibilities, have agent repeat back |
| Handoff incomplete | Review checklist, identify gaps, send supplementary information |

## Resources

- [Onboarding Checklist](references/onboarding-checklist.md)
- [Role Briefing](references/role-briefing.md)
- [Project Handoff](references/project-handoff.md)
- [Overview and Examples](references/onboarding-overview-and-examples.md)
- [Op: Execute Onboarding](references/op-execute-onboarding-checklist.md)
- [Op: Deliver Role Briefing](references/op-deliver-role-briefing.md)
- [Op: Conduct Project Handoff](references/op-conduct-project-handoff.md)
- [Op: Validate Handoff](references/op-validate-handoff.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
