---
name: amcos-label-taxonomy-ref
description: Use when consulting detailed label taxonomy references. Trigger with label taxonomy lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Label Taxonomy Reference

## Overview

Reference material for label taxonomy. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-label-taxonomy` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-label-taxonomy` for error handling.

## Examples

```bash
# Look up label commands for agent assignment
cat references/label-commands-and-examples.md | grep -A3 "assign"
```

Expected: gh CLI commands for applying assignment labels to issues.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the label taxonomy topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [label-commands-and-examples](references/label-commands-and-examples.md) — Topics: Label Commands and Examples, Table of Contents, AMCOS Label Commands, When Agent Spawned, Assign new agent to issue, When Agent Terminated, Clear assignment from all agent's issues, When Agent Blocked, Mark issue blocked, When Escalating to Human, Reassign to human, Agent Registry and Labels, Query agent info from registry via REST API, Returns: {"session_name": "code-impl-01", "status": "active", "current_issues": [42, 43]}, Sync Check, Find issues assigned to agent from GitHub labels, Compare with registry (via REST API), Should match, Example 1: Spawning Agent and Assigning to Issue, Step 1: Add assignment label, Step 2: Update status from backlog to ready, Step 3: Update team registry via REST API, Step 4: Verify, Output: assign:implementer-1, status:todo, Example 2: Terminating Agent and Clearing Assignments, Step 1: Find all issues assigned to agent, Step 2: Remove assignment and update status, Step 3: Remove agent from team registry via REST API, Step 4: Verify no issues remain assigned, Output: (empty), Example 3: Handling Blocked Agent, Step 1: Update status to blocked, Step 2: Add comment explaining blocker, Step 3: Escalate to human if needed, Step 4: Verify, Output: assign:human, status:blocked, priority:high
