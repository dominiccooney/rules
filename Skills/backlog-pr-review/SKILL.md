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

## Stepped triage

Stop at the first decisive gate:

1. **Legitimacy and safety:** Is this a genuine contribution rather than spam,
   phishing, or meaningless churn?
2. **Purpose and hygiene:** Is the intended outcome focused and understandable?
   Is there enough issue/reproduction/context to evaluate it? Scale hygiene
   expectations with scope.
3. **Product direction:** If it worked exactly as described, would Cline want
   the behavior? For unapproved cross-product policy or architecture, redirect
   to discussion rather than reviewing a large implementation.
4. **Present relevance:** Is the problem already fixed, the proposal duplicated,
   the feature removed, or the changed path superseded?
5. **Current applicability:** Does the PR affect the shipped path today? A clean
   rebase proves textual compatibility, not relevance.
6. **Engineering review:** If the PR survives, hand it to existing engineering
   rules and review skills. Do not recreate their caller, contract, concurrency,
   UI, or testing checks here.

Common dispositions are: close as duplicate, superseded, already implemented,
obsolete, or out of direction; request a split or prior design discussion; or
advance to engineering review. A useful sub-change in an otherwise rejected PR
is a lead to verify independently, not a reason to keep the PR open.

## Closure messages

Use the shortest message that states:

1. the disposition,
2. the decisive evidence (usually a replacement PR or removed path), and
3. a path to disagree when the conclusion could be mistaken.

Match detail to the relationship. Close collaborators with shared context
usually benefit from a direct sentence or two.

For **external or new contributors**:

- Briefly thank them for the contribution.
- If no Cline member responded for an extended period, apologize for the slow
  response. Do not imply the contributor caused the delay.
- Welcome future contributions, even when this PR cannot move forward.
- Keep this to one or two additional sentences; warmth does not require a long
  postmortem.

Treat GitHub `FIRST_TIME_CONTRIBUTOR` and `NONE` as external by default. Use
contribution history and shared context to recognize regular contributors;
`CONTRIBUTOR` alone is not conclusive. Before apologizing, check whether a Cline
member already provided timely feedback.

Example for an external contributor after a long wait:

> #12345 implemented this in the current SDK path, so I’m closing this as
> superseded. Thank you for the contribution, and sorry we were slow to respond.
> We’d be glad to see future contributions; please let us know if the merged fix
> misses a distinct case from this PR.

## Backlog sweep safeguards

- Never close solely because a PR is old, conflicting, or lacks tests.
- Verify every cited replacement is merged and covers the stated purpose.
- Do not post duplicate comments when a batch command times out; re-read remote
  state before resuming.
- When closure rests on an obsolete implementation, check whether the old code
  is still present but unused. Record it separately for a deletion follow-up;
  do not mix that cleanup into the closure decision.
- After a batch, verify every remote state and posted/edited comment.