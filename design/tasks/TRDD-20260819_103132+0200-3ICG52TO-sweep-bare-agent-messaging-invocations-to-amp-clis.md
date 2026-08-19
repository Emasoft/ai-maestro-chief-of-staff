---
trdd-id: 3ICG52TO
title: Sweep bare agent-messaging skill invocations to the frozen amp-* CLIs
column: dev
created: 2026-08-19T10:31:32+0200
updated: 2026-08-19T10:31:32+0200
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

- [ ] Zero remaining bare-name INVOCATION teachings in live surfaces (skills/, agents/,
      commands/, scripts/, CLAUDE.md) — verified by grep re-measure, with any surviving hits
      individually justified as prose/pointer.
- [ ] Converted teachings name the frozen CLI verbs, not the raw API and not SendMessage.
- [ ] Suite green, ruff clean, `trddgrep validate` exit 0.
- [ ] Published in the next release and reported to the hub.
