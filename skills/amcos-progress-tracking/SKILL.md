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

### Checklist

Copy this checklist and track your progress:

- [ ] Update task status in `progress.md` with ISO timestamp
- [ ] Document any blockers and cascade dependency changes
- [ ] Recover session state if interrupted

### PROCEDURE 4: Update Task Progress

**Trigger:** Task completes, status changes, task blocked, or dependency resolves.

**States:** PENDING, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED

1. Identify the changed task
2. Open `progress.md`
3. Update status with ISO timestamp
4. Document blockers if any
5. Cascade state changes to dependent tasks
6. Write immediately

**Guide:** See 08-manage-progress-tracking in Resources

**Dependencies:** See 09-task-dependencies in Resources

### PROCEDURE 5: Recover Session After Interruption

**Trigger:** Unexpected termination, manual interruption, or long break.

1. Load all three memory files
2. Read each for last state, blockers, and patterns
3. Validate consistency; present summary
4. Ask user to confirm resumption

**Guide:** See 10-recovery-procedures in Resources

### Implementation Scripts

## Output

| Procedure | Result |
|-----------|--------|
| Update Progress | Updated task state with timestamp in `progress.md` |
| Recover Session | Summary with last state and proposed resumption point |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Inconsistent progress | See 15-progress-validation in Resources |
| Corrupted files | See 13-file-recovery in Resources |
| Context drift | See 14-context-sync in Resources |
| Not surviving compaction | See 17-compaction-integration in Resources |

## Examples

**Input:** Task "implement-auth" changes to COMPLETED.
**Output:** Updated `progress.md`:
```
- implement-auth: COMPLETED (2026-03-01T12:00:00Z)
  Dependent tasks unblocked: write-auth-tests
```

## Resources

- [08-manage-progress-tracking](references/08-manage-progress-tracking.md) — Task states, procedures, dependencies, snapshots
  - Purpose
  - Part Files
  - Quick Reference
- [09-task-dependencies](references/09-task-dependencies.md) — Dependency types, management, critical path
- [10-recovery-procedures](references/10-recovery-procedures.md) — Recovery from failures
  - When you need to understand the purpose
  - Understanding recovery scenarios
  - Recovering from failed compaction
  - Recovering from corrupted memory
  - Recovering from lost context
  - Recovering from snapshot failure
  - Emergency recovery procedures
  - For implementation examples
  - If issues occur
- [15-progress-validation](references/15-progress-validation.md) — Validation rules
  - Parts
- [13-file-recovery](references/13-file-recovery.md) — File corruption recovery
  - Part 1: Detection and Basic Recovery
  - Part 2: Advanced Recovery and Prevention
  - Quick Reference: Which Procedure to Use
- [14-context-sync](references/14-context-sync.md) — Context synchronization
  - Overview
  - Document Parts
  - Quick Reference
- [17-compaction-integration](references/17-compaction-integration.md) — Compaction integration
  - Document Parts
  - Quick Reference
