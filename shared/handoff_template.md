# Handoff Document Template

This template defines the standard format for handoff documents between roles in the 4-plugin architecture.

## Plugin Prefixes

| Plugin | Prefix | Full Name |
|--------|--------|-----------|
| Chief of Staff | `amcos-` | AI Maestro Chief of Staff Agent |
| Architect | `amaa-` | AI Maestro Architect Agent |
| Orchestrator | `amoa-` | AI Maestro Orchestrator Agent |
| Integrator | `amia-` | AI Maestro Integrator Agent |

## Handoff File Format

```yaml
---
uuid: "handoff-{uuid}"
from_role: "amcos" | "amaa" | "amoa" | "amia"
to_role: "amcos" | "amaa" | "amoa" | "amia"
created: "ISO-8601 timestamp"
github_issue: "#issue_number"  # Optional
subject: "Brief description"
priority: "urgent" | "high" | "normal" | "low"
requires_ack: true | false
status: "pending" | "acknowledged" | "completed" | "rejected"
---

## Context

[Background information and context for this handoff]

## Requirements / Deliverables

[What needs to be done or what is being delivered]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Dependencies

- Depends on: [list of dependencies]
- Blocks: [list of blocked items]

## Notes

[Additional notes or considerations]
```

## Chief of Staff Context Handoff

When Chief of Staff hands off context to another session (for session continuity):

```yaml
---
uuid: "handoff-{uuid}"
from_role: "amcos"
to_role: "amcos"  # Same role - session continuity
created: "ISO-8601 timestamp"
handoff_type: "session_continuity"
reason: "context_limit" | "user_request" | "scheduled" | "error_recovery"
---

## Session State

### Active Agents

| Session Name | Role | Status | Task | Progress |
|--------------|------|--------|------|----------|
| amaa-project-abc123 | architect | active | Design API | 75% |
| amoa-project-def456 | orchestrator | blocked | Implement feature | 50% |

### Pending Approvals

| Request ID | Type | From | Waiting Since | Priority |
|------------|------|------|---------------|----------|
| apr-001 | push | amoa-project-def456 | 2025-02-01T10:30:00Z | high |

### Open Issues

| Issue | Assigned To | Status | Blocker |
|-------|-------------|--------|---------|
| #123 | amaa-project-abc123 | in-progress | none |
| #124 | amoa-project-def456 | blocked | needs_approval |

### User Preferences

- Notification level: verbose | normal | quiet
- Auto-approve: [list of auto-approved action types]
- Active project: {project_name}

### Recent Actions

1. [timestamp] Action 1 description
2. [timestamp] Action 2 description
3. [timestamp] Action 3 description

### Pending User Questions

1. [Question about X - waiting since timestamp]

## Checkpoint State

Last validated phase per agent:

| Agent | Phase | Validated At |
|-------|-------|--------------|
| amaa-project-abc123 | design_complete | 2025-02-01T10:00:00Z |
| amoa-project-def456 | tests_written | 2025-02-01T09:45:00Z |

## Resume Instructions

1. Load active agent states
2. Check for pending approvals
3. Resume heartbeat monitoring
4. Continue from last checkpoint
```

## Communication Hierarchy

```
USER <-> AMCOS (Chief of Staff) <-> AMAA (Architect)
                                  <-> AMOA (Orchestrator)
                                  <-> AMIA (Integrator)
```

**CRITICAL**: Architect (amaa-), Orchestrator (amoa-), and Integrator (amia-) do NOT communicate directly with each other. All communication flows through Chief of Staff (amcos-).

## Handoff Types

### 1. User Request -> Role Assignment
- From: amcos (chief-of-staff)
- To: amaa | amoa | amia
- Purpose: Route user request to appropriate specialist

### 2. Design Complete -> Orchestration
- From: amaa (via amcos)
- To: amoa (via amcos)
- Purpose: Hand off approved design for implementation

### 3. Implementation Complete -> Integration
- From: amoa (via amcos)
- To: amia (via amcos)
- Purpose: Signal work ready for quality gates

### 4. Quality Gate Results -> User
- From: amia (via amcos)
- To: user
- Purpose: Report integration status and request approvals

### 5. Session Continuity (COS-specific)
- From: amcos
- To: amcos (new session)
- Purpose: Transfer state when context limit reached or session ends

### 6. Emergency Handoff
- From: any role
- To: amcos
- Purpose: Urgent state transfer when agent must terminate unexpectedly

## File Naming Convention

```
handoff-{uuid}-{from}-to-{to}.md

Examples:
- handoff-a1b2c3d4-amcos-to-amaa.md    # COS assigns to Architect
- handoff-e5f6g7h8-amaa-to-amcos.md    # Architect reports to COS
- handoff-i9j0k1l2-amcos-to-amoa.md    # COS assigns to Orchestrator
- handoff-m3n4o5p6-amoa-to-amcos.md    # Orchestrator reports to COS
- handoff-q7r8s9t0-amcos-to-amia.md    # COS assigns to Integrator
- handoff-u1v2w3x4-amia-to-amcos.md    # Integrator reports to COS
- handoff-w5x6y7z8-amcos-to-amcos.md   # COS session continuity
- handoff-a9b0c1d2-amoa-emergency.md  # Emergency handoff from Orchestrator
```

## Storage Location

All handoff files are stored in: `docs_dev/handoffs/`

## Handoff Lifecycle

1. **Created** - Handoff document created, status: pending
2. **Sent** - AI Maestro message sent to recipient
3. **Acknowledged** - Recipient confirms receipt, status: acknowledged
4. **In Progress** - Recipient actively working on task
5. **Completed** - Task finished, status: completed
6. **Rejected** - Recipient cannot accept, status: rejected (with reason)

