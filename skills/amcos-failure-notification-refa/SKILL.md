---
name: amcos-failure-notification-refa
description: Use when consulting detailed failure notification references. Trigger with failure notification lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Failure Notification Reference

## Overview

Reference material for failure notification. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-failure-notification` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-failure-notification` for error handling.

## Examples

```bash
# Look up edge case protocol for AI Maestro unavailable
cat references/edge-case-protocols.md | grep -A5 "AI Maestro Unavailable"
```

Expected: detection methods and fallback communication steps.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the failure notification topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [edge-case-protocols](references/edge-case-protocols.md) — Edge case protocols for unavailable services, timeouts, approval failures
  - 1.0 AI Maestro Unavailable
    - 1.1 Detection Methods
    - 1.2 Response Workflow
    - 1.3 Fallback Communication
  - 2.0 GitHub Unavailable
    - 2.1 Detection Methods
    - 2.2 Response Workflow
    - 2.3 Status Caching
  - 3.0 Remote Agent Timeout
    - 3.1 Detection Methods
    - 3.2 Architect Agent Timeout
    - 3.3 Orchestrator Agent Timeout
    - 3.4 Integrator Agent Timeout
  - 4.0 User Incomplete Input
    - 4.1 Detection Methods
    - 4.2 Clarification Protocol
    - 4.3 Progressive Requirement Gathering
  - 5.0 Approval Workflow Failures
    - 5.1 User Unresponsive
    - 5.2 Conflicting Approvals
    - 5.3 Approval Timeout
  - 6.0 Role Routing Failures
    - 6.1 Agent Unavailable
    - 6.2 Ambiguous Routing
    - 6.3 Capacity Issues
  - 7.0 Handoff Failures
    - 7.1 Missing Handoff Files
    - 7.2 Corrupted Handoff Data
    - 7.3 Version Mismatch
  - 8.0 Session Memory Failures
    - 8.1 Memory Load Failure
    - 8.2 Memory Save Failure
    - 8.3 Memory Corruption
- [proactive-handoff-protocol](references/proactive-handoff-protocol.md) — Proactive handoff triggers, templates, UUID tracking
  1. [Automatic Handoff Triggers](#automatic-handoff-triggers)
  2. [Handoff Document Location](#handoff-document-location)
  3. [Mandatory Handoff Sections](#mandatory-handoff-sections)
  4. [Proactive Writing Rules](#proactive-writing-rules)
  5. [Handoff Quality Checklist](#handoff-quality-checklist)
  6. [Protocol for Handing Off GitHub Operations](#protocol-for-handing-off-github-operations)
     - 6.1 [When to Hand Off GitHub Operations](#when-to-hand-off-github-operations)
     - 6.2 [GitHub Handoff Template](#github-handoff-template)
     - 6.3 [GitHub Handoff Decision Flow](#github-handoff-decision-flow)
  7. [Protocol for Handing Off Design Operations](#protocol-for-handing-off-design-operations)
     - 7.1 [When to Hand Off Design Operations](#when-to-hand-off-design-operations)
     - 7.2 [Design Handoff Template](#design-handoff-template)
     - 7.3 [Design Handoff Decision Flow](#design-handoff-decision-flow)
  8. [UUID Tracking Across Handoffs](#uuid-tracking-across-handoffs)
     - 8.1 [UUID Chain Concept](#uuid-chain-concept)
     - 8.2 [UUID Format Standards](#uuid-format-standards)
     - 8.3 [UUID Registry Location](#uuid-registry-location)
     - 8.4 [UUID Propagation Rules](#uuid-propagation-rules)
     - 8.5 [UUID Lookup Before Handoff](#uuid-lookup-before-handoff)
  - Handoff trigger summary:
    1. **Task Completion**: Before reporting task done
    2. **Session End**: When session is about to end (PreCompact, Stop)
    3. **Role Transition**: When work moves to another role
    4. **Context Limit**: When approaching context window limit
    5. **Blocking Issue**: When blocked and escalating
- [failure-notifications](references/failure-notifications.md) — Failure notification procedures, severity levels, recovery patterns
  - 4.1 What are failure notifications - Understanding error messages
  - 4.2 When to send failure notifications - Failure triggers
    - 4.2.1 Installation failures - Skill or plugin not installed
    - 4.2.2 Restart failures - Agent did not come back online
    - 4.2.3 Configuration failures - Settings not applied
    - 4.2.4 Timeout failures - Operation did not complete in time
  - 4.3 Failure notification procedure - Step-by-step process
    - 4.3.1 Capture error details - What went wrong
    - 4.3.2 Compose failure message - What to tell agents
    - 4.3.3 Send notification - Using the `agent-messaging` skill
    - 4.3.4 Provide recovery guidance - How to proceed
    - 4.3.5 Log failure - Record for analysis
  - 4.4 Failure message format - Standard error structure
  - 4.5 Error severity levels - Critical, error, warning
  - 4.6 Recovery guidance patterns - Common recovery steps
  - 4.7 Examples - Failure scenarios
  - 4.8 Troubleshooting - Notification delivery during failures
