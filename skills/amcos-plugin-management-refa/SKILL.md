---
name: amcos-plugin-management-refa
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

**Input:** "Install a plugin from marketplace and validate it"

```bash
cat references/plugin-installation.md | head -60
```

**Expected result:** Step-by-step install procedure with marketplace check, install command, restart, and verification.

## Resources

- [plugin-installation](references/plugin-installation.md) — Installation prerequisites, procedure, scopes, updating, uninstalling, examples, troubleshooting
- [plugin-validation](references/plugin-validation.md) — Validation levels, CLI/script validation, common errors, fixes, examples, troubleshooting
