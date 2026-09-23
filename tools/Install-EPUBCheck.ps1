param()

$ErrorActionPreference = "Stop"

$Version = "5.4.0"
$Root = Split-Path -Parent $PSScriptRoot
$ToolRoot = Join-Path $PSScriptRoot "epubcheck"
$Destination = Join-Path $ToolRoot $Version
$Url = "https://github.com/w3c/epubcheck/releases/download/v$Version/epubcheck-$Version.zip"

$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("mfl-epubcheck-" + [guid]::NewGuid().ToString("N"))
$ZipPath = Join-Path $TempRoot "epubcheck.zip"
$Expanded = Join-Path $TempRoot "expanded"

New-Item -ItemType Directory -Path $TempRoot -Force | Out-Null
New-Item -ItemType Directory -Path $Expanded -Force | Out-Null
New-Item -ItemType Directory -Path $ToolRoot -Force | Out-Null

Write-Host "Downloading EPUBCheck $Version..."
Invoke-WebRequest -Uri $Url -OutFile $ZipPath

$DownloadHash = (
    Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256
).Hash.ToLower()

Expand-Archive `
    -LiteralPath $ZipPath `
    -DestinationPath $Expanded `
    -Force

$Jar = Get-ChildItem `
    -Path $Expanded `
    -Recurse `
    -File `
    -Filter "epubcheck.jar" |
Select-Object -First 1

if (-not $Jar) {
    throw "EPUBCheck archive did not contain epubcheck.jar"
}

if (Test-Path $Destination) {
    Remove-Item $Destination -Recurse -Force
}

New-Item `
    -ItemType Directory `
    -Path $Destination `
    -Force |
Out-Null

Copy-Item `
    -Path (Join-Path $Jar.Directory.FullName "*") `
    -Destination $Destination `
    -Recurse `
    -Force

$InstalledJar = Join-Path $Destination "epubcheck.jar"

if (-not (Test-Path $InstalledJar)) {
    throw "Installed epubcheck.jar was not found."
}

$JarHash = (
    Get-FileHash `
        -LiteralPath $InstalledJar `
        -Algorithm SHA256
).Hash.ToLower()

$Record = [ordered]@{
    tool = "EPUBCheck"
    version = $Version
    source_url = $Url
    downloaded_zip_sha256 = $DownloadHash
    installed_jar_sha256 = $JarHash
    installed_path = $InstalledJar
    installed_utc = (Get-Date).ToUniversalTime().ToString("o")
}

$Record |
ConvertTo-Json |
Set-Content `
    (Join-Path $Destination "MFL_INSTALL_RECORD.json") `
    -Encoding UTF8

Write-Host "`nEPUBCHECK VERSION:"
& java -jar $InstalledJar --version

Write-Host "`nINSTALLED:"
Write-Host $InstalledJar

Write-Host "`nDOWNLOAD SHA-256:"
Write-Host $DownloadHash

Remove-Item $TempRoot -Recurse -Force
