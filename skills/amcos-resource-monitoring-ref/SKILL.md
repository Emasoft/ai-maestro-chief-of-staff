---
name: amcos-resource-monitoring-ref
description: Use when consulting detailed resource monitoring references. Trigger with resource monitoring lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Resource Monitoring Reference

## Overview

Reference material for resource monitoring. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-resource-monitoring` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-resource-monitoring` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Check CPU and memory usage before spawning agents"

```bash
cat references/system-resources.md | head -60
```

**Expected result:** Resource monitoring commands for CPU, memory, disk, network with health assessment thresholds.

## Resources

- [system-resources](references/system-resources.md) — CPU, memory, disk, network monitoring, thresholds, health assessment, examples
- [instance-limits](references/instance-limits.md) — Session limits, API rate limits, concurrency, scaling decisions, examples
