Param(
[Parameter(Mandatory=$true)][string]$SessionId,
[Parameter(Mandatory=$true)][string]$Kind,
[Parameter(Mandatory=$true)][string]$Name,
[Parameter(Mandatory=$true)][string]$Content
)
$ErrorActionPreference = "Stop"
$today = Get-Date -Format "yyyy-MM-dd"
$base = "..codex\archives$today\session-$SessionId"
if (-not (Test-Path $base)) { New-Item -ItemType Directory -Path $base -Force | Out-Null }
$out = Join-Path $base ("$Kind" + $Name)
$outDir = Split-Path $out -Parent
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
$Content | Out-File -FilePath $out -Encoding ASCII
Write-Host "Archived: $out"
