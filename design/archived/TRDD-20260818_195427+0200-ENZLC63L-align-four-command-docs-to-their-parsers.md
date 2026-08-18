---
trdd-id: ENZLC63L
title: Align four command docs to the flags their scripts actually parse
column: complete
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T23:40:02+0200
implementation-commits: [b261e74]
current-owner: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: docs
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: user
min-approval-requirement: none
created-by: DAESKVN9
npt: []
eht: []
blocked-by: []
release-via: publish
external-refs: [ai-maestro TRDD-BRRJK57P]
priority: 3
---

# Align four command docs to the flags their scripts actually parse

Phase-2 remediation of axis-1 findings 5–8 (report
`reports/plugin-self-audit/20260816_170747+0200-axis1-missing-features.md`, hub-verified). One
class, four files: the command doc promises flags its script's argparse rejects, so the doc's own
examples fail at the shell.

Direction of the fix: **docs down to the parser, not parser up to the docs.** The flags were
invented by the docs; nobody asked for the features, and implementing them now would be building
to a typo. If any of them turn out genuinely wanted later, that is a feature card with its own
justification.

| doc | promised but absent | parser reality |
|---|---|---|
| `commands/amcos-configure-plugins.md` | `--enable`/`--disable`; `--add`/`--remove` "repeatable" | `--add/--remove/--list` mutually exclusive, one action per run (`amcos_configure_plugins.py:196-205`) |
| `commands/amcos-reindex-skills.md` | `--wait`, `--timeout`, `--verbose` (used by its own examples) | only `session_name`, `--force`, `--dry-run` (`amcos_reindex_skills.py:120-132`) |
| `commands/amcos-performance-report.md` | bare invocation as first example; `--format/--compare/--detailed` | `--agent/--project/--all` REQUIRED mutually-exclusive group; JSON only, `--compact` (`amcos_performance_report.py:358-383`) |
| `commands/amcos-resource-report.md` | `--format/--include-history/--verbose/--watch` | only `--check-spawn/--status` + `--compact`; output unconditionally JSON (`amcos_resource_monitor.py:249-261`) |

## Acceptance criteria

- [x] Each doc's arguments table lists exactly the parser's flags — nothing more. → verified per
      file against the argparse blocks; resource-report's fictional agent-listing/trends sections
      replaced with what the script measures (verified by RUNNING it).
- [x] Every example in each doc, run verbatim, is accepted by the parser. → all four checked:
      argparse-level acceptance (perf --all exit 0, reindex --dry-run 0, configure --list 0,
      resource --check-spawn exit 1 = runtime "cannot spawn", not a usage error).
- [x] Behaviour differences stated in one line each (single-action, JSON-only, no watch/wait).
- [x] Suite green (341), ruff clean.

## Approval log

- 2026-08-18T23:40:02+0200 — COMPLETED. Flow: todo → dev → testing (parsers accept every
  example, suite 341) → ai_review (llm-ext 3-model ensemble on the commands/ diff: 2/3 approve
  all four files; the one REJECT — argument-hint missing optional --project-dir on
  performance-report — was a valid nit and was FIXED before closing; report
  reports/llm-externalizer/20260818_233923+0200-code_task-enzl.diff-1629a5.md) → complete.
  Implementation commit b261e74 (+ the nit fix in the closing commit).
