# Using Memory Scripts

## Overview

Memory operations are provided by the unified `ecos_memory_manager.py` script in the `scripts/` subdirectory. This script exposes subcommands for all common memory tasks and can be used manually or integrated into agent workflows. The individual standalone scripts (`initialize-memory.py`, `validate-memory.py`, `load-memory.py`, `save-memory.py`, `archive-memory.py`) have been superseded by subcommands of `ecos_memory_manager.py`.

**Benefits:**
- Consistent memory operations via a single unified CLI
- Automated validation
- Error handling built-in
- Immediate persistence (writes happen on each operation)
- Standardized output formats

---

## Table of Contents

This document is split into parts for efficient loading. Read the section relevant to your current task.

### Part 1: Initialize and Validate

**File:** [18-using-scripts-part1-initialize-validate.md](18-using-scripts-part1-initialize-validate.md)

**Contents:**
- 1.1 Overview - What are memory scripts and why use them
- 1.2 Available Commands - Full inventory table of all `ecos_memory_manager.py` subcommands
- 1.3 Initialize Memory - `ecos_memory_manager.py init` for creating new memory structure
  - 1.3.1 Basic initialization for new projects
- 1.4 Validate Memory - `ecos_memory_manager.py validate` for checking memory integrity
  - 1.4.1 Basic validation workflow

**When to read:** Starting new projects, setting up memory, validating after manual edits

---

### Part 2: Health Check, Update, Compact, and Repair

**File:** [18-using-scripts-part2-load-save-archive-repair.md](18-using-scripts-part2-load-save-archive-repair.md)

**Contents:**
- 2.1 Check Memory Health - `ecos_memory_manager.py health` for reporting on memory state
  - 2.1.1 Health check text output
  - 2.1.2 Health check JSON output
- 2.2 Update Memory - `ecos_memory_manager.py` add-* subcommands for immediate persistence
  - 2.2.1 Available write subcommands (add-decision, set-focus, add-progress, add-pattern, etc.)
- 2.3 Compact Memory - `ecos_memory_manager.py compact` for archiving old content
  - 2.3.1 Compact with automatic backup
- 2.4 repair-memory.py - Recovering from corruption (planned)

**When to read:** Session initialization, compaction prep, maintenance, recovery

---

### Part 3: Workflows, Examples, and Troubleshooting

**File:** [18-using-scripts-part3-workflows-examples.md](18-using-scripts-part3-workflows-examples.md)

**Contents:**
- 3.1 Common Workflows (all using `ecos_memory_manager.py` subcommands)
  - 3.1.1 Daily Startup workflow
  - 3.1.2 Before Compaction workflow
  - 3.1.3 Weekly Maintenance workflow
  - 3.1.4 Emergency Recovery workflow
- 3.2 Implementation Examples
  - 3.2.1 Python integration for agent workflows
- 3.3 Troubleshooting
  - 3.3.1 Module not found errors
  - 3.3.2 Permission denied issues
  - 3.3.3 False positive validation errors

**When to read:** Daily operations, integrating scripts into agents, fixing issues

---

## Quick Reference: Command Inventory

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `ecos_memory_manager.py init` | Create new memory structure | New project setup |
| `ecos_memory_manager.py validate` | Check memory integrity | After manual edits, before compaction |
| `ecos_memory_manager.py health --json` | Report on memory state | Session start, after compaction |
| `ecos_memory_manager.py add-decision\|set-focus\|add-progress\|add-pattern` | Persist changes immediately | During work, before compaction |
| `ecos_memory_manager.py compact` | Archive old content | Weekly maintenance |
| `repair-memory.py` | Fix corrupted memory (planned) | After crashes, corruption |

---

## Quick Reference: Common Commands

```bash
# Daily startup
python scripts/ecos_memory_manager.py validate
python scripts/ecos_memory_manager.py health

# Before compaction
python scripts/ecos_memory_manager.py validate
python scripts/ecos_memory_manager.py health

# Weekly maintenance
python scripts/ecos_memory_manager.py compact
python scripts/ecos_memory_manager.py validate

# Emergency recovery
python scripts/ecos_memory_manager.py validate
python scripts/ecos_memory_manager.py health --json
python scripts/ecos_memory_manager.py init  # If beyond repair
```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** SKILL.md (Implementation Scripts section)
