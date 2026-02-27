---
name: amcos-validate-skills
description: "Validate skills for an agent's plugin using the CPV plugin validator"
argument-hint: "<PLUGIN_DIR> [--verbose]"
user-invocable: true
allowed-tools: ["Bash(uv run --with pyyaml python:*)"]
---

# Validate Skills Command

Validate agent skills using the CPV (Claude Plugins Validation) plugin validator. This validates the full plugin structure including all skills, commands, hooks, and manifest.

## Usage

```bash
# Validate the current plugin directory
uv run --with pyyaml python scripts/validate_plugin.py . --verbose

# Validate a specific skill directory using CPV skill validator
uv run --with pyyaml python scripts/validate_skill.py <skill-dir>
```

## What This Command Does

1. **Validates Plugin Structure**
   - Checks manifest.yaml existence and format
   - Validates YAML frontmatter fields across all components
   - Verifies directory structure matches manifest declarations

2. **Validates Skills Structure**
   - Checks SKILL.md existence and format
   - Validates YAML frontmatter fields (name, description, etc.)
   - Verifies reference documents are accessible
   - Checks for progressive disclosure structure

3. **Validates Commands and Hooks**
   - Command markdown files format and frontmatter
   - Hook configuration validity
   - Script references resolve to existing files

4. **Reports Validation Results**
   - Lists all components with pass/fail status
   - Details specific validation errors by severity (CRITICAL, MAJOR, MINOR)
   - Zero tolerance for CRITICAL and MAJOR issues

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `PLUGIN_DIR` | Yes | Path to the plugin directory (use `.` for current directory) |
| `--verbose` | No | Show detailed validation output |

## Examples

### Validate the current plugin

```bash
uv run --with pyyaml python scripts/validate_plugin.py . --verbose
```

### Validate a specific skill directory

```bash
uv run --with pyyaml python scripts/validate_skill.py skills/amcos-onboarding
```

## Validation Checks

The CPV validator performs these checks:

| Check | Description | Severity |
|-------|-------------|----------|
| manifest.yaml exists | Plugin manifest must exist | CRITICAL |
| Valid frontmatter | YAML frontmatter must parse correctly | CRITICAL |
| Required fields | `name`, `description` must be present | MAJOR |
| SKILL.md exists | Main skill file must exist per skill | MAJOR |
| References valid | All referenced files must exist | MAJOR |
| Scripts exist | Referenced scripts must be present | MAJOR |
| No broken links | Internal references must resolve | MINOR |

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "manifest.yaml not found" | Not a valid plugin directory | Check path |
| "SKILL.md missing" | Skill directory incomplete | Create SKILL.md |
| "Invalid frontmatter" | YAML parse error | Fix YAML syntax |
| "validate_plugin.py not found" | CPV scripts not synced | Re-sync from CPV plugin |

## Prerequisites

- CPV validation scripts must be present in `scripts/` (synced by push-plugins.sh)
- `pyyaml` is provided at runtime via `uv run --with pyyaml`

## Notes

- This command uses the CPV (Claude Plugins Validation) plugin validator, which is the standard validator for all AI Maestro plugins
- The validator scripts are automatically synced from the CPV plugin into each plugin's `scripts/` directory by `push-plugins.sh`
- Zero tolerance policy: CRITICAL and MAJOR issues must be fixed before pushing

## Related Commands

- `/amcos-configure-plugins` - Configure plugins for an agent
- `/amcos-reindex-skills` - Trigger PSS reindex after skill changes
- `/amcos-orchestration-status` - Check agent orchestration status
