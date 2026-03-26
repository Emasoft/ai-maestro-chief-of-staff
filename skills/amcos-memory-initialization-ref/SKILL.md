---
name: amcos-memory-initialization-ref
description: Use when consulting detailed memory initialization references. Trigger with memory initialization lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Memory Initialization Reference

## Overview

Reference material for memory initialization. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-memory-initialization` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-memory-initialization` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "How do I initialize session memory from scratch?"

```bash
# Look up the reference
cat references/01-initialize-session-memory.md | head -50
```

**Expected result:** Step-by-step initialization procedure with directory creation and file templates.

## Resources

- [01-initialize-session-memory](references/01-initialize-session-memory.md) — Initialization procedure, directory structure, file templates, validation, troubleshooting
- [00-session-memory-examples](references/00-session-memory-examples.md) — Examples: init, recovery, progress update, context update, pattern recording
