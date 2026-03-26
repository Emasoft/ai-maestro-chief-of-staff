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

### PROCEDURE 2: Configure Local Plugin Directory

**When/Steps:** Create directory structure, add plugin.json, configure components, launch with --plugin-dir.

### PROCEDURE 3: Validate Plugin Installation

**When/Steps:** Run validate command, check errors, verify components, test hooks.

### PROCEDURE 4: Manage Plugins on Remote Agents

**When/Steps:** Use `ai-maestro-agents-management` skill or GovernanceRequest pipeline for cross-host operations.

See [remote-plugin-management](references/remote-plugin-management.md) — Topics: Remote Plugin Management, Table of Contents, 1. Overview, 2. Remote Installation, 2.1 Installation Procedure, 2.2 Installation Message Format, 3. Remote Updates, 3.1 Update Procedure, 3.2 Update Message Format, 4. Troubleshooting, 4.1 Installation Fails, 4.2 Update Fails

## Examples

**Input:** "Install plugin grepika on agent libs-svg-svgbbox and validate"

**Output:**
```
1. Installed grepika v1.2.0 from marketplace
2. Validation: manifest OK, hooks OK, MCP tools OK
3. Agent libs-svg-svgbbox restarted with plugin active
[DONE] Plugin grepika installed and validated on libs-svg-svgbbox.
```

See [plugin-overview-and-examples](references/plugin-overview-and-examples.md) — Topics: Plugin Management - Overview, Examples, and Reference, Table of Contents, Plugin Lifecycle, What Is Plugin Management, Plugin Components, Examples: Installing from Marketplace, Step 1: Add marketplace (first time only), Step 2: Install plugin, Step 3: Verify installation, Step 4: RESTART Claude Code (required!), Exit and relaunch claude, Examples: Local Plugin Development, Launch Claude Code with local plugin, Launch with multiple local plugins, Examples: Plugin Directory Structure, Examples: Plugin Validation, Validate plugin structure, Check hooks registration, Debug plugin loading, Examples: Install Plugin on Remote Agent, Examples: Restart Agent After Plugin Changes, Remote Plugin Operations Table, Key Takeaways, Task Checklist

## Error Handling

| Issue | Resolution |
|-------|------------|

## Resources

