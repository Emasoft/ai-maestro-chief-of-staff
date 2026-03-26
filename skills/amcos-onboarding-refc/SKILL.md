---
name: amcos-onboarding-refc
description: Use when consulting detailed onboarding references. Trigger with onboarding lookups.
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

## Examples

See referenced files for step-by-step examples.

## Resources

- [op-validate-handoff](references/op-validate-handoff.md) — Topics: Validate Handoff Document, Contents, When to Use, Prerequisites, Procedure, Step 1: Check Required Fields, Check if document has required fields, Step 2: Verify UUID Is Unique, Check existing handoffs, Ensure UUID doesn't already exist, Should return nothing for new handoffs, Step 3: Verify Target Agent Exists, Step 4: Verify Referenced Files Exist, Extract file references from handoff, Step 5: Check for Placeholder Markers, Find [TBD], TODO, FIXME, or placeholder text, Should return nothing for complete handoffs, Step 6: Validate Markdown Format, Check for broken links, Check for unclosed formatting, Step 7: Verify Current State Is Accurate, Step 8: Run Validation Script (If Available), Use the CPV plugin validator to validate the plugin (including handoff documents), Checklist, Examples, Example: Complete Handoff Validation, Step 1: Required fields, Step 2: UUID uniqueness, Step 3: Target agent exists, Step 4: Referenced files, Step 5: Placeholders, Example: Fixing Common Validation Issues, Before (invalid), After (valid), Before (invalid), After (valid), Before (invalid), After (valid), Example: Validation Script Usage, Use the CPV plugin validator for full plugin validation (includes handoff checks), Expected output:, Validating plugin: ai-maestro-chief-of-staff, [OK] Manifest valid, [OK] Skills validated, [OK] Commands validated, [OK] Hooks validated, [OK] Scripts validated, Validation PASSED, Error Handling, Related Operations
