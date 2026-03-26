---
name: amcos-acknowledgment-protocol-ref
description: Use when consulting detailed acknowledgment protocol references. Trigger with acknowledgment protocol lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Acknowledgment Protocol Reference

## Overview

Reference material for acknowledgment protocol. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-acknowledgment-protocol` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-acknowledgment-protocol` for error handling.

## Examples

```bash
# Look up acknowledgment timeout policy
cat references/acknowledgment-protocol.md | grep -A5 "Timeout"
```

Expected: timeout values and reminder intervals for each ACK type.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the acknowledgment topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [acknowledgment-protocol](references/acknowledgment-protocol.md) — Topics: Acknowledgment Protocol Reference, Table of Contents, 3.1 What is the acknowledgment protocol, 3.2 When to require acknowledgments, 3.2.1 Disruptive operations, 3.2.2 State-changing operations, 3.2.3 Multi-agent coordination, 3.3 Acknowledgment procedure, 3.3.1 Send acknowledgment request, 3.3.2 Start timeout timer, 3.3.3 Send reminders, 3.3.4 Process response, 3.3.5 Proceed or timeout, 3.4 Acknowledgment message format, 3.5 Reminder message format, 3.6 Response handling, 3.7 Timeout behavior, 3.8 Examples, Example 1: Successful Acknowledgment Flow, Example 2: Acknowledgment with Reminders, Example 3: Timeout and Proceed, Example 4: Agent Requests Extension, 3.9 Troubleshooting, Issue: Agent never responds to acknowledgment requests, Issue: Acknowledgment received but not recognized, Issue: Reminders not being sent, Issue: Timeout too short for agent task, Issue: Multi-agent acknowledgment tracking fails
