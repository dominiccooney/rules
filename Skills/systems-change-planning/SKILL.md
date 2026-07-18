---
name: systems-change-planning
description: Plan a non-trivial code change as a systems change before implementing. Locates the essential complexity, chooses the simplest structure to derisk it, and derives contracts, environments, and consistency boundaries from the change — use before starting implementation of features, fixes touching configuration/state/concurrency, or anything crossing process or host boundaries.
---

# Systems-Change Planning

Produce a short written plan BEFORE editing code. The plan's purpose is to
make later review cheap: every declared invariant collapses a family of
review questions into one check.

Skip this skill for plumbing (renames, doc edits, mechanical refactors with
no behavior change). If step 1 finds no essential complexity, say so and
stop — a one-line plan is a valid output.

## Step 1 — Model the essential complexity

1. **Name the central user-visible promise** in one sentence.
   ("The shell named in the tool prompt is the shell that runs the commands.")
2. **Locate the essential complexity** — the irreducibly hard thing, usually
   one sentence. ("A mutable setting feeds both prompting and execution,
   which must agree.") If you cannot find one, the task is plumbing; stop.
3. **Choose the simplest structure that makes the failure unrepresentable** —
   not guarded against, unrepresentable. Candidates, in order of preference:
   - a single shared resolver both readers call
   - a snapshot type whose fields travel together
   - a state machine with explicit transitions
   - a declared consistency boundary (see step 3)
4. **State the invariants** the structure establishes, one sentence each.
5. **List non-goals explicitly.** These bound both implementation and review.

## Step 2 — Derive the plan from the change (not from brainstorming)

Answer only the questions raised by boundaries the change actually touches:

| If the change touches… | Answer… |
|---|---|
| An external contract (config schema, API, file format) | Where is the authoritative type/schema for the exact supported version range? What is its FULL declared shape (arrays, nulls, legacy values) — not just the shape observed in examples? |
| Runtime APIs | What is the oldest runtime that executes this code path (remote hosts, JetBrains-bundled Node, oldest supported VS Code)? |
| Child processes / executables | Which environment owns the executable and the cwd? (A path valid inside WSL is ENOENT on the Windows host.) |
| Packaging | Is every dependency present in the extracted artifact with the repository's node_modules unavailable? |
| Shared or persisted state | Who are ALL the writers and readers? Do they use the same resolver/format? Grep for every consumer before editing. |
| Emulated host behavior | Verify against upstream types, docs, tests, then source — in that order. Do not infer the contract from our own codebase. |

Then build the **execution-boundary matrix**: one row per (process, OS/namespace,
runtime version, config source, artifact) combination that actually executes
the changed path. Rows that are unsupported get an explicit "unsupported"
entry, never a silent assumption of the dev environment.

## Step 3 — Declare the consistency boundary

For every mutable setting or dependency involved, state exactly when a change
becomes effective: immediately / next tool call / next model request / next
turn / next session / next restart. All values that must agree transition at
that same boundary. Write the boundary as one sentence in the plan and later
in a code comment.

## Step 4 — Plan tests at the boundary where risk lives

| Risk | Test at |
|---|---|
| Schema interpretation | contract fixture using the real declared shape (incl. the branches not taken) |
| Packaging | extracted artifact, repo dependencies renamed away |
| Runtime floor | typecheck/test pinned to the minimum runtime's API definitions |
| Config transition | change the setting immediately before AND immediately after the declared boundary |
| Cross-module behavior | integration through the real callers — never a stub that re-implements the invariant |

## Step 5 — Decide refactor-first

If implementing the model forces touching code for reasons OTHER than the
behavior change, split a preparatory refactor into its own commit/PR ("make
the change easy, then make the easy change"). If the change is already local,
skip — a mandatory prep-refactor is its own form of scope creep.

## Step 6 — Draft the PR description skeleton

Sketch the eventual PR description now, with gaps: the Situation/Complication/
Answer introduction (the Answer is the central promise from step 1) and the
test plan's commands with placeholders for results. If the introduction won't
write, the design is not understood yet — go back to step 1. Keep it to a
dozen lines; this is a sketch to complete at PR time, not a PRFAQ.

## Output format

A plan of roughly one page: promise, essential complexity, chosen structure,
invariants (numbered), consistency boundary, boundary matrix, test plan,
non-goals, refactor-first decision, PR skeleton. Then implement in the order:
model → API → tests-on-the-real-implementation → wiring.
