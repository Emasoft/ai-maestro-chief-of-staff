---
name: amcos-validate-skills
description: "Validate skills for an agent's plugin using the remote CPV plugin validator"
argument-hint: "<PLUGIN_DIR> [--strict]"
user-invocable: true
allowed-tools: ["Bash(uvx:*)"]
---

# Validate Skills Command

Validate agent skills using the **remote CPV (Claude Plugins Validation)
validator**, fetched from GitHub at invocation time. There are NO local
validator scripts in this plugin — local copies drift from upstream rules, so
validation always runs the canonical remote validator (the same one
`scripts/publish.py` gates releases with).

## Usage

```bash
# Validate the whole plugin (advisory mode: exit 0/1/2/3 by worst severity)
uvx --from git+https://github.com/Emasoft/claude-plugins-validation \
    --with pyyaml cpv-remote-validate plugin <PLUGIN_DIR>

# Strict mode (the publish gate): ANY CRITICAL/MAJOR/MINOR/NIT fails
uvx --from git+https://github.com/Emasoft/claude-plugins-validation \
    --with pyyaml cpv-remote-validate plugin <PLUGIN_DIR> --strict

# Lint-only pass (markdownlint / ruff / mypy / yamllint / toml)
uvx --from git+https://github.com/Emasoft/claude-plugins-validation \
    --with pyyaml cpv-remote-validate lint <PLUGIN_DIR>
```

## What This Command Does

1. **Validates Plugin Structure** — manifest (`.claude-plugin/plugin.json`),
   directory layout, version consistency.
2. **Validates Skills** — SKILL.md frontmatter (name, description), reference
   documents resolve, progressive-disclosure structure, description budgets.
3. **Validates Agents, Commands and Hooks** — frontmatter fields,
   `allowed-tools` values, hook configuration and script references.
4. **Reports Results** — findings by severity (CRITICAL / MAJOR / MINOR /
   NIT / WARNING) with file:line locations.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `PLUGIN_DIR` | Yes | Path to the plugin directory (use `.` for current directory) |
| `--strict` | No | Publish-gate mode: any CRITICAL/MAJOR/MINOR/NIT finding fails (exit non-zero) |

## Exit Codes

| Exit | Meaning |
|------|---------|
| 0 | All checks passed (WARNINGs are advisory) |
| 1 | CRITICAL issues found |
| 2 | MAJOR issues found |
| 3 | MINOR issues found (advisory unless `--strict`) |
| 4 | NIT issues found (advisory unless `--strict`) |

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| `uvx: command not found` | uv not installed | Install uv: https://docs.astral.sh/uv/ |
| Network failure fetching CPV | GitHub unreachable | Retry; validation fails closed (never validate with a stale local copy) |
| Findings reported | Plugin issues | Fix the plugin per the report. Never suppress or exempt a finding — devitalize or remove the offending content |

## Notes

- The remote validator is the single source of truth — this plugin deliberately
  ships **zero** local validator scripts so rules can never drift.
- False positives and validator bugs are reported upstream as issues on
  `Emasoft/claude-plugins-validation`, not worked around locally.
- Zero tolerance at publish time: `scripts/publish.py` runs this same validator
  with `--strict` and refuses to push on any non-zero exit.

## Related Commands

- `/amcos-configure-plugins` - Configure plugins for an agent
- `/amcos-reindex-skills` - Trigger PSS reindex after skill changes
- `/amcos-staff-status` - Check staff and orchestration status
