---
name: amcos-resource-monitoring-ref
description: Use when consulting detailed resource monitoring references. Trigger with resource monitoring lookups.
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

## Examples

See referenced files for step-by-step examples.

## Resources

- [system-resources](references/system-resources.md) — Topics: System Resources Reference, Table of Contents, 1.1 Types Of System Resources, CPU, Memory, Disk, Network, 1.2 Monitoring CPU Usage, Basic CPU Check, macOS: Get CPU usage percentage, Linux: Get CPU usage, Load Average Check, Get 1, 5, 15 minute load averages, Parse individual values, CPU-Intensive Process Detection, Find top CPU consumers, Find processes using more than 50% CPU, CPU Health Assessment, CPU Health Levels, 1.3 Monitoring Memory, Basic Memory Check, macOS: Get memory statistics, Calculate free memory in MB (macOS), Linux: Get memory info, Memory Percentage Calculation, macOS, Linux, Per-Process Memory, Top memory consumers, Memory used by Claude Code processes, Memory Health Assessment, Memory Health Levels, 1.4 Monitoring Disk Space, Basic Disk Check, Check disk space on all mounted filesystems, Check specific mount point, Get free space in GB, Disk Usage Percentage, Get usage percentage, Large File Detection, Find files larger than 100MB, Find large log files, Inode Usage, Check inode usage (many small files can exhaust inodes), Disk Health Assessment, Disk Health Levels, 1.5 Monitoring Network, Connectivity Check, Check internet connectivity, Check AI Maestro connectivity, Use the ai-maestro-agents-management skill to verify AI Maestro health status, Check DNS resolution, Latency Check, Measure latency to key endpoints, AI Maestro latency, Use the ai-maestro-agents-management skill to check AI Maestro response time, Port Availability, Check if key ports are listening, Network Health Assessment, Network Health Levels, 1.6 Resource Thresholds, Recommended Thresholds, Threshold Configuration, design/memory/resource-thresholds.md, Resource Thresholds, CPU, Memory, Disk, Network (latency), Dynamic Threshold Adjustment, 1.7 System Resource Examples, Example: Complete Resource Check Script, !/bin/bash, check-resources.sh, CPU, Memory, Disk, Network, Use the ai-maestro-agents-management skill to check AI Maestro health, Example: Resource Alert Generation, !/bin/bash, generate-resource-alert.sh, Resource Alert, Recommended Actions, 1.8 Troubleshooting, Issue: Resource commands not working, Issue: Memory metrics seem incorrect, Issue: Disk space not freed after deletion, Issue: Network checks pass but communication fails
- [instance-limits](references/instance-limits.md) — Topics: Instance Limits Reference, Table of Contents, 2.1 Types Of Instance Limits, Session Limits, API Rate Limits, Concurrency Limits, Message Queue Limits, 2.2 Counting Active Sessions, Query AI Maestro Registry, Session Categorization, Session Count History, design/memory/session-history.md, Session Count History, 2.3 Tracking API Rate Limits, Anthropic API Limits, Anthropic API Usage, AI Maestro Throughput, Rate Limit Headers, Example: Check GitHub rate limit using gh CLI, Example output:, {"limit":5000,"remaining":4987,"reset":1706780400}, Rate Limit Tracking File, design/memory/rate-limits.md, Rate Limit Status, Anthropic API, GitHub API, AI Maestro, 2.4 Managing Concurrency, Tool Execution Concurrency, Git Concurrency Rule, Git Concurrency Rule, File Write Concurrency, File Write Rules, Concurrency Tracking, design/memory/concurrency-status.md, Active Operations, Queued Operations, 2.5 Making Scaling Decisions, When to Scale Up, When to Scale Down, Capacity Assessment, Capacity Assessment, Scaling Decision Matrix, 2.6 Instance Limit Examples, Example: Pre-Spawn Resource Check, Example: Rate Limit Monitoring, Example: Scaling Decision Log, Scaling Decision Log, 2025-02-01T10:00:00Z - Scale Up, 2025-02-01T16:00:00Z - Scale Down, 2.7 Troubleshooting, Issue: Session count exceeds expected limit, Issue: Rate limits being hit frequently, Issue: Git operations deadlock, Issue: Cannot spawn new agents despite available resources
