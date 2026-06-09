# Chief of Staff hooks

Hook registrations live in [`hooks.json`](hooks.json). Hook input arrives via
**stdin as JSON** — the scripts read stdin, not env vars. All registrations use
the `args` exec form (Claude Code v2.1.139+) for path-safe invocation; the
scripts themselves live in [`../scripts/`](../scripts/).

This file documents what each registered hook does. Keep it in sync with
`hooks.json` when adding, removing, or repointing a hook.

## Registered hooks

| Event | Script | Timeout | Purpose |
|---|---|---|---|
| `SessionStart` | `amcos_session_start.py` | 5s | Load session memory, initialize agent tracking, check system resources |
| `SessionEnd` | `amcos_session_end.py` | 5s | Save session memory and context on exit |
| `UserPromptSubmit` | `amcos_resource_check.py` | 5s | Check system resources before processing the user prompt |
| `UserPromptSubmit` | `amcos_heartbeat_check.py` | 5s | Check heartbeat status of all active agents before processing |
| `Stop` | `amcos_stop_check.py` | 10s | Block exit until all coordination work is complete and handoffs are saved |

## Notes

- The two `UserPromptSubmit` entries are independent matcher blocks and both
  fire on every prompt; each is non-blocking (additional-context only).
- The `Stop` hook honors the Claude Code v2.1.143 consecutive-block cap
  (8 blocks by default, override via `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`);
  see the docstring in `scripts/amcos_stop_check.py`.
- Validation: `python3 scripts/validate_hook.py hooks/hooks.json` checks the
  registration shape, exec form, and script presence.
