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
agent: amcos-chief-of-staff-main-agent
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

**Guide:** `references/08-manage-progress-tracking.md`

**Dependencies:** `references/09-task-dependencies.md`

**Runbook:** `references/op-update-task-progress.md`

### PROCEDURE 5: Recover Session After Interruption

**Trigger:** Unexpected termination, manual interruption, or long break.

1. Load all three memory files
2. Read each for last state, blockers, and patterns
3. Validate consistency; present summary
4. Ask user to confirm resumption

**Guide:** `references/10-recovery-procedures.md`

**Runbook:** `references/op-recover-session.md`

### Implementation Scripts

Script `amcos_memory_manager.py`. See `references/18-using-scripts.md`.

## Output

| Procedure | Result |
|-----------|--------|
| Update Progress | Updated task state with timestamp in `progress.md` |
| Recover Session | Summary with last state and proposed resumption point |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Inconsistent progress | See `references/15-progress-validation.md` |
| Corrupted files | See `references/13-file-recovery.md` |
| Context drift | See `references/14-context-sync.md` |
| Files too large | See `references/16-memory-archival.md` |
| Not surviving compaction | See `references/17-compaction-integration.md` |

## Examples

**Input:** Task "implement-auth" changes to COMPLETED.
**Output:** Updated `progress.md`:
```
- implement-auth: COMPLETED (2026-03-01T12:00:00Z)
  Dependent tasks unblocked: write-auth-tests
```

## Resources

- `references/08-manage-progress-tracking.md`
- `references/09-task-dependencies.md`
- `references/10-recovery-procedures.md`
- `references/op-update-task-progress.md`
- `references/op-recover-session.md`
