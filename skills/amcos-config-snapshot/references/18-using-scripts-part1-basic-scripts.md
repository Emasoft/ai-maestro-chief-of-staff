# Using Memory Scripts - Part 1: Basic Operations

## Table of Contents

1. [Overview](#overview)
   - What Are Memory Scripts?
   - Why Use Scripts?
2. [Available Commands](#available-commands)
3. [Basic Operations](#basic-operations)
   - [Initialize Memory](#initialize-memory) - `amcos_memory_manager.py init`
   - [Validate Memory](#validate-memory) - `amcos_memory_manager.py validate`
   - [Check Memory Health](#check-memory-health) - `amcos_memory_manager.py health --json`
   - [Update Memory](#update-memory) - `amcos_memory_manager.py` add-* subcommands

**See Also:** [Part 2: Advanced Scripts & Workflows](18-using-scripts-part2-advanced-workflows.md)

---

## Overview

### What Are Memory Scripts?

Memory operations are provided by the unified `amcos_memory_manager.py` script in the `scripts/` subdirectory. This script exposes subcommands for all common memory tasks and can be used manually or integrated into agent workflows. The individual standalone scripts (`initialize-memory.py`, `validate-memory.py`, `load-memory.py`, `save-memory.py`) have been superseded by subcommands of `amcos_memory_manager.py`.

### Why Use Scripts?

**Benefits:**
- Consistent memory operations
- Automated validation
- Error handling built-in
- Batch operations support
- Standardized output formats

---

## Available Commands

### Command Inventory

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `amcos_memory_manager.py init` | Create new memory structure | None | Memory files created |
| `amcos_memory_manager.py validate` | Check memory integrity | Memory files | Validation report |
| `amcos_memory_manager.py health --json` | Report on memory state | Memory files | Health report (JSON) |
| `amcos_memory_manager.py add-decision\|set-focus\|add-progress\|add-pattern` | Persist changes to memory | Update data | Updated memory files (immediate write) |
| `amcos_memory_manager.py compact` | Archive old content | Memory files | Compacted files with backups |
| `repair-memory.py` | Fix corrupted memory (planned) | Corrupted files | Repaired files |

---

## Basic Operations

### Initialize Memory

**Purpose:** Create new session memory structure with template files.

**Command:** `amcos_memory_manager.py init`

**Usage:**
```bash
python scripts/amcos_memory_manager.py init
```

The `init` subcommand calls `initialize_memory()` which creates the `design/memory/` directory and populates it with template files for `activeContext.md`, `progress.md`, and `patterns.md`.

**Examples:**

**Example 1: Basic initialization**
```bash
python scripts/amcos_memory_manager.py init
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

### Validate Memory

**Purpose:** Validate memory files for correctness and consistency.

**Command:** `amcos_memory_manager.py validate`

**Usage:**
```bash
python scripts/amcos_memory_manager.py validate
```

The `validate` subcommand calls `validate_memory()` which checks that the memory directory exists, validates required sections in `activeContext.md` (such as `## Current Focus` and `## Active Decisions`), and checks that `progress.md` and `patterns.md` exist.

**Examples:**

**Example 1: Basic validation**
```bash
python scripts/amcos_memory_manager.py validate
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

### Check Memory Health

**Purpose:** Load and report on all memory files, showing file sizes, entry counts, and any issues.

**Command:** `amcos_memory_manager.py health --json`

This replaces the concept of the old `load-memory.py` script. "Loading memory" into agent context is an agent-level operation (the agent reads the files directly into its context window). The `health` subcommand provides a structured report of the memory state for diagnostics.

**Usage:**
```bash
python scripts/amcos_memory_manager.py health
python scripts/amcos_memory_manager.py health --json
```

**Examples:**

**Example 1: Health check (text output)**
```bash
python scripts/amcos_memory_manager.py health
```

Output:
```
Memory Health Report:
  activeContext.md: 12KB, 3 decisions, 1 focus set
  progress.md: 8KB, 25 entries (12 completed)
  patterns.md: 5KB, 8 patterns

No issues found.
```

**Example 2: Health check (JSON output)**
```bash
python scripts/amcos_memory_manager.py health --json
```

Output:
```json
{
  "activeContext": {"size_kb": 12, "decisions": 3, "focus_set": true},
  "progress": {"size_kb": 8, "entries": 25, "completed": 12},
  "patterns": {"size_kb": 5, "count": 8},
  "issues": []
}
```

**When to use:**
- Session initialization (to understand current memory state)
- After context compaction (to verify memory survived)
- Resuming interrupted work (to assess what is available)

---

### Update Memory

**Purpose:** Persist changes to memory files immediately.

**Commands:** Various `amcos_memory_manager.py` subcommands for writing data.

All write operations are handled by specific subcommands. Memory is persisted immediately on each operation via `write_file_safely()` in `amcos_memory_operations.py`. There is no deferred "save" concept -- every subcommand writes to disk immediately.

**Available write subcommands:**
```bash
# Record a decision in activeContext.md
python scripts/amcos_memory_manager.py add-decision "Use PostgreSQL for persistence"

# Set the current focus in activeContext.md
python scripts/amcos_memory_manager.py set-focus "Implementing auth middleware"

# Log an error in activeContext.md
python scripts/amcos_memory_manager.py log-error "Connection timeout to database"

# Clear all errors from activeContext.md
python scripts/amcos_memory_manager.py clear-errors

# Get recent errors from activeContext.md
python scripts/amcos_memory_manager.py get-errors

# Add a progress entry to progress.md
python scripts/amcos_memory_manager.py add-progress "Completed login endpoint implementation"

# Add a pattern to patterns.md
python scripts/amcos_memory_manager.py add-pattern "Fail-Fast Error Propagation" "Let errors propagate, handle at boundary layers only"

# Search patterns in patterns.md
python scripts/amcos_memory_manager.py search-patterns "error"
```

**When to use:**
- During active work sessions (to record decisions, progress, patterns as they happen)
- Before context compaction (to ensure all current state is persisted)
- Before session termination (to capture final state)

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Chief of Staff Agents
**Related:** [Part 2: Advanced Scripts & Workflows](18-using-scripts-part2-advanced-workflows.md)
