---
trdd-id: 3ICG52TO
title: Sweep bare agent-messaging skill invocations to the frozen amp-* CLIs
column: published
created: 2026-08-19T10:31:32+0200
updated: 2026-08-19T14:45:29+0200
release-via: publish
implementation-commits: [0dda475, a59c331, f91367d]
current-owner: ai-maestro-chief-of-staff
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: bugfix
scope: project
project-id: ai-maestro-chief-of-staff
min-approval-requirement: none
relevant-rules: [1]
external-refs: ["hub SWEEP directive 2026-08-19 (USER mandate)", "AMOA model commit d5d1588"]
---

# Sweep bare `agent-messaging` skill invocations to the frozen amp-* CLIs

Hub orchestration directive (USER mandate 2026-08-19), with the hub's own correction applied:
`agent-messaging` is a REAL knowledge skill shipped by ai-maestro-plugin — the defect is only
teachings that INVOKE it by BARE NAME as the send mechanism. In a role agent's session the bare
name does not resolve (plugin skills resolve namespaced as `ai-maestro-plugin:agent-messaging`),
so every "Use the `agent-messaging` skill to send:" instruction fails at runtime.

Measured 2026-08-19: **553 invocation-shaped lines** (`Use the \`agent-messaging\` skill`)
across **145 files** outside `design/` (worst offenders: amcos-onboarding op-file 23×, the
recovery/failure/handoff reference sets 16-18× each).

## Method (hub-refined; AMOA d5d1588 is the model)

1. **Classify each hit** — INVOCATION-shaped teaching vs prose/infra/historical reference.
2. **Convert invocation teachings** to the frozen `amp-*` CLIs (`amp-send.sh` et al.), keeping
   each teaching's recipient/subject/payload semantics intact.
3. **Namespace** (`ai-maestro-plugin:agent-messaging`) only where a knowledge POINTER is
   genuinely meant.
4. **Never bulk-delete on string presence** — the count is an upper bound by string match.
5. Historical prose in `design/` archived cards is out of scope (frozen; not live teaching).

## Acceptance criteria

- [x] Zero remaining bare-name INVOCATION teachings in live surfaces (skills/, agents/,
      commands/, scripts/, CLAUDE.md) — verified by grep re-measure, with any surviving hits
      individually justified as prose/pointer.
- [x] Converted teachings name the frozen CLI verbs, not the raw API and not SendMessage.
- [x] Suite green, ruff clean, `trddgrep validate` exit 0.
- [x] Published in the next release and reported to the hub.

## Closure — 2026-08-19T14:45:29+0200

Executed as 15 parallel lean-worker batches (per-batch reports in gitignored
`reports/sweep-3ICG52TO/`): ~700 conversions across 145 files. Re-measure: 0 bare
invocation teachings outside design/; survivors = namespaced pointers, TOC anchor slugs,
and the `.agent.toml` `required_skills` identifier (machine-read list, bare by that list's
convention — its sibling entry is bare too). Two follow-on gate fixes: post-op 2.3.3 TOC
line desync (a59c331) and changelog privilege-escalation-shape devitalization via
cliff.toml commit_preprocessors (f91367d). Published v2.32.7; hub report sent.

## Approval log

- 2026-08-19T14:45:29+0200 — PUBLISHED (release v2.32.7). Tier-0 sweep under hub SWEEP
  directive (USER mandate 2026-08-19); publish under the standing USER GO of 2026-08-19.
