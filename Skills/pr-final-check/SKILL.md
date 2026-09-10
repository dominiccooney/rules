---
name: pr-final-check
description: Required final pass before creating or updating any PR, including review fixes, rebases and stack changes. Remove dead production code (including code used only by tests), refresh stale comments, and simplify the whole PR description against the final diff and current validation evidence.
---

# PR Final Check

Hand reviewers a focused change: live code, accurate comments, and a concise
description of what ships. Run after implementation and engineering-review
fixes, before publishing or handing an updated PR back for review. This applies
to small and documentation-only PRs too; mark code checks not applicable when
there is no code change. It does not replace engineering review or grant
permission to edit another contributor's branch or PR.

## 1. Establish the final scope

Read the full diff against the PR's current target branch, including local
changes intended for submission, not just the latest commit. Read the current
PR description (or draft), relevant review feedback, and validation evidence.
Record the base/head revisions and any uncommitted changes being checked.

Inspect changed definitions and paths whose callers the PR removes or replaces.
Search the whole source tree for their consumers, including outside changed
files. Exclude dependencies and build output from source searches; inspect
generated registrations or shipped artifacts separately when they establish
reachability. Keep unrelated pre-existing cleanup out of this PR.

## 2. Remove dead code

For each added, changed, or orphaned production definition, trace a path from a
real production entry point. Classify references as production use, test use,
re-export/declaration, documentation, or generated output. Reference counts,
passing tests, and an export alone are not evidence of production use.

- Follow callers transitively: helpers that call each other but have no path
  from a production entry point are dead too. Check abandoned branches,
  adapters, options and compatibility wrappers, not only functions.
- **Production code whose only callers are tests is dead and must be removed.**
  Delete it and move useful behavioral assertions to the real production entry
  point. Delete assertions for constraints that belong only to the dead helper.
  Put genuine test fixtures/utilities under test support, not production code.
  Do not add dummy callers, test-only exports, deprecation tags, or speculative
  future-use justifications to keep an unused implementation.
- Before declaring a definition dead from a text search, check framework
  registration, callbacks, reflection, configuration, scripts, package entry
  points, side-effect imports and supported platform/build variants. For a
  public API used outside the repository, cite the declared supported contract;
  do not break it merely because local callers are absent. Type-only contracts
  can have real compile-time consumers. Record concrete evidence for retention,
  not hypothetical consumers; unresolved reachability is an open question, not
  a clean pass or permission to delete.
- After deletion, follow newly orphaned helpers, imports, exports, types and
  dependencies until the affected path is clean. Preserve meaningful coverage
  through the implementation that actually runs.

## 3. Refresh comments against the surviving code

Read comments and docstrings on changed code, its callers, and its interfaces,
including unchanged comments made stale by the diff. Verify stated constraints,
examples, return values, errors, lifecycle and platform behavior against the
implementation and tests.

Rewrite or remove stale claims, obsolete migration/deprecation notes, and
comments describing deleted or bypassed paths. Move still-useful rationale to
the live implementation rather than preserve dead code to host its explanation.
Apply the development rules' **Comments**, **Pyramid Principle**, and **Edit
Line by Line** guidance: explain the enduring reason or contract, not the PR's
history; consolidate repeated explanations. Recheck TODOs and their conditions.

## 4. Edit the whole PR description

Check whether the description needs changes; do not assume every update needs
more text. Apply the development rules' **Pyramid Principle**, **Edit Line by
Line**, and **Testing and PR Test Plans** guidance.

- Lead with the answer to the reader's question, supported by the problem and
  why this change solves it. Group supporting points without overlap.
- Compare every claim with the final diff: scope, behavior, issue resolution,
  dependencies, limitations, screenshots and test instructions/results.
- Make an explicit deletion/consolidation pass. Remove stale claims, debugging
  history, superseded approaches, repeated caveats, redundant lists and empty
  template sections. Merge sections that answer the same question. Replace
  obsolete text in place instead of appending an update or another test report.
- Keep necessary limitations and reproducible test commands with prerequisites
  and working directory. Tie results to the revision/environment actually
  tested; distinguish unrun, failed or skipped checks from passes. Do not claim
  earlier-revision results verify the current revision.
- Use consistent terms, plain language and concise sentences. Respect the
  repository's template and preserve useful issue links. Leave text that is
  already accurate, focused and concise alone; there is no rewrite quota.

## 5. Validate and close the loop

After code cleanup, rerun relevant tests, typechecks and lint using the
repository's commands, and return the cleanup delta to engineering review when
required. Recheck affected reachability, comments and description against that
final code and evidence; fixes can orphan more code or invalidate prose.

Immediately before publishing, re-read the remote branch state and, for an
existing PR, its target and description. If relevant state changed, refresh
affected checks and coordinate concurrent edits rather than overwrite someone
else's text. After publishing, read back the PR description and verify the
intended head and rendered text on GitHub.
Read-only reviewers report findings and proposed edits instead of mutating them.

Report briefly in the handoff, not as another PR-description section:

- Dead code: removed definitions and preserved behavioral coverage, or checked
  scope and evidence for retention; no findings / not applicable are valid.
- Comments: corrected or verified, with unresolved claims called out.
- Description: simplified/updated or unchanged with a brief reason.
- Validation: checked revision, commands/results, and published verification
  when authorized. Unresolved checks are not a completed pass.
