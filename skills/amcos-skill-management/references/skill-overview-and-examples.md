# Skill Management - Overview, Examples, and Reference

## Table of Contents
- What Is Skill Management
- Skill Architecture Diagram
- Skill Components
- Examples: Validating a Skill
- Examples: SKILL.md Frontmatter
- Examples: Triggering PSS Reindex
- Examples: Generating Agent Prompt XML
- Key Takeaways
- Task Checklist

## What Is Skill Management

Skill management is the administration of agent skills that provide specialized knowledge and procedures. It includes:

- **Validation**: Ensuring skills conform to the Agent Skills specification
- **Reindexing**: Updating the skill index for PSS discovery
- **PSS Integration**: Configuring skills for AI-analyzed keyword matching

## Skill Architecture Diagram

```
+-----------------------------------------------------------+
|                    SKILL DIRECTORY                          |
|  +-----------------------------------------------------+  |
|  |  SKILL.md                                            |  |
|  |  - YAML frontmatter (name, description, etc.)       |  |
|  |  - Procedures with TOC                              |  |
|  |  - References links                                 |  |
|  +-----------------------------------------------------+  |
|  +-----------------------------------------------------+  |
|  |  references/                                         |  |
|  |  - Detailed procedure documentation                 |  |
|  |  - Each file has own TOC                            |  |
|  +-----------------------------------------------------+  |
|  +-----------------------------------------------------+  |
|  |  scripts/   (optional)                              |  |
|  |  - Automation helpers                               |  |
|  +-----------------------------------------------------+  |
+-----------------------------------------------------------+
                           |
                           v
+-----------------------------------------------------------+
|              PERFECT SKILL SUGGESTER                       |
|  +-----------------------------------------------------+  |
|  |  Skill Index                                         |  |
|  |  - Keywords extracted from skills                   |  |
|  |  - Co-usage relationships                           |  |
|  |  - Weighted scoring for activation                  |  |
|  +-----------------------------------------------------+  |
+-----------------------------------------------------------+
```

## Skill Components

A skill directory contains:
- **SKILL.md**: Main file with YAML frontmatter, procedures, and reference links
- **references/**: Detailed procedure documentation with individual TOCs
- **scripts/**: Optional automation helpers

## Examples: Validating a Skill

```bash
# Install skills-ref if not present
pip install skills-ref

# Validate a skill directory
skills-ref validate /path/to/my-skill

# Expected output for valid skill
# Skill: my-skill
# Status: VALID
# Warnings: 0
# Errors: 0

# Read skill properties
skills-ref read-properties /path/to/my-skill
```

## Examples: SKILL.md Frontmatter

```yaml
---
name: amcos-staff-planning
description: Use when analyzing staffing needs, assessing role requirements, planning agent capacity, or creating staffing templates for multi-agent orchestration
license: Apache-2.0
compatibility: Requires access to agent registry, project configuration files, and understanding of agent capabilities and workload patterns.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
---
```

## Examples: Triggering PSS Reindex

```bash
# Using PSS slash command
/pss-reindex-skills

# Or via script
python scripts/pss_reindex_skills.py --skills-dir /path/to/skills

# Verify index updated
cat ~/.claude/skills-index.json | jq '.skills | length'
```

## Examples: Generating Agent Prompt XML

```bash
# Generate available_skills XML for agent prompts
skills-ref to-prompt /path/to/skill-a /path/to/skill-b

# Output
# <available_skills>
# <skill>
# <name>skill-a</name>
# <description>What skill-a does</description>
# <location>/path/to/skill-a/SKILL.md</location>
# </skill>
# ...
# </available_skills>
```

## Key Takeaways

1. **Validate before publish** - Catch errors early with skills-ref
2. **Reindex after changes** - PSS needs fresh index to discover updates
3. **Description is key** - PSS extracts keywords from description
4. **Use natural language** - Keywords should appear naturally in content
5. **Test discovery** - Verify skills activate for expected queries

## Task Checklist

- [ ] Understand skill architecture and PSS integration
- [ ] Learn PROCEDURE 1: Validate skill structure
- [ ] Learn PROCEDURE 2: Reindex skills for PSS
- [ ] Learn PROCEDURE 3: Configure PSS integration
- [ ] Practice validating a skill with skills-ref
- [ ] Practice triggering a skill reindex
- [ ] Practice optimizing a skill for PSS discovery
- [ ] Verify skill appears in PSS suggestions
