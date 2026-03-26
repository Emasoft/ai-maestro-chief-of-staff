---
name: amcos-memory-initialization
description: Use when initializing session memory. Trigger with new sessions or recovery.
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

### Fundamentals

Session memory uses three files: `activeContext.md` (current work), `patterns.md` (learned patterns), `progress.md` (task tracking). Details: see 00-session-memory-fundamentals in Resources

### Lifecycle

Three phases: **Load** (read and validate at start), **Update** (write changes during work), **Save** (persist before exit). Details: see 00-session-memory-lifecycle in Resources

### PROCEDURE 1: Initialize Session Memory

**Trigger:** Session start, post-compaction, post-interruption, or memory recreation.

1. Check `design/memory/` exists; create if missing
2. Read all three memory files
3. Validate Markdown syntax and required sections
4. Create missing files from templates
5. Report loaded state (sizes, counts, issues)

**Directory structure:** see 02-memory-directory-structure in Resources

**Runbook:** see op-initialize-session-memory in Resources

### Checklist

Copy this checklist and track your progress:

- [ ] Validate `design/memory/` directory and three memory files exist
- [ ] Initialize missing files from templates
- [ ] Run Markdown validation on all memory files

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
| Invalid Markdown | Run validation, fix errors per 02-memory-directory-structure
| Empty files | Re-initialize with templates |
| Permission denied | Check file system permissions |

## Examples

```bash
# Initialize new session memory
uv run python scripts/amcos_memory_manager.py init \
  --session amoa-project-alpha --project project-alpha

# Verify initialization
uv run python scripts/amcos_memory_manager.py validate
```

**Expected result:** `design/memory/` created with `activeContext.md`, `patterns.md`, `progress.md` populated from templates.

## Resources

- [00-session-memory-fundamentals](references/00-session-memory-fundamentals.md) — Memory components
  - What Is Session Memory
  - Key Characteristics
  - Session Memory Components
- [00-session-memory-lifecycle](references/00-session-memory-lifecycle.md) — Lifecycle phases
  - Overview
  - Phase 1: Session Initialization (Load)
  - Phase 2: Session Execution (Update)
  - Phase 3: Session Termination (Save)
- [02-memory-directory-structure](references/02-memory-directory-structure.md) — Directory layout
  - Purpose
  - Canonical Structure
  - Directory Descriptions
  - File Naming Conventions
  - Structure Validation
  - Examples
  - Troubleshooting
- [op-initialize-session-memory](references/op-initialize-session-memory.md) — Initialization runbook
  - Purpose
  - When To Use This Operation
  - Session Memory Components
  - Steps
  - Checklist
  - Output
  - Directory Structure
  - Related References
  - Next Operation

