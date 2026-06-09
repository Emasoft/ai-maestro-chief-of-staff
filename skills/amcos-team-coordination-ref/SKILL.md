---
name: amcos-team-coordination-ref
description: Use when consulting detailed team coordination references. Trigger with team coordination lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Team Coordination Reference

## Overview

Reference material for team coordination. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-team-coordination` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-team-coordination` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Assign the developer role to a new team member"

```bash
cat references/role-assignment.md | head -50
```

**Expected result:** Role definitions, capability matching, assignment procedure, confirmation protocol, and transition handling.

## Resources

- [teammate-awareness](references/teammate-awareness.md) — Team roster management, status polling, activity detection, inactive handling, examples
  - 3.1 [Managing The Team Roster](#31-managing-the-team-roster)
  - 3.2 [Polling Agent Status](#32-polling-agent-status)
  - 3.3 [Detecting Agent Activity](#33-detecting-agent-activity)
  - 3.4 [Handling Inactive Agents](#34-handling-inactive-agents)
  - 3.5 [Reporting Team Status](#35-reporting-team-status)
  - 3.6 [Teammate Awareness Examples](#36-teammate-awareness-examples)
  - 3.7 [Troubleshooting](#37-troubleshooting)
- [role-assignment](references/role-assignment.md) — Role definitions, matching, assignment procedure, confirmation, transitions, examples
  - 1.1 [What Are Agent Roles](#11-what-are-agent-roles)
  - 1.2 [Standard Role Definitions](#12-standard-role-definitions)
  - 1.3 [Matching Agents To Roles](#13-matching-agents-to-roles)
  - 1.4 [Role Assignment Procedure](#14-role-assignment-procedure)
  - 1.5 [Confirming Role Acceptance](#15-confirming-role-acceptance)
  - 1.6 [Managing Role Transitions](#16-managing-role-transitions)
  - 1.7 [Role Assignment Examples](#17-role-assignment-examples)
  - 1.8 [Troubleshooting](#18-troubleshooting)
