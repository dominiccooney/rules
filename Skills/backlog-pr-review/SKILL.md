---
name: backlog-pr-review
description: Triage a pull-request backlog methodically, decide whether to close or advance each PR, and write concise, respectful reviewer communication. Use for backlog sweeps and closure-message drafting. Defers implementation correctness to engineering review skills.
---

# Backlog PR Review

Review PRs in stages so cheap disposition decisions happen before detailed
engineering review. This skill owns **triage, disposition, and communication**.
It does not duplicate software-engineering rules: when a live, aligned PR needs
implementation analysis, invoke the appropriate planning or inventory-review
skill instead.

The goal of a sweep is to change each PR's state. A PR you touch should end
closed, merged, or one concrete step closer to merging — and when that step is
safe to take yourself (rebase, regenerate artifacts, re-run tests), take it
rather than requesting it. Analysis that ends in a recommendation with no state
change is an incomplete sweep item. Improving this skill is a byproduct of
sweeps, never the deliverable.

Each sweep item follows the same sequence: triage through the gates, record the
evidence and disposition, act on the disposition, then communicate. Later steps
draw only on the record built by earlier ones.

## Stepped triage

Stop at the first decisive gate:

1. **Legitimacy and safety:** Is this a genuine contribution rather than spam,
   phishing, or meaningless churn?
2. **Present relevance:** Is the problem already fixed, the proposal duplicated,
   the feature removed, or the changed path superseded on current `main`? This
   comes second because it is the cheapest decisive gate: there is no point
   weighing purpose, direction, or engineering on work that is already shipped.
3. **Purpose and hygiene:** Is the intended outcome focused and understandable?
   Is there enough issue/reproduction/context to evaluate it? Scale hygiene
   expectations with scope.
4. **Product direction:** If it worked exactly as described, would Cline want
   the behavior? For unapproved cross-product policy or architecture, redirect
   to discussion rather than reviewing a large implementation.
5. **Engineering review:** If the PR survives, hand it to existing engineering
   rules and review skills. Do not recreate their caller, contract, concurrency,
   UI, or testing checks here.

Common dispositions are: close as duplicate, superseded, already implemented,
obsolete, or out of direction; request a split or prior design discussion; or
advance to engineering review. A useful sub-change in an otherwise rejected PR
is a lead to verify independently, not a reason to keep the PR open.

## Evidence record

For each PR, keep a record of the decisive gate, the disposition, and the
evidence: the commands run against current `main` (`git show`, `git grep`, a
checkout of `origin/main`) and their relevant output. The PR's own description,
diff, age, and CI results are claims to test against `main`, not evidence about
`main`. A gate answered only from PR-local context is not answered, and a
disposition without a filled record is not decided.

The record is what makes the rest of the sweep safe: the action and the
message must cite it, batches can be reviewed from it, and a mistaken closure
can be traced through it.

## Probing relevance

A cheap probe: `git grep` on `main` for the symbols, paths, and mechanisms the
PR touches. A rebase attempt is the next probe up, but read its result
carefully. A clean rebase proves textual compatibility, not relevance; the
problem may already be solved another way. A failed rebase proves nothing on
its own — what matters is *why* it failed:

- **Adjacent-line noise:** the surrounding code shifted but the PR's target
  still exists. Textual churn, not a relevance signal. Resolve and move on.
- **The target is gone or replaced:** the list, function, or mechanism the PR
  modifies no longer exists on `main`. A strong supersession signal. Find what
  replaced it, and record it, before resolving anything.

When a PR adds an entry to a hand-maintained list (providers, commands, tools,
model catalogs), check whether that list still exists on `main`. The PR is
superseded when the mechanism itself was replaced by generation or data-driven
registration — even when no one added the PR's specific item by hand. A large
regenerated artifact in the diff (a generated catalog, lockfile, or snapshot)
is a hint that generation may now be the system, not just an output.

## Closure messages

Use the shortest message that states:

1. the disposition,
2. the decisive evidence from the record (usually a replacement PR or removed
   path), and
3. a path to disagree when the conclusion could be mistaken.

Match detail to the relationship. Close collaborators with shared context
usually benefit from a direct sentence or two.

For **external or new contributors**, add one or two sentences that:

- thank them for the contribution;
- apologize for a slow response when no Cline member responded for an extended
  period — check the thread first, and do not imply the contributor caused the
  delay;
- welcome future contributions, even when this PR cannot move forward.

Treat GitHub `FIRST_TIME_CONTRIBUTOR` and `NONE` as external by default. Use
contribution history and shared context to recognize regular contributors;
`CONTRIBUTOR` alone is not conclusive.

Example for an external contributor after a long wait:

> #12345 implemented this in the current SDK path, so I’m closing this as
> superseded. Thank you for the contribution, and sorry we were slow to respond.
> We’d be glad to see future contributions; please let us know if the merged fix
> misses a distinct case from this PR.

Before posting, lint the draft against the evidence record:

- **No promises of follow-up work** (docs, cleanups, ports of a sub-change).
  The urge to soften a closure with a gift is how unowned commitments get made;
  warmth comes from thanks and a genuine path to disagree, not from new
  obligations. A salvageable sub-change stays in the record for separate triage
  and is not mentioned publicly until it is done.
- **No claims beyond the record.** Every referenced PR, path, or behavior must
  appear in the evidence; delete anything you would have to re-verify to
  defend.
- **The disposition in the message matches the disposition in the record.**

## Backlog sweep safeguards

- Never close solely because a PR is old, conflicting, or lacks tests.
- Verify every cited replacement is merged and covers the stated purpose, and
  record both checks.
- Do not post duplicate comments when a batch command times out; re-read remote
  state before resuming.
- When closure rests on an obsolete implementation, check whether the old code
  is still present but unused on `main`. Record it for a separate deletion
  follow-up; do not mix that cleanup into the closure decision.
- Post comments with real characters, not escape sequences: `gh` CLI `-f`/`-F`
  string fields do not interpret `\n` or `\uXXXX`. Write the message to a file
  and pass `-F body=@file`.
- After a batch, verify every remote state and posted/edited comment, including
  how each comment rendered.