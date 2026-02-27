# Using Memory Scripts: Initialize and Validate

## Table of Contents

1. [Overview](#overview)
2. [Available Commands](#available-commands)
3. [Initialize Memory](#initialize-memory) - `ecos_memory_manager.py init`
4. [Validate Memory](#validate-memory) - `ecos_memory_manager.py validate`

---

## Overview

### What Are Memory Scripts?

Memory operations are provided by the unified `ecos_memory_manager.py` script in the `scripts/` subdirectory. This script exposes subcommands for all common memory tasks and can be used manually or integrated into agent workflows. The individual standalone scripts (`initialize-memory.py`, `validate-memory.py`, `load-memory.py`, `save-memory.py`, `archive-memory.py`) have been superseded by subcommands of `ecos_memory_manager.py`.

### Why Use Scripts?

**Benefits:**
- Consistent memory operations via a single unified CLI
- Automated validation
- Error handling built-in
- Immediate persistence (writes happen on each operation)
- Standardized output formats

---

## Available Commands

### Command Inventory

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `ecos_memory_manager.py init` | Create new memory structure | None | Memory files created |
| `ecos_memory_manager.py validate` | Check memory integrity | Memory files | Validation report |
| `ecos_memory_manager.py health --json` | Report on memory state | Memory files | Health report (JSON) |
| `ecos_memory_manager.py add-decision\|set-focus\|add-progress\|add-pattern` | Persist changes to memory | Update data | Updated memory files (immediate write) |
| `ecos_memory_manager.py compact` | Archive old content | Memory files | Compacted files with backups |
| `repair-memory.py` | Fix corrupted memory (planned) | Corrupted files | Repaired files |

---

## Initialize Memory

**Purpose:** Create new session memory structure with template files.

**Command:** `ecos_memory_manager.py init`

The `init` subcommand calls `initialize_memory()` which creates the `design/memory/` directory and populates it with template files for `activeContext.md`, `progress.md`, and `patterns.md`.

**Usage:**
```bash
python scripts/ecos_memory_manager.py init
```

**Examples:**

**Example 1: Basic initialization**
```bash
python scripts/ecos_memory_manager.py init
```

Output:
```
Creating memory directory: design/memory
Creating activeContext.md... Done
Creating patterns.md... Done
Creating progress.md... Done
Creating backups directory... Done

Memory structure initialized successfully.
```

**When to use:**
- Starting new project
- After corrupting all memory files
- Setting up test environment

---

## Validate Memory

**Purpose:** Validate memory files for correctness and consistency.

**Command:** `ecos_memory_manager.py validate`

The `validate` subcommand calls `validate_memory()` which checks that the memory directory exists, validates required sections in `activeContext.md` (such as `## Current Focus` and `## Active Decisions`), and checks that `progress.md` and `patterns.md` exist.

**Usage:**
```bash
python scripts/ecos_memory_manager.py validate
```

**Examples:**

**Example 1: Basic validation**
```bash
python scripts/ecos_memory_manager.py validate
```

Output:
```
Validating session memory in design/memory

Checking activeContext.md...
  OK File exists
  OK Required sections present

Checking patterns.md...
  OK File exists

Checking progress.md...
  OK File exists

Validation passed.
```

**When to use:**
- After manual memory edits
- Before context compaction
- During troubleshooting
- Regular maintenance checks

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Related:** [18-using-scripts.md](18-using-scripts.md) (Main index)
