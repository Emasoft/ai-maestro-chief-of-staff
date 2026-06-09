---
name: amcos-agent-termination-ref
description: Use when consulting detailed agent termination references. Trigger with agent termination lookups. Loaded by ai-maestro-chief-of-staff-main-agent
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

```bash
# Look up graceful vs forced termination procedures
cat references/termination-procedures.md | grep -A3 "Graceful\|Forced"
```

Expected: step-by-step procedures for both termination types.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the termination topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [termination-procedures](references/termination-procedures.md) — Termination procedures reference: triggers, graceful vs forced shutdown, validation, troubleshooting
  - 2.1 What is agent termination - Understanding clean shutdown
  - 2.2 When to terminate agents - Termination triggers
    - 2.2.1 Task completion - Work finished
    - 2.2.2 Error conditions - Unrecoverable failures
    - 2.2.3 Resource reclamation - Freeing capacity
    - 2.2.4 User request - Manual termination
  - 2.3 Termination procedure - Step-by-step shutdown
    - 2.3.1 Work verification - Ensuring completion
    - 2.3.2 State preservation - Saving final state
    - 2.3.3 Termination signal - Sending shutdown command
    - 2.3.4 Confirmation await - Waiting for acknowledgment
    - 2.3.5 Registry cleanup - Removing agent record
  - 2.4 Graceful vs forced termination - Choosing termination type
  - 2.5 Post-termination validation - Verifying cleanup
  - 2.6 Examples - Termination scenarios
  - 2.7 Troubleshooting - Termination issues
