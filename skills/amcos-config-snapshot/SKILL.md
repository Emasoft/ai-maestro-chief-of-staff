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

Captures config state at session start, detects drift, and resolves conflicts.

## Prerequisites

- Session memory initialized (`amcos-memory-initialization`)
- Config files in `design/config/` (if EOA installed)

## Instructions

### PROCEDURE 7: Capture Config Snapshot

**Trigger:** Session init, after loading memory, before work.

1. Read configs from `design/config/`
2. Create snapshot with timestamp and file hashes
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

**Trigger:** Every 30 min, before major tasks, on unexpected behavior.

1. Read current configs and saved snapshot
2. Compare timestamps; if different, compare hashes
3. Classify changes; log in `activeContext.md`; trigger Procedure 9 if critical

**Guide:** [references/20-config-change-detection.md](references/20-config-change-detection.md)
  <!-- TOC: 20-config-change-detection.md -->
  - Detection Methods
  - Timestamp Based Detection
  - Content Based Detection
  - ...and 5 more sections
  <!-- /TOC -->

**Runbook:** [references/op-detect-config-changes.md](references/op-detect-config-changes.md)

### PROCEDURE 9: Handle Config Conflicts

**Trigger:** Critical changes detected or orchestrator request.

Types: **A** Non-Breaking, **B** Breaking-Future, **C** Breaking-Immediate, **D** Irreconcilable.

Steps: Classify (A-D), apply strategy, update snapshot.

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
  <!-- TOC: ai-maestro-integration.md -->
  - What Is AI Maestro
  - Core Capabilities
  - Session Management
  - ...and 5 more sections
  <!-- /TOC -->
  <!-- TOC: error-handling.md -->
  - Error Handling Philosophy
  - Error Categories
  - Communication Errors
  - ...and 5 more sections
  <!-- /TOC -->
  <!-- TOC: 00-key-takeaways-and-next-steps.md -->
  - Key Takeaways
  - Next Steps
  - Resources Index
  <!-- /TOC -->

## Output

| Procedure | Result |
|-----------|--------|
| Capture Snapshot | `config-snapshot.md` with hashes |
| Detect Changes | Change report in `activeContext.md` |
| Handle Conflicts | Resolved per type, snapshot updated |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Config dir missing | Skip if EOA not installed; log warning |
| Snapshot corrupted | Re-capture from current configs |
| Hash mismatch | Recalculate; check encoding |
| Irreconcilable conflict | Stop work, escalate |

## Examples

```bash
# Capture snapshot
uv run python scripts/amcos_memory_manager.py add-decision \
  --decision "Config snapshot captured"

# Adopt config after Type B
uv run python scripts/amcos_memory_manager.py set-focus \
  --focus "Adopting config v2.1 (Type B)"
```

## Resources

- [19-config-snapshot-creation.md](references/19-config-snapshot-creation.md)
- [20-config-change-detection.md](references/20-config-change-detection.md)
- [21-config-conflict-resolution.md](references/21-config-conflict-resolution.md)
- [op-capture-config-snapshot.md](references/op-capture-config-snapshot.md)
- [op-detect-config-changes.md](references/op-detect-config-changes.md)
- [op-handle-config-conflicts.md](references/op-handle-config-conflicts.md)
- [ai-maestro-integration.md](references/ai-maestro-integration.md)
- [error-handling.md](references/error-handling.md)
- [00-key-takeaways-and-next-steps.md](references/00-key-takeaways-and-next-steps.md)

---

**Version:** 1.0.0 | **Last Updated:** 2025-02-01
