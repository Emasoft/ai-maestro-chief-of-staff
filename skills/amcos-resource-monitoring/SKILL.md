---
name: amcos-resource-monitoring
description: Use when monitoring system resources or managing capacity. Trigger with resource checks, alerts, or instance limit queries.
user-invocable: false
license: Apache-2.0
compatibility: Requires system access, AI Maestro installed, alerting capabilities.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff Resource Monitoring Skill

## Overview

Track system resources, instance limits, and resource alerts to ensure multi-agent team capacity.

## Prerequisites

1. Resource monitoring scripts available
2. Resource limits configured
3. Alert thresholds defined

## Instructions

1. Identify resource to monitor
2. Query current usage
3. Compare against limits
4. Act if limits exceeded

### Checklist

Copy this checklist and track your progress:

- [ ] Resource type identified (CPU/memory/disk/agents/API rate)
- [ ] Current usage queried
- [ ] Usage compared against thresholds
- [ ] Alerts triggered or corrective action taken if exceeded

## Output

Memory: usage/limit/%. Agents: active/max. API: rate/quota.

## Core Procedures

### PROCEDURE 1: Check System Resources

Check CPU/memory/disk/network every 15 min, before spawning agents, or on issues. See `references/system-resources.md`.
  - [Types Of System Resources](#11-types-of-system-resources)
  - [Monitoring CPU Usage](#12-monitoring-cpu-usage)
  - [Monitoring Memory](#13-monitoring-memory)
  - [Monitoring Disk Space](#14-monitoring-disk-space)
  - [Monitoring Network](#15-monitoring-network)

### PROCEDURE 2: Monitor Instance Limits

Count sessions, check API rate limits, verify concurrency. See `references/instance-limits.md`.
  - [Types Of Instance Limits](#21-types-of-instance-limits)
  - [Counting Active Sessions](#22-counting-active-sessions)
  - [Tracking API Rate Limits](#23-tracking-api-rate-limits)
  - [Managing Concurrency](#24-managing-concurrency)
  - [Making Scaling Decisions](#25-making-scaling-decisions)

### PROCEDURE 3: Handle Resource Alerts

Identify alert, assess severity, act, notify. See `references/resource-alerts.md`.
  - [Types Of Resource Alerts](#31-types-of-resource-alerts)
  - [Alert Severity Levels](#32-alert-severity-levels)
  - [Alert Response Procedures](#33-alert-response-procedures)
  - [Alert Escalation](#34-alert-escalation)
  - [Alert Prevention](#35-alert-prevention)

## Operational Procedures

- `references/op-check-system-resources.md` - System checks runbook
- `references/op-monitor-instance-limits.md` - Instance limits runbook
- `references/op-handle-resource-alert.md` - Alert response runbook

## Examples

**Input:** "Check system resources before spawning 3 new agents"

**Output:**
```
System resources: CPU 45%, Memory 6.2/16GB (39%), Disk 58GB free
Active agents: 7/15 (headroom: 8). Spawning 3 is safe.
[DONE] Resources OK - 3 agents can be spawned.
```

See `references/examples-and-checklists.md` for full examples and task checklist.
  - [Task Checklist](#task-checklist)
  - [Example 1: Basic System Resource Check](#example-1-basic-system-resource-check)
  - [Example 2: Counting Active Agent Sessions](#example-2-counting-active-agent-sessions)
  - [Example 3: Resource Alert Response](#example-3-resource-alert-response)

## Error Handling

- Unable to check resources: verify commands, check permissions
- Instance count inconsistent: force registry refresh, reconcile
- Alerts not triggering: verify config, check interval, test mechanism

## Resources

- `references/system-resources.md`
- `references/instance-limits.md`
- `references/resource-alerts.md`
- `references/monitoring-commands.md`
- `references/examples-and-checklists.md`
