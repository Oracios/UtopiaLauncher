<#
  generate-neoforge-core.ps1

  Genere le bloc "coeur" NeoForge (module ForgeHosted) pour le distribution.json
  du launcher Helios/Utopia. A relancer UNIQUEMENT quand tu changes de version NeoForge.

  Ce que fait le script :
    1. Telecharge l'installeur NeoForge officiel et en extrait le version.json.
    2. Telecharge le jar "universal" + les 47 bibliotheques (depuis maven public)
       pour calculer leur taille + MD5 (le distribution.json Helios exige des MD5).
    3. Assemble le module ForgeHosted + sous-module VersionManifest + 1 sous-module
       Library par bibliotheque.

  Les bibliotheques pointent DIRECTEMENT vers leurs URLs maven publiques
  (maven.neoforged.net / libraries.minecraft.net) : rien a re-heberger cote FTP.
  Le SEUL fichier a heberger est le version.json (genere dans neoforge-upload/).

  Sorties :
    tools/neoforge-core.json
        -> le bloc a injecter dans le distribution.json (utilise par generate-distribution.ps1)
    tools/neoforge-upload/versions/<id>/<id>.json
        -> a uploader sur le FTP, a la racine du repo Utopia (BaseRepoUrl)

  Usage :
    & "tools/generate-neoforge-core.ps1"                 # version par defaut
    & "tools/generate-neoforge-core.ps1" -Version 21.1.233
#>
param(
    [string]$Version = "21.1.233",
    [string]$BaseRepoUrl = "https://apk.nerysia.fr/utopia-laucher"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression.FileSystem

$toolsDir = $PSScriptRoot
$work     = Join-Path $env:TEMP "utopia-neoforge-core"
$cache    = Join-Path $work "dl"
New-Item -ItemType Directory -Force $work  | Out-Null
New-Item -ItemType Directory -Force $cache | Out-Null

$mavenBase    = "https://maven.neoforged.net/releases"
$installerUrl = "$mavenBase/net/neoforged/neoforge/$Version/neoforge-$Version-installer.jar"
$installerJar = Join-Path $work "neoforge-$Version-installer.jar"

function Get-File($url, $dest) {
    if (-not (Test-Path -LiteralPath $dest)) {
        Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
    }
    return $dest
}
function Get-Md5($path) { return (Get-FileHash -Algorithm MD5 -LiteralPath $path).Hash.ToLower() }

Write-Host "1/5  Installeur NeoForge $Version..." -ForegroundColor Cyan
Get-File $installerUrl $installerJar | Out-Null

Write-Host "2/5  Extraction du version.json..." -ForegroundColor Cyan
$zip = [System.IO.Compression.ZipFile]::OpenRead($installerJar)
$entry = $zip.Entries | Where-Object { $_.FullName -eq 'version.json' }
$reader = New-Object System.IO.StreamReader($entry.Open())
$vjson  = $reader.ReadToEnd()
$reader.Close(); $zip.Dispose()
$ver = $vjson | ConvertFrom-Json
$vmId = $ver.id   # ex. neoforge-21.1.233

# Ecrit le version.json a uploader : neoforge-upload/versions/<id>/<id>.json
$uploadDir = Join-Path $toolsDir "neoforge-upload"
$vmDir     = Join-Path $uploadDir "versions\$vmId"
New-Item -ItemType Directory -Force $vmDir | Out-Null
$vmFile = Join-Path $vmDir "$vmId.json"
[System.IO.File]::WriteAllText($vmFile, $vjson)   # UTF-8 sans BOM
$vmSize = (Get-Item -LiteralPath $vmFile).Length
$vmMd5  = Get-Md5 $vmFile

Write-Host "3/5  Jar universal..." -ForegroundColor Cyan
$uniUrl  = "$mavenBase/net/neoforged/neoforge/$Version/neoforge-$Version-universal.jar"
$uniFile = Join-Path $cache "neoforge-$Version-universal.jar"
Get-File $uniUrl $uniFile | Out-Null
$uniSize = (Get-Item -LiteralPath $uniFile).Length
$uniMd5  = Get-Md5 $uniFile

Write-Host "4/5  Bibliotheques ($($ver.libraries.Count)) - telechargement + MD5..." -ForegroundColor Cyan
$libSubs = New-Object System.Collections.ArrayList
$i = 0
foreach ($lib in $ver.libraries) {
    $i++
    $a = $lib.downloads.artifact
    $dest = Join-Path $cache ($a.path -replace '[\\/]', '_')
    Get-File $a.url $dest | Out-Null
    [void]$libSubs.Add([ordered]@{
        id       = $lib.name
        name     = "NeoForge Library ($($lib.name))"
        type     = "Library"
        artifact = [ordered]@{
            size = [int64](Get-Item -LiteralPath $dest).Length
            MD5  = (Get-Md5 $dest)
            url  = $a.url
        }
    })
    Write-Progress -Activity "Bibliotheques NeoForge" -Status "$i / $($ver.libraries.Count)" -PercentComplete ([int]($i * 100 / $ver.libraries.Count))
}
Write-Progress -Activity "Bibliotheques NeoForge" -Completed

Write-Host "5/5  Assemblage du bloc ForgeHosted..." -ForegroundColor Cyan
$subModules = New-Object System.Collections.ArrayList
[void]$subModules.Add([ordered]@{
    id       = $vmId
    name     = "NeoForge (version.json)"
    type     = "VersionManifest"
    artifact = [ordered]@{
        size = [int64]$vmSize
        MD5  = $vmMd5
        url  = "$BaseRepoUrl/versions/$vmId/$vmId.json"
    }
})
foreach ($s in $libSubs) { [void]$subModules.Add($s) }

$core = [ordered]@{
    id         = "net.neoforged:neoforge:$Version`:universal"
    name       = "NeoForge $Version"
    type       = "ForgeHosted"
    artifact   = [ordered]@{
        size = [int64]$uniSize
        MD5  = $uniMd5
        url  = $uniUrl
    }
    subModules = $subModules
}

$outFile = Join-Path $toolsDir "neoforge-core.json"
$core | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $outFile -Encoding UTF8

Write-Host ""
Write-Host "OK - bloc coeur ecrit : $outFile" -ForegroundColor Green
Write-Host "A UPLOADER sur le FTP (racine du repo $BaseRepoUrl) :" -ForegroundColor Yellow
Write-Host "    $uploadDir\  ->  1 fichier : versions/$vmId/$vmId.json" -ForegroundColor Yellow
Write-Host "Bibliotheques : $($ver.libraries.Count) (URLs maven publiques, rien a re-heberger)" -ForegroundColor Gray
