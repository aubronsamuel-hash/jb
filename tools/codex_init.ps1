Param()
$ErrorActionPreference = "Stop"
$paths = @(
"..codex\logs",
"..codex\archives",
"..codex\sessions",
".\docs\roadmap",
".\docs\specs",
".\scripts\guards",
".\scripts\utils",
".\backend\app",
".\backend\tests",
".\frontend\src",
".\frontend\tests"
)
foreach ($p in $paths) { if (-not (Test-Path $p)) { New-Item -ItemType Directory -Path $p -Force | Out-Null } }
Write-Host "Folders ready."
