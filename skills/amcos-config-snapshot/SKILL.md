---
name: amcos-config-snapshot
description: Use when capturing config snapshots, detecting config changes, or resolving config version conflicts. Trigger with config management or snapshot needs.
user-invocable: false
license: Apache-2.0
compatibility: Requires file system access to design/memory/ directory. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-main
---

# Config Snapshot Management

## Overview

Captures config state at session start, detects drift, and resolves conflicts. Covers Chief of Staff integrations.

## Prerequisites

- Session memory initialized (`amcos-memory-initialization`)
- Config files in `design/config/` (if EOA installed)

## Instructions

### PROCEDURE 7: Capture Config Snapshot

**Trigger:** Session init, after loading memory, before work.

1. Read configs from `design/config/`
2. Create snapshot with timestamp, session ID, and file hashes
3. Save to `design/memory/config-snapshot.md`; record in `activeContext.md`

**Guide:** [references/19-config-snapshot-creation.md](references/19-config-snapshot-creation.md)
  <!-- TOC: 19-config-snapshot-creation.md -->
  - What Is A Config Snapshot
  - Procedure 1: Create Initial Snapshot
  - Snapshot Structure
  - ...and 5 more sections
  <!-- /TOC -->

**Runbook:** [references/op-capture-config-snapshot.md](references/op-capture-config-snapshot.md)

### PROCEDURE 8: Detect Config Changes

**Trigger:** Every 30 min, after notifications, before major tasks, on unexpected behavior.

1. Read current configs and saved snapshot
2. Compare timestamps; if different, compare hashes
3. Classify changes and log in `activeContext.md`; trigger Procedure 9 if critical

**Guide:** [references/20-config-change-detection.md](references/20-config-change-detection.md)
  <!-- TOC: 20-config-change-detection.md -->
  - Detection Methods
  - Timestamp Based Detection
  - Content Based Detection
  - ...and 5 more sections
  <!-- /TOC -->

**Runbook:** [references/op-detect-config-changes.md](references/op-detect-config-changes.md)

### PROCEDURE 9: Handle Config Conflicts

**Trigger:** Critical changes detected, incompatible work, or orchestrator request.

Types: **A** Non-Breaking (adopt now), **B** Breaking-Future (finish task, adopt), **C** Breaking-Immediate (pause, adopt, restart), **D** Irreconcilable (stop, escalate).

Steps: Classify (A-D), apply strategy, update snapshot, record in `activeContext.md`.

**Guide:** [references/21-config-conflict-resolution.md](references/21-config-conflict-resolution.md)
  <!-- TOC: 21-config-conflict-resolution.md -->
  - Conflict Types and Resolution Strategies
  - Resolution Procedures 1-2
  - Resolution Procedures 3-4
  - ...and 2 more sections
  <!-- /TOC -->

**Runbook:** [references/op-handle-config-conflicts.md](references/op-handle-config-conflicts.md)

### Chief of Staff Integrations

See [ai-maestro-integration.md](references/ai-maestro-integration.md) (messaging), [error-handling.md](references/error-handling.md) (fail-fast), [00-key-takeaways-and-next-steps.md](references/00-key-takeaways-and-next-steps.md) (principles).

## Output

| Procedure | Result |
|-----------|--------|
| Capture Snapshot | `config-snapshot.md` with timestamps and hashes |
| Detect Changes | Change report in `activeContext.md` |
| Handle Conflicts | Conflict resolved per type, snapshot updated |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Config dir missing | Skip if EOA not installed; log warning |
| Snapshot corrupted | Re-capture from current configs |
| Hash mismatch | Recalculate; check encoding |
| Irreconcilable conflict | Stop work, escalate |

## Examples

```bash
# Capture snapshot at session start
uv run python scripts/amcos_memory_manager.py add-decision \
  --decision "Config snapshot captured" --rationale "Session start"

# Adopt config after Type B detection
uv run python scripts/amcos_memory_manager.py set-focus \
  --focus "Adopting config v2.1 (Type B)" --previous "Task done"
```

## Resources

- [references/19-config-snapshot-creation.md](references/19-config-snapshot-creation.md) - Snapshots
- [references/20-config-change-detection.md](references/20-config-change-detection.md) - Detection
- [references/21-config-conflict-resolution.md](references/21-config-conflict-resolution.md) - Conflicts
- [references/op-capture-config-snapshot.md](references/op-capture-config-snapshot.md) - Runbook: capture
- [references/op-detect-config-changes.md](references/op-detect-config-changes.md) - Runbook: detect
- [references/op-handle-config-conflicts.md](references/op-handle-config-conflicts.md) - Runbook: conflicts
- [references/ai-maestro-integration.md](references/ai-maestro-integration.md) - AI Maestro
- [references/error-handling.md](references/error-handling.md) - Errors
- [references/00-key-takeaways-and-next-steps.md](references/00-key-takeaways-and-next-steps.md) - Takeaways

---

**Version:** 1.0.0 | **Last Updated:** 2025-02-01
