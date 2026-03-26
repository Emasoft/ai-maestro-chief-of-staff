---
name: amcos-failure-notification-refa
description: Use when consulting detailed failure notification references. Trigger with failure notification lookups.
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

See referenced files for step-by-step examples.

## Resources

- [edge-case-protocols](references/edge-case-protocols.md) — Topics: Edge Case Protocols for Chief of Staff Agent, Table of Contents, 1.0 AI Maestro Unavailable, 1.1 Detection Methods, 1.2 Response Workflow, 1.3 Fallback Communication, Handoff: User Request, Request, Expected Response, Delivery Method, 2.0 GitHub Unavailable, 2.1 Detection Methods, 2.2 Response Workflow, 2.3 Status Caching, Project Status (Cached Data), Open Issues, Open PRs, 3.0 Remote Agent Timeout, 3.1 Detection Methods, 3.2 Architect Agent Timeout, 3.3 Orchestrator Agent Timeout, 3.4 Integrator Agent Timeout, 4.0 User Incomplete Input, 4.1 Detection Methods, 4.2 Clarification Protocol, 4.3 Progressive Requirement Gathering, 5.0 Approval Workflow Failures, 5.1 User Unresponsive, 5.2 Conflicting Approvals, 5.3 Approval Timeout, 6.0 Role Routing Failures, 6.1 Agent Unavailable, 6.2 Ambiguous Routing, 6.3 Capacity Issues, 7.0 Handoff Failures, 7.1 Missing Handoff Files, 7.2 Corrupted Handoff Data, 7.3 Version Mismatch, 8.0 Session Memory Failures, 8.1 Memory Load Failure, 8.2 Memory Save Failure, 8.3 Memory Corruption, Emergency Recovery, Related Documents
- [proactive-handoff-protocol](references/proactive-handoff-protocol.md) — Topics: Proactive Handoff Protocol, Automatic Handoff Triggers, Table of Contents, Handoff Document Location, Mandatory Handoff Sections, Context, Progress, Current State, Blockers (if any), Next Steps, References, Proactive Writing Rules, Handoff Quality Checklist, Protocol for Handing Off GitHub Operations, When to Hand Off GitHub Operations, GitHub Handoff Template, GitHub Operation Context, Linked References, Design Links (if applicable), Module Links (if applicable), Operation Details, Expected Outcome, UUID Tracking Note, GitHub Handoff Decision Flow, Protocol for Handing Off Design Operations, When to Hand Off Design Operations, Design Handoff Template, Design Context, Request Details, For New Design, For Update, For Linking, Pre-Handoff Search Results, Expected Deliverable, UUID Tracking, Design Handoff Decision Flow, UUID Tracking Across Handoffs, UUID Chain Concept, UUID Format Standards, UUID Registry Location, UUID Propagation Rules, UUID Lookup Before Handoff, Search for related designs, Check existing UUIDs in registry
- [failure-notifications](references/failure-notifications.md) — Topics: Failure Notifications Reference, Table of Contents, 4.1 What are failure notifications, 4.2 When to send failure notifications, 4.2.1 Installation failures, 4.2.2 Restart failures, 4.2.3 Configuration failures, 4.2.4 Timeout failures, 4.3 Failure notification procedure, 4.3.1 Capture error details, 4.3.2 Compose failure message, 4.3.3 Send notification, 4.3.4 Provide recovery guidance, 4.3.5 Log failure, 4.4 Failure message format, 4.5 Error severity levels, 4.6 Recovery guidance patterns, 4.7 Examples, Example 1: Skill Installation Failure, Example 2: Agent Restart Failure, Example 3: Configuration Change Failure, Example 4: Operation Timeout Failure, 4.8 Troubleshooting, Issue: Failure notification not delivered, Always wrap operations with failure notification, Issue: Failure notification too vague, Issue: Multiple failure notifications for same failure, Issue: Agent panics after failure notification, Issue: Failure notification during system outage
