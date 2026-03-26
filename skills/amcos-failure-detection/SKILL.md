---
name: amcos-failure-detection
description: Use when detecting or classifying agent failures. Trigger with health check failures, heartbeat timeouts, or error events.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AMCOS Failure Detection

## Overview

Detect and classify agent failures in a multi-agent system coordinated via AI Maestro. Covers heartbeat monitoring, message delivery failure detection, and severity classification.

## Prerequisites

- AI Maestro running locally with agent registry accessible
- Heartbeat config at `$CLAUDE_PROJECT_DIR/.amcos/agent-health/heartbeat-config.json`
- Task tracking at `$CLAUDE_PROJECT_DIR/.amcos/agent-health/task-tracking.json`

## Instructions

### Phase 1: Failure Detection

1. Check heartbeat status via AI Maestro agent status API
2. Verify message delivery to the suspect agent
3. Review task completion progress for timeouts
4. If any signal indicates failure, proceed to Classification

| Mechanism | Signal | Response Time |
|-----------|--------|---------------|
| Heartbeat timeout | Missed pings | 30-60 seconds |
| Message delivery failure | API error | Immediate |
| Acknowledgment timeout | No ACK | 5-15 minutes |
| Task completion timeout | Stalled progress | Variable |

### Phase 2: Failure Classification

1. Gather evidence: error messages, heartbeat history, agent status
2. Match against classification criteria
3. Determine category and log to incident log
4. Route: Transient -> wait; Recoverable -> `amcos-recovery-execution`; Terminal -> `amcos-agent-replacement`

| Category | Recovery | Example |
|----------|----------|---------|
| **Transient** | Auto (< 5 min) | Network hiccup, rate limit |
| **Recoverable** | Intervention | Session hibernated, OOM |
| **Terminal** | Replacement | Host crash, disk corruption |

### Quick Reference

```
DETECT --> CLASSIFY --> RESPOND
  Transient --> Wait & Retry
  Recoverable --> amcos-recovery-execution
  Terminal --> amcos-agent-replacement
```

## Output

| Result | Next Action |
|--------|-------------|
| Transient detected | Wait 5 min, verify auto-recovery |
| Recoverable detected | Route to `amcos-recovery-execution` |
| Terminal detected | Route to `amcos-agent-replacement` |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Agent unresponsive to ping | Wait 30s, retry, then classify |
| Cannot determine failure type | Default to recoverable |
| AI Maestro API unreachable | Use fallback file-based communication |

## Examples

```bash
# Send health check ping to suspect agent
amp-send.sh ampa-svgbbox-impl "Health check" high '{"type":"ping"}'
```

Expected: agent responds within 30s; if no response, classify as failure.

## Checklist

Copy this checklist and track your progress:
- [ ] Check heartbeat status and message delivery
- [ ] Classify failure (Transient/Recoverable/Terminal)
- [ ] Document evidence and route to correct handler

## Resources

- [failure-classification](references/failure-classification.md) — Failure classification criteria, escalation thresholds, recording
  - 2.1 When to use this document
  - 2.2 Overview of failure categories
  - 2.3 Transient failures
    - 2.3.1 Definition and characteristics
    - 2.3.2 Examples of transient failures
    - 2.3.3 Expected recovery time
    - 2.3.4 Recommended response
  - 2.4 Recoverable failures
    - 2.4.1 Definition and characteristics
    - 2.4.2 Examples of recoverable failures
    - 2.4.3 Expected recovery time
    - 2.4.4 Recommended response
  - 2.5 Terminal failures
    - 2.5.1 Definition and characteristics
    - 2.5.2 Examples of terminal failures
    - 2.5.3 When replacement is required
    - 2.5.4 Recommended response
  - 2.6 Classification decision matrix
  - 2.7 Escalation thresholds
  - 2.8 Recording failure events
