# Agent Replacement Protocol

## Table of Contents

- 4.1 When to use this document
- 4.2 Overview of the replacement protocol
- 4.3 Phase 1: Failure confirmation and artifact preservation
  - 4.3.1 Confirming agent cannot be recovered
  - 4.3.2 Identifying recoverable artifacts
  - 4.3.3 Preserving git commits and logs
- 4.4 Phase 2: Manager notification and approval
  - 4.4.1 Composing the replacement request
  - 4.4.2 Required information for approval
  - 4.4.3 Handling approval response
  - 4.4.4 Handling rejection response
- 4.5 Phase 3: Creating the replacement agent
  - 4.5.1 Selecting the host for the new agent
  - 4.5.2 Creating a new local folder
  - 4.5.3 Cloning the git repository
  - 4.5.4 Starting the new Claude Code session
  - 4.5.5 Registering with AI Maestro
- 4.6 Phase 4: Orchestrator notification
  - 4.6.1 Notifying orchestrator about replacement
  - 4.6.2 Requesting handoff document generation
  - 4.6.3 Requesting GitHub Project update
- 4.7 Phase 5: Work handoff to new agent
  - 4.7.1 Sending handoff documentation
  - 4.7.2 Sending task assignments
  - 4.7.3 Awaiting acknowledgment
  - 4.7.4 Verifying new agent understanding
- 4.8 Phase 6: Cleanup and closure
  - 4.8.1 Updating incident log
  - 4.8.2 Notifying manager of completion
  - 4.8.3 Archiving old agent records
- 4.9 Complete replacement workflow checklist

---

## 4.1 When to Use This Document

Use this document when:
- An agent has been classified as a **terminal failure** per `references/failure-classification.md`
- All recovery strategies have been exhausted per `references/recovery-strategies.md`
- Manager (AMAMA) has approved agent replacement
- You need to create a new agent to take over the failed agent's work

**CRITICAL**: The replacement agent has NO MEMORY of the old agent. All context, in-progress work, and task understanding must be explicitly transferred through documentation.

---

## 4.2 Overview of the Replacement Protocol

The replacement protocol consists of six phases executed in sequence:

```
Phase 1: Failure Confirmation --> Phase 2: Manager Approval --> Phase 3: Create Agent
                                                                        |
                                                                        v
Phase 6: Cleanup <-- Phase 5: Work Handoff <-- Phase 4: Orchestrator Notification
```

| Phase | Owner | Duration | Key Output |
|-------|-------|----------|------------|
| 1. Failure Confirmation | AMCOS | 5-10 min | Artifact inventory |
| 2. Manager Approval | AMAMA | 5-30 min | Approval decision |
| 3. Create Agent | AMCOS + User | 10-30 min | New agent online |
| 4. Orchestrator Notification | AMCOS -> AMOA | 5-10 min | Handoff docs, kanban update |
| 5. Work Handoff | AMCOS -> New Agent | 10-20 min | Agent acknowledgment |
| 6. Cleanup | AMCOS | 5 min | Incident closed |

**Total estimated time**: 40-110 minutes depending on complexity and response times.

---

## 4.3 Phase 1: Failure Confirmation and Artifact Preservation

### 4.3.1 Confirming Agent Cannot Be Recovered

Before proceeding with replacement, AMCOS must document that recovery is impossible:

**Confirmation checklist:**


```markdown
## Recovery Exhaustion Confirmation

Agent: [AGENT_SESSION_NAME]
Failure detected: [ISO_TIMESTAMP]
Classification: TERMINAL

### Recovery Attempts

| Strategy | Attempted | Result | Notes |
|----------|-----------|--------|-------|
| Wait and Retry | Yes/No | Failed/N/A | [details] |
| Soft Restart | Yes/No | Failed/N/A | [details] |
| Hard Restart | Yes/No | Failed/N/A | [details] |
| Hibernate-Wake | Yes/No | Failed/N/A | [details] |
| Resource Adjustment | Yes/No | Failed/N/A | [details] |

### Terminal Failure Evidence

- [ ] Agent process confirmed dead
- [ ] Host unreachable OR working directory corrupted
- [ ] 3+ consecutive recovery failures
- [ ] State unrecoverable (context lost, credentials invalid, etc.)


Confirmed by: AMCOS
Confirmation timestamp: [ISO_TIMESTAMP]
```

### 4.3.2 Identifying Recoverable Artifacts

Even when the agent cannot be recovered, some work products may be salvageable:

**Artifact categories:**

| Artifact Type | Location | Recovery Method |
|---------------|----------|-----------------|
| Git commits | Remote repository | Clone from origin |
| Local uncommitted changes | Agent's working directory | May be lost if disk corrupted |
| Log files | Project `logs/` directory | Copy if host accessible |
| Conversation history | Claude session | Lost if session terminated |
| Task tracking files | `$CLAUDE_PROJECT_DIR/.amcos/` | Copy if accessible |
| Handoff documents | `thoughts/shared/handoffs/` | Likely preserved in git |

### 4.3.3 Preserving Git Commits and Logs

**Step 1: Check last known commit from the failed agent**

If AMCOS has SSH access to the host:

```bash
# Attempt to get git status from failed agent's directory
ssh USER@HOST "cd /path/to/agent/project && git log -1 --oneline" 2>/dev/null
```

**Step 2: Document the last known state**

Create an artifact inventory at `$CLAUDE_PROJECT_DIR/.amcos/agent-health/artifacts-AGENT_NAME.md` documenting the git state, preserved logs, and lost artifacts.

---

## 4.4 Phase 2: Manager Notification and Approval

### 4.4.1 Composing the Replacement Request

AMCOS must request approval from the manager (AMAMA) before creating a replacement agent.

Use the `agent-messaging` skill to send the replacement approval request:
- **Recipient**: `amama-assistant-manager`
- **Subject**: `[APPROVAL REQUIRED] Agent replacement request`
- **Priority**: `urgent`
- **Content**: type `replacement-approval-request`, including:
  - Message explaining the terminal failure and need for replacement
  - Agent name
  - Failure summary (failure type, cause, detected timestamp, recovery attempts count, last recovery attempt timestamp)
  - Impact assessment (tasks affected, estimated work lost, downstream dependencies)
  - Replacement plan (new agent name, target host, estimated time to operational, handoff required from AMOA)
  - Artifacts preserved and lost
  - Awaiting approval flag
  - Response requested by timestamp

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### 4.4.2 Required Information for Approval

The manager needs the following to make an informed decision:

| Information | Why Needed |
|-------------|------------|
| Agent name and role | Context about what was being done |
| Failure cause | Understanding what went wrong |
| Recovery attempts | Confidence that replacement is necessary |
| Impact assessment | Understanding of consequences |
| Work lost | Planning for redo effort |
| Replacement plan | Feasibility check |
| Artifacts preserved | What can be recovered |

### 4.4.3 Handling Approval Response

When manager approves, the response will include any additional instructions:

```json
{
  "type": "replacement-approval",
  "decision": "approved",
  "message": "Replacement approved. Proceed with the plan.",
  "additional_instructions": [
    "Use the same session name (libs-svg-svgbbox) to maintain continuity",
    "Prioritize task-001 for the replacement agent"
  ],
  "approved_by": "amama-assistant-manager",
  "approved_at": "2025-01-15T11:00:00Z"
}
```

**Upon approval:**
1. Log the approval
2. Proceed to Phase 3

### 4.4.4 Handling Rejection Response

The manager may reject the replacement request:

```json
{
  "type": "replacement-approval",
  "decision": "rejected",
  "message": "Replacement not approved at this time.",
  "reason": "The host machine is being repaired. Wait 2 hours and retry recovery.",
  "alternative_action": "wait_and_retry_in_2_hours",
  "rejected_by": "amama-assistant-manager",
  "rejected_at": "2025-01-15T11:00:00Z"
}
```

**Upon rejection:**
1. Log the rejection
2. Follow the alternative action specified
3. Reschedule replacement request if appropriate

---

## 4.5 Phase 3: Creating the Replacement Agent

### 4.5.1 Selecting the Host for the New Agent

The replacement agent should run on a stable host. Considerations:

| Factor | Recommendation |
|--------|----------------|
| Same host as failed agent | Only if failure was software, not hardware |
| Different host | Preferred if hardware failure suspected |
| Resource availability | Ensure sufficient CPU/memory/disk |
| Network connectivity | Must be able to reach AI Maestro and git remotes |

### 4.5.2 Creating a New Local Folder

The replacement agent needs a fresh working directory. **The new agent will NOT inherit the old agent's local files.**

Use the `agent-messaging` skill to request the user to create the folder:
- **Recipient**: the user or admin
- **Subject**: `[USER ACTION REQUIRED] Create folder for replacement agent`
- **Priority**: `high`
- **Content**: type `user-action-required`, with instructions to create the new directory at the target path

### 4.5.3 Cloning the Git Repository

The new agent must clone the project repository to access code and history.

Use the `agent-messaging` skill to request the user to clone the repository:
- **Recipient**: the user or admin
- **Subject**: `[USER ACTION REQUIRED] Clone repository for replacement agent`
- **Priority**: `high`
- **Content**: type `user-action-required`, with instructions to clone the repo and checkout the appropriate branch

### 4.5.4 Starting the New Claude Code Session

Use the `agent-messaging` skill to request the user to start a new Claude Code session:
- **Recipient**: the user or admin
- **Subject**: `[USER ACTION REQUIRED] Start Claude Code session for replacement agent`
- **Priority**: `high`
- **Content**: type `user-action-required`, with instructions to create a tmux session, navigate to the working directory, and start Claude Code

### 4.5.5 Registering with AI Maestro

The new agent should automatically register when it starts (via AI Maestro hooks).

Use the `ai-maestro-agents-management` skill to verify the agent is registered with status "online".

If registration fails, troubleshoot:
1. Check agent has AI Maestro hooks enabled
2. Check AI Maestro server is running
3. Check agent's session name matches expected

---

## 4.6 Phase 4: Orchestrator Notification

### 4.6.1 Notifying Orchestrator About Replacement

AMCOS must notify the orchestrator (AMOA) that an agent has been replaced so that:
1. The orchestrator can generate a handoff document for the new agent
2. The GitHub Project kanban can be updated to reassign tasks

Use the `agent-messaging` skill to notify the orchestrator:
- **Recipient**: `amoa-orchestrator`
- **Subject**: `[AGENT REPLACED] Handoff required for new agent`
- **Priority**: `high`
- **Content**: type `agent-replacement-notification`, including:
  - Message explaining the replacement and requesting handoff documentation and task reassignment
  - Old agent details (name, status "terminated", last commit, tasks in progress)
  - New agent details (name, status "online", working directory, git branch)
  - Actions required: generate handoff document, update GitHub Project kanban

### 4.6.2 Requesting Handoff Document Generation

The orchestrator (AMOA) is responsible for generating a comprehensive handoff document that includes:

| Section | Content |
|---------|---------|
| Project Overview | What the project is about |
| Current Sprint Goals | What needs to be achieved |
| Assigned Tasks | Tasks assigned to this agent |
| Task Details | Requirements, acceptance criteria, dependencies |
| Codebase Context | Key files, architecture, conventions |
| In-Progress Work | What the old agent was working on |
| Known Issues | Blockers, bugs, concerns |
| Communication Channels | How to report progress, ask questions |

The orchestrator will create this document at:
```
$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/AGENT_NAME/handoff-TIMESTAMP.md
```

### 4.6.3 Requesting GitHub Project Update

The orchestrator must update the GitHub Project kanban to:

1. **Reassign tasks** from old agent to new agent
2. **Update task status** if any were marked "in progress" by old agent
3. **Add note** about agent replacement to affected tasks

---

## 4.7 Phase 5: Work Handoff to New Agent

### 4.7.1 Sending Handoff Documentation

Once AMOA has generated the handoff document, use the `agent-messaging` skill to send it to the new agent:
- **Recipient**: the new agent session name
- **Subject**: `[ONBOARDING] Welcome - please read handoff documentation`
- **Priority**: `urgent`
- **Content**: type `agent-onboarding`, including:
  - Message explaining this is a replacement agent with no memory of previous work
  - Handoff document path
  - Step-by-step instructions (read handoff completely, review git history, check assigned tasks, reply acknowledging assignments, ask clarifying questions)
  - Git branch and last known commit
  - GitHub Project URL

### 4.7.2 Sending Task Assignments

After the handoff document, use the `agent-messaging` skill to send specific task assignments:
- **Recipient**: the new agent session name
- **Subject**: `[TASK ASSIGNMENTS] Your assigned tasks`
- **Priority**: `high`
- **Content**: type `task-assignment`, including:
  - Message explaining these were previously assigned to the predecessor
  - Tasks list (each with task ID, title, priority, status, GitHub issue URL, and notes about predecessor progress)

### 4.7.3 Awaiting Acknowledgment

The new agent MUST acknowledge the handoff before AMCOS considers the replacement complete.

**Expected acknowledgment:**

```json
{
  "type": "handoff-acknowledgment",
  "message": "I have read the handoff documentation and understand my assignments.",
  "handoff_document_read": true,
  "tasks_understood": ["task-001", "task-002"],
  "questions": [],
  "ready_to_begin": true
}
```

**If no acknowledgment within 15 minutes:**

Use the `agent-messaging` skill to send a reminder:
- **Recipient**: the new agent session name
- **Subject**: `[REMINDER] Handoff acknowledgment required`
- **Priority**: `urgent`
- **Content**: type `acknowledgment-reminder`, requesting receipt acknowledgment and response deadline

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### 4.7.4 Verifying New Agent Understanding

After acknowledgment, use the `agent-messaging` skill to verify understanding:
- **Recipient**: the new agent session name
- **Subject**: `[VERIFICATION] Confirm task understanding`
- **Priority**: `normal`
- **Content**: type `understanding-verification`, asking the agent to summarize the primary task in their own words, including acceptance criteria and planned approach

---

## 4.8 Phase 6: Cleanup and Closure

### 4.8.1 Updating Incident Log

Record the complete incident with resolution in the incident log at `$CLAUDE_PROJECT_DIR/.amcos/agent-health/incident-log.jsonl`.

### 4.8.2 Notifying Manager of Completion

Use the `agent-messaging` skill to inform the manager that replacement is complete:
- **Recipient**: `amama-assistant-manager`
- **Subject**: `[RESOLVED] Agent replacement complete`
- **Priority**: `normal`
- **Content**: type `replacement-complete`, including:
  - Message confirming successful replacement
  - Incident summary (original failure, detected timestamp, approval timestamp, new agent online timestamp, handoff acknowledged timestamp, total downtime)
  - New agent status: "operational"
  - Work lost and work recovered
  - Incident ID

### 4.8.3 Archiving Old Agent Records

Move old agent's records to archive:

```bash
# Archive old agent configuration
mv $CLAUDE_PROJECT_DIR/.amcos/agent-health/heartbeat-config.json.backup-AGENT_NAME \
   $CLAUDE_PROJECT_DIR/.amcos/archive/agents/

# Keep incident log intact (do not archive)
```

---

## 4.9 Complete Replacement Workflow Checklist

Use this checklist to track progress through the replacement protocol:

```markdown
## Agent Replacement Checklist

- [ ] 4.1 Confirm replacement is necessary (failure classification, recovery exhausted)
- [ ] 4.2 Review replacement protocol overview
- [ ] 4.3.1 Confirm agent cannot be recovered
- [ ] 4.3.2 Identify recoverable artifacts
- [ ] 4.3.3 Preserve git commits and logs
- [ ] 4.4.1 Compose replacement request for manager
- [ ] 4.4.2 Prepare required information for approval
- [ ] 4.4.3 Handle approval response
- [ ] 4.4.4 Handle rejection response
- [ ] 4.5.1 Select host for new agent
- [ ] 4.5.2 Create new local folder
- [ ] 4.5.3 Clone git repository
- [ ] 4.5.4 Start new Claude Code session
- [ ] 4.5.5 Register with AI Maestro
- [ ] 4.6.1 Notify orchestrator about replacement
- [ ] 4.6.2 Request handoff document generation
- [ ] 4.6.3 Request GitHub Project update
- [ ] 4.7.1 Send handoff documentation to new agent
- [ ] 4.7.2 Send task assignments to new agent
- [ ] 4.7.3 Await acknowledgment from new agent
- [ ] 4.7.4 Verify new agent understanding
- [ ] 4.8.1 Update incident log
- [ ] 4.8.2 Notify manager of completion
- [ ] 4.8.3 Archive old agent records
```

## Summary

| Phase | Step | Status |
|-------|------|--------|
| 1. Failure Confirmation | 4.3.1-4.3.3 | ☐ |
| 2. Manager Approval | 4.4.1-4.4.4 | ☐ |
| 3. Create Agent | 4.5.1-4.5.5 | ☐ |
| 4. Orchestrator Notification | 4.6.1-4.6.3 | ☐ |
| 5. Work Handoff | 4.7.1-4.7.4 | ☐ |
| 6. Cleanup | 4.8.1-4.8.3 | ☐ |

---

*For questions about this protocol, contact the AI Maestro Chief of Staff (AMCOS).*
