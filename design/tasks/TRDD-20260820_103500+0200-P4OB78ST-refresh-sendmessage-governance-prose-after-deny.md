---
trdd-id: P4OB78ST
title: Refresh SendMessage governance prose after the harness deny landed
column: complete
created: 2026-08-20T10:35:00+0200
updated: 2026-08-20T10:52:00+0200
release-via: none
implementation-commits: [pending-local]
current-owner: ai-maestro-chief-of-staff
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: docs
scope: project
project-id: ai-maestro-chief-of-staff
approval-tier: 0
external-refs: ["hub AMP-only directive 2026-08-20 (USER mandate)", "ai-maestro 556f340f"]
---

# Refresh SendMessage governance prose after the harness deny landed

USER directive 2026-08-20: inside the ai-maestro harness the client SendMessage tool is
DENIED (`permissions.deny: ["SendMessage"]` written into each registered agent workdir's
`.claude/settings.local.json` on create/wake/sweep — ai-maestro 556f340f). AMP is the only
inter-agent channel.

The COS plugin ships NO teach-to-use SendMessage prose (swept in TRDD-3ICG52TO, v2.32.7).
But several governance passages in `agents/ai-maestro-chief-of-staff-main-agent.md`
(~lines 747, 783-784, 794, 815, 821, 911, 913) DESCRIBE the client tool as an unguarded
side door — "over `SendMessage` nothing refuses you, and it is forbidden just the same".
That fact is now stale: the deny makes the refusal structural. Not a runtime hazard
(nothing invokes the tool), purely a stale-fact refresh.

## Task

Update those passages to state: the client tool is structurally denied in registered
agent workdirs (556f340f, self-repairing on the sweep); the R6-graph warnings remain
valid for any surface the deny does not cover (forks, dev sessions, general-purpose
subagents that inherit the full tool surface).

## Acceptance criteria

- [x] Every "nothing refuses you"-shaped claim about the client SendMessage tool is
      updated to reflect the structural deny, without weakening the R6 warnings.
- [x] No new teach-to-use instruction introduced; amp-* CLIs remain the only taught path.
- [x] Suite green (341), ruff clean, trddgrep validate exit 0; commits ride the next
      release (direct push is publish-gated by policy).

## Approval log

- 2026-08-20T10:52:00+0200 — COMPLETED (Tier-0 docs). 7 passages refreshed in
  agents/ai-maestro-chief-of-staff-main-agent.md; the inbound-untrusted-data warning
  (unaffected by the deny) left as-is.
