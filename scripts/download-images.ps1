$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot\..

$imgs = @(
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Charlie_Shrem_2013.jpg'; out = 'assets/img/profiles/charlie-shrem-2013.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/e/ed/Ross_Ulbricht_by_Gage_Skidmore.jpg'; out = 'assets/img/profiles/ross-ulbricht-gage-skidmore.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/e/e1/Changpeng_Zhao_in_2022.jpg'; out = 'assets/img/profiles/changpeng-zhao-2022.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/7/78/Ruja_Ignatova_FBI.jpg'; out = 'assets/img/profiles/ruja-ignatova-fbi.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/6/6a/Roger_Ver.jpg'; out = 'assets/img/profiles/roger-ver.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/2/29/Do_Kwon.png'; out = 'assets/img/profiles/do-kwon.png' }
)

foreach ($i in $imgs) {
  Write-Host "Downloading $($i.url) -> $($i.out)"
  $dir = Split-Path -Parent $i.out
  if ($dir -and !(Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  Invoke-WebRequest -Uri $i.url -OutFile $i.out -Headers @{ 'User-Agent' = 'Mozilla/5.0' }
}
