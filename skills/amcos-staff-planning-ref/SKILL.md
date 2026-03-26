---
name: amcos-staff-planning-ref
description: Use when consulting detailed staff planning references. Trigger with staff planning lookups.
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

## Examples

See referenced files for step-by-step examples.

## Resources

- [staffing-templates](references/staffing-templates.md) — Topics: Staffing Templates Reference, Table of Contents, 3.1 What are staffing templates, 3.2 Template structure, 3.2.1 Metadata section, 3.2.2 Roles section, 3.2.3 Assignments section, 3.2.4 Constraints section, 3.3 Built-in templates, 3.3.1 Project bootstrap template, 3.3.2 Feature development template, 3.3.3 Bug triage template, 3.3.4 Release preparation template, 3.4 Creating custom templates, 3.5 Template validation, Use the CPV plugin validator for template validation, 3.6 Examples, Example: Applying Feature Development Template, Load template, Customize for specific feature, Apply template, Output, Spawning code-implementer-01 as developer, Spawning code-implementer-02 as developer, Spawning test-engineer-01 as tester, Assignments created: 6 tasks across 3 agents, 3.7 Troubleshooting, Issue: Template roles not matching available agents, Issue: Dependency cycle in assignments, Issue: Template too rigid for project
- [capacity-planning](references/capacity-planning.md) — Topics: Capacity Planning Reference, Table of Contents, 2.1 What is capacity planning, 2.2 Capacity metrics, 2.2.1 Context window utilization, 2.2.2 Concurrent execution limits, 2.2.3 Blocking operation impact, 2.3 Capacity planning procedure, 2.3.1 Agent inventory, Agent Inventory, 2.3.2 Task estimation, 2.3.3 Allocation calculation, 2.3.4 Bottleneck identification, Bottlenecks Identified, 2.4 Load balancing strategies, Strategy 1: Round-Robin, Strategy 2: Least-Loaded, Strategy 3: Affinity-Based, Strategy 4: Priority-Based, 2.5 Scaling decisions, When to scale up (add agents), When to scale down (remove agents), Scaling procedure, 2.6 Examples, Example: Sprint Planning, 2.7 Troubleshooting, Issue: Agents constantly at capacity, Issue: Agents mostly idle, Issue: Single agent is bottleneck
- [role-assessment](references/role-assessment.md) — Topics: Role Assessment Reference, Table of Contents, 1.1 What is role assessment, 1.2 When to perform assessment, 1.3 Assessment procedure, 1.3.1 Capability extraction, 1.3.2 Agent type mapping, 1.3.3 Gap analysis, 1.3.4 Priority ordering, 1.4 Assessment output format, Role Assessment: [Project Name], Required Capabilities, Agent Type Mapping, Gap Analysis, Staffing Recommendation, Notes, 1.5 Validation checklist, 1.6 Examples, Example: Web Application Feature, 1.7 Troubleshooting, Issue: Cannot determine required capabilities, Issue: Multiple agents match same capability, Issue: Critical capability has no matching agent
