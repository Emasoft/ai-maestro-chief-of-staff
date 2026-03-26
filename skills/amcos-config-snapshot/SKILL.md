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
agent: ai-maestro-chief-of-staff-main-agent
---

# Config Snapshot Management

## Overview

Captures config state at session start, detects drift, and resolves conflicts.

## Prerequisites

- Session memory initialized (`amcos-memory-initialization`)
- Config files in `design/config/` (if AMOA installed)

## Instructions

Copy this checklist and track your progress:
- [ ] Capture config snapshot at session start
- [ ] Detect, classify, and resolve conflicts

### PROCEDURE 7: Capture Config Snapshot

**Trigger:** Session init, after loading memory, before work.

1. Read configs from `design/config/`
2. Create snapshot with timestamp and file hashes
3. Save to `design/memory/config-snapshot.md`; record in `activeContext.md`

**Guide:** [19-config-snapshot-creation](references/19-config-snapshot-creation.md) — Topics: Config Snapshot Creation, Table of Contents, Part Files, Overview, What Is a Config Snapshot?, When to Create Snapshots, What Is a Config Snapshot?, Location, Purpose, Why Snapshots Matter, Without Snapshots, With Snapshots, Creation Procedures, PROCEDURE 1: Create Initial Snapshot, PROCEDURE 2: Update Snapshot, PROCEDURE 3: Validate Snapshot, Snapshot Structure, Examples, Troubleshooting

### PROCEDURE 8: Detect Config Changes

**Trigger:** Every 30 min, before major tasks, on unexpected behavior.

1. Read current configs and saved snapshot
2. Compare timestamps; if different, compare hashes
3. Classify changes; log in `activeContext.md`; trigger Procedure 9 if critical

**Guide:** [20-config-change-detection](references/20-config-change-detection.md) — Topics: Detecting Config Changes, Table of Contents, Part Files, Overview, What Is Config Change Detection?, Why Detection Matters, Detection Methods, Method 1: Timestamp Comparison, Method 2: Content Hash Comparison, Method 3: Line-by-Line Diff, Method 4: Notification-Based, Detection Procedures, PROCEDURE 1: Timestamp-Based Detection, PROCEDURE 2: Content-Based Detection, PROCEDURE 3: Change Notification Handling, PROCEDURE 4: Periodic Drift Check, Change Classification, Examples, Troubleshooting

### PROCEDURE 9: Handle Config Conflicts

**Trigger:** Critical changes detected or orchestrator request.

Types: **A** Non-Breaking, **B** Breaking-Future, **C** Breaking-Immediate, **D** Irreconcilable.

Steps: Classify (A-D), apply strategy, update snapshot.

### Chief of Staff Integrations

## Output

| Procedure | Result |
|-----------|--------|
| Capture Snapshot | `config-snapshot.md` with hashes |
| Detect Changes | Change report in `activeContext.md` |
| Handle Conflicts | Resolved per type, snapshot updated |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Config dir missing | Skip if AMOA not installed; log warning |
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

- [19-config-snapshot-creation](references/19-config-snapshot-creation.md) — Topics: Config Snapshot Creation, Table of Contents, Part Files, Overview, What Is a Config Snapshot?, When to Create Snapshots, What Is a Config Snapshot?, Location, Purpose, Why Snapshots Matter, Without Snapshots, With Snapshots, Creation Procedures, PROCEDURE 1: Create Initial Snapshot, PROCEDURE 2: Update Snapshot, PROCEDURE 3: Validate Snapshot, Snapshot Structure, Examples, Troubleshooting

**Version:** 1.0.0

