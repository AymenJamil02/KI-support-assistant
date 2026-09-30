$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 -m portfolio.server
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python -m portfolio.server
} else {
    Write-Host 'Bitte Python 3.11 oder neuer von python.org installieren.'
    exit 1
}
