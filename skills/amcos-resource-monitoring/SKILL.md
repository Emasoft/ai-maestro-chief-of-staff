---
name: ecos-resource-monitoring
description: Use when monitoring system resources, tracking instance limits, managing resource alerts, and ensuring team capacity is maintained. Trigger with resource checks or limit alerts.
user-invocable: false
license: Apache-2.0
compatibility: Requires system access for resource checks, AI Maestro for agent monitoring, and alerting capabilities. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
workflow-instruction: "support"
procedure: "support-skill"
---

# Emasoft Chief of Staff Resource Monitoring Skill

## Overview

Resource monitoring ensures that the multi-agent team has sufficient capacity to operate effectively. The Chief of Staff tracks system resources, monitors instance limits, and responds to resource alerts before they cause coordination failures or degraded performance.

## Prerequisites

Before using this skill, ensure:
1. Resource monitoring scripts are available
2. Resource limits are configured
3. Alert thresholds are defined

## Instructions

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

## What Is Resource Monitoring?

Resource monitoring is the continuous observation of system capacity and agent instance health. Unlike traditional system monitoring focused on servers, Chief of Staff resource monitoring focuses on the resources that affect agent coordination: context windows, instance counts, message queues, and system capacity.

**Key characteristics:**
- **Proactive**: Detect issues before they cause problems
- **Agent-focused**: Monitor what matters for AI agent operations
- **Actionable**: Alerts include recommended actions
- **Continuous**: Regular checks, not just on-demand

## Resource Monitoring Components

### 1. System Resources
CPU, memory, disk, and network affecting agent operations.

### 2. Instance Limits
Number of active agents, API rate limits, and concurrency constraints.

### 3. Resource Alerts
Notifications when resources approach or exceed thresholds.

## Core Procedures

### PROCEDURE 1: Check System Resources

**When to use:** Regularly (every 15 minutes), before spawning new agents, when performance issues are reported.

**Steps:** Check CPU usage, check memory availability, check disk space, check network connectivity, report findings.

**Related documentation:**

#### System Resources ([references/system-resources.md](references/system-resources.md))
- 1.1 Resource types → Types Of System Resources section
- 1.2 CPU monitoring → Monitoring CPU Usage section
- 1.3 Memory monitoring → Monitoring Memory section
- 1.4 Disk monitoring → Monitoring Disk Space section
- 1.5 Network monitoring → Monitoring Network section
- 1.6 Thresholds → Resource Thresholds section
- 1.7 Examples → System Resource Examples section
- 1.8 Issues → Troubleshooting section

### PROCEDURE 2: Monitor Instance Limits

**When to use:** Before spawning agents, when approaching limits, when coordination slows.

**Steps:** Count active sessions, check API rate limits, verify concurrency headroom, assess scaling needs.

**Related documentation:**

#### Instance Limits ([references/instance-limits.md](references/instance-limits.md))
- 2.1 Limit types → Types Of Instance Limits section
- 2.2 Session counting → Counting Active Sessions section
- 2.3 Rate limit tracking → Tracking API Rate Limits section
- 2.4 Concurrency management → Managing Concurrency section
- 2.5 Scaling decisions → Making Scaling Decisions section
- 2.6 Examples → Instance Limit Examples section
- 2.7 Issues → Troubleshooting section

### PROCEDURE 3: Handle Resource Alerts

**When to use:** When resource thresholds are exceeded, when alerts are triggered, when degradation is detected.

**Steps:** Identify alert type, assess severity, take immediate action, notify relevant parties, document incident.

**Related documentation:**

#### Resource Alerts ([references/resource-alerts.md](references/resource-alerts.md))
- 3.1 Alert types → Types Of Resource Alerts section
- 3.2 Severity levels → Alert Severity Levels section
- 3.3 Response procedures → Alert Response Procedures section
- 3.4 Escalation → Alert Escalation section
- 3.5 Prevention → Alert Prevention section
- 3.6 Examples → Resource Alert Examples section
- 3.7 Issues → Troubleshooting section

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand resource monitoring purpose and scope
- [ ] Learn PROCEDURE 1: Check system resources
- [ ] Learn PROCEDURE 2: Monitor instance limits
- [ ] Learn PROCEDURE 3: Handle resource alerts
- [ ] Configure monitoring thresholds
- [ ] Set up automated alerts
- [ ] Practice resource issue response

## Examples

### Example 1: Basic System Resource Check

```bash
# Check CPU usage
cpu_usage=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')

# Check available memory
mem_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
mem_free_mb=$((mem_free * 4096 / 1024 / 1024))

# Check disk space
disk_free=$(df -h / | tail -1 | awk '{print $4}')

echo "CPU: ${cpu_usage}%, Memory Free: ${mem_free_mb}MB, Disk Free: ${disk_free}"
```

### Example 2: Counting Active Agent Sessions

Use the `ai-maestro-agents-management` skill to list all active sessions and count them.

Compare the active session count against the configured maximum (e.g., 20 sessions). If the count exceeds the limit, log a warning: `WARNING: Exceeding recommended session limit`.

**Verify**: the active session count is within the configured limit.

### Example 3: Resource Alert Response

```markdown
# Resource Alert: High Memory Usage

**Timestamp:** 2025-02-01T10:30:00Z
**Alert Type:** Memory threshold exceeded
**Severity:** WARNING
**Current Value:** 85% memory used
**Threshold:** 80%

## Immediate Actions Taken

1. Identified agents with large context windows
2. Requested context compaction from orchestrator-master
3. Paused new agent spawning

## Resolution

Memory usage dropped to 72% after compaction.
Monitoring continues at increased frequency (5 min interval).
```

## Operational Procedures

Step-by-step runbooks for executing each resource monitoring operation. Use these when performing the actual procedures described above.

### Check System Resources ([references/op-check-system-resources.md](references/op-check-system-resources.md))

Detailed step-by-step runbook for monitoring CPU, memory, disk, and network resources that affect agent operations.

- When to Use: Every 15 minutes, before spawning agents, when performance issues reported, when agents report slowdowns
- Step 1: Check CPU Usage (thresholds: normal <70%, warning 70-85%, critical >85%)
- Step 2: Check Memory Availability (thresholds: normal >2GB, warning 1-2GB, critical <1GB)
- Step 3: Check Disk Space (thresholds: normal <70%, warning 70-85%, critical >85%)
- Step 4: Check Network Connectivity (AI Maestro health check)
- Step 5: Report Findings
- Automated Script, Checklist

### Monitor Instance Limits ([references/op-monitor-instance-limits.md](references/op-monitor-instance-limits.md))

Detailed step-by-step runbook for tracking active agent sessions, API rate limits, and concurrency constraints to ensure team capacity.

- When to Use: Before spawning agents, approaching limits, coordination slows, every 5 minutes during active operations
- Step 1: Count Active Sessions (limits: conservative 10, normal 15, max 20)
- Step 2: Check API Rate Limits (messages/minute, API calls/minute, 20% headroom)
- Step 3: Verify Concurrency Headroom
- Step 4: Assess Scaling Needs
- Step 5: Document Instance State
- Instance Limit Thresholds table, Checklist

### Handle Resource Alert ([references/op-handle-resource-alert.md](references/op-handle-resource-alert.md))

Detailed step-by-step runbook for responding to resource threshold violations with appropriate actions to maintain system health.

- When to Use: Resource thresholds exceeded, monitoring scripts trigger alerts, degradation detected
- Alert Severity Levels: INFO (approaching), WARNING (exceeded, 15min response), CRITICAL (severe, immediate)
- Step 1: Identify Alert Type (CPU_HIGH, MEMORY_LOW, DISK_FULL, SESSION_LIMIT, RATE_LIMIT, NETWORK_DOWN)
- Step 2: Assess Severity
- Step 3: Take Immediate Action (type-specific response procedures)
- Step 4: Notify Relevant Parties (EAMA for WARNING/CRITICAL)
- Step 5: Document Incident
- Alert Response Matrix, Checklist

## Error Handling

### Issue: Unable to check system resources

**Symptoms:** Commands fail, metrics unavailable, monitoring gaps.

**Solution:** Verify command availability, check permissions, use alternative methods, document and alert if persistent.

### Issue: Instance count is inconsistent

**Symptoms:** AI Maestro reports different count than observed.

**Solution:** Force session registry refresh, verify session names, reconcile discrepancies, update roster.

### Issue: Alerts not being triggered

**Symptoms:** Resources exceed thresholds but no alerts.

**Solution:** Verify alert configuration, check monitoring interval, test alert mechanism, review threshold values.

## Key Takeaways

1. **Monitor proactively** - Do not wait for failures to check resources
2. **Focus on agent-relevant resources** - Context windows and instances matter most
3. **Set appropriate thresholds** - Leave headroom for bursts
4. **Respond quickly to alerts** - Resource issues cascade rapidly
5. **Document all incidents** - Patterns help prevent future issues

## Resources

- [System Resources](references/system-resources.md)
- [Instance Limits](references/instance-limits.md)
- [Resource Alerts](references/resource-alerts.md)
- [Monitoring Commands](references/monitoring-commands.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
**Target Audience:** Emasoft Chief of Staff Agent
**Difficulty Level:** Intermediate
