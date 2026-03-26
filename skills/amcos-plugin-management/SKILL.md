---
name: amcos-plugin-management
description: Use when installing, configuring, or validating Claude Code plugins. Trigger with plugin management requests.
user-invocable: false
license: Apache-2.0
compatibility: Requires Claude Code CLI, plugin directories, and AI Maestro.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff - Plugin Management Skill

## Overview

Install, configure, and maintain Claude Code plugins. Covers marketplace install, local directories, validation, and remote agent plugins.

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

Copy this checklist and track your progress:

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

See [plugin-installation](references/plugin-installation.md) — Topics: Plugin Installation Reference, Table of Contents, 1.2 Installation prerequisites

### PROCEDURE 2: Configure Local Plugin Directory

**When/Steps:** Create directory structure, add plugin.json, configure components, launch with --plugin-dir.

See [local-configuration](references/local-configuration.md) — Topics: Local Configuration Reference, Table of Contents, 2.2 Directory structure

### PROCEDURE 3: Validate Plugin Installation

**When/Steps:** Run validate command, check errors, verify components, test hooks.

See [plugin-validation](references/plugin-validation.md) — Topics: Plugin Validation Reference, Table of Contents, 3.2 Validation levels

### PROCEDURE 4: Manage Plugins on Remote Agents

**When/Steps:** Use `ai-maestro-agents-management` skill or GovernanceRequest pipeline for cross-host operations.

See [remote-plugin-management](references/remote-plugin-management.md) — Topics: Remote Plugin Management, Table of Contents, 1. Overview

## Examples

**Input:** "Install plugin grepika on agent libs-svg-svgbbox and validate"

**Output:**
```
1. Installed grepika v1.2.0 from marketplace
2. Validation: manifest OK, hooks OK, MCP tools OK
3. Agent libs-svg-svgbbox restarted with plugin active
[DONE] Plugin grepika installed and validated on libs-svg-svgbbox.
```

See [plugin-overview-and-examples](references/plugin-overview-and-examples.md) — Topics: Plugin Management - Overview, Examples, and Reference, Table of Contents, Plugin Lifecycle

## Error Handling

| Issue | Resolution |
|-------|------------|
| Install fails | [plugin-installation](references/plugin-installation.md) — Topics: Plugin Installation Reference, Table of Contents, 1.2 Installation prerequisites
| Plugin not loading | [local-configuration](references/local-configuration.md) — Topics: Local Configuration Reference, Table of Contents, 2.2 Directory structure
| Validation errors | [plugin-validation](references/plugin-validation.md) — Topics: Plugin Validation Reference, Table of Contents, 3.2 Validation levels

## Resources

- [plugin-installation](references/plugin-installation.md) — Topics: Plugin Installation Reference, Table of Contents, 1.2 Installation prerequisites

