---
name: amcos-staff-planning
description: Use when analyzing staffing needs, assessing role requirements, planning agent capacity, or creating staffing templates for multi-agent orchestration. Trigger with team sizing or staffing requests. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires access to agent registry, project configuration files, and understanding of agent capabilities and workload patterns. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff - Staff Planning Skill

## Overview

Staff planning analyzes project requirements, assesses agent capabilities, plans capacity allocation, and creates staffing templates for efficient multi-agent orchestration.

## Prerequisites

1. Task requirements are defined
2. Available agent pool is known
3. Resource limits are understood

## Instructions

1. Analyze task requirements
2. Determine required agent count and types
3. Check resource availability
4. Recommend team composition

### Checklist

Copy this checklist and track your progress:

- [ ] List all tasks and required skill types
- [ ] Map tasks to available agent capabilities
- [ ] Verify resource limits are not exceeded
- [ ] Document recommended team composition

## Output

| Analysis Type | Output |
|---------------|--------|
| Task analysis | Required skills, estimated effort |
| Team sizing | Recommended agent count by role |
| Resource check | Availability vs requirements |

## Core Procedures

### PROCEDURE 1: Assess Role Requirements

**When/Steps:** Analyze requirements, list capabilities, map to agent types, identify gaps.

### PROCEDURE 2: Plan Agent Capacity

**When/Steps:** Inventory agents, estimate task requirements, calculate allocation, identify bottlenecks.

### PROCEDURE 3: Create Staffing Templates

**When/Steps:** Identify scenario, list roles, define assignments, document template.

## Examples

**Input:** "Plan staffing for a 3-service microservices migration project"

```
Role Assessment: Microservices Migration
Required: 2x backend (Rust), 1x DevOps, 1x QA
Total: 4 agents | Bottleneck: DevOps (single point)
Recommendation: Add 1 backup DevOps agent
```

**Expected result:** Staffing plan with role mapping, capacity check, and bottleneck analysis.

## Error Handling

| Issue | Resolution |
|-------|------------|

## Resources

---

**Version:** 1.0
**Last Updated:** 2025-02-01
