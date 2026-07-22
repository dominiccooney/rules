#!/usr/bin/env bash

# Global TaskStart hook: sync git-tracked skills (Documents/Cline/Skills)
# into ~/.cline/skills so the extension picks up the latest versions.
# Sync failures must not block the task, so errors are reported in the
# hook output but cancel stays false.

set -u

# Consume stdin (hook input JSON); this hook does not need it.
cat >/dev/null || true

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
sync_script="$script_dir/../Scripts/sync-skills.sh"
error_message=''

"$sync_script" >/dev/null 2>&1
sync_exit_code=$?
if ((sync_exit_code != 0)); then
	error_message="Skill sync failed with exit code $sync_exit_code"
fi

printf '{"cancel":false,"contextModification":"","errorMessage":"%s"}\n' "$error_message"
exit 0