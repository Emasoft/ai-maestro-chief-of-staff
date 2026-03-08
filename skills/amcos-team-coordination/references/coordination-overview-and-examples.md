# Team Coordination - Overview, Examples, and Reference

## Table of Contents
- What Is Team Coordination
- Team Coordination Components
- Examples: Assigning a Role to a New Agent
- Examples: Broadcasting a Team Update
- Examples: Checking Team Status
- Examples: Full Coordination Workflow with Input/Output
- Examples: Role Assignment with Input/Output
- Examples: Team Status Query with Input/Output
- Key Takeaways
- Task Checklist

## What Is Team Coordination

Team coordination is the process of organizing multiple AI agents to work together on shared goals. The Chief of Staff acts as the central coordination point, ensuring agents are assigned appropriate roles, can communicate effectively, and remain aware of each other's progress and status.

**Key characteristics:**
- **Distributed**: Team members run in separate Claude Code sessions
- **Asynchronous**: Communication happens via message queues, not direct calls
- **Role-based**: Each agent has a defined role with specific responsibilities
- **Status-aware**: Chief of Staff tracks all team member states

## Team Coordination Components

### 1. Role Assignment
Matching agents to roles based on capabilities and task requirements.

### 2. Team Messaging
Facilitating communication between team members via AI Maestro.

### 3. Teammate Awareness
Maintaining visibility into all team members' current status and activities.

## Examples: Assigning a Role to a New Agent

Use the `agent-messaging` skill to send a role assignment message:
- **Recipient**: `helper-agent-generic`
- **Subject**: `Role Assignment: Code Reviewer`
- **Priority**: `high`
- **Content**: type `role-assignment`, explaining that the agent is assigned the Code Reviewer role with responsibilities: review PRs, enforce code standards, provide feedback

**Verify**: confirm message delivery and await role acceptance acknowledgment.

## Examples: Broadcasting a Team Update

Use the `agent-messaging` skill to broadcast a message to all team members:
- **Subject**: `Sprint Planning Complete`
- **Priority**: `normal`
- **Content**: type `announcement`, informing that Sprint 5 planning is complete and all tasks are assigned

**Verify**: confirm delivery to all team members.

## Examples: Checking Team Status

Use the `ai-maestro-agents-management` skill to list all active sessions and their status, including each agent's name, status, and last seen timestamp.

**Verify**: all expected team members appear in the list with correct status.

## Examples: Full Coordination Workflow with Input/Output

**Input:** User requests a new team for project "auth-service"

```
User message: "Set up a team for the auth-service project.
I need an architect, an orchestrator, and two programmers."
```

**Output:** AMCOS creates the team and confirms formation

```
[TEAM-FORMED] auth-service
  Agents spawned:
    - eaa-auth-service-architect (Architect) - ACTIVE
    - eoa-auth-service-orchestrator (Orchestrator) - ACTIVE
    - auth-service-programmer-001 (Programmer) - ACTIVE
    - auth-service-programmer-002 (Programmer) - ACTIVE
  Team registry updated via REST API
  Messages sent: 4 role assignments delivered
```

## Examples: Role Assignment with Input/Output

**Input:** AMCOS assigns a code reviewer role to an existing agent

```json
{
  "to": "eia-feature-reviewer",
  "subject": "Role Assignment: Code Reviewer for auth-service",
  "priority": "high",
  "content": {
    "type": "role-assignment",
    "message": "You are assigned as Code Reviewer for auth-service. Responsibilities: review all PRs, enforce code standards, verify test coverage above 80%."
  }
}
```

**Output:** Agent acknowledges the role assignment

```json
{
  "from": "eia-feature-reviewer",
  "subject": "Role Accepted: Code Reviewer for auth-service",
  "content": {
    "type": "role-acceptance",
    "message": "Role accepted. Ready to review PRs for auth-service."
  }
}
```

## Examples: Team Status Query with Input/Output

**Input:** Query team status via AI Maestro API

```bash
curl -s "http://localhost:23000/api/sessions" | jq '.sessions[] | select(.project == "auth-service")'
```

**Output:** Current team status result

```json
[
  {"name": "eaa-auth-service-architect", "role": "Architect", "status": "active", "last_seen": "2026-02-14T10:30:00Z"},
  {"name": "eoa-auth-service-orchestrator", "role": "Orchestrator", "status": "active", "last_seen": "2026-02-14T10:29:45Z"},
  {"name": "auth-service-programmer-001", "role": "Programmer", "status": "active", "last_seen": "2026-02-14T10:28:12Z"},
  {"name": "auth-service-programmer-002", "role": "Programmer", "status": "idle", "last_seen": "2026-02-14T10:15:00Z"}
]
```

## Key Takeaways

1. **Role assignment requires confirmation** - Do not assume assignment succeeded without acknowledgment
2. **Message priority matters** - Use appropriate priority to ensure timely delivery
3. **Continuous awareness is essential** - Poll status regularly, not just when needed
4. **Log all coordination actions** - Maintain audit trail for debugging and recovery
5. **Handle failures gracefully** - Retry, escalate, but never ignore coordination failures

## Task Checklist

- [ ] Understand team coordination purpose and components
- [ ] Learn PROCEDURE 1: Assign agent roles
- [ ] Learn PROCEDURE 2: Send team messages
- [ ] Learn PROCEDURE 3: Maintain teammate awareness
- [ ] Practice role assignment workflow
- [ ] Practice team messaging via AI Maestro
- [ ] Practice status monitoring and reporting
