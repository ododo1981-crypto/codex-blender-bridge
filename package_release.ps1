$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$dist = Join-Path $root "dist"
$zip = Join-Path $dist "codex_blender_bridge_addon.zip"
$versionZip = Join-Path $dist "codex_blender_bridge_addon_v0.2.1.zip"
$src = Join-Path $root "codex_blender_bridge_addon\__init__.py"

New-Item -ItemType Directory -Force -Path $dist | Out-Null

if (Test-Path -LiteralPath $zip) {
    Remove-Item -LiteralPath $zip -Force
}
if (Test-Path -LiteralPath $versionZip) {
    Remove-Item -LiteralPath $versionZip -Force
}

$pythonCandidates = @(
    "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe",
    "python"
)

$python = $null
foreach ($candidate in $pythonCandidates) {
    try {
        & $candidate --version | Out-Null
        $python = $candidate
        break
    } catch {
    }
}

if (-not $python) {
    throw "Python was not found."
}

& $python -c "import pathlib, zipfile; src=pathlib.Path(r'$src'); outputs=[pathlib.Path(r'$zip'), pathlib.Path(r'$versionZip')]; [zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED).write(src, 'codex_blender_bridge_addon/__init__.py') for z in outputs]; [print(z) for z in outputs]"

Write-Host "Created $zip"
Write-Host "Created $versionZip"
