# TRDD-23c5566e — Claude Code v2.1 (.101→.143) Adoption Backlog

**TRDD ID:** `23c5566e-9555-47dc-8a8c-d45c61d7e194`
**Filename:** `design/tasks/TRDD-23c5566e-9555-47dc-8a8c-d45c61d7e194-cc-2-1-adoption-backlog.md`
**Tracked in:** this repo (`design/tasks/` is git-tracked)

**Status:** Not started
**Plugin:** ai-maestro-chief-of-staff
**Created:** 2026-05-16
**Source analysis:** `reports/changelog-research/20260516_073019+0200-claude-code-v2.1.81-to-v2.1.143-chief-of-staff-impact.md`

## Context

Claude Code shipped ~62 releases between v2.1.81 and v2.1.143 (one-month window
ending 2026-05-16). The v2.13.0 bump landed the **mechanical, low-risk** items:

- Pinned minimum Claude Code version to 2.1.139.
- Migrated `hooks/hooks.json` to the `args` exec form (CC 2.1.139+).
- Updated `scripts/validate_hook.py` to accept both `command` and `args` forms.
- Documented the v2.1.143 Stop-hook 8-block cap and the
  `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` override.
- Fixed the malformed `allowed-tools` in `commands/amcos-transfer-agent.md`.

This TRDD tracks the **deferred** HIGH and MEDIUM adoption items — things that
require design judgement, refactoring, or new feature surface, and are not
purely mechanical. They were intentionally left out of v2.13.0 to keep that
release a tight safety-and-compatibility patch.

## Backlog items (each becomes its own PR / sub-section when picked up)

### Item A — PreCompact hook for coordination-state preservation (HIGH-11)

**Source:** Claude Code v2.1.105 introduced the PreCompact hook event and
allows hooks to block compaction (`exit 2` or `{"decision":"block"}`).

**Problem:** AMCOS coordinates multi-agent state across turns. Conversation
compaction can silently drop critical handoff context (active-agents list,
pending-handoffs queue, in-flight GovernanceRequest IDs). On a fresh post-
compact turn, the chief-of-staff agent may not know that AMOA is still waiting
on an acknowledgement.

**Design sketch:**
- New script `scripts/amcos_pre_compact.py`.
- Register under `hooks/hooks.json` → `"PreCompact"` event.
- Default behaviour: snapshot `state.md` + `.amcos-logs/handoffs/` to
  `.amcos-logs/<ts>-pre-compact.json` BEFORE allowing compaction to proceed.
  Always returns allow (exit 0) — snapshot is for crash-recovery / forensics.
- Optional (env-gated by `AMCOS_BLOCK_COMPACT_ON_PENDING_HANDOFF=1`): block
  compaction when `amcos_team_registry.py` reports any agent in
  `WAITING_FOR_HANDOFF` state. Returns `{"decision":"block", "reason": ...}`
  so the user gets a clear "finish handoff X before compacting" message.

**Acceptance:**
- Compaction triggered with active handoffs → snapshot file written.
- Compaction triggered with no handoffs → no block, snapshot written anyway
  (cheap insurance).
- Env-gated block path covered by a unit test that mocks the registry.

**Dependencies:** None — purely additive.

---

### Item B — Plugin `monitors` replacing UserPromptSubmit heartbeat (HIGH-12)

**Source:** Claude Code v2.1.105 introduced plugin-declared `monitors` under
`plugin.json` → `experimental.monitors[]` that auto-arm at session start.

**Problem:** `amcos-heartbeat-check` runs on every `UserPromptSubmit`. That
couples agent-health detection to user activity — if the user goes idle for an
hour, no heartbeats fire even when an agent has gone unresponsive. It also
wastes a hook fire on every turn, even those that don't need a heartbeat.

**Design sketch:**
- Add `experimental.monitors` block to `.claude-plugin/plugin.json`:
  ```json
  "experimental": {
    "monitors": [{
      "name": "amcos-heartbeat-monitor",
      "interval": "300s",
      "command": ["python3", "${CLAUDE_PLUGIN_ROOT}/scripts/amcos_heartbeat_check.py"]
    }]
  }
  ```
- Verify monitor fire-cadence and exit-code handling against the Claude Code
  reference. Right now `amcos_heartbeat_check.py` reads stdin JSON shaped for
  UserPromptSubmit — the monitor invocation may not provide that shape, so
  the script needs a defensive `try/except json.JSONDecodeError` (which it
  already has, but the new code path should be exercised).
- Remove the `amcos-heartbeat-check` entry from `hooks/hooks.json` once the
  monitor is verified working.
- Keep `amcos-resource-check` on `UserPromptSubmit` (it really does depend on
  the prompt — checking resources right before a long turn).

**Acceptance:**
- Heartbeat warnings fire every 5 min regardless of user activity.
- `UserPromptSubmit` hook event has only `amcos-resource-check`.
- Bump min Claude Code version to whichever release stabilised
  `experimental.monitors[]` (TBD on a future scan — feature is still
  `experimental.` at the time of writing).

**Dependencies:** Verify the monitors API is stable enough for production
use before promoting.

---

### Item C — terminalSequence adoption for notifications (MED-1, MED-2)

**Source:** Claude Code v2.1.141 lets hook JSON output carry a
`terminalSequence` field for window-title / bell / desktop-notification cues
without a controlling terminal.

**Problem:** AMCOS notification paths today rely on the user's terminal /
the AI Maestro inbox bell. Cross-platform desktop notification of "agent
stalled" / "approval pending" is currently absent.

**Design sketch:**
- In `scripts/amcos_resource_check.py`: when an alert triggers, include
  `"terminalSequence": "\u0007"` (bell) and a `"title": "⚠️ Resources"` cue
  in the hook output JSON.
- In `scripts/amcos_notification_protocol.py`: when broadcasting urgent
  governance notifications, attach a `terminalSequence` with the bell.
- Keep stdout-summary lines unchanged — `terminalSequence` is additive.

**Acceptance:**
- Resource-warning hook output now contains a `terminalSequence` key.
- Visual inspection: macOS, iTerm2, and Terminal.app all ring the bell on
  resource alerts.

---

### Item D — `effort.level` and `duration_ms` capture (MED-3)

**Source:**
- Claude Code v2.1.119 added `duration_ms` to PostToolUse hook input.
- Claude Code v2.1.133 added `effort.level` to hook input (overall turn
  effort classification).

**Problem:** `amcos_performance_report.py` currently reports counts but not
per-turn effort or per-tool latency. Adding these enables richer dashboards
and identifies slow tools across the team.

**Design sketch:**
- Add a new `PostToolUse` hook → `scripts/amcos_tool_telemetry.py`. Captures
  `tool_name`, `duration_ms`, `effort.level`, `cwd`, `session_id`. Appends
  to `.amcos-logs/tool-telemetry/<YYYYMMDD>.jsonl`.
- Update `amcos_performance_report.py` to consume that JSONL and emit a
  per-agent table: average effort, p50/p95 tool latency, top-3 slowest
  tools.

**Acceptance:**
- Performance report includes new effort + latency columns.
- JSONL file accumulates one entry per tool use.
- No PII (raw command args, file contents) leaks into the JSONL.

---

### Item E — Per-agent frontmatter `hooks:` refactor (HIGH-15, HIGH-16)

**Source:** Claude Code v2.1.116 made agent frontmatter `hooks:` fire when
running as `--agent` main-thread. v2.1.118 unblocked agent-type hooks for
events beyond Stop/SubagentStop.

**Problem:** All 5 hooks live in centralised `hooks/hooks.json`. Some are
generic (resource-check, heartbeat, stop-check) but some are or could be
agent-specific (recovery-coordinator's pre-flight, skill-validator's index
warm-up). Centralisation makes the hook surface harder to scan and couples
unrelated agents.

**Design sketch:**
- Identify per-agent specialised hook logic that today lives in the
  centralised scripts but is only relevant for one agent.
- Move those into the agent frontmatter `hooks:` of the relevant
  `agents/*.md`. Leave truly cross-cutting hooks (session-start, stop-check)
  in `hooks/hooks.json`.
- Document the refactor pattern in `docs/hook-architecture.md` (new file).

**Acceptance:**
- At least one agent (`amcos-recovery-coordinator` is the most obvious
  candidate) ships its own frontmatter `hooks:`.
- Centralised `hooks/hooks.json` only contains genuinely cross-cutting hooks.
- Validator still passes (validate_agent + validate_hook).

**Risk:** This is a refactor, not breakage. Defer to a sprint where time
permits design discussion. Low urgency.

---

### Item F — `/goal` replacement for wait-for-* polling commands (MED-4)

**Source:** Claude Code added a `/goal` command (~v2.1.139 era) that keeps
Claude working until a completion condition is met, replacing manual polling.

**Problem:** `commands/amcos-wait-for-agent-ok.md` and
`commands/amcos-wait-for-approval.md` today loop via repeated polling. The
implementation is fragile (loop in markdown is hard to reason about) and
wastes turns.

**Design sketch:**
- Rewrite the body of both commands to set a `/goal` whose completion
  predicate calls the relevant status-check script.
- Keep the same external interface (slash-command arguments unchanged).

**Acceptance:**
- Both commands work with a single `/goal` invocation each.
- No regression in approval/ok detection.

---

### Item G — Per-spawned-agent OTEL correlation (MED-5)

**Source:** Claude Code v2.1.139 propagates `x-claude-code-agent-id` and
`x-claude-code-parent-agent-id` headers on API requests from sub-agents.

**Problem:** `amcos_team_registry.py` cannot today correlate token spend or
latency to a specific spawned agent — it only sees aggregate session
numbers.

**Design sketch:**
- Have `amcos_spawn_agent.py` record the spawned agent's ID alongside the
  registry entry.
- Update the team-registry consumer to join on those headers via OTEL.

**Acceptance:**
- Team report shows per-spawned-agent cost / latency.
- Existing fields unchanged.

---

### Item H — PostToolUse `updatedToolOutput` for governance scrubbing (MED-13, MED-14)

**Source:** Claude Code v2.1.121 + v2.1.139 added `continueOnBlock` and
`hookSpecificOutput.updatedToolOutput` so PostToolUse hooks can rewrite or
reject tool results before Claude sees them.

**Problem:** Future governance use case: when an agent runs a tool whose
output reveals sensitive infra (e.g. `kubectl get secrets`), AMCOS could
scrub the result before the agent sees it.

**Design sketch:** Pure speculation at this stage — capture the capability
in the backlog so a future security-hardening sprint can pick it up.
Acceptance criteria TBD.

---

## Sequencing

Suggested order when an adoption sprint opens:

1. **Item A** (PreCompact) — pure additive, lowest risk, immediate value.
2. **Item D** (telemetry) — additive, unlocks better performance reports.
3. **Item C** (terminalSequence) — additive, UX win.
4. **Item B** (monitors) — wait for `experimental.monitors[]` to graduate.
5. **Item F** (`/goal`) — modest refactor, frees up command complexity.
6. **Item G** (OTEL) — depends on team-registry redesign.
7. **Item E** (per-agent hooks refactor) — pure architectural cleanup.
8. **Item H** (PostToolUse scrubbing) — speculative, parked.

## Out of scope for this TRDD

- v2.1.81 → v2.1.100 changes (not currently in the upstream changelog —
  re-run the research agent against those versions if Anthropic backfills
  them).
- Anything that requires breaking AMCOS API contracts with AMOA / AMAA / AMIA
  (those need their own TRDDs).

## Source artefacts

- Impact analysis: `reports/changelog-research/20260516_073019+0200-claude-code-v2.1.81-to-v2.1.143-chief-of-staff-impact.md`
- Plugin inventory: `reports/chief-of-staff-inventory/20260516_072427+0200-plugin-surface-inventory.md`
- Upstream changelog: <https://code.claude.com/docs/en/changelog.md>
