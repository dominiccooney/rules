# Copies skills from this git-tracked folder (Documents\Cline\Skills) into
# ~/.cline/skills, where the Cline extension actually scans for global skills.
# Documents\Cline is the git-tracked source of truth; ~/.cline/skills is a
# build product of this script.
#
# Each skill listed in skills-manifest.txt is mirrored individually (stale files
# inside a skill are removed). Skills listed in retired-skills.txt are deleted.
# Other skills that exist only in ~/.cline/skills are left alone, so
# machine-local or test skills survive.
#
# Run directly, or automatically via Hooks\TaskStart.ps1.

$ErrorActionPreference = "Stop"

$sourceRoot = Join-Path $PSScriptRoot "..\Skills"
$manifest = Join-Path $PSScriptRoot "skills-manifest.txt"
$retiredManifest = Join-Path $PSScriptRoot "retired-skills.txt"
$destRoot = Join-Path $env:USERPROFILE ".cline\skills"

if (-not (Test-Path $sourceRoot)) {
    exit 0
}
if (-not (Test-Path $manifest)) {
    Write-Error "Manifest not found: '$manifest'"
    exit 1
}
if (-not (Test-Path $retiredManifest)) {
    Write-Error "Retired-skills manifest not found: '$retiredManifest'"
    exit 1
}

function Read-SkillNames {
    param(
        [Parameter(Mandatory = $true)] [string] $Path,
        [Parameter(Mandatory = $true)] [string] $Kind
    )

    $names = @()
    foreach ($line in Get-Content -Path $Path) {
        $skillName = ($line -replace '#.*$', '').Trim()
        if (-not $skillName) {
            continue
        }
        if ($skillName -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*$') {
            throw "Invalid $Kind skill name: '$skillName'"
        }
        if ($names -contains $skillName) {
            throw "Duplicate $Kind skill: '$skillName'"
        }
        $names += $skillName
    }
    return $names
}

$activeSkills = @(Read-SkillNames -Path $manifest -Kind "active")
$retiredSkills = @(Read-SkillNames -Path $retiredManifest -Kind "retired")

foreach ($skillName in $activeSkills) {
    if ($retiredSkills -contains $skillName) {
        Write-Error "Skill is both active and retired: '$skillName'"
        exit 1
    }
    $skillDir = Join-Path $sourceRoot $skillName
    if (-not (Test-Path -Path $skillDir -PathType Container)) {
        Write-Error "Manifest skill not found: '$skillName'"
        exit 1
    }
}

New-Item -ItemType Directory -Path $destRoot -Force | Out-Null

foreach ($skillName in $retiredSkills) {
    $dest = Join-Path $destRoot $skillName
    Remove-Item -LiteralPath $dest -Recurse -Force -ErrorAction SilentlyContinue
}

foreach ($skillName in $activeSkills) {
    $skillDir = Join-Path $sourceRoot $skillName
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
