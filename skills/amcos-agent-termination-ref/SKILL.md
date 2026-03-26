---
name: amcos-agent-termination-ref
description: Use when consulting detailed agent termination references. Trigger with agent termination lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Agent Termination Reference

## Overview

Reference material for agent termination. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-agent-termination` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-agent-termination` for error handling.

## Examples

See referenced files for step-by-step examples.

## Resources

- [termination-procedures](references/termination-procedures.md) — Topics: Termination Procedures Reference, Table of Contents, 2.1 What is agent termination, 2.2 When to terminate agents, 2.2.1 Task completion, 2.2.2 Error conditions, 2.2.3 Resource reclamation, 2.2.4 User request, 2.3 Termination procedure, 2.3.1 Work verification, 2.3.2 State preservation, 2.3.3 Termination signal, 2.3.4 Confirmation await, 2.3.5 Registry cleanup, 2.4 Graceful vs forced termination, Graceful Termination, Forced Termination, 2.5 Post-termination validation, 2.6 Examples, Example 1: Graceful Termination After Task Completion, Agent completed its task, Step 1: Verify work complete, Step 2: Request graceful termination, Step 3: Wait for confirmation, Step 4: Update registry, Step 5: Notify orchestrator, Example 2: Forced Termination Due to Error, Agent is stuck in error state, Step 1: Attempt graceful first, Step 3: Mark as terminated regardless of response, Step 4: Log the incident, 2.7 Troubleshooting, Issue: Agent does not respond to termination request, Issue: State not saved during termination, Issue: Agent remains in registry after termination, Issue: Dependent agents not notified
