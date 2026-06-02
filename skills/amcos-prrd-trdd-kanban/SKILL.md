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

## COS is a GATEKEEPER, not an unfiltered relay (two-tier filter)

**This is the COS's reason to exist.** Governance R6 forces every
team-internal agent (ORCH, ARCH, INT, MEMBER) to write ONLY to its
COS. The COS then FILTERS each inbound request into one of two tiers —
it does NOT forward everything upstream. Forwarding everything would
overload the MANAGER and nullify the COS's purpose.

Full tier tables, the unifying principle, the consolidation rule, and
the escalation message format are in the **prrd-trdd-kanban** universal
skill's `cos-delegation-authority.md` reference (bundled in
ai-maestro-plugin). Summary:

| Tier | COS action |
|------|-----------|
| **COS-AUTONOMOUS** | COS decides/acts **within the team**, nothing goes upstream. Covers: intra-team task assignment/sequencing/relay, answering scope questions already determined by the TRDD/PRRD, approving anything already EXEMPT (`exempt-operations.md`), team health/lifecycle within the approved R12 composition, in-team problem triage. |
| **COS-ESCALATE** | COS forwards a **single consolidated** approval-request to MANAGER. Covers: hard-floor ops, NON-EXEMPT ops, resource/composition changes (new member, budget, tool, credential), PRRD/governance/baseline changes, cross-team anything, unresolvable in-team disputes, and **anything the COS is unsure about** (conservative default). |

**Presence-independent.** The COS classifies the same way whether or
not the user is present. User presence is a MANAGER-tier concern,
applied AFTER the COS escalates (the MANAGER's `amama-presence-tracker`
+ `amama-autonomous-fallback` decide escalate-to-USER vs
decide-autonomously). The COS never reads presence itself.

**Consolidate, don't flood.** When several members raise related
COS-ESCALATE requests, batch them into ONE MANAGER approval-request,
not N pings. That batching IS the load-absorption the COS exists for.

COS is the SOLE entry/exit point of the team (R6 v3): MANAGER ↔ COS ↔
members. COS owns NO kanban columns; it filters, routes, consolidates,
and transcribes MANAGER verdicts into the TRDD `## Approval log`.

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
