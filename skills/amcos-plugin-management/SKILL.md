---
name: amcos-plugin-management
description: Use when installing, configuring, or validating Claude Code plugins. Trigger with plugin install, update, or validation requests.
user-invocable: false
license: Apache-2.0
compatibility: Requires access to Claude Code CLI, plugin directories, and understanding of plugin manifest format and hooks configuration. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff - Plugin Management Skill

## Overview

Plugin management enables the Chief of Staff to install, configure, and maintain Claude Code plugins across projects. Covers marketplace installation, local plugin directories, validation, and remote agent plugin management.

## Prerequisites

1. Plugin validation scripts are available
2. Plugin directories are accessible
3. Agent restart capability is available

## Instructions

1. Identify plugin operation needed (install, update, validate)
2. Execute the operation
3. Verify plugin integrity
4. Restart affected agents if needed

### Checklist

- [ ] Plugin operation type confirmed (install/update/validate/remove)
- [ ] Plugin manifest (plugin.json) validated
- [ ] Plugin hooks and components verified functional
- [ ] Affected agents restarted and confirmed operational

## Output

| Operation | Output |
|-----------|--------|
| Install | Plugin installed, agents restarted |
| Update | Plugin updated, version logged |
| Validate | Validation report generated |

## Core Procedures

### PROCEDURE 1: Install Plugin from Marketplace

**When/Steps:** Check marketplace, verify plugin, run install, restart Claude Code, verify.

See `references/plugin-installation.md` and `references/op-install-plugin-marketplace.md`.

### PROCEDURE 2: Configure Local Plugin Directory

**When/Steps:** Create directory structure, add plugin.json, configure components, launch with --plugin-dir.

See `references/local-configuration.md` and `references/op-configure-local-plugin.md`.

### PROCEDURE 3: Validate Plugin Installation

**When/Steps:** Run validate command, check errors, verify components, test hooks.

See `references/plugin-validation.md` and `references/op-validate-plugin.md`.

### PROCEDURE 4: Manage Plugins on Remote Agents

**When/Steps:** Use `ai-maestro-agents-management` skill or GovernanceRequest pipeline for cross-host operations.

See `references/remote-plugin-management.md` and `references/op-install-plugin-remote.md`.

## Examples

**Input:** "Install plugin grepika on agent libs-svg-svgbbox and validate"

**Output:**
```
1. Installed grepika v1.2.0 from marketplace
2. Validation: manifest OK, hooks OK, MCP tools OK
3. Agent libs-svg-svgbbox restarted with plugin active
[DONE] Plugin grepika installed and validated on libs-svg-svgbbox.
```

See `references/plugin-overview-and-examples.md` for full examples including marketplace install, local development, directory structure, validation, and remote agent operations.
- Plugin Lifecycle
- What Is Plugin Management
- Plugin Components
- Examples: Installing from Marketplace
- Examples: Local Plugin Development
- Examples: Plugin Directory Structure
- Examples: Plugin Validation
- Examples: Install Plugin on Remote Agent
- Examples: Restart Agent After Plugin Changes
- Remote Plugin Operations Table
- Key Takeaways
- Task Checklist

## Error Handling

| Issue | Resolution |
|-------|------------|
| Plugin install fails | See `references/plugin-installation.md` Section 1.8 |
| Local plugin not loading | See `references/local-configuration.md` Section 2.7 |
| Validation errors | See `references/plugin-validation.md` Section 3.7 |

## Resources

- `references/plugin-installation.md`
- `references/local-configuration.md`
- `references/plugin-validation.md`
- `references/remote-plugin-management.md`
- `references/installation-procedures.md`
- `references/plugin-overview-and-examples.md`
- `references/op-install-plugin-marketplace.md`
- `references/op-configure-local-plugin.md`
- `references/op-install-plugin-remote.md`
- `references/op-restart-agent-plugin.md`
- `references/op-validate-plugin.md`

---

**Version:** 1.0
**Last Updated:** 2025-02-01
