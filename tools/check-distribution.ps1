# Verifie que le distribution.json LIVE ne contient aucun lien casse (404).
#
# A lancer APRES chaque changement de mods sur le FTP (ou n'importe quand) pour
# savoir en quelques secondes si une regeneration est necessaire. Contrairement
# a la generation, ce script ne touche a rien : il lit juste la distribution
# publiee et teste chaque URL de mod/fichier.
#
# Usage: .\tools\check-distribution.ps1

$distUrl = "https://apk.nerysia.fr/utopia-laucher/distribution.json"

Write-Host "Telechargement du distribution.json live..." -ForegroundColor Cyan
try {
    $bust = [DateTimeOffset]::Now.ToUnixTimeSeconds()
    $dist = Invoke-RestMethod -Uri "$distUrl`?t=$bust" -TimeoutSec 30
} catch {
    Write-Host "ERREUR: impossible de recuperer le distribution.json ($($_.Exception.Message))" -ForegroundColor Red
    exit 1
}

$server = $dist.servers[0]
Write-Host ("Version modpack : {0}" -f $server.version) -ForegroundColor Green

# Collecte recursive de toutes les URLs hebergees sur notre serveur.
$urls = New-Object System.Collections.Generic.List[object]
function Collect-Urls($modules) {
    foreach ($m in $modules) {
        if ($m.artifact -and $m.artifact.url -and $m.artifact.url -like "*apk.nerysia.fr*") {
            $urls.Add([pscustomobject]@{ name = $m.name; type = $m.type; url = $m.artifact.url })
        }
        if ($m.subModules) { Collect-Urls $m.subModules }
    }
}
Collect-Urls $server.modules
Write-Host ("Liens a verifier : {0}" -f $urls.Count) -ForegroundColor Cyan
Write-Host ""

# HEAD en parallele (PowerShell 7+). N'emet un objet que pour les liens casses.
$bad = $urls | ForEach-Object -ThrottleLimit 24 -Parallel {
    $item = $_
    try {
        $r = Invoke-WebRequest -Uri $item.url -Method Head -TimeoutSec 20 -ErrorAction Stop
        if ($r.StatusCode -ne 200) {
            [pscustomobject]@{ name = $item.name; type = $item.type; code = $r.StatusCode }
        }
    } catch {
        $code = 0
        try { if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode.value__ } } catch {}
        [pscustomobject]@{ name = $item.name; type = $item.type; code = $code }
    }
}

if (-not $bad -or @($bad).Count -eq 0) {
    Write-Host "OK : aucun lien casse. La distribution est saine, les joueurs peuvent tout telecharger." -ForegroundColor Green
    exit 0
} else {
    $bad = @($bad)
    Write-Host ("ATTENTION : {0} lien(s) casse(s) !" -f $bad.Count) -ForegroundColor Red
    foreach ($b in $bad) {
        Write-Host ("  [HTTP {0}] {1} : {2}" -f $b.code, $b.type, $b.name) -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Cause probable : tu as change des mods sur le FTP sans regenerer." -ForegroundColor White
    Write-Host "Solution       : .\tools\generate-distribution.ps1 -Bump patch" -ForegroundColor Cyan
    exit 1
}
