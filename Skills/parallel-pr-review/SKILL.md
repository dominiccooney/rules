---
name: parallel-pr-review
description: Review multiple pull requests concurrently by pinning one base revision, creating an isolated worktree and subagent per PR, delegating one authoritative backlog review, coordinating genuine escalations, verifying remote outcomes, and cleaning every worktree. Use for parallel PR backlog sweeps.
---

# Parallel PR Review

Run independent PR reviews concurrently without duplicating engineering analysis
or sharing a mutable checkout. This skill owns **batch orchestration and resource
lifecycle**. Each subagent owns one complete `backlog-pr-review`, including its
required `inventory-review` sub-step when the PR reaches Gate 5.

The driver does not re-review completed work. It resolves escalations, checks
evidence records for completeness, verifies remote outcomes once, and cleans up.

## Batch contract

A batch reviews PRs against one target branch. Read each PR's target branch
(GitHub `baseRefName`) first, and split PRs with different repositories or
target branches into separate batches.

Before creating anything, choose a deterministic per-repository parent beneath
the system temporary directory. Check it for incomplete ledgers from earlier
batches and finish or report their cleanup before starting another batch. Then
create a unique batch directory and persist a resource ledger inside it. Update
the ledger immediately after every acquisition or release so a resumed driver
can clean a partially created batch. Record:

- repository owner/name, repository root, remote, and target branch;
- the original checkout's branch or detached `HEAD`, commit SHA, and exact file
  status before the batch;
- the pinned base SHA shared by the whole batch;
- the PR numbers, head SHAs, temporary refs, worktree paths, agent IDs, and run
  IDs in a resource ledger;
- the authenticated GitHub identity and its authority to review, close, or merge.

The pinned base SHA is the current remote tip of the target branch, fetched at
batch start — never a PR's merge base, its historical branch point, or an
unfetched remote-tracking ref. An old PR is reviewed against the target branch
as it is today, not as it was when the PR was written. That SHA is the batch's
consistency boundary: every reviewer tests and cites that snapshot even if the
target branch moves during the batch.

## Create isolated worktrees

The driver creates and owns one detached worktree per PR. Subagents never create,
remove, or reuse worktrees.

1. Fetch the target branch from its remote once and resolve its tip as the
   pinned base SHA.
2. Fetch each pull-request head into a batch-specific temporary ref. Record the
   exact head SHA; do not rely on a mutable contributor branch name.
3. Add each worktree detached at the pinned base SHA. Use paths containing the
   PR number so commands and cleanup remain auditable.
4. Verify that every worktree path starts at the base SHA and that every
   temporary PR ref resolves to its recorded head SHA before spawning agents.

Detached worktrees avoid local branch-name collisions and give the integration
the correct parent direction: pinned base first, PR head second. A reviewer may
merge the recorded PR head, rebase a temporary local branch, or otherwise probe
integration inside its assigned worktree, but it must record the result and
leave unrelated worktrees and the user's checkout alone. Integration history is
temporary and must never be pushed.

Never place two agents in the same worktree. Never let an agent infer its working
directory: include the absolute worktree path, base SHA, head SHA, and repository
name in its task.

## Delegate one authoritative pass

Spawn one subagent per PR, then dispatch all independent reviews asynchronously.
Do not create a second layer of shared task records unless the batch has real
dependencies or reassignment needs.

Each assignment must require the reviewer to:

1. Work only in its absolute worktree path.
2. Invoke `backlog-pr-review` for the assigned PR. That skill invokes
   `inventory-review` if the PR reaches engineering review.
3. Use the pinned base SHA for current-main evidence and integrate the recorded
   PR head into that snapshot before Gate 5 testing.
4. Take the safe disposition itself: close when an early gate is decisive,
   retarget or comment when that advances the PR, or approve/request changes
   after engineering review. Do not stop at a recommendation.
5. Immediately before any GitHub action, re-read the PR's remote head SHA. If it
   differs from the recorded head, do not act on the stale review: update the
   ledger and worktree, then review the changed diff before choosing a
   disposition. Re-read the PR's target branch too: a retargeted PR invalidates
   the batch snapshot, so escalate for a rebuilt review against the new target
   instead of acting. Also re-read the existing reviews/comments so a retry or
   another reviewer cannot cause a duplicate action.
6. Verify every GitHub action and how its communication rendered.
7. Return exactly one structured evidence record:

```text
PR and URL:
Worktree, base SHA, and head SHA:
Decisive gate:
Disposition:
Current-main evidence:
Inventory-review outcome (Gate 5 only):
Tests and results:
GitHub action and URL:
Verified final remote state:
Escalation or none:
```

The first pass should be complete enough that the driver does not ask for a
second inventory-shaped report.

## Authority and escalations

Delegate routine, evidence-backed review actions. Escalate before:

- merging, unless the user explicitly delegated merge authority for this batch;
- an ambiguous product-direction or architecture decision;
- a closure whose relevance evidence is incomplete or contradictory;
- destructive repository changes or action outside the assigned PR;
- acting when the authenticated identity's authority is unclear.

Do not escalate a routine changes-requested review, an evidence-backed early-gate
closure, or a test/rebase probe merely so the driver can repeat the analysis.

Agents send escalations through the mailbox with the decisive evidence, proposed
action, and alternatives. The driver answers the decision only; the same agent
then completes and verifies its review.

## Coordinate without polling

After dispatching all runs, wait for completions and read the mailbox. Poll only
when a run stalls or an escalation arrives. Progress narration is not evidence
and should not trigger more repository or GitHub queries.

When one agent finishes early, leave its worktree intact until its report and
remote action are verified. Do not assign that PR to another agent unless the
first run failed without acting.

## Verify once

After all agents finish:

1. Check each evidence record has a decisive gate, evidence against the pinned
   base, matching reviewed and remote head SHAs, a disposition, an action URL,
   and a verified state.
2. Batch-fetch the final state, review decision, head SHA, and posted review or
   comment for every PR. Confirm the text rendered correctly and no duplicate
   action was posted.
3. Fetch the target branch once more. If it moved, inspect only the intervening
   diff for overlap with each PR's changed contracts, successor paths, or
   decisive evidence. Reopen a review only when that delta can change its
   disposition; a moving branch alone is not a reason to repeat every review.

The driver may reject an incomplete or internally contradictory evidence record.
It must not rerun `inventory-review` simply to gain confidence in a complete,
coherent record.

## Clean up every exit

Cleanup is part of the batch result, not best effort. Account for success,
subagent error, cancellation, timeout, driver interruption, and partial setup.

1. Wait for or cancel active runs before removing their worktrees.
2. Shut down every spawned subagent.
3. For every ledger entry, remove the worktree with `git worktree remove
   --force`; remove only paths underneath the recorded temporary batch root.
4. Delete the batch-specific temporary PR refs.
5. Run `git worktree prune`, then remove the ledger and empty batch directory.
6. Verify the worktrees, temporary refs, active runs, and agents are gone.
7. Confirm the user's original checkout has the same branch and file status it
   had before the batch. Report pre-existing changes; never clean them.

If cleanup fails, report the exact remaining resource and path. Never describe a
batch as complete while an owned worktree, ref, run, or subagent remains.

## Final report

Summarize each PR's decisive gate, disposition, action link, and final remote
state. State the pinned base SHA and whether the target branch moved
relevantly. Confirm resource cleanup and whether the user's checkout remained
unchanged.
