---
name: amcos-plugin-management-refb
description: Use when consulting detailed plugin management references. Trigger with plugin management lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Plugin Management Reference

## Overview

Reference material for plugin management. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-plugin-management` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-plugin-management` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Set up a local plugin directory for development"

```bash
cat references/local-configuration.md | head -50
```

**Expected result:** Directory structure, manifest creation, component setup, and launch configuration steps.

## Resources

- [local-configuration](references/local-configuration.md) — Local plugin directory structure, manifest, component setup, dev workflow, examples, troubleshooting
