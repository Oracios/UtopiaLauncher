# Script PowerShell â€” GÃ©nÃ©rer les infos MD5 + taille pour distribution.json
# Usage: .\get-mod-info.ps1 "C:\chemin\vers\fichier.jar"
# Ou glisser-dÃ©poser plusieurs fichiers: .\get-mod-info.ps1 *.jar

param(
    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$FilePaths
)

Write-Host ""
Write-Host "=== Utopia Launcher - GÃ©nÃ©rateur d'infos pour distribution.json ===" -ForegroundColor Cyan
Write-Host ""

foreach ($FilePath in $FilePaths) {
    $files = Get-Item $FilePath -ErrorAction SilentlyContinue
    if (-not $files) {
        Write-Host "Fichier introuvable : $FilePath" -ForegroundColor Red
        continue
    }
    
    foreach ($file in $files) {
        $md5 = (Get-FileHash $file.FullName -Algorithm MD5).Hash.ToLower()
        $size = $file.Length
        $name = $file.Name
        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($name)

        Write-Host "--- $name ---" -ForegroundColor Yellow
        Write-Host "  Taille  : $size bytes"
        Write-Host "  MD5     : $md5"
        Write-Host ""
        Write-Host "  Snippet JSON (mod obligatoire) :" -ForegroundColor Green
        Write-Host @"
  {
    "id": "generated.fabricmod:$baseName@jar",
    "name": "$baseName",
    "type": "FabricMod",
    "artifact": {
      "size": $size,
      "MD5": "$md5",
      "url": "https://www.nerysia.fr/launcher/servers/Utopia-1.21.1/forgemods/required/$name"
    }
  }
"@
        Write-Host ""
        Write-Host "  Snippet JSON (mod optionnel desactive par defaut) :" -ForegroundColor Magenta
        Write-Host @"
  {
    "id": "generated.fabricmod:$baseName@jar",
    "name": "$baseName",
    "type": "FabricMod",
    "artifact": {
      "size": $size,
      "MD5": "$md5",
      "url": "https://www.nerysia.fr/launcher/servers/Utopia-1.21.1/forgemods/optionaloff/$name"
    },
    "required": {
      "value": false,
      "def": false
    }
  }
"@
        Write-Host ""
        Write-Host ("=" * 60) -ForegroundColor DarkGray
        Write-Host ""
    }
}


