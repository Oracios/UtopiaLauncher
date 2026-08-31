# Verifie que le distribution.json LIVE ne contient aucun lien casse (404).
#
# A lancer APRES chaque changement de mods sur le FTP (ou n'importe quand) pour
# savoir en quelques secondes si une regeneration est necessaire. Ce script ne
# modifie rien : il lit la distribution publiee et teste chaque URL.
#
# Necessite PowerShell 7+.  Usage :  pwsh .\tools\check-distribution.ps1

# Windows PowerShell 5.1 ne connait pas "ForEach-Object -Parallel". Sans ce
# garde, la boucle echouait et le script annoncait "aucun lien casse" sans avoir
# rien teste du tout : un faux positif bien pire qu'une erreur.
if ($PSVersionTable.PSVersion.Major -lt 7) {
    Write-Host "ERREUR : ce script necessite PowerShell 7 ou plus recent." -ForegroundColor Red
    Write-Host ("  Version detectee : {0}" -f $PSVersionTable.PSVersion) -ForegroundColor Yellow
    Write-Host "  Relance-le avec :  pwsh .\tools\check-distribution.ps1" -ForegroundColor Cyan
    exit 2
}

$distUrl = "https://apk.nerysia.fr/utopia-laucher/distribution.json"

Write-Host "Telechargement du distribution.json live..." -ForegroundColor Cyan
try {
    $bust = [DateTimeOffset]::Now.ToUnixTimeSeconds()
    $dist = Invoke-RestMethod -Uri "$distUrl`?t=$bust" -TimeoutSec 30
} catch {
    Write-Host "ERREUR : impossible de recuperer le distribution.json ($($_.Exception.Message))" -ForegroundColor Red
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

# HEAD en parallele. On emet un resultat pour CHAQUE lien (et pas seulement pour
# les casses), ce qui permet de verifier ensuite qu'ils ont tous ete testes.
$results = @($urls | ForEach-Object -ThrottleLimit 24 -Parallel {
    $item = $_
    $code = 0
    try {
        $r = Invoke-WebRequest -Uri $item.url -Method Head -TimeoutSec 20 -ErrorAction Stop
        $code = [int]$r.StatusCode
    } catch {
        try { if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode.value__ } } catch {}
    }
    [pscustomobject]@{ name = $item.name; type = $item.type; code = $code }
})

# Garde-fou : si tous les liens n'ont pas ete testes, on ne declare surtout pas
# que tout va bien.
if ($results.Count -ne $urls.Count) {
    Write-Host ("ERREUR : seuls {0} liens sur {1} ont pu etre testes." -f $results.Count, $urls.Count) -ForegroundColor Red
    Write-Host "  Resultat NON fiable : relance la verification." -ForegroundColor Yellow
    exit 1
}

$bad = @($results | Where-Object { $_.code -ne 200 })

if ($bad.Count -eq 0) {
    Write-Host ("OK : {0} liens verifies, aucun casse. Les joueurs peuvent tout telecharger." -f $results.Count) -ForegroundColor Green
    exit 0
} else {
    Write-Host ("ATTENTION : {0} lien(s) casse(s) sur {1} !" -f $bad.Count, $results.Count) -ForegroundColor Red
    foreach ($b in $bad) {
        Write-Host ("  [HTTP {0}] {1} : {2}" -f $b.code, $b.type, $b.name) -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Cause probable : des mods ont change sur le FTP sans regeneration." -ForegroundColor White
    Write-Host "Solution       : .\tools\generate-distribution.ps1 -Bump patch" -ForegroundColor Cyan
    exit 1
}
