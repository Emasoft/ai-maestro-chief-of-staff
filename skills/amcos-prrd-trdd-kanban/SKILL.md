---
name: amcos-prrd-trdd-kanban
description: "CHIEF-OF-STAFF's role in the PRRD / TRDD / Kanban workflow. COS does NOT own kanban columns directly — it ROUTES messages and proposals between the team layer (ORCH/ARCH/INT/MEMBER) and the governance layer (MANAGER). Use when COS forwards a PRRD proposal, relays approval decisions, broadcasts TRDD status updates, or aggregates team status for AMAMA."
allowed-tools: "Bash(python3:*), Bash(get-prrd.py:*), Bash(findprrd.py:*), Bash(findtrdd.py:*), Bash(kanban.py:*), Bash(amp-send:*), Bash(amp-inbox:*), Read, Edit, Grep, Glob"
metadata:
  author: "Emasoft"
  version: "1.1.0"
---

## Overview

The CHIEF-OF-STAFF is the team GATEKEEPER — a two-tier filter, NOT an
unfiltered relay. Governance R6 forces every team-internal agent (ORCH,
ARCH, INT, MEMBER) to write ONLY to its COS; the COS then classifies each
request as COS-AUTONOMOUS (decide within the team, nothing upstream) or
COS-ESCALATE (forward ONE consolidated approval-request to MANAGER).
Forwarding everything would overload the MANAGER and nullify the COS.
COS owns NO kanban columns. For universal mechanics and the FULL tier
tables / unifying principle / consolidation rule / escalation format, see
the `prrd-trdd-kanban` skill in `ai-maestro-plugin` and its bundled
`cos-delegation-authority.md`.

## Prerequisites

- The universal `prrd-trdd-kanban` skill (ai-maestro-plugin) for the
  shared PRRD/TRDD/kanban mechanics and tier tables.
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
     already EXEMPT (`exempt-operations.md`), team health/lifecycle
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
flow). The MANAGER ratified that schema (Tier-2, COS#11): the **8-column
model**, a simplified projection of the TRDD v2 lifecycle.

**The 8 columns** — keep `ai-review` and `human-review` DISTINCT (the
R26–R40 dual-review / human-gate depends on it; collapsing them hides the
human gate), and keep `blocked` a first-class lane:

`backlog · todo · in-progress · ai-review · human-review · merge-release · done · blocked`

**TRDD `column:` → board lane** (a TRDD's frontmatter `column:` drives its lane):

| Board lane | TRDD v2 `column:` values |
|---|---|
| `backlog` | backburner, todo |
| `todo` | dispatch |
| `in-progress` | dev, testing |
| `ai-review` | ai_review |
| `human-review` | human_review |
| `merge-release` | complete, publish, deploy |
| `done` | published, live |
| `blocked` | blocked |

Keep ONE `merge-release` lane — the TRDD frontmatter (`release-via`,
publish-vs-deploy) carries that detail; the lane is not split.

**Status:** COS applies this schema via the `kanban-config` CLI verb at
team creation. That verb is not yet deployed (ai-maestro#36), so the
schema above is the design COS configures the moment the verb ships — the
model is locked in now. The velocity/distribution monitoring half of
COS#11 (parts 2-4) rides the deployed `amp-kanban-*` CLIs.

## Resources

For the full two-tier authority tables, the unifying principle, the
consolidation rule, and the escalation message format, read the universal
`prrd-trdd-kanban` skill in `ai-maestro-plugin` together with its bundled
`cos-delegation-authority.md` and `exempt-operations.md` references. The
universal skill is the single source of truth for the shared mechanics;
this skill only adds the COS gatekeeper role on top of it.
