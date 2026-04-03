---
name: amcos-failure-detection-ref
description: Use when consulting detailed failure detection references. Trigger with failure detection lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Failure Detection Reference

## Overview

Reference material for failure detection. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-failure-detection` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-failure-detection` for error handling.

## Examples

```bash
# Look up heartbeat monitoring configuration
cat references/failure-detection.md | grep -A5 "Heartbeat"
```

Expected: heartbeat interval settings and response interpretation.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the failure detection topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [failure-detection](references/failure-detection.md) — Topics: Failure Detection for Remote Agents, Table of Contents, 1.1 When to Use This Document, 1.2 Overview of Failure Detection Mechanisms, 1.3 Heartbeat Monitoring via AI Maestro, 1.3.1 How Heartbeat Polling Works, 1.3.2 Configuring Heartbeat Intervals, 1.3.3 Interpreting Heartbeat Responses, 1.4 Message Delivery Failure Detection, 1.4.1 Detecting Undelivered Messages, 1.4.2 Detecting Unacknowledged Messages, 1.4.3 Timeout Thresholds for Message Acknowledgment, 1.5 Task Completion Timeout Detection, 1.5.1 Monitoring Task Progress, 1.5.2 Detecting Stalled Tasks, 1.5.3 Distinguishing Slow Tasks from Failed Agents, 1.6 Agent Status Queries, 1.6.1 Querying Agent Online Status, 1.6.2 Interpreting Status Responses, 1.7 Failure Detection Decision Flowchart, Troubleshooting, Heartbeats show agent offline but it is running, False positives during long operations, AI Maestro not responding
