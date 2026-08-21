param(
    [switch]$Force,
    [switch]$LegacyCodexHome
)

$ErrorActionPreference = 'Stop'

$RepoUrl = 'https://github.com/5l33m/cai.git'
$Branch = 'feature/agent-trust-boundary-red-team-skill'
$PublicPath = 'skills/AI-red-team'
$EnginePath = 'skills/agent-trust-boundary-red-team'

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git is required but was not found in PATH.'
}

if ($LegacyCodexHome) {
    $CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
    $SkillsRoot = Join-Path $CodexHome 'skills'
} else {
    $SkillsRoot = Join-Path (Join-Path $HOME '.agents') 'skills'
}

$Destination = Join-Path $SkillsRoot 'ai-red-team'

if (Test-Path $Destination) {
    if (-not $Force) {
        throw "Destination already exists: $Destination`nRe-run with -Force to replace it."
    }
    Remove-Item -Recurse -Force $Destination
}

$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("ai-red-team-" + [guid]::NewGuid().ToString('N'))
$Checkout = Join-Path $TempRoot 'repo'

try {
    New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null

    git clone --quiet --depth 1 --filter=blob:none --no-checkout --branch $Branch $RepoUrl $Checkout
    if ($LASTEXITCODE -ne 0) { throw 'Failed to clone AI-red-team source repository.' }

    Push-Location $Checkout
    try {
        git sparse-checkout init --cone | Out-Null
        git sparse-checkout set $PublicPath $EnginePath | Out-Null
        git checkout --quiet $Branch
        if ($LASTEXITCODE -ne 0) { throw 'Failed to check out AI-red-team source files.' }
    }
    finally {
        Pop-Location
    }

    New-Item -ItemType Directory -Force -Path $Destination | Out-Null

    # Copy the tested executable engine into the installed skill directory.
    Copy-Item -Path (Join-Path $Checkout "$EnginePath\*") -Destination $Destination -Recurse -Force

    # Overlay the public AI-red-team identity and operator docs.
    foreach ($Name in @('SKILL.md','README.md','MODULES.md')) {
        Copy-Item -Path (Join-Path $Checkout "$PublicPath\$Name") -Destination (Join-Path $Destination $Name) -Force
    }

    # Preserve this installer for easy upgrades.
    Copy-Item -Path (Join-Path $Checkout "$PublicPath\install-codex.ps1") -Destination (Join-Path $Destination 'install-codex.ps1') -Force

    $SkillFile = Join-Path $Destination 'SKILL.md'
    if (-not (Test-Path $SkillFile)) { throw "Installation verification failed: $SkillFile not found." }

    $Header = Get-Content $SkillFile -TotalCount 5 -Raw
    if ($Header -notmatch 'name:\s*ai-red-team') {
        throw 'Installation verification failed: Codex skill ID is not ai-red-team.'
    }

    Write-Host ''
    Write-Host 'AI-red-team installed successfully.' -ForegroundColor Green
    Write-Host "Location: $Destination"
    Write-Host 'Codex skill ID: ai-red-team'
    Write-Host ''
    Write-Host 'Restart Codex if it is already running, then try:'
    Write-Host '  Use ai-red-team to assess this agent. Start with Core Proof.'
    Write-Host ''
    Write-Host 'To verify files:'
    Write-Host "  Get-ChildItem `"$Destination`""
}
finally {
    if (Test-Path $TempRoot) {
        Remove-Item -Recurse -Force $TempRoot -ErrorAction SilentlyContinue
    }
}
