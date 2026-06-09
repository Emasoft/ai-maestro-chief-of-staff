---
name: amcos-plugin-management-refa
description: Use when consulting detailed plugin management references. Trigger with plugin management lookups. Loaded by ai-maestro-chief-of-staff-main-agent
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

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Install a plugin from marketplace and validate it"

```bash
cat references/plugin-installation.md | head -60
```

**Expected result:** Step-by-step install procedure with marketplace check, install command, restart, and verification.

## Resources

- [plugin-installation](references/plugin-installation.md) — Installation prerequisites, procedure, scopes, updating, uninstalling, examples, troubleshooting
  - 1.1 What is plugin installation - Understanding plugin deployment
  - 1.2 Installation prerequisites - Requirements before install
    - 1.2.1 Marketplace registration - Adding marketplaces
    - 1.2.2 Plugin discovery - Finding available plugins
    - 1.2.3 Version selection - Choosing plugin version
  - 1.3 Installation procedure - Step-by-step installation
    - 1.3.1 Marketplace check - Verifying marketplace active
    - 1.3.2 Plugin availability - Confirming plugin exists
    - 1.3.3 Install command - Running installation
    - 1.3.4 Restart requirement - Restarting Claude Code
    - 1.3.5 Verification - Confirming installation success
  - 1.4 Installation scopes - User, project, local, managed
  - 1.5 Updating plugins - Upgrading to new versions
  - 1.6 Uninstalling plugins - Removing plugins
  - 1.7 Examples - Installation scenarios
  - 1.8 Troubleshooting - Installation issues
- [plugin-validation](references/plugin-validation.md) — Validation levels, CLI/script validation, common errors, fixes, examples, troubleshooting
  - 3.1 What is plugin validation - Checking plugin correctness
  - 3.2 Validation levels - What gets checked
    - 3.2.1 Manifest validation - plugin.json structure
    - 3.2.2 Component validation - commands, agents, skills
    - 3.2.3 Hook validation - hooks.json and scripts
    - 3.2.4 Path validation - File references
  - 3.3 Validation procedure - Running validation
    - 3.3.1 CLI validation - claude plugin validate
    - 3.3.2 Script validation - Using validation scripts
    - 3.3.3 Manual inspection - Checking files directly
  - 3.4 Common validation errors - Frequent issues
    - 3.4.1 Manifest errors - Missing fields, wrong types
    - 3.4.2 Path errors - Broken references
    - 3.4.3 Hook errors - Invalid hook configuration
    - 3.4.4 Permission errors - Script not executable
  - 3.5 Fixing validation errors - Resolution procedures
  - 3.6 Examples - Validation scenarios
  - 3.7 Troubleshooting - Validation issues
