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

Identify alert, assess severity, act, notify. See [resource-alerts](references/resource-alerts.md) — Topics: Resource Alerts Reference, Table of Contents, 3.1 Types Of Resource Alerts, Memory Alert, CPU Alert, Disk Alert, Network Alert, Rate Limit Alert, Instance Limit Alert, 3.2 Alert Severity Levels, INFO, WARNING, CRITICAL, EMERGENCY, 3.3 Alert Response Procedures, Memory Alert Response, CPU Alert Response, Disk Alert Response, Network Alert Response, 3.4 Alert Escalation, Escalation Path, Escalation Message Format, Resource Alert Escalation, Current State, Actions Taken, Why Escalating, Recommended Action, User Notification Format, 3.5 Alert Prevention, Proactive Monitoring, Monitoring Schedule, Capacity Planning, Best Practices, 3.6 Resource Alert Examples, Example: Memory Warning Alert, Resource Alert: Memory Warning, Analysis, Actions Taken, Expected Outcome, Escalation, Example: CPU Critical Alert, Resource Alert: CPU Critical, Analysis, Actions Taken, Current State, Escalation, Example: Emergency Disk Alert, Resource Alert: Disk Emergency, Analysis, Immediate Actions, Current State, Post-Incident Actions Required, User Notification, 3.7 Troubleshooting, Issue: Alerts not triggering, Issue: Too many false positive alerts, Issue: Alert response not effective, Issue: Escalation not reaching recipients

## Operational Procedures

- [op-check-system-resources](references/op-check-system-resources.md) — Topics: Operation: Check System Resources, Contents, Purpose, When To Use This Operation, Steps, Step 1: Check CPU Usage, macOS, Linux, Step 2: Check Memory Availability, macOS, Linux, Step 3: Check Disk Space, Check root filesystem, Step 4: Check Network Connectivity, Check AI Maestro connectivity, Step 5: Report Findings, System Resource Check, Checklist, Output, Automated Script, !/bin/bash, System resource check script, CPU, Memory, Disk, AI Maestro, Related References, Next Operation

## Examples

**Input:** "Check system resources before spawning 3 new agents"

**Output:**
```
System resources: CPU 45%, Memory 6.2/16GB (39%), Disk 58GB free
Active agents: 7/15 (headroom: 8). Spawning 3 is safe.
[DONE] Resources OK - 3 agents can be spawned.
```

See [examples-and-checklists](references/examples-and-checklists.md) — Topics: Resource Monitoring Examples and Checklists, Table of Contents, Task Checklist, Example 1: Basic System Resource Check, Check CPU usage, Check available memory, Check disk space, Example 2: Counting Active Agent Sessions, Example 3: Resource Alert Response, Resource Alert: High Memory Usage, Immediate Actions Taken, Resolution

## Error Handling

- Unable to check resources: verify commands, check permissions
- Instance count inconsistent: force registry refresh, reconcile
- Alerts not triggering: verify config, check interval, test mechanism

## Resources

