---
trdd-id: ENZLC63L
title: Align four command docs to the flags their scripts actually parse
column: ai_review
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T20:39:01+0200
current-owner: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: docs
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

- [ ] Each doc's arguments table lists exactly the parser's flags — nothing more.
- [ ] Every example in each doc, run verbatim, is accepted by the parser (exit 0 or a real run).
- [ ] Where behaviour differs from what the old doc implied (single-action, JSON-only), the doc
      says so in one line rather than silently dropping the claim.
- [ ] Suite green, ruff clean.
