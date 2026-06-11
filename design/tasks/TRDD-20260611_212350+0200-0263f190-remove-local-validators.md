---
trdd-id: 0263f190-6a45-4a0e-9da5-f188403af0f5
title: Remove the vendored local validator suite — remote CPV is the only validator
column: dev
created: 2026-06-11T21:23:50+0200
updated: 2026-06-11T21:23:50+0200
current-owner: cos-ai-maestro-chief-of-staff
assignee: cos-ai-maestro-chief-of-staff
priority: 2
severity: MEDIUM
effort: M
labels: [validation, cpv, cleanup]
task-type: refactor
parent-trdd: null
relevant-rules: [1]
release-via: publish
delivery: direct-push
target-branch: main
publish-target: ai-maestro-plugins
test-requirements: [unit, lint]
impacts: [public-api]
external-refs: ["github.com/Emasoft/claude-plugins-validation"]
---

# TRDD-0263f190 — Remove local validators; remote CPV only

## Why

USER directive (2026-06-11): "remove the local validation scripts and only
invoke the cpv plugin." Local copies of the CPV validator suite drift from
upstream rules (this repo's copies had already diverged — e.g. its
`amcos_design_validate.py` enforced the pre-3-pillars doc schema and rejected
v2 TRDDs). Validation policy: findings are fixed by devitalizing or removing
the offending content — never by suppressing or exempting a rule (the exempt
list was found exploitable). Validator bugs / false positives are filed
upstream on `Emasoft/claude-plugins-validation`.

## What was removed (all tracked → recoverable from git history)

**20 scripts:** `amcos_design_validate.py`, `cpv_validation_common.py`,
`validate_agent.py`, `validate_command.py`, `validate_documentation.py`,
`validate_encoding.py`, `validate_enterprise.py`, `validate_hook.py`,
`validate_lsp.py`, `validate_marketplace_pipeline.py`,
`validate_marketplace.py`, `validate_mcp.py`, `validate_rules.py`,
`validate_scoring.py`, `validate_security.py`,
`validate_skill_comprehensive.py`, `validate_skill.py`, `validate_xref.py`,
plus dead dependents `lint_files.py` and `smart_exec.py`.

**2 test files:** `tests/test_validate_command.py`,
`tests/test_amcos_design_validate.py` (they tested the removed modules).

**Helper preservation:** `parse_gitignore` + `is_path_gitignored` were inlined
verbatim into `scripts/gitignore_filter.py` (publish.py depends on it) before
deleting `cpv_validation_common.py`.

## Surfaces repointed to remote CPV

`commands/amcos-validate-skills.md` (rewritten), `hooks/README.md`,
`tests/README.md`, `tests/test_component_contracts.py` (docstring),
`skills/amcos-skill-management/references/validation-procedures.md` (§5/§6.1
+ TOC), `skills/amcos-failure-notification/references/design-document-protocol.md`
(§4.3 + python example → 3-pillars supersession note),
`skills/amcos-plugin-management/references/plugin-validation.md`,
`skills/amcos-onboarding/references/{op-conduct-project-handoff,
op-validate-handoff,onboarding-overview-and-examples}.md`,
`skills/amcos-staff-planning/references/staffing-templates.md`, `README.md`.

Canonical invocation everywhere:
`uvx --from git+https://github.com/Emasoft/claude-plugins-validation --with
pyyaml cpv-remote-validate plugin . [--strict]`

**Kept:** `skills-ref` mentions (live external CLI, not a local validator);
`scripts/publish.py` (the pipeline that INVOKES remote CPV);
`gitignore_filter.py` (utility).

## Acceptance criteria

- Zero non-tombstone references to any removed module in shipped surfaces.
- pytest gate green; CPV strict exit 0; published in the same minor as the
  memory-bank retirement (TRDD-5f717ded).
