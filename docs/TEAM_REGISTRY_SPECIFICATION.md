# Team Registry Specification

> **SUPERSEDED**: The file-based `.ai-maestro/team-registry.json` approach is superseded.
> Team registries are now managed exclusively via the **frozen `aimaestro-*.sh` CLIs**
> (`aimaestro-teams.sh` / `aimaestro-agent.sh`) — the immutable wrappers over the
> AI Maestro registry API. Plugins call these CLIs, never the HTTP API directly.

**Version**: 2.12.0
**Last Updated**: 2026-03-13

This document specifies the team registry CLI surface, agent registration, and naming conventions for the AMCOS plugin.

---

## Overview

Team registries are managed centrally through the frozen **`aimaestro-teams.sh`**
CLI (and the agent-side CLIs). There are no local JSON files to maintain. All
team and agent data is stored server-side; plugins reach it through the stable
CLI commands below, never by calling the HTTP API.

---

## CLI Surface

### Teams — `aimaestro-teams.sh`

| Command | Description |
|---------|-------------|
| `aimaestro-teams.sh create --name N [flags]` | Create a new team — **MANAGER-only** (R29.1); not a COS action |
| `aimaestro-teams.sh list` | List all teams |
| `aimaestro-teams.sh show <teamId>` | Show one team |
| `aimaestro-teams.sh update <teamId> [flags]` | Update a team |
| `aimaestro-teams.sh delete <teamId> [--delete-agents]` | Delete a team — **MANAGER-only** (R29.1); not a COS action |
| `aimaestro-teams.sh add-agent <teamId> <agentUUID>` | Add one member (COS, under a MANAGER mandate; auth via AID — R28, no password) |
| `aimaestro-teams.sh remove-agent <teamId> <agentUUID>` | Remove one member (COS, under a MANAGER mandate; auth via AID — R28, no password) |

### Agents

Team membership is changed via `aimaestro-teams.sh add-agent` / `remove-agent`
(above). Two registry operations have **no** frozen-CLI verb yet:

| Operation | Status |
|-----------|--------|
| Register a brand-new agent into a team (with role / sub_role / plugin / host metadata) | <!-- DECOUPLE-BLOCKED ai-maestro#76: agent register-into-team has no frozen-CLI verb (aimaestro-teams.sh add-agent attaches an existing agent UUID, it does not create+register a new agent with metadata). Pending a follow-up verb. --> |
| Set an agent's status (hibernate / wake / terminate) on the registry | <!-- DECOUPLE-BLOCKED ai-maestro#76: agent status-set has no frozen-CLI verb. Pending a follow-up verb. --> |

### Base host

The CLI talks to this host by default (override with `AIMAESTRO_API_BASE`):

```
default: http://localhost:23000
```

---

## CLI Usage Examples

### Create a Team (MANAGER-only — R29.1)

Team creation is a **MANAGER** action — the MANAGER creates the team and auto-spawns the COS + the 5 base members (R29.1). The COS does NOT run this; it is shown only to document the CLI surface. The COS completes & customizes the team it is created into, under the MANAGER's mandate (R30).

```bash
# Run by the MANAGER (not the COS); auth via AID — R28, no password
aimaestro-teams.sh create \
  --name "svgbbox-library-team" \
  --gh-owner "Emasoft" --gh-repo "svgbbox"
```

### Register an Agent to a Team

Registering a brand-new agent (with role / sub_role / plugin / host metadata)
has **no** frozen-CLI verb yet:

<!-- DECOUPLE-BLOCKED ai-maestro#76: agent register-into-team has no frozen-CLI verb (aimaestro-teams.sh add-agent attaches an existing agent UUID, it does not create+register a new agent with metadata). Pending a follow-up verb. -->

To attach an **already-registered** agent (by UUID) to a team:

```bash
aimaestro-teams.sh add-agent svgbbox-library-team <agent-uuid>   # COS, under a MANAGER mandate; auth via AID — R28, no password
```

### List Team Agents

```bash
aimaestro-teams.sh show svgbbox-library-team | jq '.agents'
```

### Update a Team

```bash
aimaestro-teams.sh update svgbbox-library-team --gh-owner "Emasoft" --gh-repo "svgbbox"
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
| svgbbox-library-team | programmer | 1 | `svgbbox-impl-01` |
| svgbbox-library-team | programmer | 2 | `svgbbox-impl-02` |
| ai-maestro-api-team | tester | 1 | `maestro-tester-01` |

### Organization-Wide Agents (No Team Prefix)

| Agent | Name |
|-------|------|
| Manager | `amama-assistant-manager` |
| Chief of Staff | `amcos-chief-of-staff` |
| Shared Integrator | `ai-maestro-integrator` |

---

## Role Types

> **Runtime governance**: These role definitions are a local reference. The authoritative source is the `team-governance` skill, consulted at runtime. Plugins MUST NOT hardcode governance rules, permission matrices, or role restrictions. For custom or specialized agent types, route to Haephestos v2 (the agent creation helper) instead of using predefined role mappings.

| Role | Plugin | Scope | Description |
|------|--------|-------|-------------|
| `manager` | ai-maestro-assistant-manager-agent | Organization-wide | User interface, approvals |
| `chief-of-staff` | ai-maestro-chief-of-staff | Per-team | Agent lifecycle, team management (one per team) |
| `member` | ai-maestro-*-agent | Per-team | Any team member (orchestrator, architect, programmer, tester, devops, integrator) |

### Governance Roles

> **Runtime governance**: These governance roles are a local reference. The authoritative source is the `team-governance` skill, consulted at runtime.

These are the AI Maestro governance roles used in the API:

| Governance Role | Description |
|-----------------|-------------|
| `manager` | Organization-level authority. Approvals, user interface. |
| `chief-of-staff` | Team-level operations. Agent lifecycle, team registry management. One COS per team. |
| `member` | Team-level. All agents assigned to a team are members with a functional sub-role. |

### Functional Sub-Roles (for `member` agents)

| Sub-Role | Plugin | Count per Team | Description |
|----------|--------|----------------|-------------|
| `orchestrator` | ai-maestro-orchestrator-agent | **Exactly 1** | Task management, kanban, coordination |
| `architect` | ai-maestro-architect-agent | **Exactly 1** | Design documents |
| `integrator` | ai-maestro-integrator-agent | 1+ (can be shared) | PR review, merge, CI/CD, release |
| `programmer` | ai-maestro-programmer-agent | 1+ | Code implementation |
| `tester` | ai-maestro-tester-agent | 0+ | Testing, QA |
| `devops` | ai-maestro-devops-agent | 0+ | CI/CD, deployment |

---

## Messaging via AMP Protocol

All inter-agent messaging uses the **AMP protocol** via the official scripts in `~/.local/bin/`.

### Send a Message

```bash
amp-send.sh "svgbbox-orchestrator" "[PROGRESS] Task #42: Login fix 80% complete" "Login fix implementation 80% complete. Running tests now." \
  --priority normal --type status
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

> **Note**: These examples use the frozen `amp-*` CLIs directly — this is the production mechanism (`amp-send`, `amp-inbox`, `amp-read`, `amp-reply`).

---

## Git Commit Message Format

To track which agent made each commit:

```
Fix login validation bug

- Added email format validation
- Fixed password length check
- Added unit tests

Agent: svgbbox-impl-01
Role: member/programmer
Plugin: ai-maestro-programmer-agent
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
| Role | member/programmer |
| Plugin | ai-maestro-programmer-agent |
| Host | macbook-dev-01 |
| Team | svgbbox-library-team |

*PR created via ai-maestro-bot (shared GitHub account)*
```

---

## AMCOS Responsibilities

1. **Complete & customize the team** the MANAGER created — under a MANAGER mandate (R30), add/configure the 5 base members + extra MEMBERs via `aimaestro-teams.sh add-agent`. Team `create`/`delete` is MANAGER-only (R29.1), not a COS responsibility.
2. **Register agents** — attach an existing agent UUID with `aimaestro-teams.sh add-agent <teamId> <agentUUID>`; registering a brand-new agent with metadata has no frozen-CLI verb yet (<!-- DECOUPLE-BLOCKED ai-maestro#76: agent register-into-team has no frozen-CLI verb. Pending a follow-up verb. -->)
3. **Update agent status** when agents hibernate/wake/terminate — no frozen-CLI verb yet (<!-- DECOUPLE-BLOCKED ai-maestro#76: agent status-set has no frozen-CLI verb. Pending a follow-up verb. -->)
4. **Notify all team agents** of registry changes via AMP:

```bash
amp-send.sh "svgbbox-orchestrator" "[REGISTRY UPDATE] Team contacts updated" "Agent svgbbox-impl-03 added to team. Query API for current roster." \
  --priority normal --type update
```

---

## Validation Rules

> **Runtime governance**: These validation rules are a local reference. The authoritative source is the `team-governance` skill, consulted at runtime. Plugins MUST NOT hardcode governance rules, permission matrices, or role restrictions.

1. **Team name must be unique** across all projects (enforced by API)
2. **Agent name must be unique** within the team (enforced by API)
3. **Exactly one orchestrator** per team
4. **Exactly one architect** per team
5. **At least one programmer** per team
6. **All agents must have valid AI Maestro addresses**
7. **Manager agent is organization-wide; chief-of-staff is assigned one per team**

---

## Kanban System Reference

> The team board **mirrors the 19-stage TRDD v3 `column:` pipeline 1:1** plus the
> `blocked`/`failed`/`superseded` exception lanes — NOT a projection. An earlier
> 8-column model (v2.20.0) was **superseded** by the MANAGER's ai-maestro#2
> decision (a) (COS#11). COS sets this column schema once at team creation (via
> the deployed `kanban-config` verb; the per-team column backend is gated on
> ai-maestro#2).

All projects use the canonical **22-column board** (19 lifecycle + 3 exception,
the TRDD `column:` values, in lifecycle order):

`backburner · approval · design · design_ai_review · design_human_review · todo · verify_assumptions · plan · dispatch · dev · testing · ai_review · human_review · complete · publish · published · deploy · live · live_auditing` + exceptions `blocked · failed · superseded`

The two governance review gates (`ai_review`, `human_review`) stay DISTINCT and
`blocked`/`failed`/`superseded` are first-class lanes. A TRDD's frontmatter
`column:` IS its board lane (no mapping table); the canonical column set lives in
the `amcos-prrd-trdd-kanban` skill (the single source of truth); the operational
`status:*` GitHub-issue labels are a separate, coarser layer (not 1:1 with these
lanes).

For full kanban workflow details, see **FULL_PROJECT_WORKFLOW.md**.

---

## Quick Reference: Who to Message

| When I need to... | Message this agent | How to find address |
|-------------------|--------------------|---------------------|
| Report task progress | Orchestrator | `aimaestro-teams.sh show <teamId>` filter by sub-role |
| Ask design questions | Architect | `aimaestro-teams.sh show <teamId>` filter by sub-role |
| Submit PR for review | Integrator | `aimaestro-teams.sh show <teamId>` filter by sub-role |
| Request approval | Manager | `amp-send.sh amama-assistant-manager` |
| Report agent issues | Chief of Staff | `amp-send.sh amcos-chief-of-staff` |
| Message teammate | By name | `amp-send.sh <agent-name>` |

---

**This specification must be followed by all agents. Deviations require Manager approval.**
