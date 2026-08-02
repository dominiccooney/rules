---
name: inventory-review
description: Pre-submission adversarial review of a diff, driven by inventory rather than intuition. Enumerates the resources, state machines, decision points, contracts, and suspension points in the change, applies fixed per-type checks, and triages failed checks into blocker/follow-up/limitation. Use before opening or updating a PR, or when asked to review a diff.
---

# Inventory Review

Review a diff by enumeration, not inspiration. Findings are failed checks
against an inventory, so every finding arrives evidence-backed and **zero
findings is a legitimate output** when the inventory is complete. There is
no quota; do not reach.

## Invocation contexts

This skill has two independent entry points:

1. **Pre-PR development review:** invoke it on the developer's local diff before
   opening or updating a PR. Fix or explicitly triage its blockers before
   submission.
2. **Existing-PR engineering review:** `backlog-pr-review` invokes it when a
   contributor PR survives Gates 1–5. Return the findings to that workflow,
   which owns the review action and contributor communication.

The backlog-review entry point supplements rather than replaces pre-PR review.
In either context, this skill owns read-only discovery and finding triage; its
caller owns edits, GitHub actions, and other state changes.

**Discovery is strictly read-only.** Build the full inventory and findings
list before proposing or making any edit. Do not broaden scope during review.

## Step 1 — Build the inventory from the diff

Enumerate, citing file:line for each item:

1. **Resources** created or owned: streams, processes, terminals, listeners,
   timers, temp files, child sandboxes.
2. **State machines & pending state**: anything named status/pending/deferred/
   detached/queued, caches, flags set now and read later.
3. **Decision points**: every branch on external input. Record the input's
   FULL declared domain (from its schema/types), including values no branch
   handles.
4. **Changed contracts**: fields, events, file formats, options, orderings —
   anything with more than one producer or consumer.
5. **Suspension points**: every `await`, `yield`, and event-handler
   registration inside mutating procedures.
6. **External contracts consumed**: schemas, runtime APIs, executables,
   packaging assumptions.
7. **Caller-inherited obligations**: for every procedure the diff adds an
   exit to (early return, throw, new branch), the state its CALLERS establish
   before delegating — phases, spinners, pending flags, locks, pre-emitted
   UI. Read the callback/option doc comments in the touched file: an
   obligation documented on one callback (e.g. "the failure must move the
   phase to terminal") binds every sibling exit, not just the annotated one.
8. **Declared consistency boundaries**: every mutex, queue, or "X and Y are
   serialized" invariant the diff introduces or relies on.

## Step 2 — Apply the per-type checks

**Resources → exit/lifecycle table.** For each resource, walk every exit:

| Exit | Settled exactly once? | Resource closed/owned? | User-visible status truthful? | Deferred work drained? |
|---|---|---|---|---|
| success / error / cancel / timeout / dispose / replacement-rebuild / concurrent re-entry | | | | |

"Truthful" means: the system must not report success while the requested work
failed, was killed, or is still running.

**State machines.** Are all transitions covered? Are illegal states
representable? Who invalidates the cache on install/uninstall/workspace/
provider change?

**Decision points → input-domain check.** Does the set of branches cover the
full declared domain?
Does the fix cover the whole contract on ALL platforms it applies to, not
just the platform where the bug was reported?

**Contracts → consumer audit.** For each changed contract, grep for every
producer, consumer, cache, persister, and reporter — including features from
other PRs. Verify each consumer's assumptions still hold. A migration is a
WRITE: audit every reader of the new shape and every reader still expecting
the old one.

**Suspension points → await audit.** For each mutating procedure: list its
awaits in order; for each, name the state read before and used after, and
what can invalidate it in between — including re-entry of the same procedure.
Each must be justified by one of: atomic section (reads+writes between the
same pair of awaits), snapshot + identity recheck (object identity, never an
ID that rebuilds reuse; re-check isRunning-style dynamic state), serialization
through an existing queue/mutex, or idempotence.

**External contracts → environment check.** Oldest supported runtime has the
API? Dependency present in the shipped artifact? Executable exists in the
host (not guest) environment? Tests cross the real boundary rather than
re-implementing the invariant in a stub?

**Caller-inherited obligations → exit-inheritance check.** Add every
caller-established state to the exit/lifecycle table alongside resources the
procedure creates itself. A NEW exit added by the diff inherits the full
settlement obligation of the exits that preceded it; "return early" is a
settlement decision, not an absence of one.

**Declared boundaries → resource-rooted enrollment.** Enumerate participants
from the PROTECTED RESOURCE, not from the diff: grep for every reader and
writer of the protected state and either enroll each in the boundary or
record an explicit, justified exemption. An unenrolled writer silently voids
the invariant — and every review conclusion that leaned on it. Then check
each identity recheck inside the boundary against its purpose: object
identity for ownership/cleanup ("never touch a resource someone else now
owns"); logical identity (an ID that rebuilds deliberately reuse) for
targeting continuing work at the same conversation/task. Using object
identity for targeting makes legitimate rebuilds silently cancel work;
using logical identity for cleanup makes you destroy a successor.

## Step 3 — Findings and triage

Each finding cites its inventory item and failed check, plus: concrete
supported **trigger**, **causal chain** through the code, user-visible
**impact**, affected **population**, and **recovery** (auto / obvious-retry /
silent / persistent / destructive). If trigger or chain cannot be stated
concretely, it is a question for the author, not a finding.

Triage each finding:

- **Blocker** — must be fixed in this PR. A finding is a blocker when it is
  real, introduced or touched by this PR, and fixable locally with effort
  proportional to the PR's scope. This includes: violates the PR's central
  promise or a declared invariant; breaks a supported environment; false
  success or misleading UI; data loss / security / unintended code execution;
  silent or hard to recover; dead in the shipped artifact; turns an opt-in
  limitation into a default regression. It also includes duplication that will
  drift under maintenance when the fix is a few lines in files the PR already
  touches.
- **Follow-up** — real but genuinely out of scope for this PR: unusual
  unsupported trigger, obvious+harmless+recoverable, pre-existing without
  increased exposure, or the fix is disproportionate architecture work that
  belongs in its own PR. When in doubt between blocker and follow-up, ask: is
  the fix proportional to the PR's scope and in files the PR already touches?
  If yes, it is a blocker. Do not use "follow-up" to defer fixes that are
  small, local, and in-scope just because the code works today — duplication
  that can't get out of sync is a defect, not a future concern.
- **Accepted limitation** — deliberate, acceptable, but non-obvious: request
  a code comment or PR caveat. Before accepting a limitation, verify the
  stated rationale against the codebase. An accepted limitation based on a
  false premise (e.g. "can't import due to cross-world barrier" when runtime
  imports from that package already exist) is an unreviewed defect.
- **Not actionable** — record why, then drop.

Apply the **smallest sufficient response** to blockers. Do not recommend
broad refactoring unless a blocker cannot be fixed locally.

## Step 4 — Re-inventory after fixes

Fixes are diffs too. Each round of fixes introduces new exits, new locks,
new callbacks — each with its own inherited obligations and boundary
enrollment. Before resubmitting, run steps 1–3 over the fix delta itself
(usually a minutes-long pass, not a full re-review). Do not only re-verify
the original findings.

## Step 5 — Residual pass (optional, usually empty)

One short free-form pass: "anything cross-cutting the inventory missed?"
Expected answer: nothing. Do not pad.

## Output format

1. Inventory (numbered, with file:line)
2. Checks applied per item (terse; "OK" is a fine result)
3. Findings with triage labels
4. For blockers only: smallest sufficient fix, and the test that would have
   caught it at the boundary where the risk lives
