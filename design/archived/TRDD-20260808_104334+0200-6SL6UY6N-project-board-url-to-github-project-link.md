---
trdd-id: 6SL6UY6N
title: Wire project_board_url through to githubProject instead of dropping it
column: completed
created: 2026-08-08T10:43:34+0200
updated: 2026-08-19T10:05:00+0200
current-owner: ai-maestro-chief-of-staff
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: feature
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: chief-of-staff
min-approval-requirement: none
relevant-rules: [1]
external-refs: [ai-maestro#133, ai-maestro#76]
implementation-commits: [5b5718a]
---

# Wire `project_board_url` through to `githubProject` instead of dropping it

This is the **COS half (Half 1)** of ai-maestro#133. Authored as a self-mandate: the work is
inside this plugin's own assignment scope, so it is Tier-0 under the `aimaestro-trdd-approval`
overlay and needs no external approval to enter the pipeline. CORE confirmed that routing
(2026-08-08) rather than me assuming it.

## The current behaviour, and why it is not simply a bug

`scripts/amcos_team_registry.py` accepts a `project_board_url` and then **drops it**, because
`aimaestro-teams.sh create` exposes no `--gh-project` flag. It is honest about the drop rather
than silent — there is a marker at the call site and a stderr warning telling the operator the
team is being created without the board. So a caller who supplies a board URL gets a team with no
board **and a warning**, not a silent failure.

That is worth preserving as the failure mode. When this lands, the replacement must not become
quieter than what it replaces.

## What the server side now supports (Half 2, LANDED — reachability stated)

CORE landed the server half as commit `21be3e96` on `ai-maestro@governance-rules`. **It is PUSHED
and fetchable** on `fork/governance-rules` — re-verified 2026-08-08 10:45.

An earlier revision of this card said "local-only, on no remote". That was **true when measured**
(~02:00) and became false without anyone editing the card: the reflog shows
`fork/governance-rules` was pushed six times later the same morning — 08:03, then 10:15, 10:22,
10:23, 10:40, 10:44. Worth recording rather than quietly overwriting, because the two failure
modes look identical in a document and need opposite remedies: **a stale PROBE** (checked against
refs you never refreshed) is fixed by fetching first, while **a correct probe whose FACT later
moved** is fixed only by timestamping the claim. This card carried the second. Reachability is a
property with a clock on it, so any claim about it that omits when it was taken will eventually be
wrong on its own.

Its content, verified by reading the commit rather than relayed:

- `GitHubProjectLink.repo` becomes `repo?: string`; all three team-route zod schemas accept a
  repo-less `githubProject`.
- Reads never needed the repo — the board resolves via `organization()`/`user()` GraphQL — so a
  repo-less link yields a fully live **browse-only** kanban.
- Task CRUD refuses on a repo-less link **before any mutation**, with a named reason.
- CORE also deleted a UI defect that fabricated `repo = owner`.

## The contract this half must implement

**Parse to `{owner, number}` with `repo` ABSENT — never `repo: owner`.** The fabrication CORE
removed is exactly the shortcut this parser would be tempted into, since it makes an org URL fit
the old required-repo shape. It produces a link that looks valid and points at a repo-scoped
board that does not exist.

| URL shape | Parse to | Board capability |
|---|---|---|
| `github.com/<owner>/<repo>/projects/<n>` | `{owner, repo, number}` | full (task CRUD) |
| `github.com/orgs/<owner>/projects/<n>` | `{owner, number}` | browse-only |
| `github.com/users/<owner>/projects/<n>` | `{owner, number}` | browse-only |

## Sequencing — the constraint that makes this NOT ready to start

**TWO conditions gate this card. The first is now MET; the second is not.**

**(1) Half 2 deployed — MET, verified 2026-08-08 10:53.** Not taken on report: `/api/v1/health`
and `/` both 200, and the live bundle `.next/server/chunks/9792.js` greps positive for Half 2's
production literal ("the board is browse-only"), with 456 JS files built after 10:00. Committed,
pushed, and deployed are three claims; all three are now true and each was measured.

**(2) The frozen CLI can express a board number — NOW MET (ai-maestro#137 fixed + deployed).**
Verified 2026-08-08 11:40 **through the bare command name**, not a repo-relative path: `command -v
aimaestro-teams.sh` → `~/.local/bin/aimaestro-teams.sh`, which now carries 15 `gh-number`
occurrences and the contract `--gh-owner O --gh-number N [--gh-repo R]`, validates the number as a
positive integer pre-`jq`, and emits `{owner, number: ($ghn | tonumber)}` plus `repo` only when
given. That check matters here specifically: CORE found the PATH copy was stale at Aug 5 with zero
`gh-number` while the repo copy was already fixed — a repo-relative verification would have passed
against a binary my calls never reach.

The original text of condition (2) follows, kept because the mistake is the lesson. This card's original
trigger named only condition (1), and that was an incomplete gate — recorded here rather than
silently widened, because the mistake is instructive. The COS path does not talk to the server; it
talks to `aimaestro-teams.sh`, which talks to the server. A server that can represent a board is
useless to this card while the CLI cannot express one, so "the dependency deployed" was never the
right question. **The right question is whether the dependency is reachable ALONG MY OWN CALL
PATH.**

The CLI advertises `--gh-owner O --gh-repo R  attach a GitHub project` but emits
`{githubProject: {owner, repo}}` with no `number`, while `CreateTeamSchema` requires `number` and
is `.strict()` — so every use of those flags is rejected. Pre-dates Half 2 (`number` was already
required in `21be3e96^`). Filed as ai-maestro#137.

Two bugs were masking each other: this repo declined to use the flags because it believed they did
not exist, and therefore never discovered that they also do not work. A workaround that avoids a
path is also a workaround that stops testing it.

Promote to `todo` only when BOTH hold. Until then an org-level URL keeps producing the current
recognized-but-unsupported message.

## Acceptance criteria

- [x] A repo-scoped board URL round-trips to `{owner, repo, number}` and reaches the create call.
- [x] An org/user-level URL parses to `{owner, number}` with `repo` **absent** — asserted
      explicitly, since a test that only checks `owner`/`number` passes while `repo: owner` is
      fabricated alongside them.
- [x] ~~Before Half 2 deploys, an org URL is reported as recognized-but-unsupported~~ — **moot**,
      Half 2 deployed 10:51. An org URL is now a first-class browse-only link.
- [x] A malformed URL fails loudly. No silent drop, no fabricated field.
- [x] The existing stderr warning is not made quieter by the replacement — it got **louder**: the
      no-board branch now says the repo is not recorded at all, which the old code never disclosed.

## Implementation

`scripts/amcos_team_registry.py`: `_parse_project_board_url()` + a rewritten `create_team()` argv
build. `tests/test_project_board_url.py`: 17 tests, suite 262 → 279, ruff clean.

**A bug caught in review, worth recording because the tests now pin it.** The first draft tested
the repo-scoped shape FIRST. But `orgs/<owner>/projects/<n>` is *also* four segments with
`projects` at index 2, so it matched that branch and parsed as `owner="orgs"`,
`repo=<the real owner>` — a link that validates and points nowhere. Ordering is load-bearing and
now carries a comment saying so. Falsified: restoring the wrong order reddens exactly the four org
tests, including both `repo is None` assertions.

**One design call worth stating.** `githubProject` is built ONLY from the board URL. `repo_url` is
parsed for validation but deliberately not folded in as a fallback repo — supplying a repo the
board URL never named would silently promote a browse-only org board to CRUD-capable, which is the
same fabrication ai-maestro#133 removed from the server UI. A consequence: with no board URL, the
team records no repo at all, because the server carries `repo` only inside `githubProject`. That
is now said out loud on stderr rather than silently attached-and-rejected.

**Pre-existing breakage this exposes:** the old path sent `{owner, repo}` with no `number` on
EVERY call, which the server has rejected since `de060a50`. So `create_team` could not have
succeeded with a repo URL. Verified by reading the schema and the old CLI, not by execution —
this session cannot execute it (401, see below).

## Remaining before `complete`

**2026-08-19: the e2e is now DELEGATED, not merely described.** Asked the hub session to have a
REGISTERED COS agent run the round-trip (one repo-scoped URL → `{owner, repo, number}` CRUD link;
one org URL → `{owner, number}` browse-only), since only a registered agent holds an AID and
borrowing one is forbidden. On PASS this card closes complete; on FAIL the payload comes back
here at `dev`. Until the reply, `testing` means "delegated verification pending", not local work.

Live end-to-end against a real server, which this session **cannot** do: `aimaestro-teams.sh`
returns `401 auth_required` here because this is a plugin-development session, not a registered
COS agent with an AID (R32 — the AID is the authorization). The pure parse and the argv build are
unit-tested; the round-trip belongs to a running agent. Card sits in `testing`, not `complete`,
for exactly that gap — marking it complete would claim a verification nobody has performed.

## Not in scope

Making `repo` optional server-side (CORE's task #33), and anything requiring a live agent AID —
`aimaestro-teams.sh` returns `401 auth_required` from a plugin-development session, which is R32
working correctly, not an obstacle.

## Notes

- The `--gh-project` flag on `aimaestro-teams.sh create` is tracked in the COS residual list
  ai-maestro#76; the DECOUPLE-BLOCKED markers in this repo point there since `ae04e20`.
- **Operational caveats from the live e2e (hub, 2026-08-19)**, kept because a future caller of
  `aimaestro-teams.sh create` will hit all three: (a) the CreateTeam pipeline takes ~2 min
  (auto-COS spawn) and the board linkage persists LAST — an early read of teams.json shows
  `githubProject: null` and is not a failure; (b) slow verbs print
  `Error: request to /api/teams failed (network)` exit 1 while SUCCEEDING server-side (CLI
  `curl --max-time 30` < pipeline) — false-failure + duplicate-on-retry hazard, hub card
  TRDD-ARY3NRFC; (c) `common.sh` `local -n` dies under macOS default bash 3.2 — the CLI needs
  homebrew bash first on PATH (also folded into ARY3NRFC).

## Approval log

- 2026-08-19T10:05:00+0200 — COMPLETED by ai-maestro-chief-of-staff (tier 0, own-scope
  self-mandate). Live round-trip executed by the hub session via the owner harness path
  (aim_session + one-shot sudo tokens; no agent identity borrowed): repo-scoped URL persisted
  `{"owner":"Emasoft","repo":"ai-maestro","number":7}`; org-level persisted
  `{"owner":"Emasoft","number":5}` with the repo key ABSENT (browse-only per 21be3e96),
  verified on two independent creates + one PUT update, read from ~/.aimaestro/teams/teams.json.
  Verdict PASS relayed 2026-08-19; unit half was already green (17 tests, 5b5718a).
- Verb surface to implement against: `scripts/build-script-manifest.mjs` on
  `ai-maestro@governance-rules` (tip `1ccbe9e0` at time of writing, fetchable).
