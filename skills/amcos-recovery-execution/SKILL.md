---
name: amcos-recovery-execution
description: Use when executing recovery strategies after failure classification. Trigger with recovery plan execution or strategy selection. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AMCOS Recovery Execution

## Overview

Execute recovery strategies for transient and recoverable agent failures. Covers strategy selection, execution, verification, and escalation.

## Prerequisites

- Failure classified as Transient or Recoverable via `amcos-failure-detection`
- AI Maestro running locally
- Recovery log at `$CLAUDE_PROJECT_DIR/.amcos/agent-health/recovery-log.jsonl`

## Instructions

### Phase 3: Recovery Strategies

1. Select strategy based on failure classification
2. Execute following the operational runbook
3. Verify: send ping, check heartbeat, confirm task resumption
4. Success -> log outcome, resume monitoring
5. Failure -> escalate to `amcos-agent-replacement`
6. Notify AMAMA of outcome

| Strategy | When to Use | Recovery Time |
|----------|-------------|---------------|
| Wait and Retry | Transient failures | 1-5 min |
| Restart (soft/hard) | Hung/crashed agent | 5-15 min |
| Hibernate-Wake | Suspended session | 2-5 min |
| Resource Adjustment | Memory/disk exhaustion | 15-60 min |

### File Locations

| Data | Location |
|------|----------|
| Heartbeat config | `$CLAUDE_PROJECT_DIR/.amcos/agent-health/heartbeat-config.json` |
| Task tracking | `$CLAUDE_PROJECT_DIR/.amcos/agent-health/task-tracking.json` |
| Incident log | `$CLAUDE_PROJECT_DIR/.amcos/agent-health/incident-log.jsonl` |
| Recovery log | `$CLAUDE_PROJECT_DIR/.amcos/agent-health/recovery-log.jsonl` |

### Manager Notification Priorities

| Situation | Priority | Message Type |
|-----------|----------|--------------|
| Transient failure (pattern) | `normal` | `escalation` |
| Recoverable failure detected | `high` | `failure-report` |
| Recovery attempt failed | `high` | `failure-report` |
| Terminal failure detected | `urgent` | `replacement-request` |
| Replacement complete | `normal` | `replacement-complete` |

### Troubleshooting

See troubleshooting in Resources

## Checklist

Copy this checklist and track your progress:

- [ ] Strategy selected based on failure classification
- [ ] Recovery executed per operational runbook
- [ ] Agent verified: ping, heartbeat, task resumption
- [ ] Outcome logged to recovery-log.jsonl
- [ ] AMAMA notified of recovery result

## Output

| Result | Output |
|--------|--------|
| Restart successful | Agent back online, state restored |
| Communication recovery | Message queue cleared |
| Recovery failed | Escalation to `amcos-agent-replacement` |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Strategy times out | Move to next strategy in sequence |
| Agent recovers but loses state | Restore from last checkpoint |
| Recovery causes cascading failure | Isolate agent, escalate to terminal |
| AI Maestro unavailable | Use fallback file-based communication |

## Examples

```bash
# Soft restart: check tmux session
tmux has-session -t libs-svg-svgbbox 2>/dev/null && echo "exists" || echo "gone"
```

**Expected result:** Agent session restored, heartbeat confirmed.

## Resources

- [troubleshooting](references/troubleshooting.md) — Recovery troubleshooting
  - Agent shows online but unresponsive
  - Cannot determine failure type
  - Manager does not respond
  - New replacement agent fails to register
  - Emergency handoff deadline missed
- [examples](references/examples.md) — Recovery scenario examples
  - Example 1: Agent Crash Recovery
  - Example 2: Terminal Failure with Replacement
  - Example 3: Transient Network Failure
  - Example 4: Emergency Handoff with Deadline
  - Quick Reference
