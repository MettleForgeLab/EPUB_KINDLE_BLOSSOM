[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Master,
    [Parameter(Mandatory=$true)][string]$Run
)
$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) { throw "Run Install-Local.ps1 first." }
& $python -m mfl_adapter verify --epub $Master --run $Run
if ($LASTEXITCODE -ne 0) { throw "Verification failed." }
