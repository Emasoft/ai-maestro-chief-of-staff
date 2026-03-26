---
name: amcos-staff-planning
description: Use when analyzing staffing needs, assessing role requirements, planning agent capacity, or creating staffing templates for multi-agent orchestration. Trigger with team sizing or staffing requests.
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

See [role-assessment](references/role-assessment.md) — Topics: Role Assessment Reference, Table of Contents, 1.2 When to perform assessment

### PROCEDURE 2: Plan Agent Capacity

**When/Steps:** Inventory agents, estimate task requirements, calculate allocation, identify bottlenecks.

See [capacity-planning](references/capacity-planning.md) — Topics: Capacity Planning Reference, Table of Contents, 2.2 Capacity metrics

### PROCEDURE 3: Create Staffing Templates

**When/Steps:** Identify scenario, list roles, define assignments, document template.

See [staffing-templates](references/staffing-templates.md) — Topics: Staffing Templates Reference, Table of Contents, 3.2 Template structure

## Examples

**Input:** "Plan staffing for a 3-service microservices migration project"

**Output:** "Recommended: 2 backend agents (Rust), 1 DevOps agent, 1 QA agent. Total: 4 agents. Bottleneck: DevOps (single point). Consider adding 1 backup DevOps agent."

See [staffing-overview-and-examples](references/staffing-overview-and-examples.md) — Topics: Staff Planning - Overview, Examples, and Reference, Table of Contents, What Is Staff Planning

## Error Handling

| Issue | Resolution |
|-------|------------|
| Not enough agents for roles | See [role-assessment](references/role-assessment.md) — Topics: Role Assessment Reference, Table of Contents, 1.2 When to perform assessment
| Agent capacity exceeded | See [capacity-planning](references/capacity-planning.md) — Topics: Capacity Planning Reference, Table of Contents, 2.2 Capacity metrics
| Template does not fit | See [staffing-templates](references/staffing-templates.md) — Topics: Staffing Templates Reference, Table of Contents, 3.2 Template structure

## Resources

- [role-assessment](references/role-assessment.md) — Topics: Role Assessment Reference, Table of Contents, 1.2 When to perform assessment

---

**Version:** 1.0
**Last Updated:** 2025-02-01
