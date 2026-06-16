---
trdd-id: 8e8d6618-ecd0-4b53-a733-829c4c7dfe20
title: Remove all direct /api/* calls from COS scripts — repoint to the immutable CLI layer (#20)
column: dev
created: 2026-06-15T22:18:37+0200
updated: 2026-06-16T02:21:47+0200
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
