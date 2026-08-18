---
trdd-id: NB725X9W
title: Absorb the multi-agent coordination methodology into the COS persona
column: complete
created: 2026-08-08T12:53:04+0200
updated: 2026-08-08T15:05:51+0200
current-owner: ai-maestro-chief-of-staff
task-type: docs
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: ai-maestro-hub-work-order
min-approval-requirement: none
external-refs: [ai-maestro#136]
---

# Absorb the multi-agent coordination methodology into the COS persona

Tier-0 self-card against the hub's work order (USER-commissioned: *"learn what works best and
worse, write down the optimal methodology, then improve the MANAGER/COS/ORCHESTRATOR plugins with
it"*). Source: `design/methodology/multi-agent-coordination-methodology.md` @
`ai-maestro@governance-rules` commit `cfd568b8` — **pushed**, read directly, not relayed
(measured 2026-08-08 12:53:04 +0200).

## Why this card exists at all

The practices below were *lived* on 2026-08-08 by this session. That is exactly why they are at
risk: **a lesson held only in a transcript dies with the context window.** The next COS session
inherits the persona, not the day. So the deliverable is not a summary of what happened — it is the
smallest set of instructions that reproduces the behaviour without the story.

## Assigned sections, and what is ALREADY covered

The work order names §2, §4, §5, §11 for COS. Checked the persona before writing, so the absorption
adds rather than duplicates:

| § | Practice | State before this card |
|---|---|---|
| §2 | Corrections both ways, verified both ways | **ABSENT** — 1 incidental hit. The real gap. |
| §4 | Questions outrank confidence | **PARTIAL** — the posture exists, the *discipline* does not |
| §5 | Refusal names defect / bar / re-propose path | **ALREADY LANDED** — `5daeca4` (COS#28), 6 hits |
| §11 | Honest columns | **PARTIAL** — columns documented; the trigger refinement missing |

So this card writes §2 and §4 in full, sharpens §11 with the one refinement the day produced, and
leaves §5 alone. Re-stating §5 would have been the easy way to look thorough while adding nothing.

## The §11 refinement worth more than the section

Gate a card on **"is the dependency reachable along MY OWN call path"**, not "is the dependency
deployed". This session recorded "Half 2 deployed" as a promotion trigger, watched it come true,
and *still* could not start — because the COS path reaches the server through a frozen CLI that
could not express the field. A server capability is useless to a consumer whose call path cannot
carry it.

## Acceptance criteria

- [x] §2 present as an instruction the next session can follow with no knowledge of today.
- [x] §4 present, including the RECEIVING half (a question about your code is a work item; answer
      with file:line, never recollection).
- [x] §11 refinement present, stated as the call-path gate.
- [x] §5 NOT restated.
- [x] The menu guard (relay below) is scoped to the menu SECTION, falsified both directions.

## The relay found a LIVE defect here, not a hypothetical

AUTONOMOUS's warning was not preventive for this repo — the gap already existed. **6 of 23 skills
were missing from the persona's `## Skill References` menu**: `amcos-acknowledgment-protocol`,
`amcos-failure-notification`, `amcos-label-taxonomy`, `amcos-onboarding`, `amcos-prrd-trdd-kanban`,
`amcos-team-coordination`.

And the whole-file guard would have passed over every one of them, for the precise reason the relay
gave: all six appear at lines 21-26 — **the frontmatter `skills:` preload list**. A file-wide search
finds a "mention" of every skill by construction, so the menu can rot indefinitely underneath a
green check. Measured: 23 on disk, 23 findable file-wide, 17 in the menu.

The failure mode is quiet by nature. A skill absent from the menu still LOADS, so nothing breaks —
the agent simply never learns it exists and stops routing to it. A capability going unused looks
identical to a capability nobody needed.

Fixed (6 menu lines added) and guarded by two tests: `test_every_skill_appears_in_the_persona_menu`
scoped to the section, plus `test_skill_menu_scope_is_narrower_than_the_file` — because if the
section parse ever degenerates to the whole file, the first check passes while asserting nothing.
Falsified BOTH directions: removing one skill from the menu while leaving it in frontmatter fires
the first guard naming it; widening the scope fires the second with the char counts.

## Closure record

- **Release:** v2.24.0
- **Tip sha:** `109f5f7` (`chore(release): v2.24.0`) on `origin/main` — pushed, re-fetched and read
  at `2026-08-08 15:05:51 +0200` (pasted)
- **Measured:** `2026-08-08 15:02:05 +0200` — pasted from `date`, not composed (§1; the anti-pattern
  that recurred today despite a written lesson)
- **Suite:** 293 tests green (was 291); ruff clean

## Folded-in relay from AUTONOMOUS

An RP-SKILL-MENU-01 guard that matches skill names against the WHOLE persona **passes while the
menu silently loses an entry** — a passing prose mention anywhere in an 865-line file satisfies it.
Scope the check to the menu section and falsify both directions.

This is the *vacuous-pass* family again, third variant this session: the first was a parametrized
check that asserts nothing when its list empties; the second a scan whose file census could return
zero; this one a check whose SEARCH SPACE is wider than the invariant it guards. All three are
green while measuring the wrong thing — which is why the falsification step is not optional
ceremony.

