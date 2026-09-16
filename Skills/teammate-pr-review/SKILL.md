---
name: teammate-pr-review
description: Review a fresh PR from a repository teammate. Checks that the author is a repository member with landed commits (or is named as trusted by the user) and stops if not; asks whether the problem is already solved, whether the code is in the right home, and whether the project wants the change; then runs inventory-review on the diff and writes direct, specific feedback. Use when asked to review a teammate's or trusted contributor's PR.
---

# Teammate PR Review

Review a teammate's PR the way a senior engineer would: check the questions
above the code first, then the code, then say what you found in plain words.
This skill owns **eligibility, the three questions, and the review action**.
`inventory-review` owns the diff review. `backlog-pr-review` owns external
and stale PRs.

## Step 1 — Confirm the author is a teammate

A teammate has write access to the repository and has landed code on the
target branch. Both are required. Check before reading the diff:

```bash
gh pr view <number> --json author,authorAssociation,createdAt,isDraft
git fetch origin main
git log origin/main --since='3 months ago' --author='<login>' --oneline | head
```

Match on the GitHub login, not an email: squash merges record the author as
`<id>+<login>@users.noreply.github.com`, so the login appears in the author
field whatever email the teammate commits with locally.

Then decide:

- **`MEMBER`, `OWNER` or `COLLABORATOR`, with commits on `main` in roughly
  the last three months** — a teammate. Continue.
- **`MEMBER`, `OWNER` or `COLLABORATOR`, but no recent commits** — a
  teammate with less shared context. Continue, but verify every claim the
  PR makes about the current code against `main`; do not assume they know
  what changed while they were away.
- **Anything else** — not a teammate. Stop, say so, and hand the PR to
  `backlog-pr-review`. `CONTRIBUTOR` is granted for one merged PR and does
  not confer trust, however many commits follow it.

The user may name an author as trusted for this review ("treat X as a
teammate"). Then continue as for a teammate with less shared context, and
record the override in the report. Do not infer the override from
contribution history; a well-known external contributor still goes through
`backlog-pr-review` unless the user says otherwise.

A teammate's PR that is roughly two weeks old or older also goes to
`backlog-pr-review`; age makes the cheap dispositions likely, whoever wrote
it.

## Step 2 — Ask the three questions

Answer each from `main` and the linked issue, not from the PR's description.
Stop at the first that fails and raise it with the author before reviewing
code; there is no point reviewing code that should not land.

1. **Is the problem already solved?** Grep `main` for the mechanism the PR
   touches. A teammate's branch can predate a change that fixed the
   problem another way. `backlog-pr-review`'s **Probing relevance** section
   has the method.
2. **Is this the right home?** Apply the development rules' **Placement**:
   does the behavior live in the layer that owns its state, and does every
   product that reaches that state get the same behavior through one path?
   For contracts with an external service or dependency, see
   `backlog-pr-review`'s **Upstream ownership**.
3. **Does the project want it?** For a removal, a change of default, or a
   change to a path many users are on, apply the development rules' **Levels
   of a Change**: who wants this and how we know, who loses, how we will
   learn we were wrong, how we reverse. For anything with commercial or
   competitive relevance, product clearance is required before approval;
   `backlog-pr-review`'s **Commercial and competitive clearance** says what
   counts.

For a fix or a tidy-up, questions 2 and 3 usually take a sentence each. Do
not invent business impact for a change that has none.

## Step 3 — Review the code

Invoke `inventory-review` once, on the diff as it applies to the current
`main`, with the answers from step 2. It returns the inventory, checks and
triaged findings. Do not treat the invocation, an agent summary, passing tests,
or green CI as completion. Before acting, read its evidence record and verify
that every inventory category is filled for the reviewed base and head, and
that it lists omissions explicitly. An omission that can reach the PR's central
promise blocks approval.

For a re-review after author changes, first read the past findings and replies,
then review the PR anew at its current head. The past findings are leads, not a
checklist or a limit on scope. Read the full current diff, re-inventory every
category affected by the fixes or a changed `main`, and look for new issues at
the seams between the fixes and the rest of the change. Do not approve merely
because the old comments are resolved, the requested lines changed, or CI is
green. Do not run a second unchanged-head pass merely to confirm the first.

## Step 4 — Write the review

Apply the development rules' **Two Audiences**. A teammate shares the code
and the product with you, not this rubric. For each finding, name the two
things that meet and what goes wrong where they meet, with the file and the
user case. Lead with the blockers and the path forward. Skip the thanks and
encouragement that external contributors get; teammates want brevity.

If step 2 stopped the review, say which question failed and what evidence
answers it. Give a concrete next step or a genuine path to disagree.

## Step 5 — Act and report

Take the action your authority allows: approve when there are no blockers,
request changes for blockers, or comment. Before any GitHub mutation,
re-read the head SHA and existing reviews; rebuild affected findings if they
changed.

The GitHub account is shared with its human owner, who may use it while this
review is running. A review or comment from the same login can therefore appear
without being this reviewer's action; that is normal concurrent activity.
Re-read it as review context, do not duplicate or contradict it accidentally,
and attribute only mutations this run can prove from its own submitted request
and result. Do not infer authorship from the login and timestamp alone.

Report by the actions this reviewer took, following `backlog-pr-review`'s
**Sweep reporting and action attribution**. Name the actor for any later
approve, merge or close by someone else.
