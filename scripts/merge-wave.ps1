$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot\..

$basePath = 'data/profiles.json'
$wavePath = $args[0]
if (-not $wavePath) { throw 'Usage: merge-wave.ps1 <wave.json>' }

$base = Get-Content $basePath -Raw | ConvertFrom-Json
$wave = Get-Content $wavePath -Raw | ConvertFrom-Json

# Optional: normalize incoming IDs using scripts/id-aliases.json (if present)
$aliasesPath = Join-Path $PSScriptRoot 'id-aliases.json'
$aliases = @{}
if (Test-Path $aliasesPath) {
  $aliasesJson = Get-Content $aliasesPath -Raw | ConvertFrom-Json
  if ($aliasesJson.aliases) {
    foreach ($k in $aliasesJson.aliases.PSObject.Properties.Name) {
      $aliases[$k] = $aliasesJson.aliases.$k
    }
  }
}

$rewrites = 0
foreach ($p in $wave) {
  if ($p.id -and $aliases.ContainsKey($p.id)) {
    $old = $p.id
    $p.id = $aliases[$old]
    $rewrites++
  }
}
if ($rewrites -gt 0) {
  Write-Host "Normalized IDs via aliases: rewrote=$rewrites" 
}

# index existing
$map = @{}
foreach ($p in $base.profiles) { $map[$p.id] = $p }

$added = 0
$updated = 0
foreach ($p in $wave) {
  if ($map.ContainsKey($p.id)) {
    $map[$p.id] = $p
    $updated++
  } else {
    $map[$p.id] = $p
    $added++
  }
}

# reassemble sorted
$profiles = $map.Values | Sort-Object -Property name
$base.profiles = $profiles
$base.version = [int]$base.version + 1
$base.updatedAt = (Get-Date).ToString('yyyy-MM-dd')

# write pretty
$json = $base | ConvertTo-Json -Depth 20
# ConvertTo-Json is compact-ish; write as-is
Set-Content -Path $basePath -Value $json -Encoding UTF8

Write-Host "Merged wave: added=$added updated=$updated total=$($profiles.Count)"
