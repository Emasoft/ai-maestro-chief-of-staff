# Recovery Procedures

## Table of Contents

1. [When you need to understand the purpose](#purpose)
2. [Understanding recovery scenarios](#recovery-scenarios)
3. [Recovering from failed compaction](#recovery-from-failed-compaction)
4. [Recovering from corrupted memory](#recovery-from-corrupted-memory)
5. [Recovering from lost context](#recovery-from-lost-context)
6. [Recovering from snapshot failure](#recovery-from-snapshot-failure)
7. [Emergency recovery procedures](#emergency-recovery)
8. [For implementation examples](#examples)
9. [If issues occur](#troubleshooting)

## Purpose

Recovery procedures restore session memory to a working state after failures. Effective recovery procedures:
- Minimize data loss
- Restore functionality quickly
- Prevent recurring failures
- Maintain data integrity
- Document recovery actions

## Recovery Scenarios

### Scenario Matrix

| Scenario | Severity | Recovery Time | Data Loss Risk | Primary Method |
|----------|----------|---------------|----------------|----------------|
| Failed compaction | High | 5-15 min | Medium | Restore from pre-compaction archive |
| Corrupted file | Medium | 2-5 min | Low | Restore from snapshot |
| Lost context | Medium | 5-10 min | Medium | Reconstruct from snapshots |
| Snapshot failure | Low | 1-2 min | Low | Create new snapshot |
| Complete memory loss | Critical | 15-30 min | High | Rebuild from git/docs |
| Broken symlinks | Low | 1 min | None | Recreate symlinks |

### Quick Reference: Which Part to Read

**If you need to recover from failed compaction:**
- See Recovery from Failed Compaction section below
- Contains: Stop operations, identify last good state, restore from archive, validate, document

**If you have corrupted files or lost context:**
- See Recovery from Corrupted Memory section below
- Contains: File corruption recovery, context reconstruction, source mining

**If snapshots fail or you need emergency recovery:**
- See Recovery from Snapshot Failure section below
- Contains: Disk space checks, permission fixes, complete memory rebuild

---

## Recovery Decision Tree

```
┌─────────────────────────────────────┐
│ Session Memory Issue Detected       │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ Can you read the memory files?      │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │ YES               │ NO
        ▼                   ▼
┌───────────────┐   ┌───────────────────┐
│ Files corrupt?│   │ Directory exists? │
└───────┬───────┘   └─────────┬─────────┘
        │                     │
   ┌────┴────┐          ┌─────┴─────┐
   │ YES     │ NO       │ YES       │ NO
   ▼         ▼          ▼           ▼
┌──────┐  ┌──────┐   ┌──────┐   ┌──────┐
│Part 2│  │Part 1│   │Part 3│   │Part 3│
│Corr. │  │Comp. │   │Snap. │   │Emerg.│
└──────┘  └──────┘   └──────┘   └──────┘
```

## General Recovery Principles

### Before Any Recovery

1. **Stop all operations** - Don't make changes during recovery
2. **Assess the damage** - Understand what's broken
3. **Backup current state** - Even corrupted state might have useful data
4. **Identify sources** - What backups/snapshots are available?

### During Recovery

1. **Follow the procedure** - Don't skip steps
2. **Document actions** - Record what you do
3. **Validate after each step** - Verify changes worked
4. **Don't rush** - Careful recovery prevents additional problems

### After Recovery

1. **Full validation** - Run all validation scripts
2. **Create new snapshot** - Protect the restored state
3. **Document the incident** - What happened, why, how fixed
4. **Review and prevent** - How to avoid recurrence

---

## Recovery Procedure Summaries

**Failed Compaction Recovery:**
1. Stop All Operations
2. Identify Last Good State
3. Restore from Archive
4. Validate Restored State
5. Document Recovery

**Corruption and Context Recovery:**
- Restore from snapshot or backup
- Reconstruct from conversation history
- Source mining from git/docs

**Snapshot and Emergency Recovery:**
- Check disk space and permissions
- Rebuild snapshot from current state
- Complete memory rebuild from sources
