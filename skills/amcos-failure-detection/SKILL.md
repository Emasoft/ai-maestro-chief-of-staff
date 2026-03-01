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
agent: amcos-main
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

See [references/failure-detection.md](references/failure-detection.md) and [references/op-detect-agent-failure.md](references/op-detect-agent-failure.md).
  <!-- TOC: failure-detection.md -->
  - Heartbeat monitoring via AI Maestro
  - Message delivery failure detection
  - ...and 5 more sections
  <!-- /TOC -->

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

See [references/failure-classification.md](references/failure-classification.md) and [references/op-classify-failure-severity.md](references/op-classify-failure-severity.md).
  <!-- TOC: failure-classification.md -->
  - Overview of failure categories
  - Transient failures
  - ...and 6 more sections
  <!-- /TOC -->

### Quick Reference Workflow

```
DETECT --> CLASSIFY --> RESPOND
  Heartbeat?   Transient? --> Wait & Retry
  Message?     Recoverable? --> amcos-recovery-execution
  Offline?     Terminal? --> amcos-agent-replacement
```

### Failure Response Checklist

```markdown
Agent: ___  Failure detected: ___
- [ ] Heartbeat status checked
- [ ] AI Maestro agent status queried
- [ ] Message delivery verified
- [ ] Task progress reviewed
- [ ] Failure type: [ ] Transient [ ] Recoverable [ ] Terminal
- [ ] Evidence documented, incident logged
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
# Check agent status
curl -s "$AIMAESTRO_API/api/agents" | jq '.agents[] | select(.name=="libs-svg-svgbbox")'

# Send health check ping
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to":"libs-svg-svgbbox","subject":"Health check","priority":"high","content":{"type":"ping","message":"AMCOS health check"}}'
```

## Resources

- [references/failure-detection.md](references/failure-detection.md) - Detection procedures
- [references/failure-classification.md](references/failure-classification.md) - Classification criteria
- [references/op-detect-agent-failure.md](references/op-detect-agent-failure.md) - Detect failure runbook
- [references/op-classify-failure-severity.md](references/op-classify-failure-severity.md) - Classify severity runbook
