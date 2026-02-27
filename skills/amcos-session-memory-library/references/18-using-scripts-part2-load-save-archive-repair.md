# Using Memory Scripts: Health Check, Update, Compact, and Repair

## Table of Contents

1. [Check Memory Health](#check-memory-health) - `ecos_memory_manager.py health`
2. [Update Memory](#update-memory) - `ecos_memory_manager.py` add-* subcommands
3. [Compact Memory](#compact-memory) - `ecos_memory_manager.py compact`
4. [repair-memory.py](#repair-memorypy) (planned)

---

## Check Memory Health

**Purpose:** Load and report on all memory files, showing file sizes, entry counts, and any issues. This replaces the concept of the old `load-memory.py` script. "Loading memory" into agent context is an agent-level operation (the agent reads the files directly into its context window). The `health` subcommand provides a structured report of the memory state for diagnostics.

**Command:** `ecos_memory_manager.py health`

**Usage:**
```bash
python scripts/ecos_memory_manager.py health
python scripts/ecos_memory_manager.py health --json
```

**Examples:**

**Example 1: Health check (text output)**
```bash
python scripts/ecos_memory_manager.py health
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
python scripts/ecos_memory_manager.py health --json
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

## Update Memory

**Purpose:** Persist changes to memory files immediately. This replaces the concept of the old `save-memory.py` script. All write operations are handled by specific subcommands of `ecos_memory_manager.py`. Memory is persisted immediately on each operation via `write_file_safely()` in `ecos_memory_operations.py`. There is no deferred "save" concept.

**Commands:** Various `ecos_memory_manager.py` subcommands:

```bash
# Record a decision in activeContext.md
python scripts/ecos_memory_manager.py add-decision "Use PostgreSQL for persistence"

# Set the current focus in activeContext.md
python scripts/ecos_memory_manager.py set-focus "Implementing auth middleware"

# Log an error in activeContext.md
python scripts/ecos_memory_manager.py log-error "Connection timeout to database"

# Clear all errors from activeContext.md
python scripts/ecos_memory_manager.py clear-errors

# Get recent errors from activeContext.md
python scripts/ecos_memory_manager.py get-errors

# Add a progress entry to progress.md
python scripts/ecos_memory_manager.py add-progress "Completed login endpoint implementation"

# Add a pattern to patterns.md
python scripts/ecos_memory_manager.py add-pattern "Fail-Fast Error Propagation" "Let errors propagate, handle at boundary layers only"

# Search patterns in patterns.md
python scripts/ecos_memory_manager.py search-patterns "error"
```

**When to use:**
- During active work sessions (to record decisions, progress, patterns as they happen)
- Before context compaction (to ensure all current state is persisted)
- Before session termination (to capture final state)

---

## Compact Memory

**Purpose:** Archive old completed tasks and patterns by compacting memory files. This replaces the old `archive-memory.py` script.

**Command:** `ecos_memory_manager.py compact`

The `compact` subcommand calls `compact_memory()` which backs up all memory files (using `backup_file()` to create timestamped backups), then removes old date sections from `progress.md` (by cutoff date) and trims old errors from `activeContext.md`.

**Usage:**
```bash
python scripts/ecos_memory_manager.py compact
```

**Examples:**

**Example 1: Compact memory**
```bash
python scripts/ecos_memory_manager.py compact
```

Output:
```
Backing up memory files...
  Created backup: design/memory/backups/activeContext.md.backup.20260101-180000
  Created backup: design/memory/backups/progress.md.backup.20260101-180000
  Created backup: design/memory/backups/patterns.md.backup.20260101-180000

Compacting progress.md...
  Removed 45 old entries (older than 30 days)

Compacting activeContext.md...
  Trimmed 12 old error entries

Compaction complete.
```

**When to use:**
- Memory files exceed 150KB
- Slow session initialization
- Regular maintenance (weekly)

---

## repair-memory.py

**Purpose:** Recover from corrupted or invalid memory files.

**Usage:**
```bash
python scripts/repair-memory.py [OPTIONS]
```

**Options:**
- `--directory DIR` - Memory directory
- `--file FILE` - Specific file to repair
- `--method METHOD` - Repair method (backup, reconstruct, manual)
- `--force` - Skip confirmation prompts

**Examples:**

**Example 1: Auto repair**
```bash
python scripts/repair-memory.py
```

Output:
```
Analyzing memory files...

activeContext.md: Corrupted (truncated)
patterns.md: OK
progress.md: OK

Attempting repair of activeContext.md...
Method: Restore from backup
Latest backup: backups/activeContext.md.backup.20251231-170000

Restoring... Done
Verifying... OK

Repair successful.
```

**Example 2: Specific file repair**
```bash
python scripts/repair-memory.py --file activeContext.md --method reconstruct
```

Output:
```
Repairing activeContext.md using reconstruction method...

Extracting from conversation history... Done
Reconstructing file... Done
Validating... OK

File repaired successfully.
WARNING: Some data may be incomplete. Review and update as needed.
```

**When to use:**
- Corrupted memory files
- After crash or interruption
- Failed memory operations

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Related:** [18-using-scripts.md](18-using-scripts.md) (Main index)
