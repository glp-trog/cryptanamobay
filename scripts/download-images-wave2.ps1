$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot\..

$imgs = @(
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/2/22/2021_-_Centre_Stage_PO1_0057_%2851654289843%29.jpg'; out = 'assets/img/profiles/alex-mashinsky-2021-websummit.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/5/57/Ben_Delo_on_stage_at_The_Spectator%27s_%22Who%27s_afraid_of_Bitcoin%3F%22_conference.jpg'; out = 'assets/img/profiles/ben-delo-2018.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/4/43/Blake_Benthall_by_Gage_Skidmore.jpg'; out = 'assets/img/profiles/blake-benthall-gage-skidmore.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/2/25/DJ_Khaled_2012_%28cropped%29.jpg'; out = 'assets/img/profiles/dj-khaled-2012.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Ethan_Nguyen.jpg'; out = 'assets/img/profiles/ethan-nguyen.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/7/7e/Floyd_Mayweather%2C_Jr._at_DeWalt_event_%285888721735%29_%28rotated_4%29.jpg'; out = 'assets/img/profiles/floyd-mayweather-dewalt.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/c/cd/Heather_Morgan_-_USE.jpg'; out = 'assets/img/profiles/heather-morgan.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/7/7a/John_McAfee_by_Gage_Skidmore.jpg'; out = 'assets/img/profiles/john-mcafee-gage-skidmore.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/5/59/Mark_Scott_at_University_of_Melbourne_by_Stevage.jpg'; out = 'assets/img/profiles/mark-scott-stevage-2014.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/4/48/Park_Jin_Hyok_%28Upscaled%29.jpg'; out = 'assets/img/profiles/park-jin-hyok-fbi.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/6/66/Paul_Le_Roux_being_escorted_by_DEA_agents_2_%28cropped%29.png'; out = 'assets/img/profiles/paul-le-roux-dea.png' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/d/d9/Steven_Seagal_November_2016.jpg'; out = 'assets/img/profiles/steven-seagal-2016.jpg' },
  @{ url = 'https://upload.wikimedia.org/wikipedia/commons/e/e2/VirgilGriffith.jpg'; out = 'assets/img/profiles/virgil-griffith.jpg' }
)

foreach ($i in $imgs) {
  Write-Host "Downloading $($i.url) -> $($i.out)"
  $dir = Split-Path -Parent $i.out
  if ($dir -and !(Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  Invoke-WebRequest -Uri $i.url -OutFile $i.out -Headers @{ 'User-Agent' = 'Mozilla/5.0' }
}
