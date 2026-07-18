## Workflow: Plan, Implement, Review

For any change that is more than plumbing (i.e. it touches configuration, state, concurrency, external contracts, or crosses a process/host boundary), bracket the work with two skills:

- **Before implementing**, use the `systems-change-planning` skill. It locates the essential complexity, chooses the simplest structure to make failures unrepresentable, and derives invariants, environments, and the consistency boundary from the change.
- **Before opening or updating a PR**, use the `inventory-review` skill. It enumerates the resources, state machines, decision points, contracts, and suspension points in the diff and applies fixed per-type checks. Findings are failed checks — there is no quota, and zero findings is a legitimate outcome. Discovery is read-only; triage before fixing.

The plan's declared invariants shrink the review: a stated consistency boundary collapses whole families of interleaving questions into one check.

As part of planning, draft the PR description skeleton (see Pull Request Text below): the Situation/Complication/Answer introduction and the test plan's commands, with gaps where results will go. The Answer is the plan's central promise; if you cannot draft the introduction, the design is not understood yet. Keep it to a dozen lines — this is a sketch to be completed at PR time, not an Amazon-style PRFAQ.

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

## Contracts

When code interprets an external value — a configuration field, an API response, a file format — model the full declared contract from its authoritative schema or types, not the shape observed in examples.

When you change a shared value's shape, event, location, or API, you have changed a contract: grep for every producer, consumer, cache, and reporter (including features from other PRs) and re-verify each. A migration is a write — audit all readers of both the old and new shapes.

## Reliability

Do not design functions or methods with critical return values which are easily ignored by the caller. If the caller should handle a result, use types which force the caller to handle the result in languages which can do that (Rust, C++.) In other languages (JavaScript, TypeScript) you may need to use continuations, exceptions, etc.

Functions and methods should first check their preconditions, read data, and then write data. Avoid interleaving reads and writes which could cause updates based on "torn" read state. Avoid failing in "half done" write states.

In async code, every `await` is a place where torn reads happen: state read before it may be invalid after it, including via re-entry of the same procedure. Justify each mutating procedure by one of, in order of preference: an atomic section (all reads and writes between the same pair of awaits — single-threadedness is an asset, use it); a snapshot with an identity recheck after the awaits (object identity, never an ID that a rebuild may reuse, and re-check dynamic state like `isRunning`); serialization through an existing queue or mutex; or idempotence.

For every mutable setting that affects behavior, state when a change takes effect (immediately, next tool call, next model request, next session) and make everything that must agree transition at that same boundary. For every resource or pending flag, account for all exits: success, error, cancel, timeout, disposal, replacement, and concurrent re-entry. Never report success when the requested work failed, was killed, or is still running.

Tests must cross the boundary where the risk lives: use the real implementation rather than a stub that re-implements the invariant, and when the risk is in packaging or an older runtime, test the shipped artifact or pin to the minimum runtime's API definitions.

## Comments

Phrase comments for the "eternal now" of the code as the reader will encounter it after your change. Don't refer to ephemeral artifacts the reader doesn't have access to, like your current task, debugging session, alternative designs considered, or the past state of the system. It is appropriate to positively explain design choices or refer to for example, old on-disk serialization formats still supported.

Phrase TODOs as `TODO: What when.` *What* briefly explains what to change; and *when* briefly explains the condition which will "unlock" the clean-up. Think critically about "when": If the cleanup is not blocked now, prefer to just do it. If the cleanup is likely blocked forever, then a TODO is not appropriate, but a comment briefly explaining the compromise/limitation.

## Pull Requests

Pull request branch names should be prefixed with dpc/ and have a brief, compelling topic. Feel free to rename the local branch name to match the topic name. For example, in a worktree you may find yourself working with a local branch name like 'cline5' or 'main' but you should rename it to 'fix-foo' and make the remote branch 'dpc/fix-foo'.

### Pull Request Text

In pull requests, as in comments, stick to the facts. The PR description should not dwell on ephemeral debugging steps, "phases" of implementation work, etc. Instead, motivate the change by following the Pyramid Principle:

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

If this is hard, critically consider whether the code is high quality. The PR description should be a natural introduction to the code.

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
