[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Master,
    [Parameter(Mandatory=$true)][string]$Output,
    [string]$ChromiumPath = ""
)
$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) { throw "Run Install-Local.ps1 first." }
$masterPath = (Resolve-Path -LiteralPath $Master).Path
$outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Output)
if (Test-Path -LiteralPath $outputPath) { throw "Choose a new output directory; existing runs are never overwritten." }
$profile = Join-Path $PSScriptRoot "profiles\bht_milestone_002.json"
$arguments = @("-m","mfl_adapter","build-probe","--epub",$masterPath,
               "--profile",$profile,"--out",$outputPath)
if ($ChromiumPath) { $arguments += @("--chromium",$ChromiumPath) }
& $python @arguments
if ($LASTEXITCODE -ne 0) { throw "Adapter stopped. No output was promoted; read the error above." }
& $python -m mfl_adapter verify --run $outputPath --epub $masterPath
if ($LASTEXITCODE -ne 0) { throw "Independent verification failed." }
Write-Host "Second-batch probe complete. Vertical-footprint and caption-adjacency checks passed locally; Kindle conversion and human visual acceptance remain open."
