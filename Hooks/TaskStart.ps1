# Global TaskStart hook: sync git-tracked skills (Documents\Cline\Skills)
# into ~/.cline/skills so the extension picks up the latest versions.
# Sync failures must not block the task, so errors are reported in the
# hook output but cancel stays false.

$ErrorActionPreference = "Continue"

# Consume stdin (hook input JSON); this hook doesn't need it.
[Console]::In.ReadToEnd() | Out-Null

$syncScript = Join-Path $PSScriptRoot "..\Scripts\sync-skills.ps1"
$errorMessage = ""
try {
    & $syncScript 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        $errorMessage = "Skill sync failed with exit code $LASTEXITCODE"
    }
} catch {
    $errorMessage = "Skill sync failed: $($_.Exception.Message)"
}

@{ cancel = $false; contextModification = ""; errorMessage = $errorMessage } | ConvertTo-Json -Compress
exit 0
