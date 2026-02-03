$ErrorActionPreference='Stop'
$wavePath = 'C:\Users\mr-ga\.openclaw\workspace\wave5.json'
$outPath = Join-Path $PSScriptRoot 'wave5.json'
$w = Get-Content $wavePath -Raw | ConvertFrom-Json
$w | ConvertTo-Json -Depth 20 | Set-Content -Encoding UTF8 $outPath
Write-Host "Wrote $outPath"
