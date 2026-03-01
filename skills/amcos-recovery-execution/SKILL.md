---
name: amcos-recovery-execution
description: Use when executing recovery strategies after failure classification. Trigger with recovery plan execution or strategy selection.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-main
---

# AMCOS Recovery Execution

## Overview

Execute recovery strategies for transient and recoverable agent failures. Covers strategy selection, execution, verification, and escalation to replacement when recovery fails.

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
6. Notify EAMA of outcome

| Strategy | When to Use | Recovery Time |
|----------|-------------|---------------|
| Wait and Retry | Transient failures | 1-5 min |
| Restart (soft/hard) | Hung/crashed agent | 5-15 min |
| Hibernate-Wake | Suspended session | 2-5 min |
| Resource Adjustment | Memory/disk exhaustion | 15-60 min |

See [references/recovery-strategies.md](references/recovery-strategies.md) and [references/op-execute-recovery-strategy.md](references/op-execute-recovery-strategy.md).
  <!-- TOC: recovery-strategies.md -->
  - Overview of recovery strategies
  - Strategy: Wait and Retry
  - ...and 7 more sections
  <!-- /TOC -->

Detailed operations: [references/recovery-operations.md](references/recovery-operations.md).
  <!-- TOC: recovery-operations.md -->
  - Detecting Agent Failures Using Health Checks
  - Verifying tmux Session Existence
  - ...and 10 more sections
  <!-- /TOC -->

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

See [references/troubleshooting.md](references/troubleshooting.md) for full details.
  <!-- TOC: troubleshooting.md -->
  - Agent shows online but unresponsive
  - Cannot determine failure type
  - ...and 3 more sections
  <!-- /TOC -->

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

See [references/examples.md](references/examples.md) for complete scenarios.
  <!-- TOC: examples.md -->
  - Example 1: Agent Crash Recovery
  - Example 3: Transient Network Failure
  - ...and 3 more sections
  <!-- /TOC -->

```bash
# Soft restart: check tmux session
tmux has-session -t libs-svg-svgbbox 2>/dev/null && echo "exists" || echo "gone"

# Verify recovery
curl -s "$AIMAESTRO_API/api/agents" | jq '.agents[] | select(.name=="libs-svg-svgbbox") | .status'
```

## Resources

- [references/recovery-strategies.md](references/recovery-strategies.md) - Recovery strategy procedures
- [references/recovery-operations.md](references/recovery-operations.md) - Detailed recovery operations
- [references/op-execute-recovery-strategy.md](references/op-execute-recovery-strategy.md) - Execute recovery runbook
- [references/examples.md](references/examples.md) - Complete recovery examples
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and solutions
