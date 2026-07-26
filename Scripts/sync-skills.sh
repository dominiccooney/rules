#!/usr/bin/env bash

# Copies skills from this git-tracked folder (Documents/Cline/Skills) into
# ~/.cline/skills, where the Cline extension scans for global skills.
# Documents/Cline is the git-tracked source of truth; ~/.cline/skills is a
# build product of this script.
#
# Each skill listed in skills-manifest.txt is mirrored individually (stale files
# inside a skill are removed). Skills listed in retired-skills.txt are deleted.
# Other skills that exist only in ~/.cline/skills are left alone, so
# machine-local or test skills survive.
#
# Run directly, or automatically via Hooks/TaskStart.sh.

set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source_root="$script_dir/../Skills"
manifest="$script_dir/skills-manifest.txt"
retired_manifest="$script_dir/retired-skills.txt"
: "${HOME:?HOME must be set}"
dest_root="$HOME/.cline/skills"

if [[ ! -d "$source_root" ]]; then
	exit 0
fi
if [[ ! -f "$manifest" ]]; then
	printf 'sync-skills: manifest not found: %s\n' "$manifest" >&2
	exit 1
fi
if [[ ! -f "$retired_manifest" ]]; then
	printf 'sync-skills: retired-skills manifest not found: %s\n' "$retired_manifest" >&2
	exit 1
fi
if ! command -v rsync >/dev/null 2>&1; then
	printf 'sync-skills: rsync is required\n' >&2
	exit 1
fi

contains_skill() {
	local candidate=$1
	local skill_name
	shift
	for skill_name in "$@"; do
		[[ "$skill_name" == "$candidate" ]] && return 0
	done
	return 1
}

active_skills=()
while IFS= read -r skill_name || [[ -n "$skill_name" ]]; do
	skill_name=${skill_name%%#*}
	skill_name=${skill_name#"${skill_name%%[![:space:]]*}"}
	skill_name=${skill_name%"${skill_name##*[![:space:]]}"}
	[[ -z "$skill_name" ]] && continue
	if [[ ! "$skill_name" =~ ^[[:alnum:]][[:alnum:]._-]*$ ]]; then
		printf 'sync-skills: invalid active skill name: %s\n' "$skill_name" >&2
		exit 1
	fi
	if contains_skill "$skill_name" "${active_skills[@]}"; then
		printf 'sync-skills: duplicate active skill: %s\n' "$skill_name" >&2
		exit 1
	fi
	if [[ ! -d "$source_root/$skill_name" ]]; then
		printf 'sync-skills: manifest skill not found: %s\n' "$skill_name" >&2
		exit 1
	fi
	active_skills+=("$skill_name")
done <"$manifest"

retired_skills=()
while IFS= read -r skill_name || [[ -n "$skill_name" ]]; do
	skill_name=${skill_name%%#*}
	skill_name=${skill_name#"${skill_name%%[![:space:]]*}"}
	skill_name=${skill_name%"${skill_name##*[![:space:]]}"}
	[[ -z "$skill_name" ]] && continue
	if [[ ! "$skill_name" =~ ^[[:alnum:]][[:alnum:]._-]*$ ]]; then
		printf 'sync-skills: invalid retired skill name: %s\n' "$skill_name" >&2
		exit 1
	fi
	if contains_skill "$skill_name" "${retired_skills[@]}"; then
		printf 'sync-skills: duplicate retired skill: %s\n' "$skill_name" >&2
		exit 1
	fi
	if contains_skill "$skill_name" "${active_skills[@]}"; then
		printf 'sync-skills: skill is both active and retired: %s\n' "$skill_name" >&2
		exit 1
	fi
	retired_skills+=("$skill_name")
done <"$retired_manifest"

mkdir -p -- "$dest_root"

for skill_name in "${retired_skills[@]}"; do
	rm -rf -- "$dest_root/$skill_name"
done

for skill_name in "${active_skills[@]}"; do
	rsync --archive --delete -- "$source_root/$skill_name/" "$dest_root/$skill_name/"
done
