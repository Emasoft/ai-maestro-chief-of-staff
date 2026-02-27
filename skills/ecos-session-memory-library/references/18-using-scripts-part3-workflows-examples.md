# Using Memory Scripts: Workflows, Examples, and Troubleshooting

## Table of Contents

1. [Common Workflows](#common-workflows)
   - [Daily Startup](#workflow-1-daily-startup)
   - [Before Compaction](#workflow-2-before-compaction)
   - [Weekly Maintenance](#workflow-3-weekly-maintenance)
   - [Emergency Recovery](#workflow-4-emergency-recovery)
2. [Implementation Examples](#examples)
3. [Troubleshooting](#troubleshooting)

---

## Common Workflows

### Workflow 1: Daily Startup

```bash
# 1. Validate memory
python scripts/ecos_memory_manager.py validate

# 2. Check memory health to understand current state
python scripts/ecos_memory_manager.py health

# 3. Begin work (agent reads memory files directly into context)...
```

---

### Workflow 2: Before Compaction

```bash
# 1. Ensure all current state is persisted (writes are immediate, but verify)
python scripts/ecos_memory_manager.py validate

# 2. Check memory health
python scripts/ecos_memory_manager.py health

# 3. Ready for compaction
```

---

### Workflow 3: Weekly Maintenance

```bash
# 1. Compact old content (creates backups automatically)
python scripts/ecos_memory_manager.py compact

# 2. Validate after compaction
python scripts/ecos_memory_manager.py validate

# 3. Check file sizes
du -h design/memory/*.md
```

---

### Workflow 4: Emergency Recovery

```bash
# 1. Assess damage
python scripts/ecos_memory_manager.py validate

# 2. Check health for details
python scripts/ecos_memory_manager.py health --json

# 3. If memory is corrupted beyond repair, reinitialize
python scripts/ecos_memory_manager.py init
```

---

## Examples

### Example: Integrating into Agent Workflow

```python
# In agent main loop

def initialize_session():
    """Check memory health at startup using ecos_memory_manager.py."""
    result = subprocess.run(
        ['python', 'scripts/ecos_memory_manager.py', 'health', '--json'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error checking memory health:", result.stderr)
        # Attempt reinitialization
        subprocess.run(['python', 'scripts/ecos_memory_manager.py', 'init'])
        return initialize_session()  # Retry

    state = json.loads(result.stdout)
    return state

def persist_decision(decision_text):
    """Persist a decision immediately using ecos_memory_manager.py.
    Note: writes are immediate, no deferred save needed."""
    result = subprocess.run(
        ['python', 'scripts/ecos_memory_manager.py', 'add-decision', decision_text],
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
python scripts/ecos_memory_manager.py validate
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
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** [18-using-scripts.md](18-using-scripts.md) (Main index)
