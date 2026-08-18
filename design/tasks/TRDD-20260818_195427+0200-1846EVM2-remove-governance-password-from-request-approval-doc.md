---
trdd-id: 1846EVM2
title: Remove the agent-held governance password from the amcos-request-approval command doc
column: todo
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T19:54:27+0200
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

- [ ] `--governance-password` gone from `argument-hint`, the arguments table, and every example.
- [ ] `governancePassword` field gone from both JSON payload samples (schema artifact; carries
      the wrong shape forward).
- [ ] The doc states the R32 model in one line where the flag row was: critical ops are gated by
      a sudo password requested only of the USER, only via the UI — never agent-held.
- [ ] `grep -rn "governance-password\|governancePassword" commands/ skills/ agents/` returns 0
      hits outside historical/prohibition prose.
- [ ] No password literal introduced anywhere; `$AIM_GOVERNANCE_PASSWORD` named only if a
      reference is needed at all.
- [ ] Suite green (`uv run --with pytest pytest tests/`), `ruff check .` clean.
