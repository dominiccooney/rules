---
name: make-a-change
description: Use this when making a change to the code. Drive it from conception to landing.
---

# Make a Change

## Gut Check: Need

A change can be right or wrong at five levels:

1. **Need** — do users and the business want it?
2. **Function** — are the features and content right?
3. **Structure** — does the design work on paper?
4. **Realization** — does the code work: correct, fast, secure?
5. **Surface** — formatting, layout, wording.

Three facts about the levels shape how we work:

- A failure spoils every level below it and none above. A change nobody wants is worthless however well it is built. Judge a change from the top down.
- Evidence arrives from the bottom up: the formatter answers in seconds, tests in minutes, review in days, users in months. Our checks are strongest where they matter least. Passing every check we have shows the code works; it does not show that anyone wants it.
- Low-level failures are fixed by iteration. High-level failures are fixed by reversal.

So:

- A removal, a change of default, or a change to a path many users are on must answer, in the plan: who wants this and how we know; who loses; how we will learn we were wrong; and how we would reverse it. Ship it so that reversal is cheap: a flag, a staged rollout, or the old path kept for a release.
- When fixing a failure, find the level of the cause as well as the level of the symptom. A fix below the cause is a patch, and the failure will return.
- When a shipped change fails, record the level it failed at and the level it was caught at. The distance between them is the process gap to close.

This step is required when the change removes user-visible behavior, changes a default, or alters a path many users are on. Skip it otherwise; do not invent business impact for a tidy-up.

1. **Who wants this, and how do we know?** Cite the request, issue, data or
   decision. "It simplifies the code" is a level-3 reason, not a level-1 one.
2. **Who loses?** A removal's losers exist today and can be counted. Name
   them and what they lose.
3. **How will we learn we were wrong?** A metric, a feedback channel, a date
   to look.
4. **How do we reverse it?** Choose one: a flag, a staged rollout, or the old
   path kept for a release. A change that cannot be reversed cheaply needs a
   stronger answer to question 1.

If there are no compelling answers to these questions, stop and discuss.

## Make space to work

If /tmp (if relevant) or the disk is nearly out of space, flag that and stop. You may need to clean up old worktrees first.

In general, work in a new worktree.

## The Mikado Method

We use the Mikado method to keep changes manageable in our large codebase and to incorporate feedback from our own investigations, CI, Greptile and reviewers in a productive way instead of patchily layering on hacks.

Briefly, to execute the Mikado method, you should:

1. Set a goal. This is the "Mikado goal."
2. Implement the goal or prerequisite naively. Use `step-change-planning` to implement each goal/prerequisite with high fidelity.
3. Are there errors?

For our purposes, errors are not only our own findings from step-change-planning, but correct feedback from Greptile, a relevant CI failure, relevant feedback from a reviewer, and so on.

If there are no errors, ask:

Does the change make sense? By "make sense" we mean do something useful, be something we would want to commit. If the change does NOT make sense, proceed to step 7.

If the change DOES make sense, commit your changes. If the Mikado goal is met, you can proceed to update the PR. Otherwise proceed to step 7.

If there ARE errors in step 3, continue to step 4. Note, if you learned of these errors asynchronously (for example, through Greptile's feedback, reviewer feedback, etc.) then you should identify the closest relevant goal in the Mikado graph and consider that the current goal for steps 4-7. If there are multiple relevant pieces of feedback, find the earliest relevant goal and treat that as the current goal and focus on errors related to that goal specifically.

4. Come up with immediate solutions to the errors. These are an idea or condition, not specific fixes.
5. Draw the solution(s) in step 4 as new prerequisites to the current goal.
6. Revert your changes. If, in step 3, you discovered these errors asynchronously you should revert everything up to and including the current goal.
7. Select the next prerequisite to work with. These must be leaves of your Mikado graph.

Keep snapshot copies of the Mikado graph along with your work, but don't check them in. You may want to rename them mentioning specific commits to help you revert the graph correctly, although rebasing during long changes will require extra bookkeeping.

It is normal to "learn" about the change you're making through this process of repeated reverting and rewriting. That is acceptable and even desirable. However it is important to follow the Mikado process and not "cheat" by turning goals into steps in a plan and just executing them blindly.

Naturally, this is a token-intensive method but we are willing to use this to produce extremely high quality results.

In addition, some models (you) have a tendency to try to economize tokens. This leads you to write expedient, patchy fixes. Instead, carefully refactor and continuously move toward clean architecture: Merge, reorganize and split code into related modules, files and classes; migrate similar functionality to the correct layer to share it when appropriate; clean up technical debt and simplify things as prerequisite goals to make "naive" (simple, clean) implementations possible.

## Coding Style

For longer comments and documentation, use the `writing-editing-prose` skill in addition to the rules here.

### Simplicity

You have been trained to economize tokens and tool calls, but this causes you to do things like (BAD example):

```typescript
   ...
   const { thinger } = await import('@foo/things')
   thinger.doTheThing()
   ...
```

However for clarity and consistency with the surrounding code, you should not use a dynamic import but instead insert the import statement at the start of the file.

You should eliminate the possibility of bugs arising by reducing repetition. For example:

- If a function already exists which does what you want, reuse it. If it is not accessible, make it accessible instead of cutting and pasting it.
- Ensure consistency by making things intrinsically consistent at the type level by encoding a constraint, at the implementation level by reusing functions, within a function by writing assertions, creating const variables, etc. DON'T simply duplicate things because it is convenient, because one of those duplicates may get edited and become inconsistent with the others.
- Where essential complexity exists, express it in the clearest way possible. Use a state machine can succinctly encode a system and make it clear whether there's a fixed set of states or an infinite set. Use Strategy pattern to consolidate a lot of conditionals spread across codebase into one conditional statement that creates a FooStrategy, BarStrategy or NullStrategy.

Avoid needless variation. For example, if in one function your refer to something as `accessToken`, and in another context you refer to the same concept simply as `token`, this implies a distinction that does not exist. Be specific, brief and above all: consistent.

Never introduce a pair of values that must agree but are set independently (a description and a behavior, a writer and a reader, a render order and a selection index). Derive both from one source, or snapshot them together so they travel as a unit.

### Conditionals Considered Harmful

While some conditionals are inevitable, through repeated agentic edits our codebase suffers from a number of complicated and repetitive conditional statements. Sometimes the repetition is obfuscated by thin abstractions like explaining variables or helper methods.

Of new, changed and existing conditionals, ask:

Does this conditional represent a domain concept that could be displayed with an explaining variable, helper function, by adding a method/computed property to an existing class which contains the relevant data, or by creating a class to model the concept?

Is this conditional repeated, perhaps behind an existing explaining variable/helper function/method, which should be refactored to share and reuse?

Further, could this code be simplified by factoring out conditional bodies into functions in a Strategy Pattern, where the conditional is "lifted" to instantiate the strategy once and then invoked instead of repeatedly tested? Does the data members of the strategy indicate it should be part of a larger class?

You should consider the conditionals across multiple products or phases. For example, two products may be able to share code if implementation details are abstracted from the common code behind a Strategy facade.

In general, agentic codebases do not use this enough, so you should proactively search for this. If the concept is too tortured to name (too long/too vague) or the abstraction does not pull its weight (only one or a couple of conditionals/one "non-no-op" implementation with only one behavior/the abstraction just wraps an existing property) then this is not the time to use the Strategy Pattern. Sometimes even an explaining variable is redundant.

Disciplined use of this analysis can lead to useful new abstractions forming around a common set of objects.

### Placement

Several products are built on one shared layer, and state one product writes is read by the others. Before implementing, place the behavior by asking which layer owns the state it acts on:

- Behavior lives in the layer that owns its state. A product owns only what other products cannot observe.
- The layer that creates a resource performs every transition of its lifecycle — resume, delete, migrate, recover — through one path that all products call.
- Interpretation of a shared contract is written once, next to the type that defines it. Products render the result; they do not derive it again.
- When a second product needs what a first already has, move the implementation down and make the first product a caller. Do not implement it a second time.

When the owning layer cannot host the behavior yet, record the gap in the plan and PR: which products reach the state, and what they will observe.

### The Matrix

Products, platforms, runtime versions, features and compatibility promises are the axes of a matrix. A cell is where a value on one axis meets a value on another. A change adds a value to an axis, or alters one, and so owns a row: one cell for every value on every other axis.

One value **reaches** another when a user, a process or stored data meets both. Reach is wider than code paths. A user who has two products meets a feature of one and expects it in the other. A file written by one version meets the version that reads it.

Fill every cell in the row with one of:

- **n/a** — nothing meets both. Say why in one clause.
- **supported** — works, with the evidence.
- **missing** — reached but not implemented. Record it as a limitation: who meets the gap and what they see.
- **conflicts** — breaks an assumption the other value relies on. A blocker.

A blank cell is a question, not an answer. A row with no missing or conflicting cells shows that the change fits what exists; whether anyone wants the change is a question for the Need level.

We do not keep the axes' values in a list. Find them afresh from the code, the documentation and the release history. When they cannot be found there, record that as a documentation gap.

### Contracts

When code interprets an external value — a configuration field, an API response, a file format — model the full declared contract from its authoritative schema or types, not the shape observed in examples.

When you change a shared value's shape, event, location, or API, you have changed a contract: grep for every producer, consumer, cache, and reporter (including features from other PRs) and re-verify each. A migration is a write — audit all readers of both the old and new shapes.

#### Storage Contracts

Anything persisted — a file, a row, a directory layout, a naming scheme — is a **storage contract** between every version of every product that reads or writes it. Its path and shape are the contract. Nothing checks both sides of a storage contract, so treat it as more binding than an API.

- Define each path and shape once, in the shared layer, and import it everywhere.
- Creating or deleting a file, directory or row type changes the contract as much as changing its fields does.
- For each change, state what an older reader does with the new shape and what the new reader does with old data. Version shapes, and preserve unknown fields on rewrite.
- The invariant is that every supported version of every product can read what any other wrote, and leaves it readable.

### Reliability

Do not design functions or methods with critical return values which are easily ignored by the caller. If the caller should handle a result, use types which force the caller to handle the result in languages which can do that (Rust, C++.) In other languages (JavaScript, TypeScript) you may need to use continuations, exceptions, etc.

Functions and methods should first check their preconditions, read data, and then write data. Avoid interleaving reads and writes which could cause updates based on "torn" read state. Avoid failing in "half done" write states.

In async code, every `await` is a place where torn reads happen: state read before it may be invalid after it, including via re-entry of the same procedure. Justify each mutating procedure by one of, in order of preference: an atomic section (all reads and writes between the same pair of awaits — single-threadedness is an asset, use it); a snapshot with an identity recheck after the awaits (object identity, never an ID that a rebuild may reuse, and re-check dynamic state like `isRunning`); serialization through an existing queue or mutex; or idempotence.

For every mutable setting that affects behavior, state when a change takes effect (immediately, next tool call, next model request, next session) and make everything that must agree transition at that same boundary. For every resource or pending flag, account for all exits: success, error, cancel, timeout, disposal, replacement, and concurrent re-entry. Never report success when the requested work failed, was killed, or is still running.

Tests must cross the boundary where the risk lives: use the real implementation rather than a stub that re-implements the invariant, and when the risk is in packaging or an older runtime, test the shipped artifact or pin to the minimum runtime's API definitions.

### Comments

Phrase comments for the "eternal now" of the code as the reader will encounter it after your change. Don't refer to ephemeral artifacts the reader doesn't have access to, like your current task, debugging session, alternative designs considered, or the past state of the system. It is appropriate to positively explain design choices or refer to for example, old on-disk serialization formats still supported.

Phrase TODOs as `TODO: What when.` *What* briefly explains what to change; and *when* briefly explains the condition which will "unlock" the clean-up. Think critically about "when": If the cleanup is not blocked now, prefer to just do it. If the cleanup is likely blocked forever, then a TODO is not appropriate, but a comment briefly explaining the compromise/limitation.

### Triage Test Failures

Before fixing a test failure found while working on a PR, fetch the current target branch and check whether it fails **in the same way upstream**. Compare the failing test, assertion/error and relevant OS, runtime and configuration using upstream CI logs or an isolated baseline run with the same command. Record the revisions and evidence. Red upstream CI, an unchanged test file, or a failure outside the diff is not enough to call it pre-existing; check whether this PR introduces or worsens it.

- If upstream already fixed the failure, rebase onto that fix and rerun the relevant checks instead of duplicating it.
- If the same failure exists upstream and this PR does not worsen it, keep the fix out of this PR. Reuse an existing repair PR or create a focused PR from the target branch to green main; land that first, then rebase and revalidate the original PR. Do not bundle unrelated repairs just because they are small.
- If the failure is introduced or worsened by this PR, fix the regression here. If the baseline is inconclusive or the failure is environment-specific, investigate and report that limitation rather than assume it is upstream or change unrelated code to make a local run green.

Never describe a failed, skipped, interrupted or unrun check as passing. Keep branch validation separate from upstream-failure evidence.

## Validate Changes with Computer Use

If you have access to computer use, then use it to validate that your change works as expected and has not broken anything. This can be a useful signal boost beyond unit tests.

## Pull Requests

### Self-Reviews

Before creating or updating a PR, use the `inventory-review` skill to reflect on the PR as a whole and conduct a `pr-final-check`.

### Branch Naming

Pull request branch names should be prefixed with dpc/ and have a brief, compelling topic. Feel free to rename the local branch name to match the topic name. For example, in a worktree you may find yourself working with a local branch name like 'cline5' or 'main' but you should rename it to 'fix-foo' and make the remote branch 'dpc/fix-foo'.

### Pull Request Text

Use the `writing-editing-prose` skill in addition to the following rules:

In pull requests, as in comments, stick to the facts. The PR description should not dwell on ephemeral debugging steps, "phases" of implementation work, etc. Instead, motivate the change by following the Pyramid Principle. If this is hard, critically consider whether the code is high quality. The PR description should be a natural introduction to the code.

Treat the description as one edited explanation, not an append-only log. During `pr-final-check`, look for sections to cut or consolidate as well as claims to update. Keep useful limitations and test instructions; leave accurate, focused, concise text alone. Verify the published description against the final diff and current validation evidence before handing the PR back for review.

When a PR template section does not apply (for example, the Screenshots section on a change with nothing to show), delete the heading. Never leave commentary explaining why the section is empty.

Finally:
- Be brief
- Adhere to the repository's style for PR descriptions

### Testing and PR Test Plans

PRs must include a test plan that a new teammate could follow their first week.

PR test plans SHOULD show specific commands to run relevant tests. Put automated commands in a fenced Markdown code block, not in individual bullets, so that the reader can copy and paste them. When several commands run from the same directory, change to that directory once and return when finished: use `cd foo/bar` and `cd -`, `pushd foo/bar` and `popd`, or the appropriate Windows equivalent for a Windows-specific test. Do not repeat `cd foo/bar &&` before every command.

Do not include `check-types`, `format`, `lint`, `build`, or similar commands merely because the hooks run them. These checks are not a test procedure. Include one only when the change affects that tool and running the command specifically tests the change, such as a formatter or linter change.

DON'T list tests added/changed with commentary; that doesn't help people run the tests. The tests themselves should be self explanatory about what they are testing.

Automated tests are preferable to manual tests. However manual tests can be useful for QA or curious people, so adding brief manual test plans is also good. Relying only on manual tests should only happen in exceptional situations.

When computer-use skills are available, use them to verify the change and include a manual test plan. After any shell commands needed to start the system under test, write the manual procedure as numbered steps that a person can follow. At each step that exposes behavior central to the change, state what the tester should verify. Keep the procedure short and deterministic. Put shared setup requirements in a brief preamble instead of spelling out every setup action in the steps.

"Performative" automated testing--writing tests which provide little sensitivity to likely changes of interest--is harmful because it clutters the test suite and distracts from the effective tests. Such tests MUST be avoided.

DON'T write "what could break" in test plans. We should be striving for code which doesn't break. If improvements are actionable right now within the scope of the PR, then do the work. If the work is actionable right now, but outside the scope of the PR, consider a separate clean-up or refactoring PR. If work is not actionable right now, but will be when conditions are right, use a TODO in the code. If the code is permanently defective, use a caveat.

## Linear

Don't comment about ephemera like debugging sessions in Linear. If we have specific findings it is important to share, we can do that, but in general it is better to fix things, create a PR, and mention the Linear issue in the PR. This will automatically create a link between them.
