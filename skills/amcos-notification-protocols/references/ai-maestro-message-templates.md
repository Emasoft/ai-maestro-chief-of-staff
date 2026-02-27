# AI Maestro Message Templates for AMCOS

Reference for all inter-agent message templates used by AI Maestro Chief of Staff (AMCOS).

All messages use the AMP protocol via `amp-send.sh`. Never call the HTTP API directly.

## Contents

- [1. Standard Message Format (AMP)](#1-standard-message-format-amp)
- [2. When Requesting Approval from EAMA](#2-when-requesting-approval-from-eama)
- [3. When Escalating Issues to EAMA](#3-when-escalating-issues-to-eama)
- [4. When Notifying Agents of Upcoming Operations](#4-when-notifying-agents-of-upcoming-operations)
- [5. When Reporting Operation Results](#5-when-reporting-operation-results)
- [6. When Notifying EOA of New Agent Availability](#6-when-notifying-eoa-of-new-agent-availability)
- [7. When Requesting Team Status from EOA](#7-when-requesting-team-status-from-eoa)
- [8. When Broadcasting Team Updates](#8-when-broadcasting-team-updates)
- [9. Message Type Reference](#9-message-type-reference)

---

## 1. Standard Message Format (AMP)

All messages are sent using `amp-send.sh`. Messages are automatically Ed25519-signed by the AMP transport layer.

**Setup (once per agent):**
```bash
amp-init.sh --auto
```

**Base send command:**
```bash
amp-send.sh --to <recipient> --subject "<subject>" --priority <priority> --type <type> --message "<message>"
```

**Priority values:** `urgent`, `high`, `normal`, `low`

---

## 2. When Requesting Approval from EAMA

**Use case:** Before spawning, terminating, or replacing agents.

```bash
amp-send.sh --to eama-main \
  --subject "APPROVAL REQUIRED: <operation_type>" \
  --priority normal \
  --type approval_request \
  --message "Operation: <description>. Target: <agent>. Justification: <reason>. Risk: <low|medium|high>. Rollback: <plan>. Request-ID: <uuid>. Timeout: 120s"
```

**Expected response fields:** `decision` (approved|rejected|revision_needed), `reason`, `conditions` (optional).

---

## 3. When Escalating Issues to EAMA

**Use case:** Issues outside AMCOS authority or requiring human intervention.

```bash
amp-send.sh --to eama-assistant-manager \
  --subject "[ESCALATION] <SITUATION_TYPE>" \
  --priority <urgent|high|normal> \
  --type escalation \
  --message "Issue: <description>. Severity: <low|medium|high|critical>. Affected: <resources>. Attempts: <N>. Last error: <details>. Recommended action: <action>. User decision required: <yes|no>. Escalation-ID: <uuid>"
```

**Escalation Priority Guidelines:**

| Situation | Priority | Timeout |
|-----------|----------|---------|
| Agent spawn failure (3 attempts) | `urgent` | 5 min |
| Resource exhaustion | `urgent` | 5 min |
| Approval timeout (critical) | `urgent` | 2 min |
| Agent conflict | `high` | 10 min |
| GitHub API failure | `high` | 15 min |
| Plugin failure | `normal` | 30 min |

---

## 4. When Notifying Agents of Upcoming Operations

**Use case:** Before hibernating, terminating, or moving an agent.

```bash
amp-send.sh --to <target-agent> \
  --subject "NOTICE: <operation_type> in <seconds>s" \
  --priority high \
  --type operation_notice \
  --message "Operation: <description>. Type: <hibernate|terminate|move>. Countdown: <seconds>s. Save your work and reply with 'ok' when ready."
```

**Standard countdown times:** Hibernation: 30s, Termination: 30s, Project move: 60s.

---

## 5. When Reporting Operation Results

**Use case:** After completing spawn, terminate, hibernate, wake operations.

```bash
amp-send.sh --to <requesting-agent> \
  --subject "RESULT: <operation_type> - <SUCCESS|FAILED>" \
  --priority <normal|high> \
  --type operation_result \
  --message "Operation: <description>. Status: <success|failure|partial>. Target: <resource>. Duration: <ms>ms. Error: <details or none>"
```

**Priority:** `normal` for success, `high` for failure.

---

## 6. When Notifying EOA of New Agent Availability

**Use case:** After spawning agent and adding to team.

```bash
amp-send.sh --to <orchestrator-session> \
  --subject "NEW AGENT: <agent_name> available" \
  --priority normal \
  --type team_update \
  --message "Agent: <name>. Role: <role>. Capabilities: <list>. Working dir: <path>. Registry: <path>. Agent is ready for task assignments."
```

---

## 7. When Requesting Team Status from EOA

**Use case:** Checking current status of all team members.

```bash
amp-send.sh --to <orchestrator-session> \
  --subject "REQUEST: Team status report" \
  --priority normal \
  --type status_request \
  --message "Requesting: active agents, hibernated agents, in-progress tasks, idle agents. Request-ID: <uuid>"
```

---

## 8. When Broadcasting Team Updates

**Use case:** Informing all team members of registry changes.

Send to each team member individually:

```bash
for agent in <agent1> <agent2> <agent3>; do
  amp-send.sh --to "$agent" \
    --subject "TEAM UPDATE: <update_description>" \
    --priority normal \
    --type team_broadcast \
    --message "Update: <description>. Registry: <path>. Action: <refresh_registry|update_roles|member_removed|member_added>"
done
```

**Broadcast actions:** `refresh_registry`, `update_roles`, `member_removed`, `member_added`.

---

## 9. Message Type Reference

| Message Type | Purpose | Priority | Response Expected |
|--------------|---------|----------|-------------------|
| `approval_request` | Request permission from EAMA | `normal` | Yes (timeout: 120s) |
| `escalation` | Report critical issue to EAMA | `urgent`/`high` | Yes (varies) |
| `operation_notice` | Warn agent of upcoming operation | `high` | No |
| `operation_result` | Report operation outcome | `normal`/`high` | No |
| `team_update` | Notify EOA of new agent | `normal` | No |
| `status_request` | Request team status from EOA | `normal` | Yes (timeout: 60s) |
| `team_broadcast` | Notify all team members | `normal` | No |
| `health_check` | Verify agent is responsive | `normal` | Yes (timeout: 30s) |

**Priority guidelines:**
- `urgent`: Immediate attention (< 5 min response)
- `high`: Handle soon (< 15 min response)
- `normal`: Standard (< 60 min response)
- `low`: Non-critical, handle when convenient

---

## Notes

- **Always use `amp-send.sh`** -- never call the HTTP API directly
- **Ed25519 signing** is automatic via `amp-send.sh` (keypair from `amp-init.sh --auto`)
- **Always use full session names** (e.g., `amcos-chief-of-staff`, not `ecos`)
- **Always generate unique request IDs** for operations requiring tracking
- **Always specify rollback plan** in approval requests
- **Always include duration** in operation results
- **Always use `type` field** in content for message routing
