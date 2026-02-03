import json
from pathlib import Path

def status_label(s: str) -> str:
  m = {
    'alleged':'Alleged',
    'charged':'Charged',
    'convicted':'Convicted',
    'pleaded':'Pleaded guilty',
    'wanted':'Wanted',
    'settled':'Settled',
    'sanctioned':'Sanctioned'
  }
  return m.get((s or '').lower(), s or '—')

DATA = Path(__file__).resolve().parents[1] / 'data' / 'profiles.json'

data = json.load(open(DATA, 'r', encoding='utf-8'))
changed = 0

for p in data.get('profiles', []):
  details = p.get('details')
  if not isinstance(details, list):
    details = []

  # keep existing bullets but ensure 3–5 items (conservative, sourced-by-existing-summary/timeline)
  details = [str(x).strip() for x in details if str(x).strip()]

  # generate safe bullets only from existing fields (no new claims)
  name = p.get('name','This person')
  status = status_label(p.get('status'))
  juris = ', '.join(p.get('jurisdiction') or []) or '—'
  tags = p.get('tags') or []

  if len(details) < 3:
    if len(details) == 0:
      details.append(f"Status: {status}. Jurisdiction: {juris}.")
    if len(details) == 1:
      if tags:
        top = ', '.join(tags[:5])
        details.append(f"Key tags: {top}.")
      else:
        details.append("Key tags: —.")
    if len(details) == 2:
      tl = p.get('timeline') or []
      if tl and isinstance(tl, list):
        first = tl[0]
        d = (first or {}).get('date','')
        ev = (first or {}).get('event','')
        if d and ev:
          details.append(f"Key dated item: {d} — {ev}")
        elif d:
          details.append(f"Key dated item: {d}.")
        else:
          details.append("See timeline sources for dated events and primary documentation.")
      else:
        details.append("See timeline sources for dated events and primary documentation.")

  # cap at 5 (keep earliest items)
  if len(details) > 5:
    details = details[:5]

  if p.get('details') != details:
    p['details'] = details
    changed += 1

json.dump(data, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open(DATA, 'a', encoding='utf-8').write('\n')
print(f"standardized details for {changed} profiles")
