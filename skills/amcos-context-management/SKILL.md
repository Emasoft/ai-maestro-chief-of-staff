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
agent: ai-maestro-chief-of-staff-main-agent
---

# Context Management

## Overview

Updates `activeContext.md` on focus changes, records patterns in `patterns.md`, and prepares memory for compaction.

## Prerequisites

- Session memory initialized (`amcos-memory-initialization`)
- `activeContext.md` and `patterns.md` valid

## Instructions

Copy this checklist and track your progress:
- [ ] Update active context on change
- [ ] Record patterns

### PROCEDURE 2: Update Active Context

**Trigger:** Task switch, decision made, question raised, milestone reached, or pre-compaction.

1. Identify the change type
2. Open `activeContext.md`
3. Update the relevant section with ISO timestamp
4. Write immediately (no deferred saves)

**Guide:** [03-manage-active-context](references/03-manage-active-context.md) — Topics: Manage Active Context, Table of Contents, What is Active Context

**Update patterns:** [06-context-update-patterns](references/06-context-update-patterns.md) — Topics: Context Update Patterns, Table of Contents, Update Patterns Overview

**Runbook:** [op-update-active-context](references/op-update-active-context.md) — Topics: Operation: Update Active Context, Contents, Purpose

### PROCEDURE 3: Record Discovered Patterns

**Trigger:** After identifying recurring patterns, anti-patterns, or effective solutions.

1. Identify pattern and categorize (Problem-Solution, Workflow, Decision-Logic, Error-Recovery, Configuration)
2. Open `patterns.md`, add entry with name, category, description, examples, date
3. Update pattern index; write immediately

**Guide:** [05-record-patterns](references/05-record-patterns.md) — Topics: Record Patterns - Index, Table of Contents, Parts

**Categories:** [07-pattern-categories](references/07-pattern-categories.md) — Topics: Pattern Categories, Table of Contents, Category Definitions

**Runbook:** [op-record-discovered-pattern](references/op-record-discovered-pattern.md) — Topics: Operation: Record Discovered Pattern, Contents, Purpose

### PROCEDURE 6: Prepare for Context Compaction

**Trigger:** Context usage >70%, before long-running ops, or proactively.

1. Update all three memory files with current state
2. Run `amcos_memory_manager.py validate`
3. Write all files to disk
4. Create backup
5. Confirm ready

**Safety:** [11-compaction-safety](references/11-compaction-safety.md) — Topics: Compaction Safety - Index, Table of Contents, Quick Reference

## Output

| Procedure | Result |
|-----------|--------|
| Update Context | Timestamped change in `activeContext.md` |
| Record Pattern | New categorized entry in `patterns.md` |
| Prepare Compaction | All files validated, backed up, ready |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Context out of sync | See [14-context-sync](references/14-context-sync.md) — Topics: Context Synchronization - Index, Table of Contents, Overview
| Pattern file too large | See [16-memory-archival](references/16-memory-archival.md) — Topics: Memory Archival Procedures, Table of Contents, Overview
| Validation fails pre-compaction | Fix errors first; never compact invalid memory |
| Files corrupted | See [04-memory-validation](references/04-memory-validation.md) — Topics: Memory Validation - Index, Table of Contents, Document Parts

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

- [03-manage-active-context](references/03-manage-active-context.md) — Topics: Manage Active Context, Table of Contents, What is Active Context

**Version:** 1.0.0
