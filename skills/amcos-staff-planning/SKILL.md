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
agent: amcos-chief-of-staff-main-agent
workflow-instruction: "Steps 2, 3"
procedure: "proc-evaluate-project, proc-negotiate-team"
---

# AI Maestro Chief of Staff - Staff Planning Skill

## Overview

Staff planning analyzes project requirements, assesses agent capabilities, plans capacity allocation, and creates staffing templates for efficient multi-agent orchestration.

## Prerequisites

1. Task requirements are defined
2. Available agent pool is known
3. Resource limits are understood

## Instructions

> **Output Rule**: All AMCOS scripts produce 2-line stdout summaries. Full output is written to `.amcos-logs/`.

1. Analyze task requirements
2. Determine required agent count and types
3. Check resource availability
4. Recommend team composition

## Output

| Analysis Type | Output |
|---------------|--------|
| Task analysis | Required skills, estimated effort |
| Team sizing | Recommended agent count by role |
| Resource check | Availability vs requirements |

## Core Procedures

### PROCEDURE 1: Assess Role Requirements

**When/Steps:** Analyze requirements, list capabilities, map to agent types, identify gaps.

See [references/role-assessment.md](references/role-assessment.md) and [references/op-assess-role-requirements.md](references/op-assess-role-requirements.md).

### PROCEDURE 2: Plan Agent Capacity

**When/Steps:** Inventory agents, estimate task requirements, calculate allocation, identify bottlenecks.

See [references/capacity-planning.md](references/capacity-planning.md) and [references/op-plan-agent-capacity.md](references/op-plan-agent-capacity.md).

### PROCEDURE 3: Create Staffing Templates

**When/Steps:** Identify scenario, list roles, define assignments, document template.

See [references/staffing-templates.md](references/staffing-templates.md) and [references/op-create-staffing-templates.md](references/op-create-staffing-templates.md).

## Examples

See [references/staffing-overview-and-examples.md](references/staffing-overview-and-examples.md) for full examples including role assessment, capacity planning, and template usage.
- What Is Staff Planning
- Staff Planning Components
- Role Assessment Details
- Capacity Planning Details
- Staffing Templates Details
- Examples: Role Assessment for Feature Development
- Examples: Capacity Planning
- Key Takeaways
- Task Checklist

## Error Handling

| Issue | Resolution |
|-------|------------|
| Not enough agents for roles | See [role-assessment.md](references/role-assessment.md) Section 1.7 |
| Agent capacity exceeded | See [capacity-planning.md](references/capacity-planning.md) Section 2.7 |
| Template does not fit | See [staffing-templates.md](references/staffing-templates.md) Section 3.7 |

## Resources

- [Role Assessment](references/role-assessment.md)
- [Capacity Planning](references/capacity-planning.md)
- [Staffing Templates](references/staffing-templates.md)
- [Framework Details](references/framework-details.md)
- [Overview and Examples](references/staffing-overview-and-examples.md)
- [Op: Assess Role Requirements](references/op-assess-role-requirements.md)
- [Op: Plan Agent Capacity](references/op-plan-agent-capacity.md)
- [Op: Create Staffing Templates](references/op-create-staffing-templates.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
