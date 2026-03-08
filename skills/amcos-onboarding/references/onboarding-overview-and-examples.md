# Onboarding - Overview, Examples, and Reference

## Table of Contents
- What Is Agent Onboarding
- Onboarding Components
- Examples: Initiating Onboarding for New Developer
- Examples: Role Briefing Message
- Examples: Project Handoff Summary
- Handoff Validation Checklist
- Handoff Required Fields
- Key Takeaways
- Task Checklist

## What Is Agent Onboarding

Agent onboarding is a structured process to prepare a new agent for effective participation in a multi-agent team. Unlike human onboarding which may take days or weeks, agent onboarding happens in minutes but must be thorough and precise.

**Key characteristics:**
- **Structured**: Follows a defined checklist
- **Role-specific**: Tailored to the agent's assigned role
- **Context-rich**: Provides necessary project knowledge
- **Verifiable**: Confirms understanding before work begins

## Onboarding Components

### 1. Onboarding Checklist
A systematic list of items to cover during onboarding.

### 2. Role Briefing
Detailed explanation of the agent's role, responsibilities, and expectations.

### 3. Project Handoff
Transfer of essential project knowledge, conventions, and current state.

## Examples: Initiating Onboarding for New Developer

Use the `agent-messaging` skill to send an onboarding initiation message:
- **Recipient**: `new-developer-agent`
- **Subject**: `Welcome - Onboarding Session Starting`
- **Priority**: `high`
- **Content**: type `request`, welcoming the agent to the team, introducing yourself as Chief of Staff, and requesting confirmation that the agent is ready to begin onboarding

**Verify**: confirm message delivery and await agent readiness confirmation.

## Examples: Role Briefing Message

```markdown
# Role Briefing: Developer

## Your Assigned Role
You are assigned as a **Developer** on the Authentication Module.

## Responsibilities
1. Implement features from the backlog
2. Write unit tests for all new code
3. Update documentation for your changes
4. Participate in code reviews when requested

## Reporting Structure
- **Report to:** orchestrator-master for task assignments
- **Coordinate with:** auth-code-reviewer for reviews
- **Escalate to:** chief-of-staff for blockers

## Expectations
- Acknowledge task assignments promptly
- Provide regular status updates during active work
- Request clarification if requirements are unclear
- Follow project coding conventions

Please confirm you understand these responsibilities.
```

## Examples: Project Handoff Summary

```markdown
# Project Handoff: Authentication Module

## Project Overview
We are building a secure authentication module for the main application.
Current sprint: Sprint 5 (2 weeks remaining)

## Current State
- Login endpoint: COMPLETE
- Logout endpoint: IN PROGRESS (60%)
- Password reset: NOT STARTED
- Session management: BLOCKED (waiting on logout)

## Key Files
- src/auth/login.py - Login implementation
- src/auth/logout.py - Logout implementation (your focus)
- tests/auth/ - Test directory

## Conventions
- Use async/await for all I/O operations
- All endpoints return JSON
- Error responses use standard error format
- Tests required for all new functions

## Active Context
The logout endpoint is partially implemented. Current work is at line 145.
Next step: Implement session invalidation.
```

## Handoff Validation Checklist

Before sending any handoff document to a new agent, validate using this checklist:

```markdown
### Handoff Validation Checklist

Before sending handoff:
- [ ] All required fields present (from/to/type/UUID/task)
- [ ] UUID is unique (check existing handoffs: `ls $CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/`)
- [ ] Target agent exists and is alive (use the `ai-maestro-agents-management` skill to list agents and verify the target is online)
- [ ] All referenced files exist (`test -f <path> && echo "EXISTS" || echo "MISSING"`)
- [ ] No placeholder [TBD] markers (`grep -r "\[TBD\]" handoff.md`)
- [ ] Document is valid markdown (no broken links, proper formatting)
- [ ] Acceptance criteria clearly defined
- [ ] Current state accurately reflects reality
- [ ] Contact information for questions provided
```

**Validation command:**
```bash
# Validate the plugin (including handoff documents) using the CPV plugin validator
uv run --with pyyaml python scripts/validate_plugin.py . --verbose
```

## Handoff Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `from` | Sending agent name | `amcos-chief-of-staff` |
| `to` | Target agent name | `new-developer-agent` |
| `type` | Handoff type | `project-handoff`, `role-briefing`, `emergency-handoff` |
| `UUID` | Unique handoff identifier | `HO-20250204-auth-001` |
| `task` | Task or role being handed off | `Authentication Module Development` |

## Key Takeaways

1. **Onboarding is mandatory** - Never assign work before onboarding is complete
2. **Verification is essential** - Confirm understanding at each step
3. **Role briefing must be specific** - Generic descriptions cause confusion
4. **Project handoff includes state** - Not just structure but current progress
5. **Document completion** - Record that onboarding happened and what was covered
6. **Validate before sending** - Always run handoff validation checklist

## Task Checklist

- [ ] Understand onboarding purpose and components
- [ ] Learn PROCEDURE 1: Execute onboarding checklist
- [ ] Learn PROCEDURE 2: Deliver role briefing
- [ ] Learn PROCEDURE 3: Conduct project handoff
- [ ] Practice complete onboarding workflow
- [ ] Create onboarding templates for common roles
- [ ] Verify onboarding completeness metrics
