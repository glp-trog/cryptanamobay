import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data' / 'profiles.json'

patch = {
  'alex-mashinsky': {
    'path': 'assets/img/profiles/alex-mashinsky-2021-websummit.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:2021_-_Centre_Stage_PO1_0057_(51654289843).jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/2/22/2021_-_Centre_Stage_PO1_0057_%2851654289843%29.jpg',
    'license': 'CC BY 2.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by/2.0',
    'attribution': 'Web Summit (photo by Piaras Ó Mídheach / Web Summit via Sportsfile; per Commons credit)',
    'caption': 'Alex Mashinsky at Web Summit (2021)'
  },
  'ben-delo': {
    'path': 'assets/img/profiles/ben-delo-2018.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Ben_Delo_on_stage_at_The_Spectator%27s_%22Who%27s_afraid_of_Bitcoin%3F%22_conference.jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/5/57/Ben_Delo_on_stage_at_The_Spectator%27s_%22Who%27s_afraid_of_Bitcoin%3F%22_conference.jpg',
    'license': 'CC BY-SA 4.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by-sa/4.0',
    'attribution': 'Anne Schwarz Photography (per Commons “Artist”; credit notes “Sent to me personally by request”)',
    'caption': 'Ben Delo speaking at a Spectator conference (2018)'
  },
  'blake-benthall': {
    'path': 'assets/img/profiles/blake-benthall-gage-skidmore.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Blake_Benthall_by_Gage_Skidmore.jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/4/43/Blake_Benthall_by_Gage_Skidmore.jpg',
    'license': 'CC BY-SA 3.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by-sa/3.0',
    'attribution': 'Gage Skidmore (Own work)',
    'caption': 'Blake Benthall speaking at an event (Las Vegas)'
  },
  'dj-khaled': {
    'path': 'assets/img/profiles/dj-khaled-2012.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:DJ_Khaled_2012_(cropped).jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/2/25/DJ_Khaled_2012_%28cropped%29.jpg',
    'license': 'CC BY 2.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by/2.0',
    'attribution': 'Meghan Roberts (per Commons “Artist”)',
    'caption': 'DJ Khaled (2012)'
  },
  'ethan-nguyen-frosties': {
    'path': 'assets/img/profiles/ethan-nguyen.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Ethan_Nguyen.jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Ethan_Nguyen.jpg',
    'license': 'CC BY-SA 4.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by-sa/4.0',
    'attribution': 'Thnxng (Own work)',
    'caption': 'Ethan Nguyen'
  },
  'floyd-mayweather': {
    'path': 'assets/img/profiles/floyd-mayweather-dewalt.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Floyd_Mayweather%2C_Jr._at_DeWalt_event_(5888721735)_(rotated_4).jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/7/7e/Floyd_Mayweather%2C_Jr._at_DeWalt_event_%285888721735%29_%28rotated_4%29.jpg',
    'license': 'CC BY-SA 2.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by-sa/2.0',
    'attribution': 'DEWALT POWER TOOLS FIGHT NIGHT CLUB 2010 (per Commons “Artist”)',
    'caption': 'Floyd Mayweather Jr. at a DeWalt event'
  },
  'heather-morgan': {
    'path': 'assets/img/profiles/heather-morgan.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Heather_Morgan_-_USE.jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/c/cd/Heather_Morgan_-_USE.jpg',
    'license': 'CC BY-SA 4.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by-sa/4.0',
    'attribution': 'Sonyatvnash (Own work)',
    'caption': 'Heather Morgan'
  },
  'john-mcafee': {
    'path': 'assets/img/profiles/john-mcafee-gage-skidmore.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:John_McAfee_by_Gage_Skidmore.jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/7/7a/John_McAfee_by_Gage_Skidmore.jpg',
    'license': 'CC BY-SA 3.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by-sa/3.0',
    'attribution': 'Gage Skidmore (Own work)',
    'caption': 'John McAfee speaking at Politicon (Pasadena)'
  },
  'mark-scott-onecoin': {
    'path': 'assets/img/profiles/mark-scott-stevage-2014.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Mark_Scott_at_University_of_Melbourne_by_Stevage.jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/5/59/Mark_Scott_at_University_of_Melbourne_by_Stevage.jpg',
    'license': 'CC BY-SA 3.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by-sa/3.0',
    'attribution': 'Stevage (Own work)',
    'caption': 'Mark Scott speaking at the University of Melbourne (2014)'
  },
  'park-jin-hyok': {
    'path': 'assets/img/profiles/park-jin-hyok-fbi.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Park_Jin_Hyok_(Upscaled).jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/4/48/Park_Jin_Hyok_%28Upscaled%29.jpg',
    'license': 'Public domain',
    'licenseUrl': None,
    'attribution': 'FBI (per Commons credit)',
    'caption': 'Park Jin-hyok (FBI image)'
  },
  'paul-leroux': {
    'path': 'assets/img/profiles/paul-le-roux-dea.png',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Paul_Le_Roux_being_escorted_by_DEA_agents_2_(cropped).png',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/6/66/Paul_Le_Roux_being_escorted_by_DEA_agents_2_%28cropped%29.png',
    'license': 'Public domain',
    'licenseUrl': None,
    'attribution': 'Drug Enforcement Agency (DEA), via DEA SA Eric Stouch (per Commons metadata)',
    'caption': 'Paul Le Roux escorted by DEA agents (cropped)'
  },
  'steven-seagal': {
    'path': 'assets/img/profiles/steven-seagal-2016.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Steven_Seagal_November_2016.jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/d/d9/Steven_Seagal_November_2016.jpg',
    'license': 'CC BY 4.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by/4.0',
    'attribution': 'Press Service of the President of Russia (Kremlin.ru)',
    'caption': 'Steven Seagal (2016)'
  },
  'jake-paul': {
    'path': 'assets/img/profiles/jake-paul-2019.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Jake_Paul_2019.jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/8/8d/Jake_Paul_2019.jpg',
    'license': 'CC BY 2.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by/2.0',
    'attribution': 'Erik Drost (via Flickr; per Commons)',
    'caption': 'Jake Paul (2019)'
  },
  'lindsay-lohan': {
    'path': 'assets/img/profiles/lindsay-lohan-gage-skidmore-2025.jpg',
    'sourceUrl': 'https://commons.wikimedia.org/wiki/File:Lindsay_Lohan_by_Gage_Skidmore.jpg',
    'downloadUrl': 'https://upload.wikimedia.org/wikipedia/commons/b/bc/Lindsay_Lohan_by_Gage_Skidmore.jpg',
    'license': 'CC BY-SA 3.0',
    'licenseUrl': 'https://creativecommons.org/licenses/by-sa/3.0',
    'attribution': 'Gage Skidmore (Own work; per Commons)',
    'caption': 'Lindsay Lohan at CinemaCon (2025)'
  }
}

# tolerate UTF-8 BOM introduced by some Windows tooling
with open(DATA, 'r', encoding='utf-8-sig') as f:
  data = json.load(f)

seen = set()
for p in data.get('profiles', []):
  pid = p.get('id')
  if pid in patch:
    p['images'] = patch[pid]
    seen.add(pid)

missing = sorted(set(patch) - seen)
if missing:
  raise SystemExit(f"IDs not found in profiles.json: {missing}")

with open(DATA, 'w', encoding='utf-8') as f:
  json.dump(data, f, ensure_ascii=False, indent=2)
  f.write('\n')

print(f"Applied images metadata for {len(seen)} profiles")
