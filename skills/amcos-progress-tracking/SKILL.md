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
agent: amcos-main
---

# Progress Tracking

## Overview

Tracks task progress in `progress.md`, manages dependencies, handles session recovery, and documents scripts.

## Prerequisites

- Session memory initialized (`amcos-memory-initialization`)
- `design/memory/progress.md` valid

## Instructions

### PROCEDURE 4: Update Task Progress

**Trigger:** Task completes, status changes, task blocked, or dependency resolves.

**States:** PENDING, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED

1. Identify the changed task
2. Open `progress.md`
3. Update status with ISO timestamp
4. Document blockers if any
5. Cascade state changes to dependent tasks
6. Write immediately

**Guide:** [references/08-manage-progress-tracking.md](references/08-manage-progress-tracking.md)
  <!-- TOC: 08-manage-progress-tracking.md -->
  - Purpose
  - Part Files
  - Quick Reference
  <!-- /TOC -->

**Dependencies:** [references/09-task-dependencies.md](references/09-task-dependencies.md)
  <!-- TOC: 09-task-dependencies.md -->
  - Part 1: Dependency Types and Notation
  - Part 2: Dependency Management
  - Part 3: Critical Path Analysis
  - ...and 1 more sections
  <!-- /TOC -->

**Runbook:** [references/op-update-task-progress.md](references/op-update-task-progress.md)

### PROCEDURE 5: Recover Session After Interruption

**Trigger:** Unexpected termination, manual interruption, or long break.

1. Load all three memory files
2. Read each for last state, blockers, and patterns
3. Validate consistency; present summary
4. Ask user to confirm resumption

**Guide:** [references/10-recovery-procedures.md](references/10-recovery-procedures.md)
  <!-- TOC: 10-recovery-procedures.md -->
  - Understanding recovery scenarios
  - Recovering from failed compaction
  - Recovering from corrupted memory
  - ...and 6 more sections
  <!-- /TOC -->

**Runbook:** [references/op-recover-session.md](references/op-recover-session.md)

### Implementation Scripts

Script `amcos_memory_manager.py` with subcommands: `init`, `validate`, `health`, `add-progress`, `compact`. See [references/18-using-scripts.md](references/18-using-scripts.md).
  <!-- TOC: 18-using-scripts.md -->
  - Part 1: Initialize and Validate
  - Part 2: Advanced Workflows
  - Part 3: Common Workflows
  <!-- /TOC -->

## Output

| Procedure | Result |
|-----------|--------|
| Update Progress | Updated task state with timestamp in `progress.md` |
| Recover Session | Summary with last state and proposed resumption point |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Inconsistent progress | See [15-progress-validation.md](references/15-progress-validation.md) |
| Corrupted files | See [13-file-recovery.md](references/13-file-recovery.md) |
| Context drift | See [14-context-sync.md](references/14-context-sync.md) |
| Files too large | See [16-memory-archival.md](references/16-memory-archival.md) |
| Not surviving compaction | See [17-compaction-integration.md](references/17-compaction-integration.md) |

## Examples

```bash
# Update task progress
uv run python scripts/amcos_memory_manager.py add-progress \
  --task "Implement config detection" --status "COMPLETED"

# Recovery: check health then validate
uv run python scripts/amcos_memory_manager.py health --json
uv run python scripts/amcos_memory_manager.py validate
```

## Resources

- [references/08-manage-progress-tracking.md](references/08-manage-progress-tracking.md) - Progress tracking
- [references/09-task-dependencies.md](references/09-task-dependencies.md) - Dependencies
- [references/10-recovery-procedures.md](references/10-recovery-procedures.md) - Recovery
- [references/11-compaction-safety.md](references/11-compaction-safety.md) - Compaction safety
- [references/12-pre-compaction-checklist.md](references/12-pre-compaction-checklist.md) - Checklist
- [references/13-file-recovery.md](references/13-file-recovery.md) - File recovery
- [references/14-context-sync.md](references/14-context-sync.md) - Context sync
- [references/15-progress-validation.md](references/15-progress-validation.md) - Validation
- [references/16-memory-archival.md](references/16-memory-archival.md) - Archival
- [references/17-compaction-integration.md](references/17-compaction-integration.md) - Compaction
- [references/18-using-scripts.md](references/18-using-scripts.md) - Scripts
- [references/op-update-task-progress.md](references/op-update-task-progress.md) - Runbook: progress
- [references/op-recover-session.md](references/op-recover-session.md) - Runbook: recovery

---

**Version:** 1.0.0 | **Last Updated:** 2025-02-01
