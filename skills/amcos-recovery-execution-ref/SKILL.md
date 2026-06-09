---
name: amcos-recovery-execution-ref
description: Use when consulting detailed recovery execution references. Trigger with recovery execution lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Recovery Execution Reference

## Overview

Reference material for recovery execution. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-recovery-execution` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-recovery-execution` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "How do I restart an unresponsive agent?"

```bash
cat references/recovery-operations.md | head -60
```

**Expected result:** Health check procedures, failure classification, and recovery strategies (retry, restart, hibernate-wake, replace).

## Resources

- [recovery-operations](references/recovery-operations.md) — Health checks, failure classification, recovery execution, restart procedures, logging, coordination
  - [1. Detecting Agent Failures Using Health Checks](#1-detecting-agent-failures-using-health-checks)
    - [1.1 Checking AI Maestro Registry](#11-checking-ai-maestro-registry)
    - [1.2 Verifying tmux Session Existence](#12-verifying-tmux-session-existence)
    - [1.3 Checking Process Health](#13-checking-process-health)
    - [1.4 Testing Message Response](#14-testing-message-response)
    - [1.5 Checking Host Reachability for Remote Agents](#15-checking-host-reachability-for-remote-agents)
  - [2. Classifying Failure Severity (Transient/Recoverable/Terminal)](#2-classifying-failure-severity-transientrecoverableterminal)
    - [2.1 Failure Classification Criteria Table](#21-failure-classification-criteria-table)
    - [2.2 Classification Algorithm](#22-classification-algorithm)
  - [3. Executing Recovery Strategies Based on Failure Type](#3-executing-recovery-strategies-based-on-failure-type)
    - [3.1 Recovery Strategy Decision Tree](#31-recovery-strategy-decision-tree)
    - [3.2 Transient Recovery (Automatic)](#32-transient-recovery-automatic)
    - [3.3 Recoverable Recovery (Automatic with Notification)](#33-recoverable-recovery-automatic-with-notification)
    - [3.4 Terminal Recovery (Requires Approval Unless Pre-Authorized)](#34-terminal-recovery-requires-approval-unless-pre-authorized)
  - [4. Restarting Unresponsive Agents](#4-restarting-unresponsive-agents)
    - [4.1 Soft Restart Procedure](#41-soft-restart-procedure)
    - [4.2 Wake via Lifecycle Manager](#42-wake-via-lifecycle-manager)
    - [4.3 Full Agent Replacement](#43-full-agent-replacement)
  - [5. Configuring Recovery Policies](#5-configuring-recovery-policies)
    - [5.1 Recovery Policy File Location](#51-recovery-policy-file-location)
    - [5.2 Recovery Policy Parameters](#52-recovery-policy-parameters)
  - [6. Logging All Recovery Actions](#6-logging-all-recovery-actions)
    - [6.1 Recovery Log File Format](#61-recovery-log-file-format)
    - [6.2 Recovery Event Schema](#62-recovery-event-schema)
  - [7. Coordinating with Other Agents During Recovery](#7-coordinating-with-other-agents-during-recovery)
    - [7.1 Sending Recovery Warnings](#71-sending-recovery-warnings)
    - [7.2 Notifying Orchestrator of Orphaned Tasks](#72-notifying-orchestrator-of-orphaned-tasks)
    - [7.3 Escalating to Manager for Approval](#73-escalating-to-manager-for-approval)
    - [7.4 Requesting Agent Replacement](#74-requesting-agent-replacement)
  - [8. Monitoring Agent Health Continuously](#8-monitoring-agent-health-continuously)
    - [8.1 Continuous Health Check Loop](#81-continuous-health-check-loop)
    - [8.2 On-Demand Health Check](#82-on-demand-health-check)
- [recovery-strategies](references/recovery-strategies.md) — Wait/retry, soft/hard restart, hibernate-wake, resource adjustment, replacement, troubleshooting
  - 3.1 When to use this document
  - 3.2 Overview of recovery strategies
  - 3.3 Strategy: Wait and Retry
    - 3.3.1 When to use wait and retry
    - 3.3.2 Implementation procedure
    - 3.3.3 Retry backoff schedule
    - 3.3.4 Success and failure criteria
  - 3.4 Strategy: Restart Agent
    - 3.4.1 When to use restart
    - 3.4.2 Soft restart procedure
    - 3.4.3 Hard restart procedure
    - 3.4.4 Post-restart verification
  - 3.5 Strategy: Hibernate-Wake Cycle
    - 3.5.1 When to use hibernate-wake
    - 3.5.2 Checking agent hibernation status
    - 3.5.3 Wake procedure
    - 3.5.4 Post-wake verification
  - 3.6 Strategy: Resource Adjustment
    - 3.6.1 When to use resource adjustment
    - 3.6.2 Common resource issues and fixes
    - 3.6.3 Requesting resource changes
  - 3.7 Strategy: Replace Agent
    - 3.7.1 When to proceed to replacement
    - 3.7.2 Pre-replacement checklist
    - 3.7.3 Initiating replacement protocol
  - 3.8 Strategy selection flowchart
