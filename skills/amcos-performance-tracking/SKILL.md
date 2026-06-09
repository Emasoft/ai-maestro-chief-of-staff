---
name: amcos-performance-tracking
description: Use when tracking team performance or generating reports. Trigger with metrics collection or performance analysis requests. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro (agent metrics, session memory, reporting).
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff Performance Tracking Skill

## Overview

Track agent team performance, identify strengths/weaknesses, and make data-driven decisions about team composition and task assignment.

## Prerequisites

1. Agent metrics are being collected
2. Performance baselines are established
3. Reporting templates are available

## Instructions

1. Identify performance metrics needed
2. Query agent activity logs
3. Calculate performance indicators
4. Generate performance report

### Checklist

Copy this checklist and track your progress:

- [ ] Metrics category identified (completion, quality, efficiency, communication)
- [ ] Agent activity logs queried for target time period
- [ ] Performance indicators calculated and compared to baselines
- [ ] Report generated and saved to `.amcos-logs/`

## Output

| Metric Type | Output |
|-------------|--------|
| Task completion | Completion rate, average time |
| Resource usage | Memory, CPU, API calls |
| Quality metrics | Error rate, rework rate |

## Core Procedures

### PROCEDURE 1: Collect Performance Metrics

### PROCEDURE 2: Analyze Strengths and Weaknesses

### PROCEDURE 3: Generate Performance Reports

## Operational Procedures

- [op-collect-performance-metrics](references/op-collect-performance-metrics.md) — Metric collection steps, templates, aggregation, validation
  - [Purpose](#purpose)
  - [When To Use This Operation](#when-to-use-this-operation)
  - [Metric Categories](#metric-categories)
  - [Steps](#steps)
    - [Step 1: Define Metrics to Track](#step-1-define-metrics-to-track)
  - [Agent Metrics Template](#agent-metrics-template)
    - [Task Metrics](#task-metrics)
    - [Quality Metrics](#quality-metrics)
    - [Efficiency Metrics](#efficiency-metrics)
    - [Communication Metrics](#communication-metrics)
    - [Step 2: Capture Data at Task Completion](#step-2-capture-data-at-task-completion)
    - [Step 3: Aggregate Over Time Periods](#step-3-aggregate-over-time-periods)
    - [Step 4: Validate Data Quality](#step-4-validate-data-quality)
  - [Data Quality Check](#data-quality-check)
    - [Step 5: Store Metrics](#step-5-store-metrics)
  - [Checklist](#checklist)
  - [Metric Collection Automation](#metric-collection-automation)
  - [Output](#output)
  - [Related References](#related-references)
  - [Next Operation](#next-operation)

## Examples

**Input:** "Generate weekly performance report for agent libs-svg-svgbbox"

**Output:**
```
libs-svg-svgbbox weekly report (Mar 1-7):
  Tasks completed: 12/14 (86%)  Avg time: 25min
  Error rate: 7%  Rework: 1 task
  Strength: Fast SVG parsing  Weakness: Error handling coverage
[DONE] Report saved to .amcos-logs/perf-libs-svg-svgbbox-2026-03-07.md
```

See examples-and-checklists in Resources for more examples.

## Error Handling

| Issue | Solution |
|-------|----------|
| Metrics incomplete | Automate collection, validate, backfill from logs |
| Unfair comparison | Normalize by complexity, compare similar tasks |
| Reports not actionable | Add action items, assign owners, track follow-up |

## Resources

- [examples-and-checklists](references/examples-and-checklists.md) — Performance tracking examples and task checklists
  - Task Checklist
  - Example 1: Recording Task Completion Metric
  - Example 2: Agent Strength-Weakness Summary
  - Example 3: Weekly Performance Summary
