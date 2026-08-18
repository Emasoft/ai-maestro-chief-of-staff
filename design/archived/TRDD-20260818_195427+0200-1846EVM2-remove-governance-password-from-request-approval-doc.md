---
trdd-id: 1846EVM2
title: Remove the agent-held governance password from the amcos-request-approval command doc
column: complete
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T20:03:49+0200
implementation-commits: [e3a3518]
current-owner: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: security
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: user
min-approval-requirement: 0
created-by: DAESKVN9
npt: []
eht: []
blocked-by: []
release-via: publish
external-refs: [ai-maestro TRDD-BRRJK57P]
priority: 1
---

# Remove the agent-held governance password from the amcos-request-approval command doc

Phase-2 remediation of the Phase-1 self-audit's **priority-1 finding** (axis 4, Finding 2;
report `reports/plugin-self-audit/20260816_232523+0200-axis4-bugs-conflicts.md`, hub-verified).

`commands/amcos-request-approval.md` documents an agent-held governance password —
`argument-hint` (:4), the arguments table (:52, "Manager-provided governance password"), and a
WORKED EXAMPLE `--governance-password "$GOV_PWD"` (:77). Three sibling files state the R32 model
it contradicts: `agents/amcos-approval-coordinator.md:18`,
`skills/amcos-permission-management/references/governance-details-and-examples.md:39`,
`agents/ai-maestro-chief-of-staff-main-agent.md:92`. An agent following the command's own usage
puts a secret on the command line — shell history + process list.

The defect is that the PARAMETER exists: a parameter is a value the caller must first possess,
which is exactly what R32 says the caller must never possess. So the fix deletes the parameter
and the payload field, not just the example.

## Acceptance criteria

- [x] `--governance-password` gone from `argument-hint`, the arguments table, and every example.
      → all three edits landed; the critical-op example now says the sudo gate is USER-via-UI.
- [x] `governancePassword` field gone from both JSON payload samples. → both `null` lines removed;
      the "Invalid password" error row replaced with the R32 pending-gate row.
- [x] The doc states the R32 model where the flag row was. → one paragraph under the operations
      table; the table's gate column now reads "USER via UI (R32)" for `critical`.
- [x] Repo-wide grep clean: `grep -rn "governance-password\|governancePassword" commands/ skills/
      agents/ scripts/ tests/` → only the guard tests' own detector needles remain.
- [x] No password literal introduced; `$AIM_GOVERNANCE_PASSWORD` not needed and not named.
- [x] Suite green, ruff clean → 341 passed (a NEW tree-wide guard test was added:
      `test_no_agent_held_password_anywhere_in_agent_facing_docs`, because the existing R32 guard
      scanned only one skill directory and could never have seen this defect in commands/ — the
      guard's scope was narrower than its invariant, which is how the defect survived).

## Approval log

- 2026-08-18T20:03:49+0200 — COMPLETED. Flow: todo → dev (19:57) → testing (suite 341 green,
  ruff clean) → ai_review (llm-ext 3-model ensemble, all three APPROVE — report
  `reports/llm-externalizer/20260818_200331+0200-code_task-p1.diff-0bd7b3.md`) → complete.
  Implementation commit e3a3518. human_review OUT per TRDD-BRRJK57P (hub holds that column).
