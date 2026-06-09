---
name: amcos-progress-tracking
description: Use when tracking task progress, managing task dependencies, or recovering after session interruptions. Trigger with progress updates or task dependency management. Loaded by ai-maestro-chief-of-staff-main-agent
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
  - 1.1 Type 1: Sequential Dependency - When Task B cannot start until Task A completes
  - 1.2 Type 2: Parallel with Merge - When independent tasks converge to common successor
  - 1.3 Type 3: Split Dependency - When one task enables multiple parallel workstreams
  - 1.4 Type 4: Partial Dependency - When Task B can start after Task A reaches milestone
  - 1.5 Type 5: Optional Dependency - When Task B is enhanced but not blocked by Task A
  - 2.1 Text-Based Notation - Linear chains, parallel paths, complex graphs, tables
  - 2.2 In-Task Dependency Recording - How to record dependencies in task definitions
  - Procedure 1: Record Dependency - How to record task dependencies with scripts
  - Procedure 2: Check Dependencies Met - How to verify all dependencies are satisfied
  - Procedure 3: Update Dependencies After Task Completion - How to unblock waiting tasks
  - Procedure 4: Detect Circular Dependencies - How to find circular dependency chains
  - 1.1 Definition - What is critical path and why it matters
  - 1.2 Calculation Procedure - Step-by-step critical path calculation
  - 1.3 Critical Path Script - Automated critical path analysis
  - 2.1 Validation Checklist - Dependency validation requirements
  - 2.2 Validation Script - Automated dependency validation
  - Example 1: Simple Sequential Dependencies - Linear task chain example
  - Example 2: Parallel Development with Merge - Frontend/backend parallel work example
  - Example 3: Complex Dependency Graph - Multi-path dependency example
  - Example 4: Partial Dependencies - Milestone-based dependency example
  - Troubleshooting: Task Stuck Waiting on Dependency
  - Troubleshooting: Circular Dependency Detected
  - Troubleshooting: Too Many Dependencies
  - Troubleshooting: Unknown Task Scope
  - Troubleshooting: Dependency Information Lost
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
