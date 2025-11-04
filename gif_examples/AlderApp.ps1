# PowerShell-app: Alder i måneder, uger og døgn

Write-Host "Velkommen! Jeg vil beregne din alder i måneder, uger og døgn."
$alder = Read-Host "Indtast din alder i hele år"

# Tjek at input er et tal
if ($alder -match '^\d+$') {
    $alder = [int]$alder

    # Beregninger
    $maaneder = $alder * 12
    $uger = [math]::Round($alder * 52.1775, 1)
    $doegn = [math]::Round($alder * 365.25, 0)

    # Resultat
    Write-Host ""
    Write-Host "Du er cirka:"
    Write-Host " - $maaneder måneder gammel"
    Write-Host " - $uger uger gammel"
    Write-Host " - $doegn døgn gammel"
} 
else {
    Write-Host "Fejl: Indtast venligst et gyldigt tal for alder."
}
