# Using Memory Scripts - Part 2: Advanced Scripts & Workflows

## Table of Contents

1. [Advanced Scripts](#advanced-scripts)
   - [Compact Memory](#compact-memory-amcos_memory_managerpy-compact) - `amcos_memory_manager.py compact`
   - [repair-memory.py](#repair-memorypy) - Fix corrupted memory
2. [Common Workflows](#common-workflows)
   - [Daily Startup](#workflow-1-daily-startup)
   - [Before Compaction](#workflow-2-before-compaction)
   - [Weekly Maintenance](#workflow-3-weekly-maintenance)
   - [Emergency Recovery](#workflow-4-emergency-recovery)
3. [Integration Examples](#examples)
4. [Troubleshooting](#troubleshooting)

**See Also:** [Part 1: Basic Scripts](18-using-scripts-part1-basic-scripts.md)

---

## Advanced Scripts

### Compact Memory (amcos_memory_manager.py compact)

**Purpose:** Archive old completed tasks and patterns by compacting memory files. This replaces the old `archive-memory.py` script.

**Command:** `amcos_memory_manager.py compact`

The `compact` subcommand calls `compact_memory()` which backs up all memory files (using `backup_file()` to create timestamped backups), then removes old date sections from `progress.md` (by cutoff date) and trims old errors from `activeContext.md`.

**Usage:**
```bash
python scripts/amcos_memory_manager.py compact
```

**Examples:**

**Example 1: Compact memory**
```bash
python scripts/amcos_memory_manager.py compact
```

Output:
```
Backing up memory files...
  Created backup: design/memory/backups/activeContext.md.backup.20260101-180000
  Created backup: design/memory/backups/progress.md.backup.20260101-180000

Compacting progress.md...
  Removed 45 old entries (older than 30 days)

Compacting activeContext.md...
  Trimmed 12 old error entries

Compaction complete.
```

**When to use:**
- Memory files exceed 150KB
- Slow session initialization
- Regular maintenance

---

### repair-memory.py

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

## Common Workflows

### Workflow 1: Daily Startup

```bash
# 1. Validate memory
python scripts/amcos_memory_manager.py validate

# 2. Check memory health to understand current state
python scripts/amcos_memory_manager.py health

# 3. Begin work (agent reads memory files directly into context)...
```

---

### Workflow 2: Before Compaction

```bash
# 1. Ensure all current state is persisted (writes are immediate, but verify)
python scripts/amcos_memory_manager.py validate

# 2. Check memory health
python scripts/amcos_memory_manager.py health

# 3. Ready for compaction
```

---

### Workflow 3: Weekly Maintenance

```bash
# 1. Compact old content (creates backups automatically)
python scripts/amcos_memory_manager.py compact

# 2. Validate after compaction
python scripts/amcos_memory_manager.py validate

# 3. Check file sizes
du -h design/memory/*.md
```

---

### Workflow 4: Emergency Recovery

```bash
# 1. Assess damage
python scripts/amcos_memory_manager.py validate

# 2. Check health for details
python scripts/amcos_memory_manager.py health --json

# 3. If memory is corrupted beyond repair, reinitialize
python scripts/amcos_memory_manager.py init
```

---

## Examples

### Example: Integrating into Agent Workflow

```python
# In agent main loop

def initialize_session():
    """Check memory health at startup using amcos_memory_manager.py."""
    result = subprocess.run(
        ['python', 'scripts/amcos_memory_manager.py', 'health', '--json'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error checking memory health:", result.stderr)
        # Attempt reinitialization
        subprocess.run(['python', 'scripts/amcos_memory_manager.py', 'init'])
        return initialize_session()  # Retry

    state = json.loads(result.stdout)
    return state

def persist_decision(decision_text):
    """Persist a decision immediately using amcos_memory_manager.py.
    Note: writes are immediate, no deferred save needed."""
    result = subprocess.run(
        ['python', 'scripts/amcos_memory_manager.py', 'add-decision', decision_text],
        capture_output=True
    )

    if result.returncode != 0:
        print("Error persisting decision:", result.stderr)
        return False

    return True
```

---

## Troubleshooting

### Issue: Script fails with "module not found"

**Cause:** Missing Python dependencies

**Solution:**
```bash
pip install -r requirements.txt
# Or for scripts specifically:
pip install markdown pyyaml
```

---

### Issue: Permission denied

**Cause:** Scripts not executable

**Solution:**
```bash
chmod +x scripts/*.py
# Or run with python explicitly:
python scripts/amcos_memory_manager.py validate
```

---

### Issue: Script reports errors but files look OK

**Cause:** Script validation rules may be too strict

**Solution:**
1. Review reported errors manually
2. Use `--verbose` to understand what failed
3. Fix actual issues or adjust validation rules

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Chief of Staff Agents
**Related:** [Part 1: Basic Scripts](18-using-scripts-part1-basic-scripts.md), SKILL.md (Implementation Scripts section)
