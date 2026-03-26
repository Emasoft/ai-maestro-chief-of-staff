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
agent: ai-maestro-chief-of-staff-main-agent
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

### PROCEDURE 2: Monitor Instance Limits

### PROCEDURE 3: Handle Resource Alerts

Identify alert, assess severity, act, notify. See [resource-alerts](references/resource-alerts.md)

## Operational Procedures

- [op-check-system-resources](references/op-check-system-resources.md) — CPU, memory, disk, network check procedure

## Examples

**Input:** "Check system resources before spawning 3 new agents"

**Output:**
```
System resources: CPU 45%, Memory 6.2/16GB (39%), Disk 58GB free
Active agents: 7/15 (headroom: 8). Spawning 3 is safe.
[DONE] Resources OK - 3 agents can be spawned.
```

See [examples-and-checklists](references/examples-and-checklists.md) for more examples.

## Error Handling

- Unable to check resources: verify commands, check permissions
- Instance count inconsistent: force registry refresh, reconcile
- Alerts not triggering: verify config, check interval, test mechanism

## Resources

