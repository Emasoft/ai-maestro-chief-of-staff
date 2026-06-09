---
name: amcos-failure-notification-refb
description: Use when consulting detailed failure notification references. Trigger with failure notification lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Failure Notification Reference

## Overview

Reference material for failure notification. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-failure-notification` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-failure-notification` for error handling.

## Examples

```bash
# Look up design document validation procedures
cat references/design-document-protocol.md | grep -A5 "Pre-Save Validation"
```

Expected: required validation steps before saving design documents.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the failure notification topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [design-document-protocol](references/design-document-protocol.md) — Design document protocol: GUUID format, frontmatter schema, lifecycle, validation, search, GitHub integration
  1. [Document UUID Format (GUUID)](#1-document-uuid-format-guuid)
  2. [Required Frontmatter Schema](#2-required-frontmatter-schema)
  3. [Document Lifecycle](#3-document-lifecycle)
  4. [Validation Procedures](#4-validation-procedures)
     - 4.1 [Pre-Save Validation (REQUIRED)](#41-pre-save-validation-required)
     - 4.2 [Post-Save Validation (REQUIRED)](#42-post-save-validation-required)
     - 4.3 [Validation Script Usage](#43-validation-script-usage)
  5. [Search Procedures](#5-search-procedures)
     - 5.1 [Search by UUID](#51-search-by-uuid)
     - 5.2 [Search by Type](#52-search-by-type)
     - 5.3 [Search by Status](#53-search-by-status)
     - 5.4 [Search by Keyword](#54-search-by-keyword)
     - 5.5 [Combined Search](#55-combined-search)
  6. [GitHub Integration](#6-github-integration)
     - 6.1 [Creating GitHub Issue from Design Document](#61-creating-github-issue-from-design-document)
     - 6.2 [Syncing Status](#62-syncing-status)
     - 6.3 [Linking Existing Issue](#63-linking-existing-issue)
  7. [Edge Cases and Error Handling](#7-edge-cases-and-error-handling)
     - 7.1 [Duplicate UUID](#71-duplicate-uuid)
     - 7.2 [Malformed Frontmatter](#72-malformed-frontmatter)
     - 7.3 [Missing Required Fields](#73-missing-required-fields)
     - 7.4 [Invalid Status Transition](#74-invalid-status-transition)
     - 7.5 [GitHub CLI Not Available](#75-github-cli-not-available)
     - 7.6 [Empty Search Results](#76-empty-search-results)
     - 7.7 [Design Folder Not Initialized](#77-design-folder-not-initialized)
  8. [File Naming Convention](#8-file-naming-convention)
  9. [Cross-Plugin Protocol](#9-cross-plugin-protocol)
  10. [Quick Reference](#10-quick-reference)
      - 10.1 [Create Document](#create-document)
      - 10.2 [Search Documents](#search-documents)
      - 10.3 [Validate Document](#validate-document)
