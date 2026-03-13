---
operation: route-task-blocker
parent-skill: amcos-emergency-handoff
---

# Operation: Route Task Blocker


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Decision Tree](#decision-tree)
- [Steps](#steps)
  - [Step 1: Receive and Classify Escalation](#step-1-receive-and-classify-escalation)
  - [Step 2A: Handle Directly (If AMCOS Can Resolve)](#step-2a-handle-directly-if-amcos-can-resolve)
  - [Step 2B: Route to AMA (If User Decision Needed)](#step-2b-route-to-ama-if-user-decision-needed)
  - [Step 3: Wait for Resolution](#step-3-wait-for-resolution)
  - [Step 4: Route Resolution Back to AMOA](#step-4-route-resolution-back-to-amoa)
- [Checklist: Routing a Task Blocker](#checklist-routing-a-task-blocker)
- [Checklist: When AMA Returns a Resolution](#checklist-when-ama-returns-a-resolution)
- [Output](#output)
- [Related References](#related-references)

## Purpose

Determine how to handle task blocker escalations - resolve directly if within AMCOS authority, or route to AMA if user decision required.

## When To Use This Operation

- When receiving blocker escalation from AMOA
- When work cannot proceed due to missing information or access
- When a decision requires user input

## Decision Tree

```
AMCOS receives escalation from AMOA
  |
  +-- Is it an agent failure? (crash, unresponsive, repeated failure)
  |     -> YES: Handle via failure recovery workflow (use other op-* files)
  |
  +-- Is it a task blocker that AMCOS can resolve?
  |     +-- Agent reassignment needed -> Handle directly
  |     +-- Permission within AMCOS authority -> Handle directly
  |
  +-- Is it a task blocker requiring user input?
        -> YES: Route to AMA using blocker-escalation template
```

## Steps

### Step 1: Receive and Classify Escalation

1. **Receive escalation from AMOA**
   - Note the escalation type
   - Note the task and blocker details

2. **Classify escalation type**
   - Agent failure: Use failure recovery workflow
   - Task blocker (AMCOS can resolve): Handle directly
   - Task blocker (user decision needed): Route to AMA

### Step 2A: Handle Directly (If AMCOS Can Resolve)

If blocker is agent reassignment or permission within AMCOS authority:

1. Take appropriate action
2. Notify AMOA of resolution
3. Document resolution

### Step 2B: Route to AMA (If User Decision Needed)

1. **Compose blocker-escalation message**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "amcos-chief-of-staff",
     "to": "ama-assistant-manager",
     "subject": "BLOCKER: Task requires user decision",
     "priority": "high",
     "content": {
       "type": "blocker-escalation",
       "message": "A task is blocked and requires user input. AMOA has escalated this after determining the blocker cannot be resolved by agents.",
       "task_uuid": "[task-uuid]",
       "issue_number": "[GitHub issue number of the blocked task]",
       "blocker_issue_number": "[GitHub issue number tracking the blocker problem]",
       "blocker_type": "user-decision",
       "blocker_description": "[What is blocking and why agents cannot resolve it]",
       "impact": "[Affected agents and tasks]",
       "options": ["[Options if available]"],
       "escalated_from": "amoa-[project-name]",
       "original_blocker_time": "[ISO8601 timestamp]"
     }
   }
   ```

2. **Send to AMA via AI Maestro**

3. **Track the blocker in AMCOS records**

### Step 3: Wait for Resolution

1. Monitor for AMA response
2. When AMA responds with user's decision, proceed to Step 4

### Step 4: Route Resolution Back to AMOA

1. **Receive blocker-resolution from AMA**
   - Verify it includes user's exact decision (RULE 14)

2. **Route to AMOA**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "amcos-chief-of-staff",
     "to": "amoa-orchestrator",
     "subject": "RESOLUTION: Blocker [issue_number] resolved",
     "priority": "high",
     "content": {
       "type": "blocker-resolution",
       "message": "User has provided decision for blocker.",
       "blocker_issue_number": "[GitHub issue number]",
       "resolution": "[User's exact decision]",
       "resolved_by": "user via AMA"
     }
   }
   ```

3. **Verify AMOA acknowledges receipt**

4. **Update AMCOS records to mark blocker as resolved**

## Checklist: Routing a Task Blocker

- [ ] Receive escalation from AMOA
- [ ] Determine escalation type: agent failure OR task blocker
- [ ] If agent failure: use failure recovery workflow (Phases 1-5)
- [ ] If task blocker that AMCOS can resolve: handle directly
- [ ] If task blocker requiring user input: compose blocker-escalation message
- [ ] Include `blocker_issue_number` in the message
- [ ] Send escalation to AMA via AI Maestro
- [ ] Track blocker in AMCOS records
- [ ] When AMA responds: route resolution back to AMOA
- [ ] Verify AMOA acknowledges receipt
- [ ] Update AMCOS records

## Checklist: When AMA Returns a Resolution

- [ ] Receive blocker-resolution message from AMA
- [ ] Verify resolution includes user's exact decision
- [ ] Route resolution to AMOA via AI Maestro
- [ ] Verify AMOA acknowledges receipt
- [ ] Note: AMOA will close blocker issue and notify agent
- [ ] Update AMCOS records to mark blocker as resolved

## Output

After completing this operation:
- Blocker routed to appropriate party
- Resolution tracked back to AMOA
- AMCOS records updated

## Related References

- [troubleshooting.md](troubleshooting.md) - Common blocker issues
- [agent-replacement-protocol.md](agent-replacement-protocol.md) - If blocker requires replacement
