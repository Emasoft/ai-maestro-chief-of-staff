# The Three In-Team Dialog Loops (ORCHESTRATOR-owned)

The corrected fleet workflow runs **three back-and-forth dialog loops** inside a
team. Their purpose is to prevent wasted tokens — a MEMBER must never start
coding against a half-understood task, never silently improvise around a design
flaw, and never burn an INTEGRATOR's context on a premature PR.

**All three loops are ORCHESTRATOR-owned.** They run on the team's **direct**
in-team edges (R6 v3: `ORCH ↔ ARCH`, `ORCH ↔ MEMBER`, `ORCH ↔ INT`). The
CHIEF-OF-STAFF guards the **team boundary** only and **never** relays, absorbs,
or escalates these exchanges. This document is the canonical reference for what
the loops are and for the bright line between "ORCH's job" and "COS's job".

## The loops

### Loop A — Task-comprehension handshake (before any code is written)

When a TRDD reaches `dev` and is assigned to a MEMBER, the ORCHESTRATOR opens a
handshake and the MEMBER must answer **all** of the question set before coding
starts:

- Restate the task in your own words (proves comprehension).
- Which files / domains will you touch? (surfaces single-writer collisions early.)
- What is ambiguous or under-specified?
- What risks / issues do you foresee?
- What NPT (necessary-prerequisite) or EHT (effects-handling) tasks do you anticipate?

Unresolved items go **back through the ORCHESTRATOR**. If the blocker is a
design flaw, ORCH pulls in the ARCHITECT, who revises the TRDD or authors new
TRDDs. Coding does not start until the handshake is clean.

### Loop B — In-dev issue dialog (continuously, during `dev`)

The moment a MEMBER hits any issue, ambiguity, or blocker mid-implementation,
they raise it to the ORCHESTRATOR **immediately** — they do not improvise around
it. ORCH triages and pulls in the right specialist on a direct edge:

- design flaw → ARCHITECT,
- CI / merge / release concern → INTEGRATOR.

Silently working around a design flaw is forbidden; that is exactly the failure
this loop exists to catch.

### Loop C — Pre-PR gate (before a PR is opened)

Before opening a PR or notifying the INTEGRATOR, the MEMBER must clear an
explicit "I believe it's done — PR now?" check **with the ORCHESTRATOR**. This
gate protects INTEGRATOR tokens from premature or incomplete PRs. Only after
ORCH agrees does the MEMBER open the PR / notify INT.

## Ownership matrix

| Loop | Driver | Edge (R6 v3) | COS involvement |
|---|---|---|---|
| A — task-comprehension handshake | ORCHESTRATOR ⇄ MEMBER | direct in-team | **none** — never relayed |
| B — in-dev issue dialog | MEMBER ⇄ ORCHESTRATOR (→ ARCH / INT) | direct in-team | **none** — never relayed |
| C — pre-PR gate | MEMBER ⇄ ORCHESTRATOR | direct in-team | **none** — never relayed |

## What the CHIEF-OF-STAFF does and does NOT do

**COS guards the team BOUNDARY** — it is the single entry/exit point between the
team and the outside (MANAGER, peer teams). COS routes proposals up to MANAGER,
relays MANAGER's decisions down, and enforces the approval tiers.

**COS does NOT touch the three loops.** A task-comprehension question, an in-dev
blocker, or a pre-PR readiness check belongs to the ORCHESTRATOR's domain. If a
team member sends COS one of these, the correct action is to **redirect it to the
ORCHESTRATOR**, not to answer it, relay it, or escalate it to MANAGER. COS
absorbing or escalating an in-team question is a boundary violation: it makes COS
a bottleneck and steals work from ORCH.

The bright line:

- **Crosses the team boundary** (proposal needing MANAGER/USER approval, a
  cross-team dependency, a release-pipeline decision) → **COS handles it.**
- **Stays inside the team** (the three dialog loops, day-to-day ORCH↔MEMBER
  coordination) → **ORCH handles it; COS stays out.**

## Why this exists

- Protects ORCH / ARCH / INT / MEMBER token budgets by catching
  misunderstandings before they become wasted implementation work.
- Keeps COS from becoming a relay bottleneck for high-frequency in-team chatter.
- Forces design flaws back to the ARCHITECT instead of being improvised around.

## Related rules

- **PRRD S7.1** — the three loops are ORCH-owned; COS guards the boundary only.
- **R6 v3** — COS is the sole team-boundary gateway; in-team edges are direct.
- **[ROLE_BOUNDARIES.md](ROLE_BOUNDARIES.md)** — full role boundary matrix.
- **[FULL_PROJECT_WORKFLOW.md](FULL_PROJECT_WORKFLOW.md)** — the end-to-end flow.
