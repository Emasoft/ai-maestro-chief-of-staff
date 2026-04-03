---
name: amcos-agent-replacement-ref
description: Use when consulting detailed agent replacement references. Trigger with agent replacement lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Agent Replacement Reference

## Overview

Reference material for agent replacement. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-agent-replacement` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-agent-replacement` for error handling.

## Examples

```bash
# Look up the 6-phase replacement workflow
cat references/agent-replacement-protocol.md | grep -A2 "Phase"
```

Expected: phases from failure confirmation through cleanup and closure.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the replacement topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [agent-replacement-protocol](references/agent-replacement-protocol.md) — Topics: Agent Replacement Protocol, Table of Contents, 4.1 When to Use This Document, 4.2 Overview of the Replacement Protocol, 4.3 Phase 1: Failure Confirmation and Artifact Preservation, 4.3.1 Confirming Agent Cannot Be Recovered, Recovery Exhaustion Confirmation, Recovery Attempts, Terminal Failure Evidence, 4.3.2 Identifying Recoverable Artifacts, 4.3.3 Preserving Git Commits and Logs, Attempt to get git status from failed agent's directory, 4.4 Phase 2: Manager Notification and Approval, 4.4.1 Composing the Replacement Request, 4.4.2 Required Information for Approval, 4.4.3 Handling Approval Response, 4.4.4 Handling Rejection Response, 4.5 Phase 3: Creating the Replacement Agent, 4.5.1 Selecting the Host for the New Agent, 4.5.2 Creating a New Local Folder, 4.5.3 Cloning the Git Repository, 4.5.4 Starting the New Claude Code Session, 4.5.5 Registering with AI Maestro, 4.6 Phase 4: Orchestrator Notification, 4.6.1 Notifying Orchestrator About Replacement, 4.6.2 Requesting Handoff Document Generation, 4.6.3 Requesting GitHub Project Update, 4.7 Phase 5: Work Handoff to New Agent, 4.7.1 Sending Handoff Documentation, 4.7.2 Sending Task Assignments, 4.7.3 Awaiting Acknowledgment, 4.7.4 Verifying New Agent Understanding, 4.8 Phase 6: Cleanup and Closure, 4.8.1 Updating Incident Log, 4.8.2 Notifying Manager of Completion, 4.8.3 Archiving Old Agent Records, Archive old agent configuration, Keep incident log intact (do not archive), 4.9 Complete Replacement Workflow Checklist, Agent Replacement Checklist, Phase 1: Failure Confirmation, Phase 2: Manager Approval, Phase 3: Create Agent, Phase 4: Orchestrator Notification, Phase 5: Work Handoff, Phase 6: Cleanup, Troubleshooting, New agent does not register with AI Maestro, Orchestrator does not respond to handoff request, New agent does not understand handoff documentation, Git clone fails due to authentication
