Write-Host "Velkommen til Hundevibes 3000!"
Write-Host "--------------------------------`n"

function Get-HumanAge {
    param()
    while ($true) {
        $inputAge = Read-Host "Hvor gammel er du (i menneskeaar)?"
        $parsedAge = 0
        if ([int]::TryParse($inputAge, [ref]$parsedAge) -and $parsedAge -ge 0) {
            return $parsedAge
        }
        Write-Host "Ups! Skriv lige et helt tal uden bogstaver, saa tager vi den igen." -ForegroundColor Yellow
    }
}

$humanAge = Get-HumanAge
$dogAge = [int]($humanAge * 7)
$nicknames = @(
    "mester i boldjagt",
    "snusemester",
    "pelsede ven",
    "super-sniffer",
    "kongelig hundehelt"
)
$nickname = Get-Random -InputObject $nicknames

$dogArt = @" 
 /\_/\
( o.o )
 > ^ <
"@

Write-Host ""
Write-Host $dogArt -ForegroundColor Cyan
Write-Host "Hvis du var hund, ville du vaere $dogAge aar gammel, din $nickname!" -ForegroundColor Green

if ($dogAge -gt 60) {
    Write-Host "Det er mange hundeaar! Tid til en lur i solen." -ForegroundColor Magenta
} elseif ($dogAge -ge 21) {
    Write-Host "Perfekt alder til at vaere pakkens alfa." -ForegroundColor Magenta
} else {
    Write-Host "Du er stadig en hvalp! Tid til at bide i snoerebaand." -ForegroundColor Magenta
}

Write-Host "`nTak fordi du hang ud med Hundevibes 3000. Giv en high paw!"
