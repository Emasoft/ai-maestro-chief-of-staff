# Resource Monitoring Examples and Checklists

## Table of Contents

- [Task Checklist](#task-checklist)
- [Example 1: Basic System Resource Check](#example-1-basic-system-resource-check)
- [Example 2: Counting Active Agent Sessions](#example-2-counting-active-agent-sessions)
- [Example 3: Resource Alert Response](#example-3-resource-alert-response)

---

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand resource monitoring purpose and scope
- [ ] Learn PROCEDURE 1: Check system resources
- [ ] Learn PROCEDURE 2: Monitor instance limits
- [ ] Learn PROCEDURE 3: Handle resource alerts
- [ ] Configure monitoring thresholds
- [ ] Set up automated alerts
- [ ] Practice resource issue response

## Example 1: Basic System Resource Check

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

## Example 2: Counting Active Agent Sessions

Use the `ai-maestro-agents-management` skill to list all active sessions and count them.

Compare the active session count against the configured maximum (e.g., 20 sessions). If the count exceeds the limit, log a warning: `WARNING: Exceeding recommended session limit`.

**Verify**: the active session count is within the configured limit.

## Example 3: Resource Alert Response

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
