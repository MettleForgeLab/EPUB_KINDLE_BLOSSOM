param()

$ErrorActionPreference = "Stop"

$MajorVersion = "21"
$ToolRoot = Join-Path $PSScriptRoot "java"
$Destination = Join-Path $ToolRoot "temurin-21"

$MetadataUrl = "https://api.adoptium.net/v3/assets/latest/$MajorVersion/hotspot?architecture=x64&image_type=jre&os=windows&vendor=eclipse"

$TempRoot = Join-Path `
    ([System.IO.Path]::GetTempPath()) `
    ("mfl-temurin-" + [guid]::NewGuid().ToString("N"))

$ZipPath = Join-Path $TempRoot "temurin.zip"
$Expanded = Join-Path $TempRoot "expanded"

New-Item -ItemType Directory -Path $TempRoot -Force | Out-Null
New-Item -ItemType Directory -Path $Expanded -Force | Out-Null
New-Item -ItemType Directory -Path $ToolRoot -Force | Out-Null

Write-Host "Querying Eclipse Adoptium..."

$Assets = Invoke-RestMethod -Uri $MetadataUrl

if (-not $Assets) {
    throw "Adoptium returned no Java 21 Windows x64 JRE asset."
}

$Asset = $Assets | Select-Object -First 1

$DownloadUrl = $Asset.binary.package.link
$ExpectedHash = $Asset.binary.package.checksum.ToLower()
$PackageName = $Asset.binary.package.name
$ReleaseName = $Asset.release_name

if (-not $DownloadUrl) {
    throw "No package download URL was present in Adoptium metadata."
}

if (-not $ExpectedHash) {
    throw "No package checksum was present in Adoptium metadata."
}

Write-Host "Release:" $ReleaseName
Write-Host "Package:" $PackageName
Write-Host "Downloading..."

Invoke-WebRequest `
    -Uri $DownloadUrl `
    -OutFile $ZipPath

$ActualHash = (
    Get-FileHash `
        -LiteralPath $ZipPath `
        -Algorithm SHA256
).Hash.ToLower()

Write-Host "Expected SHA-256:" $ExpectedHash
Write-Host "Actual SHA-256:  " $ActualHash

if ($ActualHash -ne $ExpectedHash) {
    throw "Temurin archive checksum did not match Adoptium metadata."
}

Expand-Archive `
    -LiteralPath $ZipPath `
    -DestinationPath $Expanded `
    -Force

$JavaExe = Get-ChildItem `
    -Path $Expanded `
    -Recurse `
    -File `
    -Filter "java.exe" |
Where-Object {
    $_.FullName -match '\\bin\\java\.exe$'
} |
Select-Object -First 1

if (-not $JavaExe) {
    throw "Extracted archive did not contain bin\java.exe."
}

$JavaHome = Split-Path `
    -Parent `
    (Split-Path -Parent $JavaExe.FullName)

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

Copy-Item `
    -Path (Join-Path $JavaHome "*") `
    -Destination $Destination `
    -Recurse `
    -Force

$InstalledJava = Join-Path $Destination "bin\java.exe"

if (-not (Test-Path $InstalledJava)) {
    throw "Installed Java executable was not found."
}

$Record = [ordered]@{
    tool = "Eclipse Temurin JRE"
    major_version = $MajorVersion
    resolved_release = $ReleaseName
    metadata_url = $MetadataUrl
    package_name = $PackageName
    download_url = $DownloadUrl
    expected_sha256 = $ExpectedHash
    downloaded_sha256 = $ActualHash
    installed_java = $InstalledJava
    installed_utc = (Get-Date).ToUniversalTime().ToString("o")
}

$Record |
ConvertTo-Json -Depth 5 |
Set-Content `
    (Join-Path $Destination "MFL_INSTALL_RECORD.json") `
    -Encoding UTF8

Write-Host "`nJAVA VERSION:"
& $InstalledJava -version

if ($LASTEXITCODE -ne 0) {
    throw "Installed Java failed its runtime check."
}

Write-Host "`nINSTALLED:"
Write-Host $InstalledJava

Remove-Item `
    -LiteralPath $TempRoot `
    -Recurse `
    -Force
