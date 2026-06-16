---
trdd-id: 8e8d6618-ecd0-4b53-a733-829c4c7dfe20
title: Remove all direct /api/* calls from COS scripts — repoint to the immutable CLI layer (#20)
column: dev
created: 2026-06-15T22:18:37+0200
updated: 2026-06-16T21:32:00+0200
current-owner: cos-ai-maestro-chief-of-staff
assignee: cos-ai-maestro-chief-of-staff
priority: 1
severity: HIGH
effort: L
labels: [decoupling, frozen-interface, no-direct-api, fleet-audit]
task-type: refactor
relevant-rules: [1]
release-via: publish
delivery: direct-push
target-branch: main
publish-target: ai-maestro-plugins
test-requirements: [unit, lint]
impacts: [public-api]
external-refs: ["github.com/Emasoft/ai-maestro-chief-of-staff/issues/20", "github.com/Emasoft/ai-maestro-assistant-manager-agent/issues/16"]
---

# TRDD-8e8d6618 — Remove direct /api/* calls from COS scripts (#20)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-06-15

**Source:** MANAGER work order #20. **USER hardened the no-direct-API rule to
ABSOLUTE (2026-06-15) + gave STANDING PRE-AUTHORIZATION: execute, do NOT stop for
approval, do NOT idle.** Rule (exception-free): no plugin calls the server API
directly; every API-touching call repoints to the immutable CLI layer. End state:
`grep -rn '/api/'` in the COS tree returns nothing. MANAGER verify-acks on publish.
Acked on #20 (issuecomment-4712078942).

**VERIFIED INVENTORY (grep + read, 2026-06-15) — a MULTI-PASS task:**

| Call class | Site(s) | Repoint target | Status |
|---|---|---|---|
| list-active | `amcos_heartbeat_check.py:272` (`/api/agents?status=active`) | `aimaestro-agent.sh list --status online --json` (verified interface) | **DOABLE NOW** |
| name-resolve | `amcos_notify_agent.py:36` (`/api/agents?name=`) | `aimaestro-agent.sh resolve` | BLOCKED ON DEPLOY — `resolve)` now in source (L90) but `~/.local/bin` copy is Apr-14 (no resolve) |
| governance-request | `amcos_approval_manager.py:48` (`/api/v1/governance/requests`) | `aimaestro-governance.sh` | BLOCKED ON DEPLOY — script landed in `~/ai-maestro/scripts/` but NOT in `~/.local/bin` |
| teams-CRUD | `amcos_team_registry.py` ×6 + `amcos_generate_team_report.py:72` (`/api/teams*`) | `aimaestro-teams.sh` | BLOCKED ON DEPLOY — script in `~/ai-maestro/scripts/` (Jun 15 21:54) but NOT in `~/.local/bin` |
| **prompt/doc API (NEW — script-only audit missed)** | `agents/amcos-approval-coordinator.md` ×7 (`/api/v1/governance/requests`); `agents/ai-maestro-chief-of-staff-main-agent.md` + `agents/amcos-team-coordinator.md` (`/api/teams*`); `commands/amcos-transfer-agent.md:28` (`/api/governance/transfers/` — distinct transfer path, in NO script audit); `docs/TEAM_REGISTRY_SPECIFICATION.md` (descriptive table) | same CLIs (governance/teams/transfer verb) | BLOCKED ON DEPLOY + final interface — repoint prompts to "invoke the CLI" once subcommands/args are stable |
| (not calls) | `amcos_spawn/hibernate/terminate/wake_agent.py:2` | — | ✅ done in v2.18.0 — stale `# TODO: Migrate to AI Maestro REST API` rewritten to CLI |

**✅ PASS 1 SHIPPED — v2.18.0 (2026-06-15).** list-active repointed to the CLI +
4 lifecycle TODOs fixed; those 5 files are grep-clean of the server-API path.
121 tests; CPV strict + lint 0/0/0/0 (publish.py local gates). Reported on #20
(issuecomment-4712252444). NB: the post-push Plugin Validation CI hung 15m
(cold-CI `uvx` build-from-source, the known CPV #114; orphan uv+python) and was
cancelled — NOT a plugin regression (local CPV strict passed; CPV validate is
static). Added a data point to cpv#114. Commits 9b4de5f (pass 1), release bump.
**REMAINING (3 pending classes, blocked on CLIs landing on ai-maestro#16):**
name-resolve (`amcos_notify_agent.py:36`, needs `resolve`), governance-request
(`amcos_approval_manager.py:48`, needs governance CLI), teams-CRUD
(`amcos_team_registry.py` ×6 + `amcos_generate_team_report.py`, needs
`aimaestro-teams.sh` ON PATH — it exists but isn't symlinked). Repoint + publish
each as its CLI lands; this TRDD stays in `dev` until `grep -rn '/api/'` is empty.

**UPDATE 2026-06-15T22:56 — deploy-gated, scope corrected (verified full-tree grep):**
The 3 script classes are now blocked on ONE thing: the CLI **deploy**. The MANAGER
confirmed (assistant-manager#16, 20:29Z) the CLIs are in **source** but NOT on PATH —
`~/.local/bin/aimaestro-agent.sh` is the Apr-14 copy (no `resolve`); `aimaestro-governance.sh`
+ `aimaestro-teams.sh` aren't in `~/.local/bin` at all; `install-agent-cli.sh` hasn't run
since April. The ai-maestro owner must deploy; the MANAGER then drives every plugin's
pass-2 repoint. Repointing now would hit the stale/missing CLI → I HOLD (not idling for
approval; a real deploy + interface dependency). **Two corrections posted on #16
(issuecomment-4712359916):** (1) **no `governance-whoami` in COS** — the complete `/api/`
set has no whoami path (that's core `prrd_lib.py` #7, mis-attributed to the COS line); COS
is 4 classes total (list-active ✅ + 3 pending), not 5. (2) **The script-only audit
undercounted** — the agent/command PROMPTS also instruct direct `/api/`
(`amcos-approval-coordinator.md` ×7 governance, `main-agent.md` + `amcos-team-coordinator.md`
teams, `amcos-transfer-agent.md:28` a distinct `/api/governance/transfers/` path in NO script
audit, + `TEAM_REGISTRY_SPECIFICATION.md`). Under the literal "`grep -rn '/api/'` returns
nothing" criterion these are in scope → pass-2 repoints scripts AND prompts/docs in one shot
on the deploy signal. Full-tree `/api/` count now: 14 in scripts (4 files) + the .md prompt/doc
references above.

**UPDATE 2026-06-16T00:51 — read the CLI source; target interfaces captured + transfer gap
VERIFIED.** Answered the MANAGER's open transfer-verb question from `~/ai-maestro/scripts/`
source (read-only) on #16 (issuecomment-4713106202). **Pass-2 repoint targets (the interfaces I'll
point COS at — modulo final pre-deploy edits):**
- governance-request → **`aimaestro-governance.sh`**: `requests` · `request` (flags `--type
  --agent --role --target-host --requested-by --payload-json --password`) · `approve`
  (`--approver --password`) · `reject` (`--rejector --reason --password`).
- teams-CRUD → **`aimaestro-teams.sh`**: `list · show · create · update · delete · add-agent ·
  remove-agent`.
- name-resolve → **`aimaestro-agent.sh resolve`** (+ `session`/`activity-update`/`user-input`
  live in `agent-session.sh`, per the MANAGER's source trace).
**Transfer verb VERIFIED ABSENT:** `grep -rniE 'transfer'` across ALL ai-maestro scripts = ZERO;
no `/api/governance/transfers` path. So `commands/amcos-transfer-agent.md`'s transfer call has NO
CLI equivalent yet — a real deploy-surface gap (candidate home: a governance `request --type
transfer` + approve, since that machinery already carries agent/role/target-host/payload). COS
can't reach grep-clean on the transfer-agent until this verb ships.

**UPDATE 2026-06-16T02:21 — scope extended to HOOKS (USER governance rule, via MANAGER #16);
COS hooks ALREADY COMPLIANT.** New fleet rule: split every script AND hook — api-part → installed
CLI, plugin carries only the non-api part; a hook needing the server calls the CLI, never `/api/`.
Audited all 5 COS hook scripts (hooks/hooks.json): `amcos_session_start` / `amcos_session_end` /
`amcos_stop_check` = purely local; `amcos_resource_check` = `subprocess` to LOCAL system cmds only
(`top`/`vm_stat`/`sysctl`/`df`, no API); `amcos_heartbeat_check` = the one server-touching hook,
**already split in pass-1 v2.18.0** (calls `aimaestro-agent.sh ... --json`, state-file fallback).
**Zero hooks call `/api/` direct or transitive; zero have an api-part lacking a CLI** → the hook-split
adds NO new work to COS pass-2 (only the same deploy dependency: the heartbeat CLI needs to be on
PATH at runtime; today it falls back gracefully). Reported on #16 (issuecomment-4713653714) — COS is
the green hook-split exemplar.

**UPDATE 2026-06-16T02:31 — transfer verb BUILT (gap closed); decoupling principle generalized.**
The ai-maestro owner built the transfer verb after my gap-find: `aimaestro-governance.sh transfer
list/create/resolve` → `/api/governance/transfers[/{id}/resolve]` (commit `d946e0dc`), verified in
source. So `amcos-transfer-agent` is **no longer a gap** — it repoints to `aimaestro-governance.sh
transfer …` once deployed. **Remaining COS pass-2 repoint targets, all now have CLIs in source**:
name-resolve→`aimaestro-agent.sh resolve`; governance-request→`aimaestro-governance.sh
request/approve/reject`; teams-CRUD→`aimaestro-teams.sh`; transfer→`aimaestro-governance.sh transfer`.
**Only `kanban-config` (COS #11, NOT #20) remains unbuilt** — still absent from `aimaestro-teams.sh`
(ai-maestro#2/#36); it's a #11 feature need, not a #20 decoupling gap. The owner also generalized
the decoupling invariant to ALL executable elements (hooks/MCP/scripts, no core exception) in
ai-maestro CLAUDE.md + PLUGIN-ABSTRACTION-PRINCIPLE.md — COS already conforms (no new work). **Net:
every CLI COS's existing /api/ elements need now EXISTS in source; the ONLY blocker is the deploy
(ai-maestro#36).** Confirmed on #16 (issuecomment-4713719202).

**UPDATE 2026-06-16T20:30 — PIVOT: do pass-2 NOW, commit-not-publish (per MANAGER's AMAMA recipe,
#16 issuecomment-4713653714). Branch `decouple/api-to-frozen-cli` created.** The repoint does NOT
need the CLIs on PATH at AUTHORING time — only the frozen SYNTAX (verified). AMAMA did its full
slice commit-not-publish on a branch; the MANAGER named COS to "do your slice now." So COS's pass-2
is doable now; publish only after #36 deploys (so COS never ships calls to an absent CLI).

**UPDATE 2026-06-16T21:13 — PASS-2 MECHANICAL WORK COMPLETE on the branch (commit-not-publish).**
All non-design-blocked repoints are done + verified on `decouple/api-to-frozen-cli` (25 components, 5 commits):
- **b1fed84** — 4 agent/command PROMPTS: `amcos-transfer-agent.md` (→ `aimaestro-governance.sh transfer create`),
  `main-agent.md` ×2 + `amcos-team-coordinator.md` (→ `aimaestro-teams.sh list/show`), `amcos-approval-coordinator.md`
  ×7 (→ `aimaestro-governance.sh request/requests/approve/reject`).
- **a19d3cf** — 5 top-level SKILL.md (pre-op-notification, agent-spawning, agent-coordination, permission-management,
  transfer-management) → teams/governance verbs.
- **90d8d67** — `amcos_notify_agent.py` `resolve_agent()` → `aimaestro-agent.sh resolve --json` (subprocess; graceful fallback kept).
- **4bc648d** — `amcos_generate_team_report.py` `fetch_teams_via_cli()` → `aimaestro-teams.sh list` (urllib + `--api` flag removed, no-legacy).
- **ad58ce1** — 14 teams-only skill REFERENCE DOCS (op-hibernate/op-spawn/op-update-team-registry ×4 skills + workflow-checklists
  + record-keeping) → `aimaestro-teams.sh list` (jq suffixes preserved; health-check → CLI reachability; "REST API"→"CLI"). Verified zero `/api/`.

**REMAINING — DESIGN-BLOCKED, held for AMAMA's `design/handoffs/api-to-cli-mapping.md` (NOT mechanical):**
- **2 big REST-client scripts** — `amcos_team_registry.py` (create/add_agent IMPEDANCE: rich registration
  `{name,role,governance_role,plugin,host,...}` vs CLI `add-agent <team> <agentUUID>`; create URL-repo vs `--gh-owner/--gh-repo`)
  and `amcos_approval_manager.py` (`respond_to_request` is password-LESS but CLI `approve`/`reject` REQUIRE `--password`;
  PATCH carries richer decision metadata than CLI flags). Both flagged on #16.
- **residual reference docs (14)** — governance ×8 (permission-management + transfer-management refs), label/agents ×3
  (label-taxonomy PATCH — verb not deployed), sessions ×1 (`coordination-overview` `/api/sessions`), 2 mixed
  (success-criteria, op-sync-registry-with-labels). All await the verb-mapping spec / residual-markers.

**main UNCHANGED (publishable, original /api/ intact) — commit-not-publish isolation verified by branch-switch grep.** Publish HELD until ai-maestro#36 deploys.

**UPDATE 2026-06-16T21:32 — MANAGER unblocked both REST clients (one premise verified-wrong); `team_registry` DONE; `approval_manager` held on a password design.** Branch now 9 commits ahead of main.
- **`amcos_team_registry.py` ✅ committed a318976** — urllib→subprocess `_run_cli`; list/create/remove-agent/update → `aimaestro-teams.sh`; 3 residuals `DECOUPLE-BLOCKED ai-maestro#36`: github_project (no `--gh-project`), update-status (no status-set verb), **add_agent (NEW finding: `agent create` REQUIRES `--dir`=spawn semantics + no `--status`; rich roster-registration has no clean verb — corrects the MANAGER's add_agent→agent-create mapping)**. Agent-drafted (rate-limit-truncated at the team_id line), fully orchestrator-reviewed + finished + committed. Spec: `scripts_dev/team-registry-repoint-spec.md`.
- **`amcos_notify_agent.py` ✅** — the resolve repoint had a BUG (parsed `session_name`; the `resolve --json` key is `tmuxSessionName`) → fixed d267c8a; comment grep-cleaned d9350c1. `resolve` IS a real verb (agent.sh:90→`cmd_resolve`@agent-session.sh:296, returns tmuxSessionName) — corrects the MANAGER's "resolve isn't a verb, use show" (they read the Apr-14 *deployed* copy). #16 issuecomment-4722644881.
- **`amcos_approval_manager.py` 🔴 HELD** — verified COS captures NO governance password anywhere (`create_request`+whole-file) AND `cmd_approve`/`cmd_reject` mandate `--password` with no env-fallback. The decision path can't repoint without introducing a password source (on-disk = security regression). Recommended a CLI `${GOVERNANCE_PASSWORD}` env-fallback (#36 candidate) so COS never handles the secret; create/list/get are mappable but I hold the whole script to land ONE clean transport (no half-urllib/half-CLI class). `sync_local_to_api` status-PATCH also has no verb. #16 issuecomment-4722668327.
- **`approve --comment`: dropped** (told MANAGER) — COS's comment survives via the YAML mirror + AMP notification, both independent of the CLI call.
- Only remaining `/api/` in scripts = `amcos_approval_manager.py` (password-gated). The 4 open #36 calls COS needs: password env-fallback, status-set verb, rich roster-registration, `--gh-project`. team_registry+add_agent finding posted #16 issuecomment-4722932335.

**FULL SCOPE (full-tree grep, BIGGER than the 4-script inventory):** 4 Python scripts
(`amcos_notify_agent.py` resolve, `amcos_approval_manager.py` governance, `amcos_team_registry.py`
×6 + `amcos_generate_team_report.py` teams) + ~25 `.md` agent/command/skill files with direct
`/api/` INSTRUCTIONS (governance, teams, transfer, agents/labels) + `TEAM_REGISTRY_SPECIFICATION.md`
(descriptive — reframe, don't strip). **FALSE POSITIVES — do NOT touch:** `skills/amcos-onboarding/
references/*` mention `src/api/auth.py` / "Backend API" = SAMPLE PROJECT content, not AI Maestro.

**VERIFIED frozen CLI verbs (read from `~/ai-maestro/scripts/` source — ground truth, NOT the
MANAGER's table summary which had `request <id>` imprecise):**
- `aimaestro-governance.sh`: `requests [--status|--type|--host|--agent]` = **LIST** (GET) · `request
  --type T [--password P] [--agent] [--role] [--target-host] [--requested-by] [--payload-json]` =
  **CREATE** (POST) · `approve <id> --password P [--approver]` · `reject <id> --password P [--reason]`
  · `transfer list|create|resolve`. **No show-single-by-id verb** → poll = `requests --status` +
  client-filter by requestId. PATCH-status ops (sync/timeout) → residual marker.
- `aimaestro-teams.sh`: `list · show <id> · create --name N [--description --agents --type --cos
  --password --gh-owner --gh-repo] · update <id> · delete <id> [--password --delete-agents] ·
  add-agent · remove-agent`.
- `aimaestro-agent.sh`: `resolve <name>|--cwd <path> [--json]` · `list [--status --json]` · session.
- **Residual marker** (recipe §3, for ops w/ no verb): `<!-- DECOUPLE-BLOCKED ai-maestro#36: <op> —
  CLI verb not yet deployed -->`. Known BLOCKED: kanban-config, presence, session-user-input,
  team-tasks, governance-password-set, single-request-by-id show, PATCH-status.
- Repoint rule: change INSTRUCTION calls only; DROP manual `-H "Authorization: Bearer $AID_AUTH"`
  (CLIs resolve auth internally); behavior unchanged; verify EVERY inserted verb vs the list above
  (MANAGER warns agents hallucinate verbs). Python scripts keep a graceful fallback like pass-1.

**NEXT ACTION (resume here):** Mechanical pass-2 is COMPLETE (see the 2026-06-16T21:13 update). Two
things remain, both GATED — not idling, real dependencies:
1. **DESIGN-BLOCKED** — `amcos_approval_manager.py` (decision path needs the `--password` env-fallback
   #36 decision; create/list/get mappable but HELD to land one clean transport) + the 14 residual
   governance/label/sessions reference docs (need the verb-mapping decisions / residual-markers). When the
   MANAGER rules on the FOUR open #36 calls COS needs — (a) `approve`/`reject` `${GOVERNANCE_PASSWORD}`
   env-fallback, (b) a status-set verb (update-status + sync_local_to_api), (c) rich roster-registration
   (add_agent), (d) `teams create --gh-project` — repoint those + drop the `DECOUPLE-BLOCKED` markers.
   (`amcos_team_registry.py` is now DONE — a318976, with 3 of those as marked residuals.)
2. **DEPLOY-GATED** — when ai-maestro#36 deploys the CLIs to `~/.local/bin`, run the full-tree verb-audit
   (`grep aimaestro-*.sh` vs the verb list) + `publish.py --dry-run`, then merge `decouple/api-to-frozen-cli`
   → main + publish. NOT before (COS must never ship calls to an absent CLI). DEPLOY_TRIGGER still 0.
Cross-check AMAMA's `design/handoffs/api-to-cli-mapping.md` when its branch merges.

**NEXT ACTION (pass 1 — doable now) [DONE]:**
1. Repoint `amcos_heartbeat_check.py` list-active → `aimaestro-agent.sh list
   --status online --json` (subprocess; tolerant `.get()` parse; KEEP the existing
   state-file fallback on any error — the CLI needs the server up at runtime, same
   as the old `/api/` call). 'active' == 'online' for the heartbeat.
2. Rewrite the 4 stale lifecycle TODOs to reference the CLI layer (kill their `/api/`).
3. Tests + CPV strict + lint green → publish minor → report version on #20.

**SUBSEQUENT PASSES (as CLIs land on ai-maestro#16):** repoint name-resolve
(`resolve`), governance-request (governance CLI), teams-CRUD (`aimaestro-teams.sh`
once on PATH). Repoint + publish each as it lands. Don't stop until
`grep -rn '/api/'` in the COS tree is empty.

## Acceptance criteria
**Refined by MANAGER on #16 (issuecomment, 21:01Z, accepted COS's corrections; tracked in
their TRDD-5fc2cb0a):** `grep -rn '/api/'` shows no direct-call **INSTRUCTIONS** in scripts
OR prompts — but **descriptive "the CLI wraps /api/X" docs are FINE**. So COS pass-2:
(1) repoints the 3 script classes to the CLIs; (2) repoints the instructing prompts
(`amcos-approval-coordinator.md`, the teams agents, `amcos-transfer-agent.md`); (3) reframes
`docs/TEAM_REGISTRY_SPECIFICATION.md` as descriptive CLI-wraps (NOT stripped). The
`amcos-transfer-agent` transfer path is a confirmed fleet CLI-surface GAP (transfer verb) the
MANAGER added to the build queue. Then tests + CPV strict + lint green; published; #20 answered.
