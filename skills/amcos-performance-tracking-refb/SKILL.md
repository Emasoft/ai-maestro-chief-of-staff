---
name: amcos-performance-tracking-refb
description: Use when consulting detailed performance tracking references. Trigger with performance tracking lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Performance Tracking Reference

## Overview

Reference material for performance tracking. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-performance-tracking` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-performance-tracking` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "What metrics should I track for agent task completion?"

```bash
cat references/performance-metrics.md | head -50
```

**Expected result:** Metric categories (completion, quality, efficiency, communication) with collection and storage procedures.

## Resources

- [performance-metrics](references/performance-metrics.md) — Metric categories, collection procedures, data storage, trend analysis, examples, troubleshooting
