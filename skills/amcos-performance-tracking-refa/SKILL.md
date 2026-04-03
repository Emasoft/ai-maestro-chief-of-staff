---
name: amcos-performance-tracking-refa
description: Use when consulting detailed performance tracking references. Trigger with performance tracking lookups. Loaded by ai-maestro-chief-of-staff-main-agent
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

**Input:** "Generate a weekly performance report for the team"

```bash
cat references/performance-reporting.md | head -60
```

**Expected result:** Report template with daily/weekly formats, distribution matrix, and actionable recommendations.

## Resources

- [performance-reporting](references/performance-reporting.md) — Report types, templates, daily/weekly summaries, individual reports, distribution, examples
- [strength-weakness-analysis](references/strength-weakness-analysis.md) — Analysis framework, benchmarks, pattern detection, recommendations, examples
