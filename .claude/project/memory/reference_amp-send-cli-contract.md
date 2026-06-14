---
name: reference_amp-send-cli-contract
description: "amp-send / aimaestro-agent CLI call failed silently / 'Invalid type' / send returned exit 1 / which --type values are valid / cross-agent message retrieval returns []"
ocd: 2026-06-14
lmd: 2026-06-14
metadata:
  node_type: memory
  type: reference
  tier: component
---
The `amp-send` executable (`~/.local/bin/amp-send` → symlink to `amp-send.sh`)
is the runtime contract this plugin's Python scripts call. It is **send-only**
and validates `--type` against EXACTLY these **ten** values (L152 regex):

`request response notification task status alert update handoff ack system`

An out-of-list `--type` → `amp-send` prints `Error: Invalid type` and exits 1.
Callers that swallow the non-zero exit (return False/[]) then **fail silently** —
the message is never sent. This was the root cause of the #19 arg-drift bugs.

Signature is **positional**: `amp-send "<recipient>" "<subject>" "<message>"
[--priority <low|normal|high|urgent>] [--type <valid>]`. The flag form
`--to/--subject/--message` is REJECTED.

**There is no CLI for retrieving ANOTHER agent's inbox** — `amp-send` is
send-only and `aimaestro-agent.sh` has no `messages` subcommand (the dead
`get_agent_messages()` that called it was removed in v2.17.0). Cross-agent
retrieval, if ever needed, must go via the AMP API, not the CLI.

## Notes and lessons learned

[^1]: [ocd:2026-06-14 lmd:2026-06-14] Verify the `--type` allow-list against the
  EXECUTABLE, never the `amp-send.md` command doc — the doc (ai-maestro-plugin
  v2.7.2) claims "exactly seven values" and omits handoff/ack/system, but the
  executable accepts ten. A fixer trusting the stale doc would wrongly "correct"
  valid `handoff`/`ack` calls and reintroduce the silent failure. WHY: docs drift
  from binaries; the binary's validation regex is the ground truth. (Filed the
  doc-staleness as ai-maestro-plugin#10.)
