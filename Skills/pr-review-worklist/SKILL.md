---
name: pr-review-worklist
description: Work through a pull-request backlog one PR at a time in the main agent, using a durable JSON worklist to resume safely after restarts, skip completed PRs, and revisit waiting PRs only when their stated condition changes. Invokes backlog-pr-review for each PR and never uses subagents.
---

# PR Review Worklist

Review a PR backlog sequentially and preserve progress across conversations. This skill owns **work selection, restart recovery, and one-item resource lifecycle**. The `backlog-pr-review` skill owns triage, disposition, and contributor communication.

## Main-agent-only constraint

Do all work in the current main-agent conversation, one PR at a time.

- **Never spawn, route work to, or communicate with a subagent or teammate.**
- Do not call delegation, mailbox, team-task, or team-outcome tools.
- Do not start a second PR while another PR is active.
- Skills invoked below run in this same conversation; they are not agents.

If the backlog is too large for one conversation, persist the active record and stop. Never introduce concurrency to increase throughput.

## Durable JSON worklist

The sole progress record is:

```text
$HOME/.cline/pr-review-worklist.json
```

On Windows it is `$env:USERPROFILE\.cline\pr-review-worklist.json`.

The `.cline` segment in the paths and ref namespaces throughout this skill is
the host agent's data directory. This is the only host-specific detail in
these review skills; on another agent, substitute its data directory while
keeping the names stable, because resume depends on finding the same paths.

JSON is the source of truth because the main consumer is an agent and state transitions are easier to validate structurally than through Markdown edits. The ordered `items` array preserves queue order. Each item carries exactly one `state`: `todo`, `in_progress`, `waiting`, or `done`.

Use the bundled standard-library CLI for all routine mutations:

```bash
WL="$HOME/.cline/skills/pr-review-worklist/worklist.py"
python3 "$WL" <command> ...
```

On Windows use `py -3` and `%USERPROFILE%\.cline\skills\pr-review-worklist\worklist.py`. The CLI requires Python 3.10 or newer and no third-party packages. Use `--path` only for tests.

Do not write inline Python, use `jq`, or edit the JSON directly when the CLI supports the operation. Run `python3 "$WL" --help` or `python3 "$WL" <command> --help` for exact arguments.

### Basic commands

```bash
python3 "$WL" init
python3 "$WL" validate
python3 "$WL" summary --json

python3 "$WL" add --repo owner/repo --number 123 \
  --title "Short purpose" --opened 2026-07-01

python3 "$WL" start \
  --next-step "Read live PR metadata, reviews, comments, and repository state"

python3 "$WL" update --pr owner/repo#123 \
  --note "live metadata and immutable refs verified" \
  --target-branch main --base FULL_BASE_SHA --head FULL_HEAD_SHA \
  --next-step "Apply the backlog review gates" \
  --evidence "Open, non-draft; no action taken" \
  --resource 'ref refs/cline-pr-review/main' \
  --resource 'ref refs/cline-pr-review/pr-123'

python3 "$WL" wait --pr owner/repo#123 --note "review paused" \
  --waiting-for "contributor update" --recheck-when "the head SHA changes" \
  --next-step "Read the changed diff" --evidence "Requested one focused change"

python3 "$WL" start --pr owner/repo#123 --note "head changed" \
  --next-step "Verify the new head before acting"

python3 "$WL" update --pr owner/repo#123 \
  --note "owned refs and worktree removed" --clear-resources

python3 "$WL" done --pr owner/repo#123 \
  --note "remote outcome and cleanup verified" \
  --outcome "Gate 2 — superseded" --evidence "Merged #456 covers the behavior" \
  --action "Commented and closed — ACTION_URL" \
  --remote-state "CLOSED at FULL_HEAD_SHA"
```

`start` selects the first `todo` item unless `--pr` names a `todo` or eligible `waiting` item. `done` rejects an active item while its `resources` array is non-empty.

## Consistency boundary

The CLI validates the full document before each write, writes a sibling temporary file, flushes it, and atomically renames it over the worklist. It rechecks the file immediately before preparing the replacement and rejects changes already visible at that boundary. This is not a cross-process lock: only one main-agent session may own the worklist at a time. If another live session may be using it, stop rather than race writers.

Update the active record immediately after every verified remote action and every acquired or released resource—not only at the end of a session.

## Resume before selecting work

On every invocation:

1. Read the JSON and run `summary --json` or `validate` before any GitHub or repository query.
2. If an item is `in_progress`, recover it before considering another PR. Re-read its remote state, head SHA, reviews, comments, and recorded resources. A planned action may already have succeeded before interruption; remote state decides whether to repeat it.
3. If recovery shows completion, verify remote state, clean resources, run `update --clear-resources`, then `done`. If progress needs an external event, run `wait`. Otherwise continue it.
4. If nothing is active, start a waiting item only when its recorded recheck condition is satisfied; otherwise run `start` for the first `todo` item.
5. Do not poll every waiting PR. Never query or re-review `done` items during routine resume.

## Review one PR

For the active item:

1. Fetch its target branch and PR head into temporary refs. Review against the target branch's current remote tip when this item starts. Run `update` immediately after acquiring resources.
2. Invoke `backlog-pr-review` in this conversation. Gates 1–5 build one shared purpose/current-main evidence record, including upstream ownership and any required product clearance.
3. If the PR reaches Gate 6, invoke `inventory-review` **once in this same conversation**, passing the integrated diff plus the Gates 1–5 record. Append its inventory, checks, findings, and boundary-test results to the same record. Resume `backlog-pr-review` for disposition and action. This is one review with an internal Gate 6 handoff—not a second independent review, subagent report, or repeated inventory pass.
4. Before any GitHub mutation, run `update` with the exact planned action. Re-read the current head, state, reviews, comments, and target branch. Rebuild affected evidence if relevant state changed.
5. Take the evidence-backed action allowed by the user's authority. Verify the remote result and rendered communication, then run `update` immediately. Never repeat an action merely because a local command timed out.
6. Remove the worktree and refs, then run `update --clear-resources`. Run `done` only after the remote outcome and cleanup are verified; run `wait` when progress depends on an external event or decision.

Use at most one isolated worktree. Prefer `$HOME/.cline/pr-review-worktrees/<owner>-<repo>/pr-<number>` and temporary refs under `refs/cline-pr-review/`. Never modify or clean the user's original checkout.

## End a session

Prefer stopping with no `in_progress` item. If interruption is unavoidable, run `update` with the last verified observation, exact next step, base/head SHAs, and every owned resource. Never delete the worklist.

Report the processed PR, resulting state, action link if any, and `summary --json` counts. If nothing is eligible, report the waiting conditions rather than polling or spawning workers.
