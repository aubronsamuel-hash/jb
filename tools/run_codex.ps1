Param(
[string]$UserPrompt = "",
[string]$SessionId = $(New-Guid).Guid
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path "./AGENT.codex.md")) { throw "AGENT.codex.md manquant" }
$spec = Get-Content "./AGENT.codex.md" -Raw
$prompt = $spec + "`n`nUSER:`n" + $UserPrompt

# NOTE: Ici, dans un environnement reel, on enverrait $prompt a l API du LLM.

# Cette version bootstrap se limite a creer les fichiers de base pour CI.

& ./tools/codex_init.ps1
"Created bootstrap with SessionId=$SessionId" | Out-Host
