---
name: backlog-pr-review
description: Triage a pull-request backlog methodically, decide whether to close or advance each PR, and write concise, respectful reviewer communication. Use for external-contributor PRs, PRs roughly two weeks old or older from anyone, and closure-message drafting; fresh colleague PRs get a spot review instead. Invokes inventory-review for implementation correctness when a PR reaches engineering review.
---

# Backlog PR Review

Review PRs in stages so cheap disposition decisions happen before detailed
engineering review. This skill owns **triage, disposition, and communication**.
It does not duplicate software-engineering rules: when a live, aligned PR reaches
engineering review, invoke the `inventory-review` skill as the required sub-step.

The goal of a sweep is to change each PR's state. A PR you touch should end
closed, merged, or one concrete step closer to merging — and when that step is
safe to take yourself (rebase, regenerate artifacts, re-run tests), take it
rather than requesting it. Analysis that ends in a recommendation with no state
change is an incomplete sweep item. Improving this skill is a byproduct of
sweeps, never the deliverable.

Each sweep item follows the same sequence: triage through the gates, record the
evidence and disposition, act on the disposition, then communicate. Later steps
draw only on the record built by earlier ones.

## When this skill applies

Apply this skill to PRs from external contributors, and to PRs roughly two
weeks old or older from anyone. Those PRs need the staged triage below because
time and distance make cheap dispositions — superseded, obsolete, duplicated —
likely.

A fresh PR from a colleague, reviewed on request, is a **spot review**, not a
backlog item. Skip this skill's triage and disposition machinery: review the
change directly with the software-engineering and design rules and skills
(`inventory-review` on the diff, the active writing guidance for the review
text).

## Stepped triage

Stop at the first decisive gate:

1. **Legitimacy and safety:** Is this a genuine contribution rather than spam,
   phishing, or meaningless churn?
2. **Present relevance:** Is the *problem* already fixed, the proposal
   duplicated, the feature removed, or the behavior superseded on current
   `main`? Relevance is a property of the problem, not of the diff: a PR
   exists to fix a defect or add a capability, and its files are merely where
   that problem lived when the PR was written. This gate comes second because
   it is the cheapest decisive gate: there is no point weighing purpose,
   direction, or engineering on work that is already shipped.
3. **Purpose and hygiene:** Is the intended outcome focused and understandable?
   Is there enough issue/reproduction/context to evaluate it? Scale hygiene
   expectations with scope.
4. **Ownership boundary:** Is this repository the right home for the behavior?
   For vendor-specific wire formats, runtime shims, schemas, and other external
   contracts, check whether the durable fix belongs in the external service
   itself or an upstream dependency. A local compatibility shim can be
   appropriate, but only after recording why this project should carry that
   external contract instead of fixing or extending its authoritative owner.
5. **Product direction and clearance:** If it worked exactly as described,
   would the project want the behavior? For unapproved cross-product policy or
   architecture, redirect to discussion rather than reviewing a large
   implementation. Changes with commercial intent or competitive relevance
   require internal clearance before GitHub approval or merge, even when the
   engineering review supports approval.
6. **Engineering review:** If the PR survives, invoke the `inventory-review`
   skill against the PR integrated with the current `main` snapshot. Do not
   recreate its caller, contract, concurrency, UI, or testing checks here.

Common dispositions are: close as duplicate, superseded, already implemented,
obsolete, or out of direction; retarget a live fix whose original code path
was replaced; request a split or prior design discussion; or advance to
engineering review. A useful sub-change in an otherwise rejected PR
is a lead to verify independently, not a reason to keep the PR open.

### Closing on direction

When the direction could plausibly be right, "this requires discussion /
design input / security review" is not a complete closure — it shuts the
contributor down without giving them a move. Respect the contribution, keep
the change moving, and be transparent: invite them to file a GitHub issue
with the proposal for discussion, or to reach the team through the project's
community channel. Routing the idea to the right forum is the state change;
the closure alone is not.

Before drafting that invitation, check the PR for a linked issue. The
contributor may already have done exactly what you are about to ask:

- If they filed an issue and no maintainer engaged with it, acknowledge
  that and apologize — never tell them to open the issue they already opened.
  Engage with the existing issue, or explain plainly why the proposal will
  not proceed.
- If the issue got a response that the PR does not reflect, cite that
  discussion in the closure.

### Commercial and competitive clearance

Treat a change as commercially or competitively relevant when it could grant
or imply first-class product placement, endorse or disadvantage a third party,
change marketplace or vendor exposure, create a strategic integration, or
otherwise affect how the project competes or partners. This is a
product-clearance question, not an engineering-severity label.

- The review may conclude in chat or in the evidence record that the change is
  technically ready and **recommend** approval.
- Do not submit an approving GitHub review or merge until a maintainer with
  product authority has cleared the direction. GitHub approval conflates
  engineering readiness with a public product decision, so repository write
  authority alone is not clearance.
- Keep internal commercial reasoning internal. Contributor-facing text may say
  that product direction is not yet decided and name the public decision needed;
  it must not speculate about competitors, partnerships, or private strategy.

For a significant product-direction change from a third-party contributor,
look for a linked feature request or discussion and read it in full. Approval
requires an unequivocally supportive response from a maintainer with authority
over that product area; an open thread, silence, a bot response, implementation
feedback, or support from another external contributor is not approval. If that
support is absent:

1. do not approve the PR on GitHub automatically;
2. record the missing product decision and the linked discussion in the review
   evidence;
3. leave the PR waiting when an internal decision can unblock it; and
4. in the review summary, recommend the smallest concrete internal action that
   moves the decision forward — for example, ask the responsible maintainer to
   answer the existing discussion, identify the acceptance criteria, or decide
   whether the project wants to own the integration.

Do not send the contributor in circles. If they already opened the required
discussion, the next step belongs to the maintainers, not to them.

### Upstream ownership

Review the ownership boundary beyond this repository, not merely across files
inside it. Ask which system has the freshest authoritative knowledge and can
fix the behavior for every consumer:

- an external service should usually own normalization of its own public API;
- a vendor-specific SDK or adapter should usually own that vendor's
  nonstandard wire format;
- a general-purpose dependency should own behavior that is part of its
  declared cross-vendor contract; and
- this repository should own its product policy, its abstract request intent,
  and compatibility behavior genuinely specific to this project.

When upstream is the durable owner, prefer an upstream fix or extension. A
local shim needs explicit evidence that upstream cannot address the need in
the required timeframe, that the project intentionally accepts the maintenance
burden, and that the shim has a clear contract boundary. Do not move
vendor-specific guesses into a generic dependency merely to move them out of
this repository.

### Engineering review handoff

Gate 6 is one handoff, not a second independent review:

1. Invoke `inventory-review` once, before taking the engineering-review action.
2. Give it the PR diff as it applies to the current `main` snapshot, plus the
   purpose and evidence already established at Gates 1–5.
3. Add its inventory, checks, findings, and boundary-test results to this PR's
   evidence record.
4. Resume this skill to choose and take the disposition: approve or merge when
   there are no blockers and authority permits it; request changes for blockers;
   or take the smallest safe step that advances the PR.

`inventory-review` is read-only discovery. This skill still owns the GitHub
action and contributor communication. Do not run a second inventory pass merely
to confirm the first; repeat it only when the reviewed diff or a relevant
`main` contract changed. Gate 6 is an additional invocation context for
`inventory-review`; it does not replace that skill's pre-PR development review.

### Contributor-facing communication

Before posting a review, change request, or closure, apply the active writing
rules: tone, the Pyramid Principle, and line-by-line editing. The evidence
record is internal reviewer material, not a draft for the contributor.

Rewrite the evidence for the person who did the work:

1. Lead with the answer and path forward: what is ready, what remains, and what
   concrete change moves the PR forward.
2. Recognize useful work already done. Thank external and first-time
   contributors, and add encouragement appropriate to the relationship.
3. Explain the reason in ordinary project language, using the relevant
   behavior, file, job, command, or user case.
4. End with a clear, achievable next step or a genuine path to disagree.

Do not leak `inventory-review` process vocabulary into public text. Translate
terms such as "inventory item," "failed check," "invariant," "consistency
boundary," or "boundary test" into the specific situation the contributor
recognizes. For example, write "the current checks run after a PR leaves draft
mode," not "the checks do not cover the draft boundary." Technical terms that
belong to the code or product are fine; unexplained reviewer-framework jargon
is not.

Be specific about deleted or replaced code. Vagaries like "the live path" or
"the current implementation" give the contributor nothing to search for.
Succinctly name the most relevant component — the function, file, or
subsystem — or, failing a good name, describe it concretely enough that the
contributor can find it and adapt their change to the new code.

Before posting, read the message once as the contributor. It should feel like
help from a teammate who wants the contribution to succeed, not an internal
audit report addressed to its subject.

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
  modifies no longer exists on `main`. This is where a rebase or `git grep`
  probe *stops* being evidence: it has answered "does the diff still apply?",
  which is never the question. Find what replaced the target and continue to
  the defect check below before resolving anything.

### Dead file ≠ dead problem

"The code this PR touches is gone" is a fact about the diff, not a
disposition. Before closing on a replaced target, name the defect or missing
capability in one sentence *without mentioning any file path* — e.g. "Windows
shell output in a non-UTF-8 code page is decoded as UTF-8 and garbles" — then
ask that sentence of the replacement code:

1. **Locate the successor.** Where does the behavior the PR changed live now?
   For a migration (classic extension → SDK, handwritten list → generator),
   the successor is usually a specific file you can open, not an abstraction.
2. **Check the defect against the successor.** Grep the successor for the same
   hazard the PR fixed (the hardcoded encoding, the missing guard, the
   unbounded buffer). Three outcomes:
   - The successor **resolves the problem** (or removed the conditions that
     produce it, e.g. the whole input path no longer exists): the PR is
     genuinely obsolete or already implemented. Cite the resolving code in the
     closure message.
   - The successor **has the same defect** — often verbatim, since migrations
     port happy-path assumptions: the PR is a *live fix pointed at the wrong
     file*. Do not close it as obsolete. Retarget instead (below).
   - You **cannot find the successor** or cannot tell: the relevance gate is
     unanswered. Leave the PR for engineering review rather than closing on
     the half-probe.
3. **Check the linked issue's state.** An open issue that the PR claims to fix
   is a strong hint the problem survived whatever replaced the code. Closing
   the PR as obsolete while its issue stays open should feel contradictory —
   if the code's removal really fixed the problem, close the issue too, with
   the same evidence.

### Retargeting a live fix

When the problem is alive but the diff is aimed at removed code, the sweep
action is a retargeting comment, not a closure. The comment should:

- confirm the diagnosis is still correct and wanted;
- name the successor path where the defect now lives, with the specific
  evidence (the hardcoded value, the missing branch);
- note concrete constraints of the new location the contributor could not
  know (shared helpers to reuse, streaming/chunking contracts, dependency
  placement), so a rebase attempt starts from reality;
- offer to port the fix with attribution if the contributor has moved on.

This keeps the sweep's state-change goal honest: the PR moved one concrete
step toward merging in its new home, instead of being counted as closed while
the user-facing bug lives on.

When a PR adds an entry to a hand-maintained list (providers, commands, tools,
model catalogs), check whether that list still exists on `main`. The PR is
superseded when the mechanism itself was replaced by generation or data-driven
registration — even when no one added the PR's specific item by hand. A large
regenerated artifact in the diff (a generated catalog, lockfile, or snapshot)
is a hint that generation may now be the system, not just an output.

This mechanism-replacement supersession applies to *capability additions*,
where the diff's value is the wiring and redoing it means a small data or
config change in the new mechanism. It does not extend to *defect fixes*: for
a bug, the diff's value is the diagnosis, and the bug either survived the
replacement or it didn't — which is exactly the defect check above.

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
- apologize for a slow response when no maintainer responded for an extended
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
- Never close a defect fix as obsolete solely because its files were removed
  or rewritten. The record must show where the behavior lives now and that
  the defect is absent there; "target gone" without a successor check is an
  unanswered gate, not a disposition.
- Verify every cited replacement is merged and covers the stated purpose, and
  record both checks.
- Do not post duplicate comments when a batch command times out; re-read remote
  state before resuming.
- Treat a successful review submission as durable. Capture the returned review
  ID and read that review directly before retrying; list and timeline reads may
  be stale. Submitted reviews cannot be deleted, and dismissal leaves a visible
  event in the PR timeline. Correct the existing review body in place when the
  API permits it instead of dismissing the review and posting a replacement.
- When closure rests on an obsolete implementation, check whether the old code
  is still present but unused on `main`. Record the dead code in the sweep
  record; do not mix that cleanup into the closure decision. At the end of the
  batch, collect these notes into one omnibus PR that deletes the dead code,
  and link in it the reviews where each dead path was detected.
- Post comments with real characters, not escape sequences: `gh` CLI `-f`/`-F`
  string fields do not interpret `\n` or `\uXXXX`. Write the message to a file
  and pass `-F body=@file`.
- After a batch, verify every remote state and posted/edited comment, including
  how each comment rendered.