# Team Registry Specification

> **SUPERSEDED**: The file-based `.ai-maestro/team-registry.json` approach is superseded.
> Team registries are now managed exclusively via the **AI Maestro REST API**.

**Version**: 2.0.0
**Last Updated**: 2026-02-27

This document specifies the team registry API, agent registration, and naming conventions for the AMCOS plugin.

---

## Overview

Team registries are managed centrally through the **AI Maestro REST API**. There are no local JSON files to maintain. All team and agent data is stored server-side and accessed via HTTP endpoints.

---

## API Endpoints

### Teams

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/teams` | Create a new team |
| `GET` | `/api/teams` | List all teams |
| `PATCH` | `/api/teams/[id]` | Update a team |
| `DELETE` | `/api/teams/[id]` | Delete a team |

### Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/agents/register` | Register an agent to a team |
| `GET` | `/api/teams/[id]/agents` | List agents in a team |

### Base URL

```
$AIMAESTRO_API  (default: http://localhost:23000)
```

---

## API Usage Examples

### Create a Team

```bash
curl -X POST "$AIMAESTRO_API/api/teams" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "svgbbox-library-team",
    "repository": "https://github.com/Emasoft/svgbbox",
    "github_project": "https://github.com/orgs/Emasoft/projects/12",
    "created_by": "amcos-chief-of-staff"
  }'
```

### Register an Agent to a Team

```bash
curl -X POST "$AIMAESTRO_API/api/agents/register" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "svgbbox-library-team",
    "name": "svgbbox-orchestrator",
    "role": "manager",
    "plugin": "ai-maestro-orchestrator-agent",
    "host": "macbook-dev-01"
  }'
```

### List Team Agents

```bash
curl -s "$AIMAESTRO_API/api/teams/svgbbox-library-team/agents" | jq .
```

### Update a Team

```bash
curl -X PATCH "$AIMAESTRO_API/api/teams/svgbbox-library-team" \
  -H "Content-Type: application/json" \
  -d '{"github_project": "https://github.com/orgs/Emasoft/projects/15"}'
```

---

## Team Naming Convention

### Format

```
<repo-name>-<project-type>-team
```

### Components

| Component | Description | Examples |
|-----------|-------------|----------|
| `repo-name` | GitHub repository name (lowercase, hyphens) | `svgbbox`, `ai-maestro`, `myapp` |
| `project-type` | Descriptive keyword for the project type | `library`, `webapp`, `api`, `cli`, `mobile` |
| `team` | Literal suffix to identify as team name | `team` |

### Examples

| Repository | Project Type | Team Name |
|------------|--------------|-----------|
| `svgbbox` | Library | `svgbbox-library-team` |
| `ai-maestro` | Backend API | `ai-maestro-api-team` |
| `my-mobile-app` | Mobile App | `my-mobile-app-mobile-team` |
| `company-website` | Web App | `company-website-webapp-team` |

### Uniqueness Requirement

Team names must be **globally unique** across all projects managed by AMCOS. The API enforces uniqueness on creation.

---

## Agent Naming Convention

### Format

```
<team-prefix>-<role>[-<instance>]
```

### Components

| Component | Description | Examples |
|-----------|-------------|----------|
| `team-prefix` | Short form of repo name | `svgbbox`, `maestro`, `myapp` |
| `role` | Agent role identifier | `orchestrator`, `architect`, `impl`, `tester` |
| `instance` | Instance number (for multiple same-role agents) | `01`, `02`, `03` |

### Examples

| Team | Role | Instance | Agent Name |
|------|------|----------|------------|
| svgbbox-library-team | orchestrator | - | `svgbbox-orchestrator` |
| svgbbox-library-team | architect | - | `svgbbox-architect` |
| svgbbox-library-team | implementer | 1 | `svgbbox-impl-01` |
| svgbbox-library-team | implementer | 2 | `svgbbox-impl-02` |
| ai-maestro-api-team | tester | 1 | `maestro-tester-01` |

### Organization-Wide Agents (No Team Prefix)

| Agent | Name |
|-------|------|
| Manager | `eama-assistant-manager` |
| Chief of Staff | `amcos-chief-of-staff` |
| Shared Integrator | `ai-maestro-integrator` |

---

## Role Types

| Role | Plugin | Scope | Description |
|------|--------|-------|-------------|
| `manager` | ai-maestro-assistant-manager-agent | Organization-wide | User interface, approvals |
| `chief-of-staff` | ai-maestro-chief-of-staff | Organization-wide | Agent lifecycle, team management |
| `member` | ai-maestro-*-agent | Per-team | Any team member (orchestrator, architect, implementer, tester, devops, integrator) |

### Governance Roles

These are the AI Maestro governance roles used in the API:

| Governance Role | Description |
|-----------------|-------------|
| `manager` | Organization-level authority. Approvals, user interface. |
| `chief-of-staff` | Organization-level operations. Agent lifecycle, team registry management. |
| `member` | Team-level. All agents assigned to a team are members with a functional sub-role. |

### Functional Sub-Roles (for `member` agents)

| Sub-Role | Plugin | Count per Team | Description |
|----------|--------|----------------|-------------|
| `orchestrator` | ai-maestro-orchestrator-agent | **Exactly 1** | Task management, kanban, coordination |
| `architect` | ai-maestro-architect-agent | **Exactly 1** | Design documents |
| `integrator` | ai-maestro-integrator-agent | 1+ (can be shared) | PR review, merge, CI/CD, release |
| `implementer` | ai-maestro-implementer-agent | 1+ | Code implementation |
| `tester` | ai-maestro-tester-agent | 0+ | Testing, QA |
| `devops` | ai-maestro-devops-agent | 0+ | CI/CD, deployment |

---

## Messaging via AMP Protocol

All inter-agent messaging uses the **AMP protocol** via the official scripts in `~/.local/bin/`.

### Send a Message

```bash
amp-send.sh --to svgbbox-orchestrator \
  --subject "[PROGRESS] Task #42: Login fix 80% complete" \
  --priority normal \
  --type progress-report \
  --message "Login fix implementation 80% complete. Running tests now."
```

### Check Inbox

```bash
amp-inbox.sh
```

### Read a Message

```bash
amp-read.sh --id <message-id>
```

### Reply to a Message

```bash
amp-reply.sh --id <message-id> \
  --message "Acknowledged. Proceed with merge when tests pass."
```

---

## Git Commit Message Format

To track which agent made each commit:

```
Fix login validation bug

- Added email format validation
- Fixed password length check
- Added unit tests

Agent: svgbbox-impl-01
Role: member/implementer
Plugin: ai-maestro-implementer-agent
Host: macbook-dev-01
Team: svgbbox-library-team
GitHub-Bot: ai-maestro-bot
```

---

## PR Body Format

```markdown
## Summary
Fix login validation bug

## Changes
- Added email format validation
- Fixed password length check
- Added unit tests

## Testing
- [x] Unit tests pass
- [x] Integration tests pass

---
**Agent Identity**
| Field | Value |
|-------|-------|
| Agent | svgbbox-impl-01 |
| Role | member/implementer |
| Plugin | ai-maestro-implementer-agent |
| Host | macbook-dev-01 |
| Team | svgbbox-library-team |

*PR created via ai-maestro-bot (shared GitHub account)*
```

---

## AMCOS Responsibilities

1. **Create teams** via `POST /api/teams`
2. **Register agents** via `POST /api/agents/register`
3. **Update agent status** when agents hibernate/wake/terminate via `PATCH /api/teams/[id]`
4. **Notify all team agents** of registry changes via AMP:

```bash
amp-send.sh --to svgbbox-orchestrator \
  --subject "[REGISTRY UPDATE] Team contacts updated" \
  --priority normal \
  --type registry-update \
  --message "Agent svgbbox-impl-03 added to team. Query API for current roster."
```

---

## Validation Rules

1. **Team name must be unique** across all projects (enforced by API)
2. **Agent name must be unique** within the team (enforced by API)
3. **Exactly one orchestrator** per team
4. **Exactly one architect** per team
5. **At least one implementer** per team
6. **All agents must have valid AI Maestro addresses**
7. **Organization agents (manager, chief-of-staff) cannot be assigned to teams**

---

## Kanban System Reference

All projects use the canonical **8-column kanban system** on GitHub Projects:

| Column | Code | Label |
|--------|------|-------|
| Backlog | `backlog` | `status:backlog` |
| Todo | `todo` | `status:todo` |
| In Progress | `in-progress` | `status:in-progress` |
| AI Review | `ai-review` | `status:ai-review` |
| Human Review | `human-review` | `status:human-review` |
| Merge/Release | `merge-release` | `status:merge-release` |
| Done | `done` | `status:done` |
| Blocked | `blocked` | `status:blocked` |

For full kanban workflow details, see **FULL_PROJECT_WORKFLOW.md**.

---

## Quick Reference: Who to Message

| When I need to... | Message this agent | How to find address |
|-------------------|--------------------|---------------------|
| Report task progress | Orchestrator | `GET /api/teams/[id]/agents` filter by sub-role |
| Ask design questions | Architect | `GET /api/teams/[id]/agents` filter by sub-role |
| Submit PR for review | Integrator | `GET /api/teams/[id]/agents` filter by sub-role |
| Request approval | Manager | `amp-send.sh --to eama-assistant-manager` |
| Report agent issues | Chief of Staff | `amp-send.sh --to amcos-chief-of-staff` |
| Message teammate | By name | `amp-send.sh --to <agent-name>` |

---

**This specification must be followed by all agents. Deviations require Manager approval.**
