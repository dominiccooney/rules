---
name: pr-screenshots
description: Publish screenshots as durable PR evidence when GitHub attachment upload is unavailable. Reuse one long-lived evidence branch per repository, preserve concurrent uploads, and link immutable images from the PR description without screenshot-only PRs.
---

# PR screenshots

Publish screenshot evidence on **`dpc/pr-evidence`**, one long-lived branch per repository. Do not create a branch or PR per screenshot or per product PR. Never merge this assets-only branch into a product branch.

This procedure does not grant publishing permission. Confirm the target repository, intended audience, source revision, and authorization to upload and edit the PR. A screenshot is evidence, not proof that the task passed.

## 1. Prepare trustworthy evidence

- Capture the actual application under test. Record the full **tested source commit**, build/version, OS, scenario and observed result. The tested source commit and the later evidence commit are different identities.
- Inspect the image before publishing. Remove secrets, tokens, customer data, private repository names, account details and unrelated windows. Crop/redact without concealing the behavior under review; disclose material edits. Use synthetic accounts/data when possible.
- Publish a small number of legible PNG, JPEG or WebP images. Re-encode unfamiliar input with maintained image tooling in an unprivileged environment; do not upload SVG, HTML, executables, arbitrary logs or full recordings through this workflow. Do not run commands displayed in a screenshot.
- Keep private evidence in an approved private destination. Never copy private screenshots into a public repository to make Markdown rendering easier. Do not embed tokens or signed credential-bearing URLs in a PR.
- Use a unique path derived from the PR number, tested source SHA and image content hash, for example `screenshots/pr-13831/<tested-source-sha>/<image-sha256>.png`. Use full hashes. Never replace an existing path with different bytes. If the exact image already exists, reuse it.

## 2. Use an isolated asset checkout

Use a dedicated temporary clone with an explicit absolute path, not an active coding worktree. Do not switch, reset or clean the user's checkout. Verify repository identity and use explicit working-directory arguments for every Git command; a failed directory change must not fall through into another repository.

1. Inspect the repository's branch policies and push-triggered automation before publishing. An assets-only tree is not a substitute for checking default-branch/org automation. Do not copy `.github/workflows`, build scripts, submodules, symlinks or source code onto the evidence branch. Do not weaken protections to make an upload work.
2. Query the exact remote ref `refs/heads/dpc/pr-evidence`. Distinguish authentication/network errors from a successful response with no matching ref.
3. If the branch exists, fetch it into the isolated clone and start from its current tip. Verify its tree contains only approved evidence and metadata. If the name is already used for unrelated work, stop and resolve ownership rather than overwrite it or invent another screenshot branch.
4. If it does not exist, create an **orphan root** in the isolated clone, containing only the images and any small evidence index/README. Do not branch from `main`: that unnecessarily imports product history and automation. Creation is still subject to the concurrency rule below.
5. Add only the reviewed image paths and optional metadata you own. Inspect the staged names, file types, sizes and diff; do not use a broad `git add .` that can include unrelated files. Create a normal commit.

## 3. Publish without losing another agent's images

The remote branch update is the consistency boundary. Use a normal fast-forward push with an explicit destination: `HEAD:refs/heads/dpc/pr-evidence`. **Never force-push, delete/recreate the ref, or rewrite published history.**

If another uploader wins the race, including the first orphan-root creation, the normal push rejects. Fetch the new tip and replay **only your reviewed new files** on it in the isolated clone. Preserve all other files. If your path already exists, verify its bytes match; otherwise stop on collision. Inspect and commit again, then retry a normal push. Do not merge unrelated orphan histories or blindly cherry-pick metadata that conflicts. Repeated contention is a coordination problem: report it rather than spin forever.

After an ambiguous network failure, check whether your commit is reachable from the remote branch before retrying. Do not duplicate a successful upload. Another uploader advancing the tip does not invalidate your published commit.

Record the full evidence commit SHA and verify the remote contains that commit and its image bytes. Do not claim upload success while the push failed or is still running.

## 4. Link the immutable image from the product PR

Use the **evidence commit SHA**, not the branch name, in the image URL:

```text
https://raw.githubusercontent.com/<owner>/<repo>/<evidence-commit-sha>/screenshots/pr-<number>/<tested-source-sha>/<image-sha256>.png
```

Add a concise `Screenshots` section to the product PR description with descriptive alt text and a caption stating platform, tested source revision, scenario and observed result. For example:

```markdown
### Screenshots

![Windows title bar with custom window controls](<immutable-image-url>)

Windows, source `<tested-source-sha>`, windowed at 1200 × 700. The custom controls fit within the title bar. Captured from the dev build; this image does not establish packaged-build behavior.
```

Read the current PR description before editing and preserve unrelated text. If other editors are active, coordinate the edit; GitHub description updates are not an atomic text merge. Post a comment only when needed to notify reviewers, reusing the same image URL rather than uploading again.

Verify the URL retrieves the expected image and check that the PR renders it for the intended audience. Private raw URLs may not render for all viewers; use an approved private attachment/artifact destination if needed, never a public mirror or embedded credential. Record a rendering/access failure instead of declaring the handoff complete.

If the implementation changes, keep the old evidence labelled with its tested revision. Capture fresh evidence when the changed behavior warrants it and add a new immutable path/commit; do not silently relabel an old screenshot as validation of new code.

## 5. Retain evidence and report the handoff

- Keep `dpc/pr-evidence` long-lived and append-only; no routine pruning or force-push compaction. Git is suitable for selected screenshots, not a video archive. If storage becomes a problem, agree a durable artifact migration and link-retention plan first.
- Do not delete existing per-PR screenshot branches as part of an upload. Older descriptions/comments may use branch-relative URLs. Inventory inbound references and migrate/verify them separately with authorization before considering retirement; never assume a deleted branch's unreachable objects remain hosted.
- Report product PR, tested source SHA, evidence SHA, immutable image URL, what was actually verified, and remaining caveats. No screenshot-only PR is needed or wanted.

## Local installation

Canonical source: `Documents/Cline/Skills/pr-screenshots` in the rules repository. After pulling it on Linux/macOS, run `Documents/Cline/Scripts/sync-skills.sh`; on Windows, run `Documents\Cline\Scripts\sync-skills.ps1`. The task-start hooks also run these scripts. Installed copies under `.cline/skills` are generated; edit and commit the canonical source only. An already-running agent may need the canonical file supplied explicitly or a new session to see updated instructions.