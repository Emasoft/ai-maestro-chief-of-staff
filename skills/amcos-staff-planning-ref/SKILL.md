---
name: amcos-staff-planning-ref
description: Use when consulting detailed staff planning references. Trigger with staff planning lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Staff Planning Reference

## Overview

Reference material for staff planning. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-staff-planning` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-staff-planning` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Plan capacity for a sprint with 3 agents"

```bash
cat references/capacity-planning.md | head -50
```

**Expected result:** Capacity metrics, agent inventory, task estimation, allocation calculation, and bottleneck identification.

## Resources

- [staffing-templates](references/staffing-templates.md) — Template structure, built-in templates, custom templates, validation, examples
  - 3.1 What are staffing templates - Reusable staffing configurations
  - 3.2 Template structure - Standard template format
    - 3.2.1 Metadata section - Template identification
    - 3.2.2 Roles section - Required agent types
    - 3.2.3 Assignments section - Default agent allocations
    - 3.2.4 Constraints section - Scheduling limitations
  - 3.3 Built-in templates - Standard templates included
    - 3.3.1 Project bootstrap template - New project setup
    - 3.3.2 Feature development template - Feature implementation
    - 3.3.3 Bug triage template - Issue investigation
    - 3.3.4 Release preparation template - Release workflow
  - 3.4 Creating custom templates - Building new templates
  - 3.5 Template validation - Ensuring template correctness
  - 3.6 Examples - Template usage scenarios
  - 3.7 Troubleshooting - Template issues
- [capacity-planning](references/capacity-planning.md) — Capacity metrics, load balancing strategies, scaling decisions, examples
  - 2.1 What is capacity planning - Understanding capacity constraints
  - 2.2 Capacity metrics - Measuring agent capacity
    - 2.2.1 Context window utilization - Token budget tracking
    - 2.2.2 Concurrent execution limits - Parallel task boundaries
    - 2.2.3 Blocking operation impact - Synchronous wait times
  - 2.3 Capacity planning procedure - Step-by-step planning
    - 2.3.1 Agent inventory - Listing available agents
    - 2.3.2 Task estimation - Sizing work items
    - 2.3.3 Allocation calculation - Assigning agents to tasks
    - 2.3.4 Bottleneck identification - Finding constraints
  - 2.4 Load balancing strategies - Distributing work evenly
  - 2.5 Scaling decisions - When to add more agents
  - 2.6 Examples - Capacity planning scenarios
  - 2.7 Troubleshooting - Capacity planning issues
- [role-assessment](references/role-assessment.md) — Assessment procedure, capability extraction, gap analysis, examples
  - 1.1 What is role assessment - Understanding role requirements analysis
  - 1.2 When to perform assessment - Triggers for role evaluation
  - 1.3 Assessment procedure - Step-by-step role analysis
    - 1.3.1 Capability extraction - Identifying required skills
    - 1.3.2 Agent type mapping - Matching skills to agent types
    - 1.3.3 Gap analysis - Finding missing capabilities
    - 1.3.4 Priority ordering - Ranking requirements by importance
  - 1.4 Assessment output format - Structured assessment results
  - 1.5 Validation checklist - Verifying assessment completeness
  - 1.6 Examples - Role assessment scenarios
  - 1.7 Troubleshooting - Common assessment issues
