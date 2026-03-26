---
name: amcos-config-snapshot-ref
description: Use when consulting detailed config snapshot references. Trigger with config snapshot lookups.
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

See referenced files for step-by-step examples.

## Resources

- [ai-maestro-integration](references/ai-maestro-integration.md) — Topics: AI Maestro Integration Reference, Table of Contents, 1.1 What Is AI Maestro, 1.2 Core Capabilities, Session Operations, Message Operations, Utility Operations, 1.3 Session Management, Listing Sessions, Getting Session Details, Session Status Values, Checking Session Existence, 1.4 Message Operations, Sending a Message, Message Fields, Content Object Format, Listing Messages, Marking as Read, Checking Unread Count, 1.5 Broadcast Operations, Sending Broadcast, Broadcast Best Practices, 1.6 Health and Status, Health Check, Service Statistics, Checking AI Maestro Availability, 1.7 Integration Examples, Example: Send and Confirm Delivery, Example: Poll for Unread Messages, Example: Team Status Query, Example: Error Handling in Messaging, 1.8 Troubleshooting, Issue: AI Maestro not responding, Issue: Messages not delivered, Issue: Session shows offline but agent is running, Issue: High latency on messaging, Issue: Duplicate messages received
- [op-detect-config-changes](references/op-detect-config-changes.md) — Topics: Operation: Detect Config Changes During Session, Contents, Purpose, When To Use This Operation, Steps, Step 1: Read Current Config Files, Step 2: Compare Timestamps, Get snapshot timestamp from file, Get current file timestamp, Step 3: Perform Content Comparison (if timestamps differ), Calculate current hash, Compare with snapshot hash, Step 4: Identify Changed Sections, Config Change Detected, Changed Sections, Step 5: Log in activeContext.md, Session Notes, Step 6: Trigger Conflict Resolution if Critical, Change Classification, Detection Methods, Method 1: Timestamp-Based (Fast), Compare modification times, Method 2: Hash-Based (Accurate), Compare content hashes, Checklist, Periodic Check Schedule, Output, Related References, Next Operation
- [21-config-conflict-resolution](references/21-config-conflict-resolution.md) — Topics: Resolving Config Conflicts, Table of Contents, Overview, What Is Config Conflict Resolution?, Why Resolution Matters, Conflict Types and Resolution Strategies, Conflict Types Quick Reference, Resolution Strategies Quick Reference, Resolution Procedures 1-2, PROCEDURE 1: Resolve Non-Breaking Changes (Type A), PROCEDURE 2: Resolve Breaking Changes - Future (Type B), Resolution Procedures 3-4, PROCEDURE 3: Resolve Breaking Changes - Immediate (Type C), PROCEDURE 4: Resolve Irreconcilable Conflicts (Type D), Decision Trees, Examples, Troubleshooting, Decision Tree 1: Initial Conflict Classification, Decision Tree 2: Breaking Change Handling, Example Scenarios, Troubleshooting Quick Reference
- [op-capture-config-snapshot](references/op-capture-config-snapshot.md) — Topics: Operation: Capture Config Snapshot at Session Start, Contents, Purpose, When To Use This Operation, Config Snapshot Purpose, Steps, Step 1: Identify Config Files, Step 2: Create Snapshot Header, Config Snapshot, Source Files, Step 3: Copy Config Content, [Config File Name], Content, Step 4: Calculate File Hashes, Calculate hash for each config file, Step 5: Save Snapshot, Write snapshot content, Step 6: Record in activeContext.md, Session Notes, Checklist, Snapshot Structure, Config Snapshot, Source Files, team-config.yaml, Content, project-rules.md, Content, Output, Related References, Next Operation
- [op-handle-config-conflicts](references/op-handle-config-conflicts.md) — Topics: Operation: Handle Config Version Conflicts, Contents, Purpose, When To Use This Operation, Conflict Types, Steps, Step 1: Classify the Conflict, Conflict Classification, Step 2A: Resolve Type A (Non-Breaking), Type A Resolution, Step 2B: Resolve Type B (Breaking-Future), Type B Resolution, Step 2C: Resolve Type C (Breaking-Immediate), Type C Resolution, Step 2D: Resolve Type D (Irreconcilable), Type D Resolution, Step 3: Update Records, Decision Tree, Checklist, For All Types, For Type A, For Type B, For Type C, For Type D, Output, Related References
