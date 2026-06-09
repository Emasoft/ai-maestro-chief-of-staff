---
name: amcos-onboarding-refb
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

**Input:** "Walk through the onboarding checklist for a new developer agent"

```bash
cat references/onboarding-checklist.md | head -60
```

**Expected result:** 7-phase onboarding checklist (welcome, team intro, comms, role, project, tooling, first task) with role-specific additions.

## Resources

- [onboarding-checklist](references/onboarding-checklist.md) — Checklist phases, role-specific additions, verification, documentation, examples, troubleshooting
  - 1.1 [Purpose Of The Onboarding Checklist](#11-purpose-of-the-onboarding-checklist)
  - 1.2 [Pre Onboarding Preparation](#12-pre-onboarding-preparation)
  - 1.3 [Core Onboarding Checklist](#13-core-onboarding-checklist)
  - 1.4 [Role Specific Additions](#14-role-specific-additions)
  - 1.5 [Onboarding Verification](#15-onboarding-verification)
  - 1.6 [Documenting Onboarding Completion](#16-documenting-onboarding-completion)
  - 1.7 [Onboarding Checklist Examples](#17-onboarding-checklist-examples)
  - 1.8 [Troubleshooting](#18-troubleshooting)
- [role-briefing](references/role-briefing.md) — Briefing components, responsibilities, reporting structure, expectations, confirmation, examples
  - 2.1 [Role Briefing Components](#21-role-briefing-components)
  - 2.2 [Explaining Role Responsibilities](#22-explaining-role-responsibilities)
  - 2.3 [Clarifying Reporting Structure](#23-clarifying-reporting-structure)
  - 2.4 [Setting Performance Expectations](#24-setting-performance-expectations)
  - 2.5 [Handling Agent Questions](#25-handling-agent-questions)
  - 2.6 [Confirming Role Understanding](#26-confirming-role-understanding)
  - 2.7 [Role Briefing Examples](#27-role-briefing-examples)
  - 2.8 [Troubleshooting](#28-troubleshooting)
