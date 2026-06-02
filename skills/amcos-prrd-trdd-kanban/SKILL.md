---
name: amcos-prrd-trdd-kanban
description: "CHIEF-OF-STAFF's role in the PRRD / TRDD / Kanban workflow. COS does NOT own kanban columns directly — it ROUTES messages and proposals between the team layer (ORCH/ARCH/INT/MEMBER) and the governance layer (MANAGER). Use when COS forwards a PRRD proposal, relays approval decisions, broadcasts TRDD status updates, or aggregates team status for AMAMA."
allowed-tools: "Bash(python3:*), Bash(get-prrd.py:*), Bash(findprrd.py:*), Bash(findtrdd.py:*), Bash(kanban.py:*), Bash(amp-send:*), Bash(amp-inbox:*), Read, Edit, Grep, Glob"
metadata:
  author: "Emasoft"
  version: "1.0.0"
---

## Overview

This is the CHIEF-OF-STAFF's role-specific layer of the PRRD / TRDD /
Kanban model. For universal mechanics, see `prrd-trdd-kanban` in
`ai-maestro-plugin`.

## Approval discipline — COS is the routing pipe

Check
[references/exempt-operations.md](references/exempt-operations.md)
in the universal skill. COS's **exempt** operations (no MANAGER
approval): routing all approval-request AMP messages from
team-internal agents to MANAGER, relaying MANAGER's decisions back
to the requesting agent, forwarding PRRD proposals, aggregating
status reports. COS **does NOT itself trigger TRDD column
transitions** — it routes requests. COS's role in the approval
mechanism is to be the AMP pipe (per R6 v3) between team-internal
agents and MANAGER. COS may transcribe MANAGER's verbatim approval
into the TRDD's `## Approval log` section so the audit trail is
durable.

COS is the **routing hub** between team-internal agents (ORCH, ARCH,
INT, MEMBER) and the governance layer (MANAGER). Under R6 v3 (2026-05-05):

- MANAGER messages COS, not team-internal agents directly
- Team-internal agents message COS, not MANAGER directly
- COS is the SOLE entry/exit point of the team

COS itself owns NO kanban columns. Its role in the PRRD/TRDD/kanban
workflow is **message routing and aggregation**.

## What COS does NOT do

- COS does NOT mutate any TRDD's `column:`, `assignee:`, or body fields.
  All mutations are performed by the column owner.
- COS does NOT mutate the PRRD. (It does forward proposals.)
- COS does NOT decide PRRD proposal outcomes. (MANAGER decides.)
- COS does NOT delegate TRDDs to specific agents. (ORCHESTRATOR does.)

## What COS does in the workflow

### Routing PRRD proposals (team → MANAGER)

When a team-internal agent (ORCH/ARCH/INT/MEM) files a PRRD proposal:

- [ ] The proposing agent runs `prrd-edit.py propose ... --routed-via
      cos-<team>`. A proposal file appears in
      `design/requirements/proposals/`.
- [ ] COS watches `design/requirements/proposals/` for new files
      (or is notified via AMP).
- [ ] COS reads the proposal, sanity-checks (well-formed frontmatter,
      meaningful rationale).
- [ ] COS AMP-sends to AMAMA: "Proposal <pid> from
      <proposing-agent> — please decide".
- [ ] On AMAMA's reply, COS updates the proposal file's `status:` and
      AMP-replies to the proposing agent.

### Routing TRDD status (team → AMAMA)

When an ORCHESTRATOR-triggered column change needs to surface upward:

- [ ] ORCH AMP-sends to COS: "TRDD-<id> transitioned X → Y"
- [ ] COS aggregates status changes into a periodic batch (e.g. every
      hour, or on AMAMA query)
- [ ] COS AMP-sends batched status to AMAMA

### Routing MANAGER directives (AMAMA → team)

When AMAMA needs to send work / decisions into the team:

- [ ] AMAMA AMP-sends to COS (only legal target per R6 v3)
- [ ] COS reads the message, determines the right in-team recipient:
      ORCH for assignment, ARCH for design, INT for ship, MEM for work
- [ ] COS AMP-relays to the in-team recipient with appropriate framing
- [ ] On the recipient's reply, COS AMP-relays back to AMAMA

### Aggregating kanban for AMAMA

When AMAMA asks "what's the team's status?":

```bash
# COS runs in its own checkout (or the team's shared workspace)
kanban.py --json | jq '{
  by_column: (.columns | to_entries | map({key: .key, count: (.value | length)})),
  red_priority: .red_priority[:3],
  drift: .drift
}'
```

Then COS composes a status summary and AMP-sends to AMAMA.

## R6 v3 routing reminders for COS

| From | To | Allowed? | Notes |
|---|---|---|---|
| Team-internal | MANAGER | NO (via COS) | COS is the sole bridge |
| Team-internal | Team-internal | YES (same-team peer) | But still flow status through COS for visibility |
| Team-internal | AUTONOMOUS / MAINTAINER | NO | COS is also blocked; MANAGER is the only governance-layer bridge per R6.2 |
| Team-internal | HUMAN | reply-only (1 edge) | COS does NOT relay these — the agent replies directly within its 1-edge quota; if it needs to initiate to USER, AMAMA must relay on its behalf |
| COS | MANAGER | YES | Standard pipe |
| COS | MAINTAINER / AUTONOMOUS | NO | R6.2 narrowed v1 — COS is no longer a cross-layer bridge |
| COS | HUMAN | reply-only (1 edge) | COS, like team-internal, has a `1`-edge to HUMAN — single reply per inbound H→COS message |

## PRRD proposal-handling checklist

### When a proposal file appears in design/requirements/proposals/

- [ ] `findtrdd.py --grep PROPOSAL-` lists current proposals (it
      doesn't distinguish but the filename does)
- [ ] Read the proposal: frontmatter + body
- [ ] Check `proposes:` (add/revise/delete/promote/demote) and
      `target-kind:` (silver/golden)
- [ ] If golden: this is going to require USER decision. Mark in
      `## COS notes` section and AMP-send to AMAMA with a "golden,
      USER decision needed" tag
- [ ] If silver: AMP-send to AMAMA with the proposal contents
- [ ] On AMAMA's decision:
      - Accepted: edit proposal `status: accepted`, AMP-reply to
        proposing agent with the accepted text and confirmation that
        the PRRD has been updated
      - Rejected: edit proposal `status: rejected`, AMP-reply with the
        rationale

## Resources

- Universal skill: `prrd-trdd-kanban`
- Existing COS skills: `amcos-agent-coordination`,
  `amcos-acknowledgment-protocol`, `amcos-staff-planner`
- COS persona: `agents/ai-maestro-chief-of-staff-main-agent.md`
- R6 v3 communication-graph reference: `ai-maestro-plugin/skills/team-governance/references/GOVERNANCE-RULES.md` §R6
