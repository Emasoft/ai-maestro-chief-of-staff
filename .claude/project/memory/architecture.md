---
name: architecture
description: "how does ai-maestro-chief-of-staff work — overview, the main parts (main agent + sub-agents, skills, commands, hooks, rules), where the PRRD/TRDDs and the publish pipeline live"
ocd: 2026-06-14
lmd: 2026-06-14
metadata:
  node_type: memory
  type: project
  tier: hub
  functionality: architecture
  globs: ["agents/**", "skills/**", "commands/**", "hooks/**", "rules/**", "scripts/**"]
---
ai-maestro-chief-of-staff (AMCOS) is a Claude Code plugin in the AI Maestro fleet.
It implements the CHIEF-OF-STAFF (COS) role: per R6 v3 the COS is the sole entry
point into a team — it routes team-internal proposals up to the MANAGER, relays
AMP messages, and owns the ORCHESTRATOR-side dialog loops. It is distributed via
the `Emasoft/ai-maestro-plugins` marketplace (Layout A hub) and depends on
`ai-maestro-plugin` (which ships the 3-pillars scripts: PRRD, TRDD, kanban).

## Parts map
- (add component/aspect pages here as they're created — e.g. the main agent +
  sub-agent roster, the amcos-* skills, the strict publish pipeline
  `scripts/publish.py`, the 3-pillars governance under `design/`)

## Applies to
- (radiates down to the component/aspect pages of this functionality — empty until
  the first one is written; wire the reciprocal `## Governed by` on each)

## See also
- (lateral links to other functionality hubs, once they exist)

## Notes and lessons learned
