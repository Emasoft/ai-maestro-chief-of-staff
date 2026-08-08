---
trdd-id: 6SL6UY6N
title: Wire project_board_url through to githubProject instead of dropping it
column: backburner
created: 2026-08-08T10:43:34+0200
updated: 2026-08-08T10:43:34+0200
current-owner: ai-maestro-chief-of-staff
task-type: feature
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: self
min-approval-requirement: 0
relevant-rules: [1]
external-refs: [ai-maestro#133, ai-maestro#76]
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

CORE landed the server half as commit `21be3e96` on `ai-maestro@governance-rules`. **That commit
is LOCAL-ONLY — it is on no remote** (verified with `git branch -r --contains`), so it is not
auditable off this host and must not be cited elsewhere as established. Its content, verified by
reading it rather than relayed:

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

**Half 2 is committed but NOT DEPLOYED** (routes are bundled; `yarn build` deliberately deferred).
The running server still enforces the old required-repo schema. So until deploy, an org-level URL
must keep producing the current recognized-but-unsupported message.

This is why the card opens in `backburner` rather than `todo`: starting now would mean writing a
parser whose org-URL branch cannot be exercised end-to-end, and the temptation would be to ship it
untested behind a flag. The trigger to move it to `todo` is **Half 2 deployed**, not Half 2
committed — the distinction that cost the fleet a night to learn.

## Acceptance criteria

- [ ] A repo-scoped board URL round-trips to `{owner, repo, number}` and reaches the create call.
- [ ] An org/user-level URL parses to `{owner, number}` with `repo` **absent** — asserted
      explicitly, since a test that only checks `owner`/`number` passes while `repo: owner` is
      fabricated alongside them.
- [ ] Before Half 2 deploys, an org URL is reported as recognized-but-unsupported — **not** a
      parse failure, so the message stays actionable.
- [ ] A malformed URL fails loudly. No silent drop, no fabricated field.
- [ ] The existing stderr warning is not made quieter by the replacement.

## Not in scope

Making `repo` optional server-side (CORE's task #33), and anything requiring a live agent AID —
`aimaestro-teams.sh` returns `401 auth_required` from a plugin-development session, which is R32
working correctly, not an obstacle.

## Notes

- The `--gh-project` flag on `aimaestro-teams.sh create` is tracked in the COS residual list
  ai-maestro#76; the DECOUPLE-BLOCKED markers in this repo point there since `ae04e20`.
- Verb surface to implement against: `scripts/build-script-manifest.mjs` on
  `ai-maestro@governance-rules` (tip `1ccbe9e0` at time of writing, fetchable).
