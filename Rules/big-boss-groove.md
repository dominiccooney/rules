# Writing

We write so that the reader understands what we want and does it. Simple, direct writing serves that purpose. Writing that tries to sound clever or wise gets in the reader's way. Our readers live all over the world and many read English as a second language. Be exact about details and kind to people.

Write in four steps: organize, write, revise, edit. Each step below has its own checks. Revise and edit after the draft exists, as separate passes; a draft written with care still contains the faults these passes look for.

## Tone

When writing for others: Affect a wilful, dynamic, welcoming, inclusive, pro-people, humble, inquisitive tone. Avoid closed-ended questions.

When writing for me, you can be as direct as you like. I am an Australian and I'm comfortable with very direct communication.

## Two Audiences

This document's concepts — the levels, placement, the matrix, storage contracts, invariants, consistency boundaries — are a working vocabulary between you and me. Use it freely in plans, in development discussion, and in your own notes.

The author of code you review does not share that vocabulary. Give them the finding in the words of the code and the product: name the two things that meet and what goes wrong where they meet. Write "a session started in the desktop app and deleted from the CLI leaves its worktree behind," not "the CLI cell of the worktree row is missing." Write "users who rely on the foreground terminal lose it, and nothing in the PR says they were asked," not "this fails the need check." Use terms from the code and the product. Do not use terms from this document.

When writing for external contributors, consider adding a small "plus alpha" of thanks and friendly encouragement. These people are not employees and took time to engage with us and we should thank them for that. If we can't act on their direct suggestions we are still grateful for their time and input and consider adding a phrase that indicates we're open to future contributions from them. (We usually DON'T need such language for our teammates who will appreciate brevity more.)

## Organize: The Pyramid Principle

In written communication beyond a few sentences, for example bug reports, PR descriptions, and module comments, use the Pyramid Principle to communicate clearly.

Here is a step-by-step guide to applying the Pyramid Principle:

1. What SUBJECT are you discussing?
2. What QUESTION are you answering in the reader's mind?
3. What is the ANSWER?
4. What is the SITUATION? Make the first non-controversial statement you can about what is going on.
5. What is the COMPLICATION? Ask yourself, "so what?" Think of something in the SITUATION to raise the QUESTION.
6. Do the QUESTION and ANSWER still follow? If not, change the QUESTION to the one raised by the COMPLICATION, or use a different COMPLICATION.

Start to compose an introduction. You can vary the order to change the tone:

CONSIDERED: Situation, Complication, Solution
DIRECT: Solution, Situation, Complication
CONCERNED: Complication, Situation, Solution

7. What NEW QUESTION is raised by the ANSWER? Then, the KEY LINE not only answers this question but gives the plan of the PR description. Decide whether you will answer INDUCTIVELY or DEDUCTIVELY.

If the group is inductive, it must either deal with cause and effect and should be ordered by time; or divide a whole into its parts and be ordered by structure; or classify like things and be
ordered by rank.

Time order: Ask yourself, "What would I do first if I were doing this? What second? etc."

Structural: Are the pieces mutually exclusive and collectively exhaustive (MECE) in terms of the whole? How do you order the pieces? To reflect a process, use time order; to emphasize location, use structural order (for example, geography); otherwise rank them (by whatever is relevant--size, priority, etc.)

Ranking: What do you label the points as? (What is the "group noun"?) Can you find anything more specifically the same about them? Can you justify their order on that basis? Are there any missing?

When using the Pyramid Principle, do NOT use "Situation", "Complication", etc. as headings. These are conceptual labels for you, but the structure should be invisible and self-supporting to the reader so that they can focus on the content and meaning of your writing.

## Write

Write the draft plainly. Say what the thing is, what is wrong with it, and what to do. Concrete nouns and verbs carry the meaning; adjectives and adverbs rarely add any.

Every sentence mixes *given* information, which the reader already has from earlier sentences or from context, with *new* information, which the sentence introduces. Readers understand a sentence by attaching the new information to the given. So put given information first and new information last. The same rule orders a paragraph: each sentence begins from what the sentence before it left the reader holding.

A counter-example, with new information first and given information last:

> Carefully consider word order. In a sentence, introduce new concepts later; put familiar words earlier. Flowing writing is created by ordering concepts from novel to familiar. Easy-to-comprehend writing is flowing writing.

Prefer the active voice, but use the passive when it puts the given information first.

Use parallel structure for parallel ideas. Above: "put given information first and new information last."

## Revise

Revise the whole draft before editing lines. Read it as the reader, who does not know what you meant. Check:

- Does the first paragraph answer the reader's question? (See the Pyramid Principle.)
- Is every noun phrase present that the reader needs? Compare the draft with what you know. A step you skipped in the text because it was obvious to you is missing for the reader.
- Are the paragraphs in the reader's order, not the order you discovered things in?
- Could the reader act on the draft and do the wrong thing? Find the sentence that permits the wrong reading and fix that sentence.

Revising also catches a fault of your own: in a long reply or on an abstract topic, the draft can turn into fluent prose that says nothing the reader can act on. Test each paragraph by restating it as a plain fact or a plain instruction. Shorten or delete any paragraph that will not restate.

## Edit Line by Line

Edit the draft line by line, after revising. The faults below are listed with the ones that cost the reader most first; check for them in that order.

**Missed connections.** Every *this*, *that*, *it*, *one*, *these*, *which* and *such* must have one obvious noun as its referent, in the same sentence or the one before. If a reader could attach the pronoun to two nouns, repeat the noun. If the referent is a whole clause or idea, name it: "this gap," "that check," not "this." The same test applies to *the former*, *the latter*, *respectively* and to any noun phrase that assumes an earlier definition.

**Slogans and antitheses.** A balanced pair ("X, not Y"; "a question, not an answer") and a sentence that could be quoted as a maxim both state a conclusion without the fact or instruction behind it. Rewrite each as a plain statement of what is so and what to do. The plain version is often longer. Keep it anyway.

**Figures of speech.** Delete clichés. Do not invent metaphors. A term defined in this document (for example *reach*) may be used because the reader can look up the definition. When a comparison helps, compare with a common object that every reader knows, and state the plain meaning beside it.

**Consistent language.** One word for one concept. A second word for the same concept implies a distinction the reader will look for and not find.

**Simple language.** Choose the short, common word. Words of Anglo-Saxon origin are usually shorter, plainer and known to more readers than their Latin or French equivalents: "teammate" over "colleague," "start" over "initiate," "use" over "utilize." When two words compete, look at where each came from and what it once meant. Ut multitudini variae placeas, noli lingua Latina uti.

**Unnecessary words.** Cut them. Then cut the sentence that repeated the sentence before it. A short text that says everything the reader needs is complete; do not add to it. Each revision of a text should leave it the same length or shorter. PR descriptions break this rule most often: each update adds a paragraph and removes none. When you update a description, delete or replace text before you add any.

**Verbs.** Prefer the active voice and a finite verb over a gerund or a nominalization ("we decided," not "the decision was made"; "delete," not "deletion of"). Keep the passive where it puts given information first.

**Sentence length.** Vary it. A run of short sentences reads as a list of slogans; a run of long ones tires the reader.

**Closing formulas.** Delete stock closings ("Say the word and I'll…", "Let me know if…"). End when the content ends.

## Typesetting

Wrap git commit messages at 76 characters.

GitHub PRs and issue text will be wrapped by the user agent. Don't add carriage returns within paragraphs.

# Canonical Rules and Skills

Before editing a rule or skill, check whether its canonical copy exists under
`~/Documents/Cline`. When it does, edit the canonical copy there, then run the
repository's applicable sync script and verify the installed copy matches.

Treat copies under `~/.cline` and other installed or generated locations as
build products, not sources. Direct edits there will be overwritten by the next
sync. Commit and push durable rule and skill changes from `~/Documents/Cline`.

# Levels of a Change

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

# Workflow: Plan, Implement, Review

For any change that is more than plumbing (i.e. it touches configuration, state, concurrency, external contracts, is reachable from more than one product, crosses a process/host boundary, or removes or changes the default of user-visible behavior), bracket the work with two skills:

- **Before implementing**, use the `systems-change-planning` skill. It locates the essential complexity, chooses the simplest structure to make failures unrepresentable, and derives invariants, environments, and the consistency boundary from the change.
- **Before opening or updating a PR**, use the `inventory-review` skill. It enumerates the resources, state machines, decision points, contracts, and suspension points in the diff and applies fixed per-type checks. Findings are failed checks — there is no quota, and zero findings is a legitimate outcome. Discovery is read-only; triage before fixing.

When reviewing someone else's PR, choose the skill by the author and the PR's age: `teammate-pr-review` for a fresh PR from a repository member, or from an author I name as trusted; `backlog-pr-review` for everyone else and for any PR roughly two weeks old or older. Both run `inventory-review` on the diff.

The plan's declared invariants shrink the review: a stated consistency boundary collapses whole families of interleaving questions into one check.

As part of planning, draft the PR description skeleton (see Pull Request Text below): the Situation/Complication/Answer introduction and the test plan's commands, with gaps where results will go. The Answer is the plan's central promise; if you cannot draft the introduction, the design is not understood yet. Keep it to a dozen lines — this is a sketch to be completed at PR time, not an Amazon-style PRFAQ.

For **every PR, including plumbing and documentation-only changes**, run `pr-final-check` after implementation and any engineering-review fixes, before creating or updating the PR and handing it back for review. This required final pass removes dead code (production code used only by tests is dead), checks comments against the surviving implementation, and simplifies the whole PR description. Repeat after review fixes, rebases and stack changes; an earlier pass does not cover a changed diff. The skill owns the procedure and completion evidence.

## Simplicity

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

## Placement

Several products are built on one shared layer, and state one product writes is read by the others. Before implementing, place the behavior by asking which layer owns the state it acts on:

- Behavior lives in the layer that owns its state. A product owns only what other products cannot observe.
- The layer that creates a resource performs every transition of its lifecycle — resume, delete, migrate, recover — through one path that all products call.
- Interpretation of a shared contract is written once, next to the type that defines it. Products render the result; they do not derive it again.
- When a second product needs what a first already has, move the implementation down and make the first product a caller. Do not implement it a second time.

When the owning layer cannot host the behavior yet, record the gap in the plan and PR: which products reach the state, and what they will observe.

## The Matrix

Products, platforms, runtime versions, features and compatibility promises are the axes of a matrix. A cell is where a value on one axis meets a value on another. A change adds a value to an axis, or alters one, and so owns a row: one cell for every value on every other axis.

One value **reaches** another when a user, a process or stored data meets both. Reach is wider than code paths. A user who has two products meets a feature of one and expects it in the other. A file written by one version meets the version that reads it.

Fill every cell in the row with one of:

- **n/a** — nothing meets both. Say why in one clause.
- **supported** — works, with the evidence.
- **missing** — reached but not implemented. Record it as a limitation: who meets the gap and what they see.
- **conflicts** — breaks an assumption the other value relies on. A blocker.

A blank cell is a question, not an answer. A row with no missing or conflicting cells shows that the change fits what exists; whether anyone wants the change is a question for the Need level.

We do not keep the axes' values in a list. Find them afresh from the code, the documentation and the release history. When they cannot be found there, record that as a documentation gap.

## Contracts

When code interprets an external value — a configuration field, an API response, a file format — model the full declared contract from its authoritative schema or types, not the shape observed in examples.

When you change a shared value's shape, event, location, or API, you have changed a contract: grep for every producer, consumer, cache, and reporter (including features from other PRs) and re-verify each. A migration is a write — audit all readers of both the old and new shapes.

### Storage Contracts

Anything persisted — a file, a row, a directory layout, a naming scheme — is a **storage contract** between every version of every product that reads or writes it. Its path and shape are the contract. Nothing checks both sides of a storage contract, so treat it as more binding than an API.

- Define each path and shape once, in the shared layer, and import it everywhere.
- Creating or deleting a file, directory or row type changes the contract as much as changing its fields does.
- For each change, state what an older reader does with the new shape and what the new reader does with old data. Version shapes, and preserve unknown fields on rewrite.
- The invariant is that every supported version of every product can read what any other wrote, and leaves it readable.

## Reliability

Do not design functions or methods with critical return values which are easily ignored by the caller. If the caller should handle a result, use types which force the caller to handle the result in languages which can do that (Rust, C++.) In other languages (JavaScript, TypeScript) you may need to use continuations, exceptions, etc.

Functions and methods should first check their preconditions, read data, and then write data. Avoid interleaving reads and writes which could cause updates based on "torn" read state. Avoid failing in "half done" write states.

In async code, every `await` is a place where torn reads happen: state read before it may be invalid after it, including via re-entry of the same procedure. Justify each mutating procedure by one of, in order of preference: an atomic section (all reads and writes between the same pair of awaits — single-threadedness is an asset, use it); a snapshot with an identity recheck after the awaits (object identity, never an ID that a rebuild may reuse, and re-check dynamic state like `isRunning`); serialization through an existing queue or mutex; or idempotence.

For every mutable setting that affects behavior, state when a change takes effect (immediately, next tool call, next model request, next session) and make everything that must agree transition at that same boundary. For every resource or pending flag, account for all exits: success, error, cancel, timeout, disposal, replacement, and concurrent re-entry. Never report success when the requested work failed, was killed, or is still running.

Tests must cross the boundary where the risk lives: use the real implementation rather than a stub that re-implements the invariant, and when the risk is in packaging or an older runtime, test the shipped artifact or pin to the minimum runtime's API definitions.

### Test Failure Triage

Before fixing a test failure found while working on a PR, fetch the current target branch and check whether it fails **in the same way upstream**. Compare the failing test, assertion/error and relevant OS, runtime and configuration using upstream CI logs or an isolated baseline run with the same command. Record the revisions and evidence. Red upstream CI, an unchanged test file, or a failure outside the diff is not enough to call it pre-existing; check whether this PR introduces or worsens it.

- If upstream already fixed the failure, rebase onto that fix and rerun the relevant checks instead of duplicating it.
- If the same failure exists upstream and this PR does not worsen it, keep the fix out of this PR. Reuse an existing repair PR or create a focused PR from the target branch to green main; land that first, then rebase and revalidate the original PR. Do not bundle unrelated repairs just because they are small.
- If the failure is introduced or worsened by this PR, fix the regression here. If the baseline is inconclusive or the failure is environment-specific, investigate and report that limitation rather than assume it is upstream or change unrelated code to make a local run green.

Never describe a failed, skipped, interrupted or unrun check as passing. Keep branch validation separate from upstream-failure evidence.

## Comments

Phrase comments for the "eternal now" of the code as the reader will encounter it after your change. Don't refer to ephemeral artifacts the reader doesn't have access to, like your current task, debugging session, alternative designs considered, or the past state of the system. It is appropriate to positively explain design choices or refer to for example, old on-disk serialization formats still supported.

Phrase TODOs as `TODO: What when.` *What* briefly explains what to change; and *when* briefly explains the condition which will "unlock" the clean-up. Think critically about "when": If the cleanup is not blocked now, prefer to just do it. If the cleanup is likely blocked forever, then a TODO is not appropriate, but a comment briefly explaining the compromise/limitation.

## Pull Requests

Pull request branch names should be prefixed with dpc/ and have a brief, compelling topic. Feel free to rename the local branch name to match the topic name. For example, in a worktree you may find yourself working with a local branch name like 'cline5' or 'main' but you should rename it to 'fix-foo' and make the remote branch 'dpc/fix-foo'.

### Pull Request Text

In pull requests, as in comments, stick to the facts. The PR description should not dwell on ephemeral debugging steps, "phases" of implementation work, etc. Instead, motivate the change by following the Pyramid Principle. If this is hard, critically consider whether the code is high quality. The PR description should be a natural introduction to the code.

Treat the description as one edited explanation, not an append-only log. During `pr-final-check`, look for sections to cut or consolidate as well as claims to update. Keep useful limitations and test instructions; leave accurate, focused, concise text alone. Verify the published description against the final diff and current validation evidence before handing the PR back for review.

When a PR template section does not apply (for example, the Screenshots section on a change with nothing to show), delete the heading. Never leave commentary explaining why the section is empty.

Finally:
- Be brief
- Adhere to the repository's style for PR descriptions

### Testing and PR Test Plans

PRs must include a test plan that a new teammate could follow their first week.

PR test plans SHOULD show specific commands to run relevant tests. DON'T list tests added/changed with commentary, that doesn't help people run the tests. The tests themselves should be self explanatory about what they are testing.

Automated tests are preferable to manual tests. However manual tests can be useful for QA or curious people, so adding brief manual test plans is also good. Relying only on manual tests should only happen in exceptional situations.

"Performative" automated testing--writing tests which provide little sensitivity to likely changes of interest--is harmful because it clutters the test suite and distracts from the effective tests. Such tests MUST be avoided.

DON'T write "what could break" in test plans. We should be striving for code which doesn't break. If improvements are actionable right now within the scope of the PR, then do the work. If the work is actionable right now, but outside the scope of the PR, consider a separate clean-up or refactoring PR. If work is not actionable right now, but will be when conditions are right, use a TODO in the code. If the code is permanently defective, use a caveat.

## Linear

Don't comment about ephemera like debugging sessions in Linear. If we have specific findings it is important to share, we can do that, but in general it is better to fix things, create a PR, and mention the Linear issue in the PR. This will automatically create a link between them.
