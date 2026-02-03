$ErrorActionPreference='Stop'
$wavePath = 'C:\Users\mr-ga\.openclaw\workspace\wave2.json'
$outPath = Join-Path $PSScriptRoot 'wave2.json'
$w = Get-Content $wavePath -Raw | ConvertFrom-Json
$w.profiles | ConvertTo-Json -Depth 20 | Set-Content -Encoding UTF8 $outPath
Write-Host "Wrote $outPath"
