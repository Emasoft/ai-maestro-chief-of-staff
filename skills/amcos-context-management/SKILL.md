---
name: amcos-context-management
description: Use when managing active context, recording discovered patterns, or preparing for context compaction. Trigger with context update or pattern recording needs.
user-invocable: false
license: Apache-2.0
compatibility: Requires file system access to design/memory/ directory. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-chief-of-staff-main-agent
---

# Context Management

## Overview

Updates `activeContext.md` on focus changes, records patterns in `patterns.md`, and prepares memory for compaction.

## Prerequisites

- Session memory initialized (`amcos-memory-initialization`)
- `activeContext.md` and `patterns.md` valid

## Instructions

> **Output Rule**: All AMCOS scripts produce 2-line stdout summaries. Full output is written to `.amcos-logs/`. Always reference log file paths in reports instead of reproducing script output.

Copy this checklist and track your progress:
- [ ] Update active context on change
- [ ] Record patterns

### PROCEDURE 2: Update Active Context

**Trigger:** Task switch, decision made, question raised, milestone reached, or pre-compaction.

1. Identify the change type
2. Open `activeContext.md`
3. Update the relevant section with ISO timestamp
4. Write immediately (no deferred saves)

**Guide:** [references/03-manage-active-context.md](references/03-manage-active-context.md)
<!-- TOC: 03-manage-active-context.md -->
- Understanding what active context is
- When to update context
- ...+6 more
<!-- /TOC -->

**Update patterns:** [references/06-context-update-patterns.md](references/06-context-update-patterns.md)
<!-- TOC: 06-context-update-patterns.md -->
- Understanding update patterns overview
- When switching tasks
- ...+8 more
<!-- /TOC -->

**Runbook:** [references/op-update-active-context.md](references/op-update-active-context.md)

### PROCEDURE 3: Record Discovered Patterns

**Trigger:** After identifying recurring patterns, anti-patterns, or effective solutions.

1. Identify pattern and categorize (Problem-Solution, Workflow, Decision-Logic, Error-Recovery, Configuration)
2. Open `patterns.md`, add entry with name, category, description, examples, date
3. Update pattern index; write immediately

**Guide:** [references/05-record-patterns.md](references/05-record-patterns.md)
<!-- TOC: 05-record-patterns.md -->
- Parts
- Quick Navigation
<!-- /TOC -->

**Categories:** [references/07-pattern-categories.md](references/07-pattern-categories.md)
  <!-- TOC: 07-pattern-categories.md -->
  - Category Definitions
  - Pattern Category Details
  - How to Choose Categories
  - ...and 1 more sections
  <!-- /TOC -->

**Runbook:** [references/op-record-discovered-pattern.md](references/op-record-discovered-pattern.md)

### PROCEDURE 6: Prepare for Context Compaction

**Trigger:** Context usage >70%, before long-running ops, or proactively.

1. Update all three memory files with current state
2. Run `amcos_memory_manager.py validate`
3. Write all files to disk
4. Create backup
5. Confirm ready

**Safety:** [references/11-compaction-safety.md](references/11-compaction-safety.md) | **Runbook:** [references/op-prepare-context-compaction.md](references/op-prepare-context-compaction.md)
  <!-- TOC: op-prepare-context-compaction.md -->
  - Purpose
  - Context Compaction Risks
  - Steps
  - ...and 5 more sections
  <!-- /TOC -->

## Output

| Procedure | Result |
|-----------|--------|
| Update Context | Timestamped change in `activeContext.md` |
| Record Pattern | New categorized entry in `patterns.md` |
| Prepare Compaction | All files validated, backed up, ready |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Context out of sync | See [14-context-sync.md](references/14-context-sync.md) |
| Pattern file too large | See [16-memory-archival.md](references/16-memory-archival.md) |
  <!-- TOC: 16-memory-archival.md -->
  - Overview
  - When to Archive
  - Archival Procedures
  - ...and 4 more sections
  <!-- /TOC -->
| Validation fails pre-compaction | Fix errors first; never compact invalid memory |
| Files corrupted | See [04-memory-validation.md](references/04-memory-validation.md) |
<!-- TOC: 04-memory-validation.md -->
- Document Parts
- Quick Reference
<!-- /TOC -->

## Examples

```bash
# Update focus on task switch
uv run python scripts/amcos_memory_manager.py set-focus \
  --focus "Implementing config detection"

# Record a pattern
uv run python scripts/amcos_memory_manager.py add-pattern \
  --name "Retry with backoff" --category "Error-Recovery"
```

## Resources

- [03-manage-active-context.md](references/03-manage-active-context.md)
- [04-memory-validation.md](references/04-memory-validation.md)
- [05-record-patterns.md](references/05-record-patterns.md)
- [06-context-update-patterns.md](references/06-context-update-patterns.md)
- [07-pattern-categories.md](references/07-pattern-categories.md)
- [op-update-active-context.md](references/op-update-active-context.md)
- [op-record-discovered-pattern.md](references/op-record-discovered-pattern.md)
- [op-prepare-context-compaction.md](references/op-prepare-context-compaction.md)

**Version:** 1.0.0
