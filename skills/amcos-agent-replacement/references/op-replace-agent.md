---
operation: replace-agent
parent-skill: amcos-agent-replacement
---

# Operation: Replace Agent


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Critical Consideration](#critical-consideration)
- [Steps](#steps)
  - [Phase 1: Confirm Failure and Preserve Artifacts](#phase-1-confirm-failure-and-preserve-artifacts)
  - [Phase 2: Request Manager Approval](#phase-2-request-manager-approval)
  - [Phase 3: Create Replacement Agent](#phase-3-create-replacement-agent)
  - [Phase 4: Notify Orchestrator](#phase-4-notify-orchestrator)
  - [Phase 5: Send Handoff to New Agent](#phase-5-send-handoff-to-new-agent)
  - [Phase 6: Cleanup and Close Incident](#phase-6-cleanup-and-close-incident)
- [Checklist](#checklist)
- [Output](#output)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Create a replacement agent when recovery fails or failure is terminal, ensuring work continuity and proper handoff.

## When To Use This Operation

- After recovery strategies have failed
- When failure is classified as TERMINAL
- When replacement is the only option for work continuity

## Critical Consideration

**The replacement agent has NO MEMORY of the old agent.**

The new agent does not know:
- What tasks were assigned
- What work was in progress
- The project context

Therefore:
- Orchestrator (AMOA) must generate handoff documentation
- AMOA must reassign tasks in GitHub Project kanban
- AMCOS must send handoff docs to new agent

## Steps

### Phase 1: Confirm Failure and Preserve Artifacts

1. **Confirm agent is unrecoverable**
   Use the `ai-maestro-agents-management` skill to perform a final status check on the agent.

2. **Preserve work artifacts**
   - Save any accessible output files
   - Backup logs if available
   - Document last known state

3. **Capture the failing agent's in-flight kanban load (read-only context)**
   Replacement decisions must be made WITH kanban context, not blind — you need
   the actual in-progress task count and IDs so the impact estimate, the AMOA
   reassignment request, and the new agent's handoff are data-driven rather than
   guessed. Query the frozen CLI (this is read-only OBSERVATION, not driving —
   R42-compliant; it is also the successor to the removed `GET /api/.../tasks?assignee=`).
   `--status` takes ONE stage per call, so query each active stage the agent
   could be mid-work in and union the results:
   ```bash
   for stage in dev testing ai_review human_review; do
     amp-kanban-list.sh --assignee "<FAILED_AGENT_ID>" --status "$stage"
   done
   ```
   `<FAILED_AGENT_ID>` is the agent's registered UUID (from the team registry).
   Record the resulting task IDs — they populate the `impact` field in Phase 2
   and the reassignment list you hand AMOA in Phase 4. You do NOT reassign them
   yourself: task reassignment on the kanban is ORCHESTRATOR-owned; you supply
   the context and request the move.

4. **Record in incident log**
   ```json
   {
     "event": "terminal_failure_confirmed",
     "agent": "failed-agent-name",
     "timestamp": "ISO8601",
     "recovery_attempts": 3,
     "in_progress_tasks": ["task-id", "..."],
     "artifacts_preserved": ["list", "of", "files"]
   }
   ```

### Phase 2: Request Manager Approval

1. **Notify AMAMA (Assistant Manager)**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "amcos-chief-of-staff",
     "to": "amama-assistant-manager",
     "subject": "APPROVAL NEEDED: Replace agent [AGENT_NAME]",
     "priority": "urgent",
     "content": {
       "type": "replacement-request",
       "message": "Agent [AGENT_NAME] has failed terminally. Requesting approval to create replacement.",
       "failed_agent": "AGENT_NAME",
       "failure_type": "terminal",
       "recovery_attempts": 3,
       "impact": "N tasks in progress (from the Phase-1 kanban capture): [task-id, ...] — will need ORCHESTRATOR reassignment"
     }
   }
   ```

2. **Wait for approval** (max 15 minutes)

3. **If no response**: Send reminder, then escalate up the chain to the MAESTRO

### Phase 3: Create Replacement Agent

1. **Determine replacement agent type**
   - Same specialization as failed agent
   - Or reassign to available agent with similar skills

2. **Request agent creation**
   - Use appropriate agent creation method
   - Assign same role/specialization

3. **Verify new agent registration**
   Use the `ai-maestro-agents-management` skill to list agents and verify the new agent appears in the registry.

### Phase 4: Notify Orchestrator

1. **Send notification to AMOA**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "amcos-chief-of-staff",
     "to": "amoa-orchestrator",
     "subject": "Agent replaced - handoff needed",
     "priority": "high",
     "content": {
       "type": "replacement-notification",
       "message": "Agent [OLD_AGENT] has been replaced by [NEW_AGENT]. Please generate handoff documentation and reassign tasks.",
       "failed_agent": "OLD_AGENT_NAME",
       "replacement_agent": "NEW_AGENT_NAME",
       "affected_tasks": ["task-1", "task-2"]
     }
   }
   ```

2. **Wait for AMOA to generate handoff documentation**

### Phase 5: Send Handoff to New Agent

1. **Receive handoff docs from AMOA**

2. **Send handoff to new agent**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "amcos-chief-of-staff",
     "to": "NEW_AGENT_NAME",
     "subject": "HANDOFF: Taking over from [OLD_AGENT]",
     "priority": "high",
     "content": {
       "type": "handoff",
       "message": "You are replacing [OLD_AGENT]. See attached handoff documentation.",
       "handoff_document_path": "thoughts/shared/handoffs/NEW_AGENT/current.md"
     }
   }
   ```

3. **Wait for acknowledgment from new agent**

### Phase 6: Cleanup and Close Incident

1. **Deregister failed agent** (if still registered)
2. **Update incident log with closure**
3. **Notify AMAMA of completion**

## Checklist

Copy this checklist and track your progress:

- [ ] Terminal failure confirmed
- [ ] Artifacts preserved
- [ ] Manager (AMAMA) notified
- [ ] Replacement approval received
- [ ] Replacement agent created
- [ ] Orchestrator (AMOA) notified
- [ ] Handoff documentation received from AMOA
- [ ] Handoff sent to new agent
- [ ] New agent acknowledged handoff
- [ ] Failed agent deregistered
- [ ] Incident closed
- [ ] AMAMA notified of completion

## Output

After completing this operation:
- New agent operational and aware of assigned work
- Failed agent deregistered
- Incident documented and closed

## Related References

- [agent-replacement-protocol.md](agent-replacement-protocol.md) - Complete replacement workflow
- [work-handoff-during-failure.md](work-handoff-during-failure.md) - Handoff procedures
- [troubleshooting.md](troubleshooting.md) - Replacement issues

## Next Operation

- Normal monitoring resumes for new agent
- If deadline critical: [op-emergency-handoff.md](op-emergency-handoff.md)
