---
name: amcos-progress-tracking-ref
description: Use when consulting detailed progress tracking references. Trigger with progress tracking lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Progress Tracking Reference

## Overview

Reference material for progress tracking. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-progress-tracking` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-progress-tracking` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Recover a session after unexpected interruption"

```bash
cat references/op-recover-session.md | head -50
```

**Expected result:** 6-step recovery procedure: load memory files, read work/task state, validate consistency, confirm resumption.

## Resources

- [op-recover-session](references/op-recover-session.md) — Session recovery procedure, scenarios, checklist
  - [Purpose](#purpose)
  - [When To Use This Operation](#when-to-use-this-operation)
  - [Steps](#steps)
    - [Step 1: Load All Memory Files](#step-1-load-all-memory-files)
    - [Step 2: Read activeContext.md for Work State](#step-2-read-activecontextmd-for-work-state)
  - [Recovery: Current State](#recovery-current-state)
    - [Step 3: Read progress.md for Task State](#step-3-read-progressmd-for-task-state)
  - [Recovery: Task State](#recovery-task-state)
    - [Step 4: Validate Memory Consistency](#step-4-validate-memory-consistency)
  - [Recovery: Validation](#recovery-validation)
    - [Step 5: Ask User to Confirm Resumption](#step-5-ask-user-to-confirm-resumption)
  - [Session Recovery Summary](#session-recovery-summary)
    - [State to Resume](#state-to-resume)
    - [Shall I resume from this state?](#shall-i-resume-from-this-state)
    - [Step 6: Update Session Start](#step-6-update-session-start)
  - [Session Notes](#session-notes)
  - [Recovery Scenarios](#recovery-scenarios)
    - [Scenario 1: Clean Resume (< 24 hours)](#scenario-1-clean-resume-24-hours)
    - [Scenario 2: Long Gap (> 24 hours)](#scenario-2-long-gap-24-hours)
    - [Scenario 3: Corrupted Files](#scenario-3-corrupted-files)
  - [Checklist](#checklist)
  - [Output](#output)
  - [Related References](#related-references)
  - [Next Operation](#next-operation)
- [16-memory-archival](references/16-memory-archival.md) — Archival triggers, procedures, organization, examples
  1. [When you need to understand the overview](#overview)
  2. [When to archive](#when-to-archive)
  3. [What to archive](#what-to-archive)
  4. [How to archive](#archival-procedures)
  5. [Understanding archive organization](#archive-organization)
  6. [For implementation examples](#examples)
  7. [If issues occur](#troubleshooting)
- [op-update-task-progress](references/op-update-task-progress.md) — Task state updates, blockers, dependencies, timestamps
  - [Purpose](#purpose)
  - [When To Use This Operation](#when-to-use-this-operation)
  - [Task States](#task-states)
  - [Steps](#steps)
    - [Step 1: Identify Changed Task](#step-1-identify-changed-task)
    - [Step 2: Open progress.md](#step-2-open-progressmd)
    - [Step 3: Update Task Status](#step-3-update-task-status)
  - [Completed Tasks](#completed-tasks)
  - [Blocked Tasks](#blocked-tasks)
  - [Active Tasks](#active-tasks)
    - [Step 4: Document Blockers (if any)](#step-4-document-blockers-if-any)
    - [Step 5: Update Dependencies](#step-5-update-dependencies)
  - [Active Tasks](#active-tasks)
    - [Step 6: Update Timestamp](#step-6-update-timestamp)
  - [Checklist](#checklist)
  - [Progress File Structure](#progress-file-structure)
  - [Active Tasks](#active-tasks)
  - [Completed Tasks](#completed-tasks)
  - [Blocked Tasks](#blocked-tasks)
  - [Paused Tasks](#paused-tasks)
  - [Output](#output)
  - [Related References](#related-references)
  - [Next Operation](#next-operation)
- [18-using-scripts](references/18-using-scripts.md) — Memory script commands, workflows, troubleshooting
  - 1.1 Overview - What are memory scripts and why use them
  - 1.2 Available Commands - Full inventory table of all `amcos_memory_manager.py` subcommands
  - 1.3 Initialize Memory - `amcos_memory_manager.py init` for creating new memory structure
    - 1.3.1 Basic initialization for new projects
  - 1.4 Validate Memory - `amcos_memory_manager.py validate` for checking memory integrity
    - 1.4.1 Basic validation workflow
  - 2.1 Check Memory Health - `amcos_memory_manager.py health` for reporting on memory state
    - 2.1.1 Health check text output
    - 2.1.2 Health check JSON output
  - 2.2 Update Memory - `amcos_memory_manager.py` add-* subcommands for immediate persistence
    - 2.2.1 Available write subcommands (add-decision, set-focus, add-progress, add-pattern, etc.)
  - 2.3 Compact Memory - `amcos_memory_manager.py compact` for archiving old content
    - 2.3.1 Compact with automatic backup
  - 2.4 repair-memory.py - Recovering from corruption (planned)
  - 3.1 Common Workflows (all using `amcos_memory_manager.py` subcommands)
    - 3.1.1 Daily Startup workflow
    - 3.1.2 Before Compaction workflow
    - 3.1.3 Weekly Maintenance workflow
    - 3.1.4 Emergency Recovery workflow
  - 3.2 Implementation Examples
    - 3.2.1 Python integration for agent workflows
  - 3.3 Troubleshooting
    - 3.3.1 Module not found errors
    - 3.3.2 Permission denied issues
    - 3.3.3 False positive validation errors
