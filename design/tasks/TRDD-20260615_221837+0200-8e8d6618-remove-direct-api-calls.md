---
trdd-id: 8e8d6618-ecd0-4b53-a733-829c4c7dfe20
title: Remove all direct /api/* calls from COS scripts — repoint to the immutable CLI layer (#20)
column: dev
created: 2026-06-15T22:18:37+0200
updated: 2026-06-15T22:41:05+0200
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
| name-resolve | `amcos_notify_agent.py:36` (`/api/agents?name=`) | `resolve` CLI | PENDING (no `resolve` subcommand) |
| governance-request | `amcos_approval_manager.py:48` (`/api/v1/governance/requests`) | governance CLI | PENDING |
| teams-CRUD | `amcos_team_registry.py` ×6 + `amcos_generate_team_report.py:72` (`/api/teams*`) | `aimaestro-teams.sh` | NEARLY — script exists in `~/ai-maestro/scripts/` (Jun 15 21:54) but NOT on PATH; needs ai-maestro owner to wire |
| (not calls) | `amcos_spawn/hibernate/terminate/wake_agent.py:2` | — | stale TODO comments `# TODO: Migrate to AI Maestro REST API` (now the WRONG advice) → rewrite to CLI |

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
`grep -rn '/api/'` in the COS tree returns nothing; every former API call goes
through the immutable CLI; tests + CPV strict + lint green; published; #20 answered.
