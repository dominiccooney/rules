#!/usr/bin/env bash

# Copies skills from this git-tracked folder (Documents/Cline/Skills) into
# ~/.cline/skills, where the Cline extension scans for global skills.
# Documents/Cline is the git-tracked source of truth; ~/.cline/skills is a
# build product of this script.
#
# Each skill listed in skills-manifest.txt is mirrored individually (stale files inside a skill
# are removed), but skills that exist only in ~/.cline/skills are left alone,
# so machine-local or test skills survive. Removing a skill from the source
# therefore requires deleting it from ~/.cline/skills manually.
#
# Run directly, or automatically via Hooks/TaskStart.sh.

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source_root="$script_dir/../Skills"
manifest="$script_dir/skills-manifest.txt"
: "${HOME:?HOME must be set}"
dest_root="$HOME/.cline/skills"

if [[ ! -d "$source_root" ]]; then
	exit 0
fi
if [[ ! -f "$manifest" ]]; then
	printf 'sync-skills: manifest not found: %s\n' "$manifest" >&2
	exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
	printf 'sync-skills: rsync is required\n' >&2
	exit 1
fi

mkdir -p -- "$dest_root"

while IFS= read -r skill_name || [[ -n "$skill_name" ]]; do
	skill_name=${skill_name%%#*}
	skill_name=${skill_name#"${skill_name%%[![:space:]]*}"}
	skill_name=${skill_name%"${skill_name##*[![:space:]]}"}
	[[ -z "$skill_name" ]] && continue
	skill_dir="$source_root/$skill_name"
	if [[ ! -d "$skill_dir" ]]; then
		printf 'sync-skills: manifest skill not found: %s\n' "$skill_name" >&2
		exit 1
	fi
	rsync --archive --delete -- "$skill_dir/" "$dest_root/$skill_name/"
done <"$manifest"
