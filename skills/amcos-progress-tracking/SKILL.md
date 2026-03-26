---
name: amcos-progress-tracking
description: Use when tracking task progress, managing task dependencies, or recovering after session interruptions. Trigger with progress updates or task dependency management.
user-invocable: false
license: Apache-2.0
compatibility: Requires file system access to design/memory/ directory. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Progress Tracking

## Overview

Tracks task progress in `progress.md`, manages dependencies, handles session recovery, and documents scripts.

## Prerequisites

- Session memory initialized (`amcos-memory-initialization`)
- `design/memory/progress.md` valid

## Instructions

Copy this checklist and track your progress:
- [ ] Update task status in progress.md
- [ ] Recover session if interrupted

### PROCEDURE 4: Update Task Progress

**Trigger:** Task completes, status changes, task blocked, or dependency resolves.

**States:** PENDING, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED

1. Identify the changed task
2. Open `progress.md`
3. Update status with ISO timestamp
4. Document blockers if any
5. Cascade state changes to dependent tasks
6. Write immediately

**Guide:** [08-manage-progress-tracking](references/08-manage-progress-tracking.md) — Topics: Manage Progress Tracking, Table of Contents, Part Files

**Dependencies:** [09-task-dependencies](references/09-task-dependencies.md) — Topics: Task Dependencies, Table of Contents, Overview

**Runbook:** [op-update-task-progress](references/op-update-task-progress.md) — Topics: Operation: Update Task Progress, Contents, Purpose

### PROCEDURE 5: Recover Session After Interruption

**Trigger:** Unexpected termination, manual interruption, or long break.

1. Load all three memory files
2. Read each for last state, blockers, and patterns
3. Validate consistency; present summary
4. Ask user to confirm resumption

**Guide:** [10-recovery-procedures](references/10-recovery-procedures.md) — Topics: Recovery Procedures, Table of Contents, Part Files

**Runbook:** [op-recover-session](references/op-recover-session.md) — Topics: Operation: Recover Session After Interruption, Contents, Purpose

### Implementation Scripts

Script `amcos_memory_manager.py`. See [18-using-scripts](references/18-using-scripts.md) — Topics: Using Memory Scripts, Table of Contents, Before compaction

## Output

| Procedure | Result |
|-----------|--------|
| Update Progress | Updated task state with timestamp in `progress.md` |
| Recover Session | Summary with last state and proposed resumption point |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Inconsistent progress | See [15-progress-validation](references/15-progress-validation.md) — Topics: Progress Validation - Index, Table of Contents, Parts
| Corrupted files | See [13-file-recovery](references/13-file-recovery.md) — Topics: Session Memory File Recovery - Index, Table of Contents, Part 2: Advanced Recovery and Prevention
| Context drift | See [14-context-sync](references/14-context-sync.md) — Topics: Context Synchronization - Index, Table of Contents, Overview
| Files too large | See [16-memory-archival](references/16-memory-archival.md) — Topics: Memory Archival Procedures, Table of Contents, Overview
| Not surviving compaction | See [17-compaction-integration](references/17-compaction-integration.md) — Topics: Compaction Integration - Index, Table of Contents, Document Parts

## Examples

**Input:** Task "implement-auth" changes to COMPLETED.
**Output:** Updated `progress.md`:
```
- implement-auth: COMPLETED (2026-03-01T12:00:00Z)
  Dependent tasks unblocked: write-auth-tests
```

## Resources

- [08-manage-progress-tracking](references/08-manage-progress-tracking.md) — Topics: Manage Progress Tracking, Table of Contents, Part Files
