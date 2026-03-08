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

Copy this checklist and track your progress:
- [ ] Update active context on change
- [ ] Record patterns

### PROCEDURE 2: Update Active Context

**Trigger:** Task switch, decision made, question raised, milestone reached, or pre-compaction.

1. Identify the change type
2. Open `activeContext.md`
3. Update the relevant section with ISO timestamp
4. Write immediately (no deferred saves)

**Guide:** `references/03-manage-active-context.md`

**Update patterns:** `references/06-context-update-patterns.md`

**Runbook:** `references/op-update-active-context.md`

### PROCEDURE 3: Record Discovered Patterns

**Trigger:** After identifying recurring patterns, anti-patterns, or effective solutions.

1. Identify pattern and categorize (Problem-Solution, Workflow, Decision-Logic, Error-Recovery, Configuration)
2. Open `patterns.md`, add entry with name, category, description, examples, date
3. Update pattern index; write immediately

**Guide:** `references/05-record-patterns.md`

**Categories:** `references/07-pattern-categories.md`

**Runbook:** `references/op-record-discovered-pattern.md`

### PROCEDURE 6: Prepare for Context Compaction

**Trigger:** Context usage >70%, before long-running ops, or proactively.

1. Update all three memory files with current state
2. Run `amcos_memory_manager.py validate`
3. Write all files to disk
4. Create backup
5. Confirm ready

**Safety:** `references/11-compaction-safety.md` | **Runbook:** `references/op-prepare-context-compaction.md`

## Output

| Procedure | Result |
|-----------|--------|
| Update Context | Timestamped change in `activeContext.md` |
| Record Pattern | New categorized entry in `patterns.md` |
| Prepare Compaction | All files validated, backed up, ready |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Context out of sync | See `references/14-context-sync.md` |
| Pattern file too large | See `references/16-memory-archival.md` |
| Validation fails pre-compaction | Fix errors first; never compact invalid memory |
| Files corrupted | See `references/04-memory-validation.md` |

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

- `references/03-manage-active-context.md`
- `references/04-memory-validation.md`
- `references/05-record-patterns.md`
- `references/06-context-update-patterns.md`
- `references/07-pattern-categories.md`
- `references/op-update-active-context.md`
- `references/op-record-discovered-pattern.md`
- `references/op-prepare-context-compaction.md`

**Version:** 1.0.0
