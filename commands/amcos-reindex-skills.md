---
name: amcos-reindex-skills
description: "Trigger Perfect Skill Suggester reindex for an agent's skills"
argument-hint: "<SESSION_NAME> [--force] [--dry-run]"
user-invocable: true
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/amcos_reindex_skills.py:*)"]
---

# Reindex Skills Command

Trigger a Perfect Skill Suggester (PSS) reindex for a specific agent. This regenerates the skill index for improved skill matching.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/amcos_reindex_skills.py" $ARGUMENTS
```

## What This Command Does

1. **Resolves Target Agent**
   - Resolves SESSION_NAME to agent identifier via AI Maestro API
   - Verifies agent has PSS plugin installed
   - Retrieves agent's project directory

2. **Sends Reindex Command via AI Maestro**
   - Sends `/pss-reindex-skills` command to target agent
   - Uses high-priority message for immediate processing
   - Includes reindex parameters if specified

3. **Reports the Send Result**
   - The command is fire-and-forget: it reports that the reindex request was sent, not the
     reindex outcome. The target agent performs the reindex on its own schedule.
   - With `--dry-run`, shows what would be sent without sending it.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `SESSION_NAME` | Yes | Target agent session name (e.g., `orchestrator-master`) |
| `--force` | No | Force full reindex even if cache is fresh |
| `--dry-run` | No | Show what would be sent without actually sending the request |

## Examples

### Trigger reindex for an agent

```bash
/amcos-reindex-skills orchestrator-master
```

### Force full reindex

```bash
/amcos-reindex-skills orchestrator-master --force
```

### Preview without sending

```bash
/amcos-reindex-skills libs-svg-svgbbox --dry-run
```

## Output Example

```
╔════════════════════════════════════════════════════════════════╗
║                    REINDEX REQUEST SENT                        ║
╠════════════════════════════════════════════════════════════════╣
║ Agent: orchestrator-master                                     ║
║ Message ID: msg-20260201-110532                                ║
║ Command: /pss-reindex-skills --force                           ║
║ Priority: high                                                 ║
╠════════════════════════════════════════════════════════════════╣
║ STATUS: Request sent via AI Maestro                            ║
╚════════════════════════════════════════════════════════════════╝
```

The command reports the SEND, not the reindex outcome — the target agent runs the reindex on
its own schedule. To see the result, check the target agent's own PSS status.

```
╔════════════════════════════════════════════════════════════════╗
║ INDEX LOCATION (on the target agent)                           ║
║ ~/.claude/cache/pss/skills-index.json                          ║
╚════════════════════════════════════════════════════════════════╝
```

## PSS Reindex Process

The Perfect Skill Suggester uses a two-pass indexing process:

### Pass 1: Factual Data Extraction
- Skill name and description
- Categories (16 predefined fields of competence)
- Keywords from skill content
- Script and reference inventory

### Pass 2: AI Co-usage Analysis
- Skill relationship mapping
- Usage pattern detection
- Weighted scoring calibration

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | SESSION_NAME not registered | Check agent name |
| "PSS not installed" | Agent doesn't have PSS plugin | Install PSS plugin first |
| "Agent not responding" | Agent session inactive | Restart agent session |
| "Reindex timeout" | Reindex took too long | Increase timeout or check agent load |
| "AI Maestro unavailable" | API not running | Start AI Maestro service |

## Prerequisites

- AI Maestro must be running (use `ai-maestro-agents-management` skill to verify)
- Target agent must be registered in AI Maestro
- Target agent must have Perfect Skill Suggester plugin installed
- Target agent session must be active

## Notes

- Reindex is **non-blocking** — the command sends the request and returns; there is no
  synchronous/wait mode
- The index is the **superset** of all skills; agent filters against its available skills
- Regenerating index clears any cached skill suggestions

## When to Reindex

Trigger a reindex when:
- New skills are added to plugins
- Skill content is significantly updated
- Plugin configuration changes
- Skill matching seems inaccurate

## Related Commands

- `/amcos-validate-skills` - Validate skills before reindexing
- `/amcos-configure-plugins` - Configure plugins (may require reindex)
- `/pss-reindex-skills` - Direct PSS reindex command (on target agent)
