# Staff Planning - Overview, Examples, and Reference

## Table of Contents
- What Is Staff Planning
- Staff Planning Components
- Role Assessment Details
- Capacity Planning Details
- Staffing Templates Details
- Examples: Role Assessment for Feature Development
- Examples: Capacity Planning
- Key Takeaways
- Task Checklist

## What Is Staff Planning

Staff planning is the process of determining which agents are needed, when they are needed, and how they should be allocated across projects and tasks. Unlike simple task assignment, staff planning considers:

- **Agent capabilities**: What each agent type can do
- **Workload patterns**: When agents are busy vs available
- **Project dependencies**: Which tasks must complete before others can start
- **Resource constraints**: Context limits, API quotas, concurrent execution limits

## Staff Planning Components

### 1. Role Assessment

Evaluating what agent roles are required for a project or task set:
- Identifying required capabilities (coding, testing, documentation, etc.)
- Matching capabilities to available agent types
- Determining specialization depth needed
- Assessing multi-role requirements

### 2. Capacity Planning

Determining how much work agents can handle:
- Estimating task durations
- Calculating parallel execution limits
- Planning for context window constraints
- Scheduling around blocking operations

### 3. Staffing Templates

Reusable configurations for common scenarios:
- Project bootstrap templates
- Feature development templates
- Bug triage templates
- Release preparation templates

## Role Assessment Details

Role assessment involves:
1. Extracting capability requirements from project/task descriptions
2. Mapping capabilities to known agent types
3. Performing gap analysis for missing capabilities
4. Prioritizing requirements by importance and urgency

## Capacity Planning Details

Capacity planning involves:
1. Creating an inventory of available agents and their current load
2. Estimating task requirements (duration, complexity, dependencies)
3. Calculating optimal task-to-agent allocation
4. Identifying bottlenecks (single-instance agents, blocking tasks)
5. Recommending mitigations (scaling, reordering, role merging)

## Staffing Templates Details

Templates contain:
- **Metadata**: Template name, scenario type, version
- **Roles**: Required agent types with counts
- **Assignments**: Default task-to-agent mappings
- **Constraints**: Scheduling limitations, dependencies

Built-in templates: project bootstrap, feature development, bug triage, release preparation.

## Examples: Role Assessment for Feature Development

```markdown
## Role Assessment: User Authentication Feature

### Required Capabilities
1. Python backend development
2. API design and implementation
3. Security best practices
4. Unit test creation
5. Integration test creation
6. Documentation writing

### Agent Type Mapping
| Capability | Agent Type | Priority |
|------------|------------|----------|
| Backend development | code-implementer | HIGH |
| API design | architect-agent | HIGH |
| Security practices | security-reviewer | MEDIUM |
| Unit tests | test-engineer | HIGH |
| Integration tests | test-engineer | MEDIUM |
| Documentation | doc-writer | LOW |

### Gap Analysis
- No security-reviewer agent available
- Mitigation: code-implementer will follow security checklist
```

## Examples: Capacity Planning

```markdown
## Capacity Plan: Sprint 42

### Available Agents
- code-implementer: 2 instances
- test-engineer: 1 instance
- doc-writer: 1 instance

### Task Allocation
| Task | Agent | Duration | Parallel |
|------|-------|----------|----------|
| Auth module | code-impl-1 | 4h | Yes |
| User profile | code-impl-2 | 3h | Yes |
| Auth tests | test-eng | 2h | After auth |
| API docs | doc-writer | 1h | After auth |

### Bottleneck
- test-engineer is single instance
- All test tasks must serialize through it
```

## Key Takeaways

1. **Role assessment precedes staffing** - Know what you need before allocating
2. **Capacity planning prevents overload** - Plan around constraints
3. **Templates accelerate setup** - Reuse proven patterns
4. **Gaps require mitigation** - Document workarounds for missing roles
5. **Bottlenecks need attention** - Single-instance agents create serialization

## Task Checklist

- [ ] Understand staff planning purpose and components
- [ ] Learn PROCEDURE 1: Assess role requirements
- [ ] Learn PROCEDURE 2: Plan agent capacity
- [ ] Learn PROCEDURE 3: Create staffing templates
- [ ] Practice role assessment for a sample project
- [ ] Practice capacity planning with constraints
- [ ] Create a custom staffing template
- [ ] Validate templates work correctly
