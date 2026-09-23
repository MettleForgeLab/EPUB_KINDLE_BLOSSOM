[CmdletBinding()]
param([switch]$SkipBrowser)
$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
Push-Location $PSScriptRoot
try {
    if (-not (Test-Path -LiteralPath $python)) {
        & py -3 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw "Python 3.11+ is required. Install Python, then rerun." }
    }
    & $python -c "import sys; assert sys.version_info >= (3,11), 'Python 3.11 or newer is required'"
    if ($LASTEXITCODE -ne 0) { throw "Unsupported Python version." }
    & $python -m pip install ".[test]"
    if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
    if (-not $SkipBrowser) {
        & $python -m playwright install chromium
        if ($LASTEXITCODE -ne 0) { throw "Chromium installation failed; inspect output above." }
    }
    & $python -m mfl_adapter doctor
    if ($LASTEXITCODE -ne 0) { throw "Environment check failed." }
}
finally { Pop-Location }
# Setup downloads dependencies/browser only. It does not upload or open the book.
