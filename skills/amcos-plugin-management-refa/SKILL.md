---
name: amcos-plugin-management-refa
description: Use when consulting detailed plugin management references. Trigger with plugin management lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Plugin Management Reference

## Overview

Reference material for plugin management. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-plugin-management` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-plugin-management` for error handling.

## Examples

See referenced files for step-by-step examples.

## Resources

- [plugin-installation](references/plugin-installation.md) — Topics: Plugin Installation Reference, Table of Contents, 1.1 What is plugin installation, 1.2 Installation prerequisites, 1.2.1 Marketplace registration, Add a marketplace, List registered marketplaces, Update marketplace cache, 1.2.2 Plugin discovery, List plugins in marketplace, Search for specific plugin, 1.2.3 Version selection, Install latest version (default), Install specific version, 1.3 Installation procedure, 1.3.1 Marketplace check, Check marketplace exists, If not found, add it, 1.3.2 Plugin availability, Search for plugin, Should return plugin info, 1.3.3 Install command, Install with default scope (user), Install to specific scope, 1.3.4 Restart requirement, Exit Claude Code, Relaunch Claude Code, Or from within Claude Code, Then relaunch, 1.3.5 Verification, List installed plugins, Check for specific plugin, Test a plugin command (if applicable), 1.4 Installation scopes, 1.5 Updating plugins, Update to latest version, Step 1: Update marketplace cache, Step 2: Uninstall current version, Step 3: Reinstall (gets latest), Step 4: RESTART Claude Code, Clean update (if issues), Clear plugin cache, Reinstall, RESTART Claude Code, 1.6 Uninstalling plugins, Uninstall plugin, Verify removed, Should return empty, RESTART Claude Code, 1.7 Examples, Example 1: First-time Installation, Complete installation flow, 1. Add marketplace, 2. Install plugin, 3. Verify, 4. EXIT and RELAUNCH Claude Code, 5. Test plugin, Example 2: Install for Project Team, Install with project scope (shared via git), In project directory, Commit settings, Team members: pull and restart Claude Code, Example 3: Local Development Plugin, Use --plugin-dir for local plugins (no install needed), Multiple local plugins, 1.8 Troubleshooting, Issue: Marketplace not found, Issue: Plugin install fails, Issue: Plugin not working after install, Issue: Hook path version mismatch, Issue: Duplicate hooks error
- [plugin-validation](references/plugin-validation.md) — Topics: Plugin Validation Reference, Table of Contents, 3.1 What is plugin validation, 3.2 Validation levels, 3.2.1 Manifest validation, 3.2.2 Component validation, 3.2.3 Hook validation, 3.2.4 Path validation, 3.3 Validation procedure, 3.3.1 CLI validation, Validate installed plugin, Validate local plugin directory, 3.3.2 Script validation, Using plugin's internal validator, With verbose output, Output as JSON, 3.3.3 Manual inspection, Verify plugin.json, Verify hooks.json, Check command frontmatter, Verify scripts executable, 3.4 Common validation errors, 3.4.1 Manifest errors, 3.4.2 Path errors, 3.4.3 Hook errors, 3.4.4 Permission errors, 3.5 Fixing validation errors, General fix procedure, Manifest fixes, Validate JSON syntax, If parse error, use JSON linter, Or recreate file carefully, Hook fixes, Validate hooks.json syntax, Check all referenced scripts exist, Permission fixes, Make all scripts executable, 3.6 Examples, Example 1: Full Validation Run, Example 2: Validation with Errors, Example 3: Skill Validation, Validate skills with skills-ref, Validate each skill, 3.7 Troubleshooting, Issue: Validation command not found, Issue: False positive errors, Issue: Validation hangs, Issue: Different results between validators
