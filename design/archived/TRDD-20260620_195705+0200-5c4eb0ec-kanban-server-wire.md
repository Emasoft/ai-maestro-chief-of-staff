---
trdd-id: 5c4eb0ec-7ded-4492-954f-efd586e0dca5
title: Ensure the 14-stage kanban columns at COS team creation + amp-kanban-list velocity (COS#11 #26 server-half)
column: published
created: 2026-06-20T19:57:05+0200
updated: 2026-06-22T10:20:29+0200
current-owner: cos
assignee: cos
priority: 3
severity: LOW
effort: M
labels: [kanban, governance, cli-integration]
task-type: feature
parent-trdd: null
npt: []
eht: []
blocked-by: []
supersedes: []
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [unit, lint]
audit-requirements: []
review-requirements: [code-review]
impacts: []
attempts: 1
last-test-result: partial
implementation-commits: [bac7802]
published-version: 2.20.6
published-at: 2026-06-22T10:20:29+0200
external-refs: ["github.com/Emasoft/ai-maestro-chief-of-staff/issues/11", "github.com/Emasoft/ai-maestro-chief-of-staff/issues/22", "github.com/Emasoft/ai-maestro/issues/2", "github.com/Emasoft/ai-maestro/issues/40", "github.com/Emasoft/ai-maestro/issues/43"]
---

# Ensure the 14-stage kanban columns at COS team creation + amp-kanban-list velocity (COS#11 #26 server-half)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body)

**UPDATE 2026-06-22T10:20 — PUBLISHED DORMANT v2.20.6 (per USER decision):** the code shipped in
**v2.20.6** (commits bac7802 + c291341 + release 2886d30; CI 4/4 green). The USER chose "publish
now (dormant)" — the live integration round-trip is DEFERRED to first live use. ⚠ SUPERSEDES the
"held local until round-trip" line below. **The live round-trip is still BLOCKED upstream by BOTH:
(1) the AI Maestro server (being brought up by the server-layer Claude — issues being fixed), and
(2) ai-maestro#46 — AMP sessions can't self-resolve identity, so `amp-kanban-list` (COS velocity)
+ the `amp-*` CLIs refuse with "Multiple AMP agents found. Use --id <uuid>"; COS must NOT guess a
uuid (state-corrupting). Same blocker as the fleet #40 round-trip.** When the server is up AND
amp-* self-identifies, run step 5 (create team → assert columns → velocity → move a task
dev→ai_review→human_review→complete) then reply/close COS#11.

**UPDATE 2026-06-20T21:35 — CODE DONE + COMMITTED (held local, unpublished):**
design (c) implemented in commit `bac7802` (NOT pushed). New `scripts/amcos_kanban.py`
(`KANBAN_14STAGE_COLUMN_IDS`, `DEFAULT_14STAGE_COLUMNS`, `ensure_kanban_columns`
verify-and-correct, `summarize_velocity`/`kanban_velocity`); `create_team` wired to
ensure columns after a successful create (fail-fast on CLI error / unresolvable team
id); `kanban-velocity` CLI subcommand added. Tests: 153 pass (22 new — real pure-logic
exercised via the module's injected `run_cli` DI seam, which exists for circular-import
reasons; this is NOT a CLI/server mock), ruff clean, CPV strict 0/0/0/0. **REMAINING —
gated on a LIVE AI Maestro server (no-mocks rule): step 5 integration round-trip**
(create team → assert the 14-stage columns → move a task
dev→ai_review→human_review→complete for COS#11) **then `publish.py` + reply/close
COS#11.** `bac7802` is HELD local until that round-trip validates the real CLI/server
path — the unit tests cover the decision logic only; the wire shapes are source-verified
(read ai-maestro teams-service.ts / kanban-config route.ts / task.ts) but NOT yet
round-tripped against a running server.

**What this is:** the SERVER-HALF of COS#11 (#26), unblocked 2026-06-20 when the
ai-maestro server-layer Claude shipped the #2 backend (AM#43) + signalled COS
(COS#22). The DOC-half already shipped (v2.20.4, TRDD-b0048a21). This TRDD wires
COS to actually ensure each team's board carries the 14-stage column set + adds the
velocity/distribution monitoring half.

**VERIFIED FACTS (read the source, do not re-derive):**
- CLI contract: `aimaestro-teams.sh kanban-config <teamId> --get | --set <columns-json> | --set-file <path>`. PUT body `{columns:[{id,label,color,icon?,roles?}]}`.
- PUT Zod schema (`ai-maestro/app/api/teams/[id]/kanban-config/route.ts`): `id` (1-64) **required**, `label` (1-128) **required**, `color` (1-64) **REQUIRED**, `icon` optional, `roles` optional; `columns` array **min 1 max 20**.
- Server `DEFAULT_KANBAN_COLUMNS` (`ai-maestro/types/team.ts:37`) is ALREADY the ratified 17-col set (14 lifecycle + blocked/failed/superseded), ids 1:1 with `DEFAULT_STATUSES`. `Team.kanbanConfig?` is OPTIONAL → a team with NO custom config already renders the 14-stage board.
- Canonical 17 ids (COS owns this SET — it is the TRDD `column:` enum): `backburner, todo, design, dispatch, dev, testing, ai_review, human_review, complete, publish, published, deploy, live, live_auditing, blocked, failed, superseded`.

**DESIGN DECISION (the crux — `color` being required forces a duplication choice):**
- (a) **explicit-set**: hardcode a 17-col columns-json (id+label+color mirrored from DEFAULT_KANBAN_COLUMNS) and `--set` at every team creation. Authoritative, but DUPLICATES the server's color/label → sync burden if the server changes a column (violates one-source-of-truth).
- (b) **rely-on-default**: never `--set`; trust the server default. Zero duplication, but COS isn't "configuring" (COS#11 says "CoS MUST configure team kanban columns").
- (c) **verify-and-correct (RECOMMENDED)**: at team creation, `kanban-config --get`, assert the returned column-ID set == the canonical 17 ids (the thing COS actually owns — the TRDD enum). If they match (the common case, since the server default already matches) → no-op, log "columns OK". If they MISMATCH/empty → `--set` a fallback 17-col columns-json (id+label+color mirrored from DEFAULT_KANBAN_COLUMNS, with a `# sync-with-server` guard comment) to drift-correct. This exercises the duplicated color values ONLY on the rare drift path, keeps the common case duplication-free, treats column-IDs (TRDD enum) as COS's SoT and color/icon as the server's.

**Recommendation:** proceed with **(c)**. It satisfies "COS ensures the columns" without routine duplication, is fail-fast on drift, and respects the layer boundary (COS owns the column-ID set = TRDD enum; server owns presentation). Flag to COS#11 only if the MANAGER reads "must configure" as mandating unconditional (a).

**NEXT ACTION (phased — execute with FRESH context, re-read each file first per context-decay):**
1. Add a COS constant `KANBAN_14STAGE_COLUMN_IDS` (the 17 ids above) — single source for the assertion; plus a minimal fallback columns-json (id+label+color from DEFAULT_KANBAN_COLUMNS) for the drift-correct path, with a sync-guard comment.
2. In `amcos_team_registry.create_team` (after the `aimaestro-teams.sh create` succeeds): call `kanban-config <teamId> --get`, parse ids, assert == canonical set; on mismatch `--set` the fallback. Fail-fast on CLI error (no silent swallow). Keep it idempotent.
3. Velocity/distribution half of COS#11 (parts 2-4): a thin read path over `amp-kanban-list` (extended task model) — counts per column / per assignee. Likely a small helper + a skill doc note; do NOT duplicate the board.
4. Tests (real, no mocks of the CLI — use a throwaway team or the documented fixture; ask the user to provide a live server if the test needs one). CPV `--strict`. `publish.py --patch`.
5. Run the COS#11 round-trip (move a task dev→ai_review→human_review→complete on a 14-stage team) — coordinate with the MANAGER's #40 close protocol; reply on COS#11 + COS#22.

**OPEN ITEMS / gotchas:**
- Verify `--set` accepts the columns-json COS builds (color required — the fallback MUST include color).
- Confirm `kanban-config --get` output format (JSON?) to parse ids reliably.
- `--gh-project` (team_registry `github_project` marker) is a #25 concern, NOT this TRDD — stays blocked (verb absent).
- Don't rely on the heartbeat/session to hold a live team; the round-trip (step 5) may need the user to confirm a test team + a running server.

## Background

COS#11 part-1 = "configure team kanban columns"; the #2 backend that makes
`kanban-config --set` persist landed 2026-06-20 (AM#43). The doc-model half
(8→14 supersession) shipped v2.20.4 (TRDD-b0048a21). This TRDD is the runtime
wire-up: ensure the 14-stage columns at team creation + the velocity half. The
column-ID set is the TRDD `column:` enum (COS's SoT); the server owns the
presentation defaults.
