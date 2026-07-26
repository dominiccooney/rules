---
name: pr-review-worklist
description: Work through a pull-request backlog one PR at a time in the main agent, using a durable worklist to resume safely after restarts, skip completed PRs, and revisit waiting PRs only when their stated condition changes. Invokes backlog-pr-review for each PR and never uses subagents.
---

# PR Review Worklist

Review a PR backlog sequentially and preserve progress across conversations. This skill owns **work selection, restart recovery, and one-item resource lifecycle**. The `backlog-pr-review` skill remains the authoritative workflow for triage, disposition, and communication; invoke it for the active PR in this main agent.

## Main-agent-only constraint

Do all work in the current main-agent conversation, one PR at a time.

- **Never spawn, route work to, or communicate with a subagent or teammate.**
- Do not call `spawn_agent`, `team_spawn_teammate`, `team_run_task`, or any other delegation, mailbox, team-task, or team-outcome tool.
- Do not start a second PR while another PR is active.
- Invoking `backlog-pr-review` and its required `inventory-review` sub-step is allowed: skills run in this same main-agent conversation and are not agents.

If the backlog is too large for one conversation, stop at an item boundary. Persist the current state and let the next main-agent conversation resume it. Never introduce concurrency to increase throughput.

## Durable worklist

The sole progress record is:

```text
$HOME/.cline/pr-review-worklist.md
```

On Windows this is `$env:USERPROFILE\.cline\pr-review-worklist.md`. On this machine it is `/home/kali/.cline/pr-review-worklist.md`.

Read this file before querying GitHub, fetching refs, creating worktrees, or choosing a PR. Do not create a repo-local copy or a second ledger. The worklist survives agent and IDE restarts and is deliberately outside temporary directories and source repositories.

Each PR appears exactly once, under exactly one state heading. State is encoded by the heading; do not add a second `Status` field that can disagree with it. Preserve this shape:

```markdown
# PR review worklist

## In progress

<!-- At most one entry. -->

## To do

- [ ] [owner/repo#123](https://github.com/owner/repo/pull/123) — short purpose

## Waiting

### [owner/repo#456](https://github.com/owner/repo/pull/456)
- Last update: 2026-07-26T12:00:00Z — concise factual update
- Waiting for: one external event or decision
- Recheck when: an observable condition, not "later"
- Next step: the exact next action after that condition
- Last verified head: full commit SHA
- Evidence/action: URLs or concise evidence
- Resources: `none`, or exact owned worktree and ref needing recovery

## Done

### [owner/repo#789](https://github.com/owner/repo/pull/789)
- Last update: 2026-07-26T12:00:00Z — verified completion
- Outcome: decisive gate and disposition
- Action: GitHub action and URL, or `none` with reason
- Verified remote state: state, review decision, and full head SHA
```

Keep `To do` entries short so the unprocessed queue is easy to scan. Expand an entry when moving it to `In progress`, `Waiting`, or `Done`. Use UTC ISO-8601 timestamps and full commit SHAs. A waiting entry must always say both what it is waiting for and the observable condition that makes it eligible again.

If the file does not exist, create it with all four empty headings before doing anything else. When adding a requested backlog, merge it into the existing file: do not duplicate PRs or reset existing states.

## Worklist consistency boundary

A state transition takes effect when the worklist is atomically replaced after the corresponding observation or action has been verified. Write a sibling temporary file and rename it over the worklist; do not leave a partially written progress record. Persist after every remote action and every acquired or released resource, not only at the end of a session.

Only one main-agent session may own the worklist at a time. If another live session may be using it, stop rather than race two writers.

## Resume before selecting work

On every invocation:

1. Read the entire worklist.
2. If `In progress` contains an entry, recover it before considering any other PR. Re-read the PR state, head SHA, reviews, comments, and recorded resources. A planned GitHub action may already have succeeded before an interruption; remote state, not the old note, decides whether to repeat it.
3. If recovery shows the item is complete, verify its remote state, clean its resources, and move it to `Done`. If it needs an external event, move it to `Waiting` with a precise recheck condition. Otherwise continue it.
4. If no item is active, select an eligible `Waiting` item whose recheck condition is known to be satisfied; otherwise select the first `To do` item.
5. Do not poll every waiting PR. Skip waiting entries unless their recorded condition can now be tested or the user supplies the awaited information.
6. Never query or re-review `Done` entries during a routine resume. Reopen one only when the user requests it or provides evidence of a material remote change.

This ordering makes interrupted side effects safe while keeping completed and blocked work cheap to skip.

## Process one PR

Move the selected entry to `In progress` before acquiring resources or beginning analysis. Record:

- start or last-update time;
- repository, PR URL, target branch, and purpose;
- last verified base and head SHAs;
- exact next step;
- evidence and actions as they accumulate;
- any owned temporary ref and worktree path.

Use at most one isolated worktree. Prefer the deterministic owned location `$HOME/.cline/pr-review-worktrees/<owner>-<repo>/pr-<number>` and a temporary ref under `refs/cline-pr-review/`. Never modify or clean the user's original checkout. Before reuse after a restart, verify that the recorded worktree and ref match the recorded SHAs; otherwise remove only the recorded owned resources and recreate them.

For the active item:

1. Fetch its target branch and PR head. Review against the target branch's current remote tip when this item starts; there is no stale batch-wide base.
2. Invoke `backlog-pr-review` in this conversation. If the PR reaches Gate 5, invoke `inventory-review` in this conversation as that skill requires.
3. Before any GitHub mutation, update `Next step` with the exact planned action. Then re-read the current head, state, reviews, and comments. If the head or a relevant target-branch contract changed, rebuild the affected evidence rather than acting on a stale review.
4. Take the evidence-backed action allowed by the user's authority. Verify the remote result and rendered communication immediately, then update the worklist immediately. Never repeat an action merely because a local command timed out.
5. Remove the active worktree and temporary ref and record `Resources: none`. Cleanup is part of the item: success, error, cancellation, timeout, and restart must all leave owned resources accounted for.
6. Move the item to `Done` only after the remote outcome and cleanup are verified. Move it to `Waiting` when progress depends on an external event or decision. If local cleanup remains, keep it `In progress`; remote completion does not make leaked resources disappear.

Do not hold multiple base snapshots, PR refs, or worktrees. Finish, defer, or recover the active item before moving to the next one.

## Waiting and completion rules

Use `Waiting` for a real suspension point: contributor changes, CI completion, product or architecture direction, missing authority, or another named external event. The note must let a future main agent decide whether to skip the item without reconstructing the review. Vague entries such as "needs follow-up" or "check later" are invalid.

Use `Done` for a verified terminal outcome or a completed review action. Record the decisive gate, disposition, action URL, final PR state or review decision, and reviewed head SHA. This is the durable evidence that allows future sessions to skip the PR.

## End or hand off a session

Prefer stopping with `In progress` empty. If interruption is unavoidable, write the last verified observation, exact next step, head/base SHAs, and all owned resources before stopping. Do not delete or archive the worklist after a sweep; it is the recovery record for the next session.

Report the PR just processed, its resulting state, the action link if any, and the counts remaining in `To do`, `Waiting`, and `Done`. If nothing is eligible, report the waiting conditions rather than polling or spawning more workers.
