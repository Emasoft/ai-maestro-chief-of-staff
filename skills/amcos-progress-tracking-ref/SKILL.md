---
name: amcos-progress-tracking-ref
description: Use when consulting detailed progress tracking references. Trigger with progress tracking lookups.
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

## Examples

See referenced files for step-by-step examples.

## Resources

- [op-recover-session](references/op-recover-session.md) — Topics: Operation: Recover Session After Interruption, Contents, Purpose, When To Use This Operation, Steps, Step 1: Load All Memory Files, Check files exist, Read each file, Step 2: Read activeContext.md for Work State, Recovery: Current State, Step 3: Read progress.md for Task State, Recovery: Task State, Step 4: Validate Memory Consistency, Recovery: Validation, Step 5: Ask User to Confirm Resumption, Session Recovery Summary, State to Resume, Shall I resume from this state?, Step 6: Update Session Start, Session Notes, Recovery Scenarios, Scenario 1: Clean Resume (< 24 hours), Scenario 2: Long Gap (> 24 hours), Scenario 3: Corrupted Files, Checklist, Output, Related References, Next Operation
- [16-memory-archival](references/16-memory-archival.md) — Topics: Memory Archival Procedures, Table of Contents, Part Files, 16-memory-archival-part1-procedures.md, 16-memory-archival-part2-examples.md, Overview, What Is Memory Archival?, Why Archive?, When to Archive, Trigger 1: File Size Threshold, Trigger 2: Completed Task Accumulation, Trigger 3: Pattern Obsolescence, Trigger 4: Session Milestone, Trigger 5: Performance Degradation, What to Archive, Archive Candidates from progress.md, Archive Candidates from patterns.md, Archive Candidates from activeContext.md, Archival Procedures, Archive Organization, Directory Structure, Naming Conventions, Examples, Troubleshooting
- [op-update-task-progress](references/op-update-task-progress.md) — Topics: Operation: Update Task Progress, Contents, Purpose, When To Use This Operation, Task States, Steps, Step 1: Identify Changed Task, Step 2: Open progress.md, Step 3: Update Task Status, Completed Tasks, Blocked Tasks, Active Tasks, Step 4: Document Blockers (if any), Step 5: Update Dependencies, Active Tasks, Step 6: Update Timestamp, Task Progress, Checklist, Progress File Structure, Task Progress, Active Tasks, Completed Tasks, Blocked Tasks, Paused Tasks, Output, Related References, Next Operation
- [18-using-scripts](references/18-using-scripts.md) — Topics: Using Memory Scripts, Table of Contents, Part 1: Initialize and Validate, Part 2: Health Check, Update, Compact, and Repair, Part 3: Workflows, Examples, and Troubleshooting, Before compaction, Weekly maintenance, Emergency recovery, Overview, Quick Reference: Command Inventory, Quick Reference: Common Commands, Daily startup
