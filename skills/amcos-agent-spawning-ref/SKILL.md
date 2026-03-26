---
name: amcos-agent-spawning-ref
description: Use when consulting detailed agent spawning references. Trigger with agent spawning lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Agent Spawning Reference

## Overview

Reference material for agent spawning. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-agent-spawning` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-agent-spawning` for error handling.

## Examples

See referenced files for step-by-step examples.

## Resources

- [spawn-procedures](references/spawn-procedures.md) — Topics: Spawn Procedures Reference, Table of Contents, 1.1 What is agent spawning, 1.2 When to spawn agents, 1.2.1 Task assignment triggers, 1.2.2 Scaling triggers, 1.2.3 Specialization triggers, 1.3 Spawn procedure, 1.3.1 Agent type selection, 1.3.2 Configuration preparation, 1.3.3 Instance creation, Spawn via Claude Code Task tool, 1.3.4 Initialization verification, 1.3.5 Registry registration, 1.4 Spawn configuration format, Required fields, Optional fields, 1.5 AI Maestro integration, 1.6 Examples, Example 1: Spawn for Feature Implementation, Spawn code-implementer for auth feature, Returns: {"agent_id": "code-impl-auth-01", "status": "RUNNING"}, Example 2: Spawn Multiple Parallel Agents, Spawn 3 test engineers for parallel test writing, Result: 3 test-engineer agents spawned, all waiting for auth, 1.7 Troubleshooting, Issue: Spawn command times out, Issue: Agent spawns but does not respond, Issue: Agent spawns with wrong configuration, Issue: Too many agents spawned
