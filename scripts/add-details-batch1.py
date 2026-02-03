import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data' / 'profiles.json'

details = {
  'sam-bankman-fried': [
    'FTX founder; U.S. criminal case resulted in conviction (see timeline sources).',
    'CFTC filed a civil fraud complaint in SDNY against Bankman-Fried and related entities (see timeline sources).',
    'Use “convicted” label for the criminal posture; separate civil allegations are cited in sources.',
    'Case posture may evolve via sentencing/appeal; verify latest filings when updating.'
  ],
  'changpeng-zhao': [
    'Binance founder/ex-CEO; publicly reported guilty plea in U.S. federal proceedings (see cited sources).',
    'Commonly framed as AML/BSA compliance enforcement rather than “scam” allegations.',
    'For specifics (counts/terms), rely on DOJ/court documents or official summaries when adding more detail.'
  ],
  'do-kwon': [
    'Terra/Luna co-founder associated with the Terra ecosystem collapse; U.S. charges have been publicly reported (see timeline sources).',
    'Jurisdiction listed as US, KR; extradition/court posture can change and should be verified periodically.',
    'Keep language tight: “charged” does not imply guilt.'
  ],
  'alex-mashinsky': [
    'Former Celsius CEO; U.S. criminal/agency charges have been publicly reported (see timeline sources).',
    'Celsius-related allegations are often tied to marketing/representations and the handling of customer assets (verify with primary docs when available).',
    'Profile should be updated to include primary charging documents/DOJ releases when accessible.'
  ],
  'caroline-ellison': [
    'Former Alameda Research CEO; CFTC press releases describe fraud charges in the FTX matter (see timeline sources).',
    'Entered a guilty plea in a parallel SDNY criminal case (per public reporting / references).',
    'Distinguish civil allegations (CFTC) from criminal plea posture in wording.'
  ],
  'gary-wang': [
    'FTX co-founder; added to the CFTC’s amended complaint in the FTX civil action (see timeline sources).',
    'Entered a guilty plea in the parallel SDNY criminal case (per public reporting / references).',
    'Keep updates scoped to cited sources; avoid speculative claims.'
  ],
  'nishad-singh': [
    'Former FTX engineering executive; CFTC filed civil fraud charges in SDNY (see timeline sources).',
    'Entered a guilty plea in the parallel SDNY criminal case (per public reporting / references).',
    'As with other FTX profiles, separate civil allegations vs criminal posture clearly.'
  ],
  'ross-ulbricht': [
    'Silk Road creator/operator; convicted in U.S. federal court and sentenced to life in prison (DOJ press release cited).',
    'Bitcoin was widely used on Silk Road; include only what is supported by court/DOJ sources.',
    'If adding more depth, cite trial verdict, sentencing memo, and judgment (primary docs) where possible.'
  ],
  'ruja-ignatova': [
    'OneCoin figure described by U.S. authorities as a fugitive; listed on the FBI Ten Most Wanted Fugitives (FBI PDF cited).',
    '“Wanted” status reflects law-enforcement posture, not a conviction.',
    'If adding more detail, prefer DOJ/SDNY releases and FBI wanted materials over secondary reporting.'
  ],
  'heather-morgan': [
    'Pleaded guilty in U.S. proceedings tied to laundering funds linked to the Bitfinex hack (see timeline sources).',
    'Often referenced alongside Ilya Lichtenstein in public summaries of the case.',
    'For deeper detail, add DOJ case press releases and plea documents if available.'
  ],
  'ilya-lichtenstein': [
    'Pleaded guilty in U.S. proceedings tied to laundering funds linked to the Bitfinex hack (see timeline sources).',
    'Often referenced alongside Heather Morgan in public summaries of the case.',
    'For deeper detail, add DOJ case press releases and plea documents if available.'
  ],
  'avraham-eisenberg': [
    'CFTC press release alleges manipulative/deceptive conduct involving Mango Markets and misappropriation of funds (see CFTC source).',
    'Use “charged” to reflect enforcement posture; allegations remain allegations unless adjudicated.',
    'If adding depth, link the complaint PDF/docket when available.'
  ],
  'arthur-hayes': [
    'BitMEX co-founder; publicly reported guilty plea in a U.S. Bank Secrecy Act / AML-program case (see timeline sources).',
    'Further depth should cite DOJ OPA releases and/or court documents rather than summaries where possible.'
  ],
  'john-mcafee': [
    'Cybersecurity entrepreneur; included due to publicly reported U.S. criminal charges related to crypto promotion/tax matters (verify posture in cited sources).',
    'Ensure any claims about outcomes are supported by official or primary documentation before adding them.',
    'If expanding, prefer DOJ press releases and charging documents.'
  ]
}

with open(DATA, 'r', encoding='utf-8') as f:
  data = json.load(f)

found = 0
for p in data.get('profiles', []):
  pid = p.get('id')
  if pid in details:
    p['details'] = details[pid]
    found += 1

with open(DATA, 'w', encoding='utf-8') as f:
  json.dump(data, f, ensure_ascii=False, indent=2)
  f.write('\n')

print('added details for', found)
