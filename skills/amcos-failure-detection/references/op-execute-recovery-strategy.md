---
operation: execute-recovery-strategy
parent-skill: amcos-failure-detection
---

# Operation: Execute Recovery Strategy


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Recovery Strategies](#recovery-strategies)
- [Steps](#steps)
  - [Strategy 1: Wait and Retry (Transient)](#strategy-1-wait-and-retry-transient)
  - [Strategy 2: Restart Agent (Soft)](#strategy-2-restart-agent-soft)
  - [Strategy 3: Restart Agent (Hard)](#strategy-3-restart-agent-hard)
  - [Strategy 4: Hibernate-Wake Cycle](#strategy-4-hibernate-wake-cycle)
  - [Strategy 5: Resource Adjustment](#strategy-5-resource-adjustment)
- [Recovery Attempt Tracking](#recovery-attempt-tracking)
- [Checklist](#checklist)
- [Escalation Criteria](#escalation-criteria)
- [Output](#output)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Attempt to restore a failed agent to operational status using appropriate recovery strategies based on failure classification.

## When To Use This Operation

- After classifying failure as RECOVERABLE
- Before escalating to agent replacement
- When intervention can restore agent function

## Recovery Strategies

| Strategy | When to Use | Time to Recover |
|----------|-------------|-----------------|
| Wait and Retry | Transient failures | 1-5 minutes |
| Restart Agent | Hung/crashed agent | 5-15 minutes |
| Hibernate-Wake | Idle/suspended session | 2-5 minutes |
| Resource Adjustment | Memory/disk exhaustion | 15-60 minutes |

## Steps

### Strategy 1: Wait and Retry (Transient)

1. Set timer for 5 minutes
2. Do not take any action
3. After timeout, re-run failure detection
4. If still failing, escalate to recoverable

### Strategy 2: Restart Agent (Soft)

R42 (messaging is the only cross-agent channel): ask the agent to restart *itself* — never inject
a command/keystroke into its session.

1. via the `amp-send` CLI: `amp-send <recipient> "<subject>" "<message>" [--type T] [--priority P]`, send the agent a graceful self-restart request (it saves
   state and restarts itself; R42.2 directive-as-message + R42.4 self-drive).
2. Wait 2 minutes for the agent to acknowledge and restart
3. Verify agent status
4. If no acknowledgment, attempt hard restart

### Strategy 3: Restart Agent (Hard)

For a hung agent that will not answer a message, force a clean reload with the R10.3
hibernate→wake cycle — a server-side lifecycle-state op (wake reloads plugin/config, R17.21),
NOT the R42-revoked `POST /api/sessions/[id]/restart` route and NOT a tmux keystroke.

1. Use the `ai-maestro-agents-management` skill to hibernate the agent, then wake it (own-team only, R10.3).
2. Wait 5 minutes for the wake and config reload to complete
3. Verify agent status
4. If still failed, classify as terminal. Terminate+respawn is a delete+create (new AID, no memory
   of the old agent) — R29/R30 MANAGER-lifecycle territory, so it requires a **MANAGER mandate**:
   route through `op-replace-agent.md` (its Phase 2 gates on MANAGER approval before the replacement
   is created). COS does not unilaterally tear down and rebuild a member.

### Strategy 4: Hibernate-Wake Cycle

1. Check if agent is hibernated
2. Use the `ai-maestro-agents-management` skill to send a wake signal to the agent.
3. Wait 2 minutes
4. Verify agent responsive

### Strategy 5: Resource Adjustment

1. Identify resource constraint (memory, disk, CPU)
2. Request resource increase from user if needed
3. Clear caches or temporary files
4. Restart after resources freed

## Recovery Attempt Tracking

Track all recovery attempts:

```json
{
  "agent": "agent-name",
  "attempt": 1,
  "strategy": "soft-restart",
  "timestamp": "ISO8601",
  "result": "success|failed",
  "details": "result details"
}
```

## Checklist

Copy this checklist and track your progress:

- [ ] Recovery strategy selected based on failure type
- [ ] Manager notified (if high severity)
- [ ] Recovery attempt initiated
- [ ] Wait period completed
- [ ] Agent status verified
- [ ] Result documented
- [ ] If failed: attempt next strategy OR escalate to terminal

## Escalation Criteria

Escalate to TERMINAL if:
- 3 consecutive recovery attempts failed
- Recovery succeeded but agent failed again within 10 minutes
- Underlying cause cannot be resolved

## Output

After completing this operation:
- Agent recovered and operational, OR
- Recovery failed and classified as TERMINAL

## Related References

- [recovery-strategies.md](recovery-strategies.md) - Complete recovery procedures
- [recovery-operations.md](recovery-operations.md) - Detailed recovery operations
- [troubleshooting.md](troubleshooting.md) - Recovery issues

## Next Operation

- If recovered: Resume normal monitoring
- If failed: Proceed to [op-replace-agent.md](op-replace-agent.md)
