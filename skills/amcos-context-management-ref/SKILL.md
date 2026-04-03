---
name: amcos-context-management-ref
description: Use when consulting detailed context management references. Trigger with context management lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Context Management Reference

## Overview

Reference material for context management. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-context-management` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-context-management` for error handling.

## Examples

```bash
# Look up context update triggers
cat references/03-manage-active-context.md | grep -A3 "Trigger"
```

Expected: list of triggers that require context updates.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the context management topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [16-memory-archival](references/16-memory-archival.md) — Topics: Memory Archival Procedures, Table of Contents, Part Files, 16-memory-archival-part1-procedures.md, 16-memory-archival-part2-examples.md, Overview, What Is Memory Archival?, Why Archive?, When to Archive, Trigger 1: File Size Threshold, Trigger 2: Completed Task Accumulation, Trigger 3: Pattern Obsolescence, Trigger 4: Session Milestone, Trigger 5: Performance Degradation, What to Archive, Archive Candidates from progress.md, Archive Candidates from patterns.md, Archive Candidates from activeContext.md, Archival Procedures, Archive Organization, Directory Structure, Naming Conventions, Examples, Troubleshooting
- [op-record-discovered-pattern](references/op-record-discovered-pattern.md) — Topics: Operation: Record Discovered Pattern, Contents, Purpose, When To Use This Operation, Pattern Categories, Steps, Step 1: Identify the Pattern, Step 2: Open patterns.md, Step 3: Add Pattern Entry, Pattern: [Descriptive Name], Problem, Solution, Example, When to Use, When NOT to Use, Step 4: Update Index, Index, Step 5: Update Timestamp, Discovered Patterns, Checklist, Example Pattern Entry, Pattern: Fail-Fast Error Propagation, Problem, Solution, Example, WRONG - swallows error, RIGHT - propagates error, When to Use, When NOT to Use, Output, Related References, Next Operation
- [op-update-active-context](references/op-update-active-context.md) — Topics: Operation: Update Active Context, Contents, Purpose, When To Use This Operation, Update Triggers, Steps, Step 1: Identify What Changed, Step 2: Open activeContext.md, Step 3: Update Relevant Section, Current Focus, Recent Decisions, Open Questions, Session Notes, Step 4: Write Changes Immediately, After editing, verify file was written, Step 5: Update Timestamp, Active Context, Checklist, Update Patterns, Pattern 1: Task Switch, Current Focus, Pattern 2: Decision Recording, Recent Decisions, Pattern 3: Pre-Compaction Update, Output, Related References, Next Operation
- [03-manage-active-context](references/03-manage-active-context.md) — Topics: Manage Active Context, Table of Contents, Purpose, What is Active Context, 1. Current Focus, Current Focus, 2. Recent Decisions, Recent Decisions, 3. Open Questions, Open Questions, 4. Context Notes, Context Notes, Context Update Triggers, Trigger 1: Starting New Task, Trigger 2: Making Important Decision, Trigger 3: Encountering Blocker, Trigger 4: Resolving Question, Trigger 5: Context Getting Large, Update Procedures, Context Snapshots, Context Pruning, Examples, Troubleshooting
