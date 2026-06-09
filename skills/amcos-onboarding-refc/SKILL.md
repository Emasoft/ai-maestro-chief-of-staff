---
name: amcos-onboarding-refc
description: Use when consulting detailed onboarding references. Trigger with onboarding lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Onboarding Reference

## Overview

Reference material for onboarding. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-onboarding` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-onboarding` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Validate a handoff document before sending to the target agent"

```bash
cat references/op-validate-handoff.md | head -50
```

**Expected result:** 8-step validation procedure checking required fields, UUID uniqueness, target agent, file refs, placeholders, markdown format, and accuracy.

## Resources

- [op-validate-handoff](references/op-validate-handoff.md) — Handoff validation procedure, field checks, UUID uniqueness, file refs, placeholder detection, examples
  - [When to Use](#when-to-use)
  - [Prerequisites](#prerequisites)
  - [Procedure](#procedure)
    - [Step 1: Check Required Fields](#step-1-check-required-fields)
    - [Step 2: Verify UUID Is Unique](#step-2-verify-uuid-is-unique)
    - [Step 3: Verify Target Agent Exists](#step-3-verify-target-agent-exists)
    - [Step 4: Verify Referenced Files Exist](#step-4-verify-referenced-files-exist)
    - [Step 5: Check for Placeholder Markers](#step-5-check-for-placeholder-markers)
    - [Step 6: Validate Markdown Format](#step-6-validate-markdown-format)
    - [Step 7: Verify Current State Is Accurate](#step-7-verify-current-state-is-accurate)
    - [Step 8: Run Validation Script (If Available)](#step-8-run-validation-script-if-available)
  - [Checklist](#checklist)
  - [Examples](#examples)
    - [Example: Complete Handoff Validation](#example-complete-handoff-validation)
    - [Example: Fixing Common Validation Issues](#example-fixing-common-validation-issues)
    - [Example: Validation Script Usage](#example-validation-script-usage)
  - [Error Handling](#error-handling)
  - [Related Operations](#related-operations)
