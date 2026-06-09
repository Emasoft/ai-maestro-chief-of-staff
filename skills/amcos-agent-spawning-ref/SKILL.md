---
name: amcos-agent-spawning-ref
description: Use when consulting detailed agent spawning references. Trigger with agent spawning lookups. Loaded by ai-maestro-chief-of-staff-main-agent
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

```bash
# Look up spawn configuration format
cat references/spawn-procedures.md | grep -A5 "Required fields"
```

Expected: required and optional fields for agent spawn configuration.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the spawning topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [spawn-procedures](references/spawn-procedures.md) — Spawn procedures reference: triggers, configuration, AI Maestro integration, troubleshooting
  - 1.1 What is agent spawning - Understanding agent creation
  - 1.2 When to spawn agents - Triggers for new agents
    - 1.2.1 Task assignment triggers - New work arrives
    - 1.2.2 Scaling triggers - Parallel execution needed
    - 1.2.3 Specialization triggers - Specific capability required
  - 1.3 Spawn procedure - Step-by-step agent creation
    - 1.3.1 Agent type selection - Choosing the right agent
    - 1.3.2 Configuration preparation - Setting parameters
    - 1.3.3 Instance creation - Executing spawn command
    - 1.3.4 Initialization verification - Confirming agent ready
    - 1.3.5 Registry registration - Recording agent existence
  - 1.4 Spawn configuration format - Standard configuration structure
  - 1.5 AI Maestro integration - Messaging new agents
  - 1.6 Examples - Spawn scenarios
  - 1.7 Troubleshooting - Spawn failures and recovery
