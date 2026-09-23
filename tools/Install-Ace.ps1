param()

$ErrorActionPreference = "Stop"

$Version = "1.4.6"
$ToolRoot = Join-Path $PSScriptRoot "ace"
$Destination = Join-Path $ToolRoot $Version

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "Node.js is not available."
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "npm is not available."
}

New-Item `
    -ItemType Directory `
    -Path $ToolRoot `
    -Force |
Out-Null

if (Test-Path $Destination) {
    Remove-Item `
        -LiteralPath $Destination `
        -Recurse `
        -Force
}

New-Item `
    -ItemType Directory `
    -Path $Destination `
    -Force |
Out-Null

$PackageJson = [ordered]@{
    name = "mfl-ace-runtime"
    version = "1.0.0"
    private = $true
} |
ConvertTo-Json

$PackageJson |
Set-Content `
    (Join-Path $Destination "package.json") `
    -Encoding UTF8

Push-Location $Destination

try {
    Write-Host "Installing Ace by DAISY $Version..."

    npm install `
        --save-exact `
        "@daisy/ace@$Version"

    if ($LASTEXITCODE -ne 0) {
        throw "npm install failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}

$Ace = Join-Path `
    $Destination `
    "node_modules\.bin\ace.cmd"

if (-not (Test-Path $Ace)) {
    throw "Ace executable was not found after installation."
}

$Lock = Join-Path $Destination "package-lock.json"

if (-not (Test-Path $Lock)) {
    throw "Ace package-lock.json was not produced."
}

$LockHash = (
    Get-FileHash `
        -LiteralPath $Lock `
        -Algorithm SHA256
).Hash.ToLower()

$Record = [ordered]@{
    tool = "Ace by DAISY"
    version = $Version
    npm_package = "@daisy/ace@$Version"
    executable = $Ace
    package_lock_sha256 = $LockHash
    node_version = (& node --version)
    npm_version = (& npm --version)
    installed_utc = (Get-Date).ToUniversalTime().ToString("o")
}

$Record |
ConvertTo-Json |
Set-Content `
    (Join-Path $Destination "MFL_INSTALL_RECORD.json") `
    -Encoding UTF8

Write-Host "`nACE VERSION:"
& $Ace --version

if ($LASTEXITCODE -ne 0) {
    throw "Ace failed its version check."
}

Write-Host "`nINSTALLED:"
Write-Host $Ace

Write-Host "`nPACKAGE LOCK SHA-256:"
Write-Host $LockHash
