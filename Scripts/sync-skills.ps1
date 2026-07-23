# Copies skills from this git-tracked folder (Documents\Cline\Skills) into
# ~/.cline/skills, where the Cline extension actually scans for global skills.
# Documents\Cline is the git-tracked source of truth; ~/.cline/skills is a
# build product of this script.
#
# Each skill listed in skills-manifest.txt is mirrored individually (stale files inside a skill
# are removed), but skills that exist only in ~/.cline/skills are left alone,
# so machine-local or test skills survive. Removing a skill from the source
# therefore requires deleting it from ~/.cline/skills manually.
#
# Run directly, or automatically via Hooks\TaskStart.ps1.

$ErrorActionPreference = "Stop"

$sourceRoot = Join-Path $PSScriptRoot "..\Skills"
$manifest = Join-Path $PSScriptRoot "skills-manifest.txt"
$destRoot = Join-Path $env:USERPROFILE ".cline\skills"

if (-not (Test-Path $sourceRoot)) {
    exit 0
}
if (-not (Test-Path $manifest)) {
    Write-Error "Manifest not found: '$manifest'"
    exit 1
}

New-Item -ItemType Directory -Path $destRoot -Force | Out-Null

foreach ($line in Get-Content -Path $manifest) {
    $skillName = ($line -replace '#.*$', '').Trim()
    if (-not $skillName) {
        continue
    }
    $skillDir = Join-Path $sourceRoot $skillName
    if (-not (Test-Path -Path $skillDir -PathType Container)) {
        Write-Error "Manifest skill not found: '$skillName'"
        exit 1
    }
    $dest = Join-Path $destRoot $skillName
    # /MIR mirrors this one skill's contents; /NJH /NJS /NDL /NFL /NC /NS keep it quiet.
    robocopy $skillDir $dest /MIR /NJH /NJS /NDL /NFL /NC /NS | Out-Null
    # Robocopy exit codes 0-7 are success (8+ are failures).
    if ($LASTEXITCODE -ge 8) {
        Write-Error "robocopy failed for skill '$skillName' (exit $LASTEXITCODE)"
        exit 1
    }
}

exit 0
