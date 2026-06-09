---
name: amcos-config-snapshot-ref
description: Use when consulting detailed config snapshot references. Trigger with config snapshot lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Config Snapshot Reference

## Overview

Reference material for config snapshot. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-config-snapshot` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-config-snapshot` for error handling.

## Examples

```bash
# Look up config snapshot capture procedure
cat references/op-capture-config-snapshot.md | grep -A5 "Step 1"
```

Expected: steps to identify config files and create snapshot header.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the config snapshot topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [ai-maestro-integration](references/ai-maestro-integration.md) — AI Maestro integration, sessions, messaging, health
  - 1.1 [What Is AI Maestro](#11-what-is-ai-maestro)
  - 1.2 [Core Capabilities](#12-core-capabilities)
  - 1.3 [Session Management](#13-session-management)
  - 1.4 [Message Operations](#14-message-operations)
  - 1.5 [Broadcast Operations](#15-broadcast-operations)
  - 1.6 [Health and Status](#16-health-and-status)
  - 1.7 [Integration Examples](#17-integration-examples)
  - 1.8 [Troubleshooting](#18-troubleshooting)
- [op-detect-config-changes](references/op-detect-config-changes.md) — Detect config changes during session
  - [Purpose](#purpose)
  - [When To Use This Operation](#when-to-use-this-operation)
  - [Steps](#steps)
    - [Step 1: Read Current Config Files](#step-1-read-current-config-files)
    - [Step 2: Compare Timestamps](#step-2-compare-timestamps)
    - [Step 3: Perform Content Comparison (if timestamps differ)](#step-3-perform-content-comparison-if-timestamps-differ)
    - [Step 4: Identify Changed Sections](#step-4-identify-changed-sections)
  - [Config Change Detected](#config-change-detected)
    - [Changed Sections](#changed-sections)
    - [Step 5: Log in activeContext.md](#step-5-log-in-activecontextmd)
  - [Session Notes](#session-notes)
    - [Step 6: Trigger Conflict Resolution if Critical](#step-6-trigger-conflict-resolution-if-critical)
  - [Change Classification](#change-classification)
  - [Detection Methods](#detection-methods)
    - [Method 1: Timestamp-Based (Fast)](#method-1-timestamp-based-fast)
    - [Method 2: Hash-Based (Accurate)](#method-2-hash-based-accurate)
  - [Checklist](#checklist)
  - [Periodic Check Schedule](#periodic-check-schedule)
  - [Output](#output)
  - [Related References](#related-references)
  - [Next Operation](#next-operation)
- [21-config-conflict-resolution](references/21-config-conflict-resolution.md) — Resolving config conflicts (Types A-D)
  1. [Overview](#overview)
  2. [Conflict Types and Resolution Strategies](#conflict-types-and-resolution-strategies)
  3. [Resolution Procedures 1-2](#resolution-procedures-1-2)
  4. [Resolution Procedures 3-4](#resolution-procedures-3-4)
  5. [Decision Trees, Examples, Troubleshooting](#decision-trees-examples-troubleshooting)
- [op-capture-config-snapshot](references/op-capture-config-snapshot.md) — Capture config snapshot at session start
  - [Purpose](#purpose)
  - [When To Use This Operation](#when-to-use-this-operation)
  - [Config Snapshot Purpose](#config-snapshot-purpose)
  - [Steps](#steps)
    - [Step 1: Identify Config Files](#step-1-identify-config-files)
    - [Step 2: Create Snapshot Header](#step-2-create-snapshot-header)
  - [Source Files](#source-files)
    - [Step 3: Copy Config Content](#step-3-copy-config-content)
  - [[Config File Name]](#config-file-name)
    - [Content](#content)
    - [Step 4: Calculate File Hashes](#step-4-calculate-file-hashes)
    - [Step 5: Save Snapshot](#step-5-save-snapshot)
    - [Step 6: Record in activeContext.md](#step-6-record-in-activecontextmd)
  - [Session Notes](#session-notes)
  - [Checklist](#checklist)
  - [Snapshot Structure](#snapshot-structure)
  - [Source Files](#source-files)
  - [team-config.yaml](#team-configyaml)
    - [Content](#content)
  - [project-rules.md](#project-rulesmd)
    - [Content](#content)
  - [Output](#output)
  - [Related References](#related-references)
  - [Next Operation](#next-operation)
- [op-handle-config-conflicts](references/op-handle-config-conflicts.md) — Handle config version conflicts
  - [Purpose](#purpose)
  - [When To Use This Operation](#when-to-use-this-operation)
  - [Conflict Types](#conflict-types)
  - [Steps](#steps)
    - [Step 1: Classify the Conflict](#step-1-classify-the-conflict)
  - [Conflict Classification](#conflict-classification)
    - [Step 2A: Resolve Type A (Non-Breaking)](#step-2a-resolve-type-a-non-breaking)
  - [Type A Resolution](#type-a-resolution)
    - [Step 2B: Resolve Type B (Breaking-Future)](#step-2b-resolve-type-b-breaking-future)
  - [Type B Resolution](#type-b-resolution)
    - [Step 2C: Resolve Type C (Breaking-Immediate)](#step-2c-resolve-type-c-breaking-immediate)
  - [Type C Resolution](#type-c-resolution)
    - [Step 2D: Resolve Type D (Irreconcilable)](#step-2d-resolve-type-d-irreconcilable)
  - [Type D Resolution](#type-d-resolution)
    - [Step 3: Update Records](#step-3-update-records)
  - [Decision Tree](#decision-tree)
  - [Checklist](#checklist)
    - [For All Types](#for-all-types)
    - [For Type A](#for-type-a)
    - [For Type B](#for-type-b)
    - [For Type C](#for-type-c)
    - [For Type D](#for-type-d)
  - [Output](#output)
  - [Related References](#related-references)
