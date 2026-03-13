---
name: amcos-memory-initialization
description: Use when initializing session memory at session start, understanding memory fundamentals, or setting up directory structure. Trigger with session initialization or memory setup.
user-invocable: false
license: Apache-2.0
compatibility: Requires file system access to design/memory/ directory. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Session Memory Initialization

## Overview

Initializes and validates the three session memory documents (`activeContext.md`, `patterns.md`, `progress.md`) in `design/memory/`. Covers memory fundamentals, lifecycle phases, and the initialization procedure.

## Prerequisites

- File system write access to `design/memory/`
- AI Maestro installed and configured

## Instructions

Copy this checklist and track your progress:
- [ ] Validate memory dir and files
- [ ] Init missing files from templates

### Fundamentals

Session memory uses three files: `activeContext.md` (current work), `patterns.md` (learned patterns), `progress.md` (task tracking). Details: `references/00-session-memory-fundamentals.md`.

### Lifecycle

Three phases: **Load** (read and validate at start), **Update** (write changes during work), **Save** (persist before exit). Details: `references/00-session-memory-lifecycle.md`.

### PROCEDURE 1: Initialize Session Memory

**Trigger:** Session start, post-compaction, post-interruption, or memory recreation.

1. Check `design/memory/` exists; create if missing
2. Read all three memory files
3. Validate Markdown syntax and required sections
4. Create missing files from templates
5. Report loaded state (sizes, counts, issues)

**Initialization guide:** `references/01-initialize-session-memory.md`

**Directory structure:** `references/02-memory-directory-structure.md`

**Runbook:** `references/op-initialize-session-memory.md`

## Output

| Step | Result |
|------|--------|
| Directory check | `design/memory/` exists or created |
| File loading | Three files read successfully |
| Validation | Required sections present, valid Markdown |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Directory missing | Create it and initialize empty files from templates |
| Invalid Markdown | Run validation, fix errors per `references/02-memory-directory-structure.md` |
| Empty files | Re-initialize with templates |
| Permission denied | Check file system permissions |

## Examples

```bash
# Initialize new session memory
uv run python scripts/amcos_memory_manager.py init \
  --session eoa-project-alpha --project project-alpha

# Verify initialization
uv run python scripts/amcos_memory_manager.py validate
```

More examples: `references/00-session-memory-examples.md`.

## Resources

- `references/00-session-memory-fundamentals.md`
- `references/00-session-memory-lifecycle.md`
- `references/00-session-memory-examples.md`
- `references/01-initialize-session-memory.md` - Initialization guide
- `references/02-memory-directory-structure.md` - Directory layout
- `references/op-initialize-session-memory.md` - Operational runbook
- `references/state-file-format.md` - State file format

---

**Version:** 1.0.0 | **Last Updated:** 2025-02-01
