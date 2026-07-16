---
name: amcos-prrd-trdd-kanban
description: "CHIEF-OF-STAFF's role in the PRRD / TRDD / Kanban workflow. COS does NOT own kanban columns directly — it ROUTES messages and proposals between the team layer (ORCH/ARCH/INT/MEMBER) and the governance layer (MANAGER). Use when COS forwards a PRRD proposal, relays approval decisions, broadcasts TRDD status updates, or aggregates team status for AMAMA."
allowed-tools: "Bash(amp-send:*), Bash(amp-inbox:*), Read, Edit, Grep, Glob"
metadata:
  author: "Emasoft"
  version: "1.2.0"
---

## Overview

The CHIEF-OF-STAFF is the team GATEKEEPER — a two-tier filter, NOT an
unfiltered relay. Governance R6 forces every team-internal agent (ORCH,
ARCH, INT, MEMBER) to write ONLY to its COS; the COS then classifies each
request as COS-AUTONOMOUS (decide within the team, nothing upstream) or
COS-ESCALATE (forward ONE consolidated approval-request to MANAGER).
Forwarding everything would overload the MANAGER and nullify the COS.
COS owns NO kanban columns. For the universal mechanics and the FULL tier
tables / unifying principle / consolidation rule / escalation format, see the
granular `ama-*` skills in `ai-maestro-plugin` (the monolithic
`prrd-trdd-kanban` skill was split into them and no longer exists). The
references hub is `ama-trdd-transition` — its
`cos-delegation-authority.md`, `exempt-operations.md`,
and `approval-tiers-and-zones.md` are the shared source of truth.

## Prerequisites

- The granular `ama-*` skills (ai-maestro-plugin >= 2.7.9) for the shared
  PRRD/TRDD/kanban mechanics: `ama-prrd-get` / `ama-prrd-find` (read rules),
  `ama-prrd-propose` (relay a SILVER-PRRD change on a team agent's behalf,
  `--routed-via <cos-session>`), `ama-proposal-approvals` (relay a proposal's
  approve/refuse/archive — COS is **relay-only**, the MANAGER decides),
  `ama-trdd-transition` (the tier-table + delegation references hub),
  `ama-trdd-write` / `-find` / `-update`, and `ama-kanban-render`.
- A PRRD and per-task TRDDs under `design/tasks/` (and proposals under
  `design/requirements/proposals/`).
- AMP (`amp-send`, `amp-inbox`) for inter-agent messaging.
- A closed team per R6 v3: MANAGER ↔ COS ↔ members is the only path; the
  COS is the sole entry/exit point.

## Instructions

1. Receive a team-agent request via AMP (`amp-inbox`). A member, ORCH,
   ARCH, or INT writes ONLY to you.
2. Classify it into one tier:
   - **COS-AUTONOMOUS** — decide within the team, nothing goes upstream.
     Covers intra-team assignment/sequencing/relay, answering scope
     questions already settled by the TRDD/PRRD, approving anything
     already EXEMPT (`ama-trdd-transition`'s `exempt-operations.md`), team health/lifecycle
     within the approved R12 composition, in-team triage.
   - **COS-ESCALATE** — anything hard-floor, NON-EXEMPT, resource or
     composition change (new member, budget, tool, credential),
     PRRD/governance/baseline change, cross-team, an unresolvable in-team
     dispute, OR anything you are unsure about (conservative default).
3. If COS-AUTONOMOUS: make the decision in-team, AMP-reply to the
   requester, and optionally log it. Do NOT escalate.
4. If COS-ESCALATE: CONSOLIDATE related items into ONE MANAGER
   approval-request and AMP-send it — never N separate pings. Batching
   IS the load-absorption the COS exists for.
5. Relay the MANAGER's verdict back to the requester via AMP and record
   it in the relevant TRDD's `## Approval log`.
6. Stay presence-independent: classify the same way whether or not the
   user is present. Presence is a MANAGER-tier concern applied AFTER you
   escalate; the COS never reads presence itself.

## Output

- In-team decisions communicated to the requester (COS-AUTONOMOUS).
- ONE consolidated MANAGER approval-request per related batch
  (COS-ESCALATE).
- MANAGER verdicts relayed back to the originating team agent.
- `## Approval log` entries appended to the affected TRDD recording each
  escalation and its verdict.

## Error Handling

- Unsure which tier a request belongs to → escalate (conservative
  default; never silently decide a borderline case in-team).
- Can't resolve a dispute or question inside the team → escalate it as a
  consolidated MANAGER approval-request.
- Never mutate a TRDD `column:`, `assignee:`, or body yourself — route
  the change to the column owner (ORCHESTRATOR delegates; the owner
  mutates). The COS only writes the `## Approval log`.

## Examples

**COS-AUTONOMOUS** — A MEMBER asks "which sub-task do I pick up next?"
The answer is fully determined by the in-flight TRDD sequencing within
the approved R12 composition. The COS replies with the assignment via
AMP and logs nothing upstream.

**COS-ESCALATE (consolidated)** — Within one window, ARCH requests a new
build tool, INT requests a credential, and a MEMBER requests a budget
bump. All three are NON-EXEMPT resource changes. The COS batches them
into ONE MANAGER approval-request, awaits the verdict, relays each
decision back, and records them in the relevant TRDDs' `## Approval log`.

## Team-board column schema (COS sets it once, at team creation)

"COS owns NO kanban columns" means COS does not MOVE cards through the
workflow — the column owners / ORCH do that. It does NOT mean COS is
absent from the board: per COS#11, **COS sets the team board's column
SCHEMA once, at team creation** (the canonical column SET, not the card
flow).

**The ratified schema is the full 14-stage TRDD v2 pipeline plus the
three exception lanes — 17 columns total, a 1:1 mirror of the TRDD
`column:` enum, NOT a projection.** An earlier **8-column** model (v2.20.0) was **superseded**
by the MANAGER's ai-maestro#2 decision (a) (COS#11): there is **NO 14→8
collapse** — a projection hid the human gate and the publish/deploy tails.
A TRDD's frontmatter `column:` IS its board lane directly, so there is no
mapping table to maintain.

**The lanes** (the TRDD v2 `column:` values, in lifecycle order) —
`ai_review` and `human_review` stay DISTINCT (the R26–R40 dual-review /
human gate depends on it; collapsing them hides the human gate), and
`blocked`/`failed`/`superseded` are first-class:

`backburner · todo · design · dispatch · dev · testing · ai_review · human_review · complete · publish · published · deploy · live · live_auditing` + exceptions `blocked · failed · superseded`

The publish/deploy tails follow each TRDD's `release-via:` (`publish` →
`published`; `deploy` → `live` → `live_auditing` soak); `release-via: none`
ends at `complete`.

**Status:** the file-based half is **live today** — the 14-stage `column:`
pipeline + the `ama-kanban-render` skill. COS applies the schema to the team SERVER
board via the deployed `kanban-config` CLI verb (`aimaestro-teams.sh
kanban-config <teamId> --set-file <schema.json>`); the remaining gate is
the **backend — ai-maestro#2** (per-team column storage, still OPEN — the
server holds only 5 hardcoded statuses, ai-maestro#40). So COS configures
the 14-stage board at team creation the moment #2 is live; the
velocity/distribution monitoring half of COS#11 (parts 2-4) rides the
deployed `amp-kanban-*` CLIs.

## Resources

For the full two-tier authority tables, the unifying principle, the
consolidation rule, and the escalation message format, read the granular
`ama-*` skills in `ai-maestro-plugin` — the references hub is
`ama-trdd-transition`, whose `cos-delegation-authority.md`,
`exempt-operations.md`, and `approval-tiers-and-zones.md`
are the single source of truth for the shared mechanics. This skill only adds
the COS gatekeeper role on top of them.
