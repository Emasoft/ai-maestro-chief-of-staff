---
name: amcos-resource-monitoring
description: Use when monitoring system resources, tracking instance limits, managing resource alerts, and ensuring team capacity is maintained. Trigger with resource checks or limit alerts.
user-invocable: false
license: Apache-2.0
compatibility: Requires system access for resource checks, AI Maestro for agent monitoring, and alerting capabilities. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-chief-of-staff-main-agent
workflow-instruction: "support"
procedure: "support-skill"
---

# AI Maestro Chief of Staff Resource Monitoring Skill

## Overview

Resource monitoring ensures the multi-agent team has sufficient capacity to operate effectively. The Chief of Staff tracks system resources, monitors instance limits, and responds to resource alerts before they cause coordination failures.

## Prerequisites

1. Resource monitoring scripts are available
2. Resource limits are configured
3. Alert thresholds are defined

## Instructions

> **Output Rule**: All AMCOS scripts produce 2-line stdout summaries. Full output is written to `.amcos-logs/`.

1. Identify resource to monitor
2. Query current usage levels
3. Compare against limits
4. Take action if limits exceeded

## Output

| Check Type | Output |
|------------|--------|
| Memory | Current usage, limit, percentage |
| Agents | Active count, max allowed |
| API calls | Rate, remaining quota |

## Core Procedures

### PROCEDURE 1: Check System Resources

Check CPU, memory, disk, and network regularly (every 15 min), before spawning agents, or when issues reported. See [system-resources.md](references/system-resources.md).
  - [Types Of System Resources](#11-types-of-system-resources)
  - [Monitoring CPU Usage](#12-monitoring-cpu-usage)
  - [Monitoring Memory](#13-monitoring-memory)
  - [Monitoring Disk Space](#14-monitoring-disk-space)
  - [Monitoring Network](#15-monitoring-network)

### PROCEDURE 2: Monitor Instance Limits

Count active sessions, check API rate limits, verify concurrency headroom. See [instance-limits.md](references/instance-limits.md).
  - [Types Of Instance Limits](#21-types-of-instance-limits)
  - [Counting Active Sessions](#22-counting-active-sessions)
  - [Tracking API Rate Limits](#23-tracking-api-rate-limits)
  - [Managing Concurrency](#24-managing-concurrency)
  - [Making Scaling Decisions](#25-making-scaling-decisions)

### PROCEDURE 3: Handle Resource Alerts

Identify alert type, assess severity, take immediate action, notify parties. See [resource-alerts.md](references/resource-alerts.md).
  - [Types Of Resource Alerts](#31-types-of-resource-alerts)
  - [Alert Severity Levels](#32-alert-severity-levels)
  - [Alert Response Procedures](#33-alert-response-procedures)
  - [Alert Escalation](#34-alert-escalation)
  - [Alert Prevention](#35-alert-prevention)

## Operational Procedures

- [op-check-system-resources.md](references/op-check-system-resources.md) - Runbook for CPU/memory/disk/network checks
- [op-monitor-instance-limits.md](references/op-monitor-instance-limits.md) - Runbook for session/rate/concurrency tracking
- [op-handle-resource-alert.md](references/op-handle-resource-alert.md) - Runbook for alert response

## Examples

See [examples-and-checklists.md](references/examples-and-checklists.md) for full examples and task checklist.
  - [Task Checklist](#task-checklist)
  - [Example 1: Basic System Resource Check](#example-1-basic-system-resource-check)
  - [Example 2: Counting Active Agent Sessions](#example-2-counting-active-agent-sessions)
  - [Example 3: Resource Alert Response](#example-3-resource-alert-response)

## Error Handling

| Issue | Solution |
|-------|----------|
| Unable to check resources | Verify command availability, check permissions |
| Instance count inconsistent | Force session registry refresh, reconcile |
| Alerts not triggering | Verify config, check interval, test mechanism |

## Resources

- [System Resources](references/system-resources.md)
- [Instance Limits](references/instance-limits.md)
- [Resource Alerts](references/resource-alerts.md)
- [Monitoring Commands](references/monitoring-commands.md)
- [Examples and Checklists](references/examples-and-checklists.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
