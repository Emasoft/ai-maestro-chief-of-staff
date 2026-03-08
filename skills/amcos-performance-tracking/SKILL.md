---
name: amcos-performance-tracking
description: Use when tracking team performance, analyzing agent strengths and weaknesses, collecting metrics, and generating performance reports. Trigger with performance review or metrics requests.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro for agent metrics, session memory for historical data, and reporting capabilities. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff Performance Tracking Skill

## Overview

Performance tracking enables the Chief of Staff to understand how well the agent team is performing, identify individual strengths and weaknesses, and make data-driven decisions about team composition and task assignment.

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

Continuously capture data at relevant events and aggregate over time periods. See `references/performance-metrics.md`.
  - [Categories Of Performance Metrics](#11-categories-of-performance-metrics)
  - [Task Completion Metrics](#12-task-completion-metrics)
  - [Quality Metrics](#13-quality-metrics)
  - [Efficiency Metrics](#14-efficiency-metrics)
  - [Communication Metrics](#15-communication-metrics)

### PROCEDURE 2: Analyze Strengths and Weaknesses

Review metrics, identify patterns, compare against benchmarks. See `references/strength-weakness-analysis.md`.
  - [Performance Analysis Framework](#21-performance-analysis-framework)
  - [Identifying Agent Strengths](#22-identifying-agent-strengths)
  - [Identifying Agent Weaknesses](#23-identifying-agent-weaknesses)
  - [Comparing Against Benchmarks](#24-comparing-against-benchmarks)
  - [Recognizing Performance Patterns](#25-recognizing-performance-patterns)

### PROCEDURE 3: Generate Performance Reports

Aggregate metrics, format for audience, include analysis. See `references/performance-reporting.md`.
  - [Types Of Performance Reports](#31-types-of-performance-reports)
  - [Structuring Performance Reports](#32-structuring-performance-reports)
  - [Daily Performance Summaries](#33-daily-performance-summaries)
  - [Weekly Performance Reviews](#34-weekly-performance-reviews)
  - [Individual Agent Reports](#35-individual-agent-reports)

## Operational Procedures

- `references/op-collect-performance-metrics.md` - Runbook for collecting metrics
- `references/op-analyze-strengths-weaknesses.md` - Runbook for analyzing performance
- `references/op-generate-performance-report.md` - Runbook for creating reports

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

See `references/examples-and-checklists.md` for full examples and task checklist.
  - [Task Checklist](#task-checklist)
  - [Example 1: Recording Task Completion Metric](#example-1-recording-task-completion-metric)
  - [Example 2: Agent Strength-Weakness Summary](#example-2-agent-strength-weakness-summary)
  - [Example 3: Weekly Performance Summary](#example-3-weekly-performance-summary)

## Error Handling

| Issue | Solution |
|-------|----------|
| Metrics data incomplete | Automate collection, add validation, backfill from logs |
| Unfair comparison | Normalize by task complexity, compare similar task types |
| Reports not driving improvements | Include action items, assign owners, track completion |

## Resources

- `references/performance-metrics.md`
- `references/strength-weakness-analysis.md`
- `references/performance-reporting.md`
- `references/report-formats.md`
- `references/examples-and-checklists.md`

---

**Version:** 1.0
**Last Updated:** 2025-02-01
