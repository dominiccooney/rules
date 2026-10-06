# Canonical Rules and Skills

Before editing a rule or skill, check whether its canonical copy exists under
`~/Documents/Cline`. When it does, edit the canonical copy there, then run the
repository's applicable sync script and verify the installed copy matches.

Treat copies under `~/.cline` and other installed or generated locations as
build products, not sources. Direct edits there will be overwritten by the next
sync. Commit and push durable rule and skill changes from `~/Documents/Cline`.

# Writing & Communication

Be quick to apply the `writing-editing-prose` skill to any written communication a paragraph or longer.

# Important Skills

For code changes, use `make-a-change` skill.

When reviewing someone else's PR, choose the skill by the author and the PR's age: `teammate-pr-review` for a fresh PR from a repository member, or from an author I name as trusted; `backlog-pr-review` for everyone else and for any PR roughly two weeks old or older. If you are doing a large number of reviews, use `pr-review-worklist` to keep track.
