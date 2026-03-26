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

Updates `activeContext.md`, records patterns, prepares memory for compaction.

## Prerequisites

- Session memory initialized (`amcos-memory-initialization`)
- `activeContext.md` and `patterns.md` valid

## Instructions

### PROCEDURE 2: Update Active Context

**Trigger:** Task switch, decision made, question raised, milestone reached, or pre-compaction.

1. Identify the change type
2. Open `activeContext.md`
3. Update the relevant section with ISO timestamp
4. Write immediately (no deferred saves)

**Update patterns:** [06-context-update-patterns](references/06-context-update-patterns.md)

### PROCEDURE 3: Record Discovered Patterns

**Trigger:** After identifying recurring patterns, anti-patterns, or effective solutions.

1. Identify pattern and categorize (Problem-Solution, Workflow, Decision-Logic, Error-Recovery, Configuration)
2. Open `patterns.md`, add entry with name, category, description, examples, date
3. Update pattern index; write immediately

**Guide:** [05-record-patterns](references/05-record-patterns.md) | **Categories:** [07-pattern-categories](references/07-pattern-categories.md)

### PROCEDURE 6: Prepare for Context Compaction

**Trigger:** Context usage >70%, before long-running ops, or proactively.

1. Update all three memory files with current state
2. Run `amcos_memory_manager.py validate`
3. Write all files to disk
4. Create backup
5. Confirm ready

**Safety:** [11-compaction-safety](references/11-compaction-safety.md)

## Output

| Procedure | Result |
|-----------|--------|
| Update Context | Timestamped change in `activeContext.md` |
| Record Pattern | New categorized entry in `patterns.md` |
| Prepare Compaction | All files validated, backed up, ready |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Context out of sync | See [14-context-sync](references/14-context-sync.md) |
| Validation fails pre-compaction | Fix errors first; never compact invalid memory |
| Files corrupted | See [04-memory-validation](references/04-memory-validation.md) |

## Examples

```bash
# Update focus on task switch
uv run python scripts/amcos_memory_manager.py set-focus \
  --focus "Implementing config detection"

# Record a pattern
uv run python scripts/amcos_memory_manager.py add-pattern \
  --name "Retry with backoff" --category "Error-Recovery"
```

## Checklist

Copy this checklist and track your progress:
- [ ] Update activeContext.md on focus changes
- [ ] Record discovered patterns in patterns.md
- [ ] Validate memory files before compaction

## Resources

- [06-context-update-patterns](references/06-context-update-patterns.md) — Update pattern types and procedures
  - Purpose
  - Update Patterns Overview
  - Part Files
  - Quick Reference
  - Troubleshooting Quick Links
- [05-record-patterns](references/05-record-patterns.md) — Pattern recording fundamentals
  - Parts
  - Quick Navigation
  - Reading Order
- [07-pattern-categories](references/07-pattern-categories.md) — Pattern category definitions
  - Purpose
  - Category Definitions
  - Pattern Category Details
  - Choosing the Right Category
  - Part Files Reference
- [11-compaction-safety](references/11-compaction-safety.md) — Compaction safety checks
  - Parts
  - Quick Reference
- [14-context-sync](references/14-context-sync.md) — Context synchronization
  - Overview
  - Document Parts
  - Quick Reference
- [04-memory-validation](references/04-memory-validation.md) — Memory validation procedures
  - Document Parts
  - Quick Reference
