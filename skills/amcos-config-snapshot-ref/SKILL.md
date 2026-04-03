---
name: amcos-config-snapshot-ref
description: Use when consulting detailed config snapshot references. Trigger with config snapshot lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Config Snapshot Reference

## Overview

Reference material for config snapshot. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-config-snapshot` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-config-snapshot` for error handling.

## Examples

```bash
# Look up config snapshot capture procedure
cat references/op-capture-config-snapshot.md | grep -A5 "Step 1"
```

Expected: steps to identify config files and create snapshot header.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the config snapshot topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [ai-maestro-integration](references/ai-maestro-integration.md) — AI Maestro integration, sessions, messaging, health
- [op-detect-config-changes](references/op-detect-config-changes.md) — Detect config changes during session
- [21-config-conflict-resolution](references/21-config-conflict-resolution.md) — Resolving config conflicts (Types A-D)
- [op-capture-config-snapshot](references/op-capture-config-snapshot.md) — Capture config snapshot at session start
- [op-handle-config-conflicts](references/op-handle-config-conflicts.md) — Handle config version conflicts
