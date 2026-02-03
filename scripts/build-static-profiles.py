import json
from pathlib import Path
import datetime

BASE = 'https://cryptanamobay.com'
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'profiles.json'
OUT_DIR = ROOT / 'profiles'


def esc(s: str) -> str:
    return (str(s or '')
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#039;'))


def status_label(status: str) -> str:
    m = {
        'alleged': 'Alleged',
        'charged': 'Charged',
        'convicted': 'Convicted',
        'pleaded': 'Pleaded guilty',
        'wanted': 'Wanted',
        'settled': 'Settled',
        'sanctioned': 'Sanctioned'
    }
    return m.get((status or '').lower(), status or '')


def build_page(p: dict, updated_at: str) -> str:
    pid = p.get('id','')
    name = p.get('name','')
    summary = p.get('summary','')
    status = status_label(p.get('status'))
    juris = ', '.join(p.get('jurisdiction') or []) or '—'
    tags = ', '.join(p.get('tags') or []) or '—'

    title = f"{name} — CryptanamoBay"
    desc = (f"{name}: {status}. {summary}" if summary else f"{name}: {status}.")
    # keep description within a reasonable length
    if len(desc) > 175:
        desc = desc[:172].rsplit(' ', 1)[0] + '…'

    canonical = f"{BASE}/profiles/{pid}.html"

    # avatar
    img_html = ""
    if (p.get('images') or {}).get('path'):
        ipath = p['images']['path']
        alt = p['images'].get('caption') or name
        img_html = f"<img class=\"avatar avatar-lg\" src=\"../{esc(ipath)}\" alt=\"{esc(alt)}\" loading=\"lazy\" />"
    else:
        img_html = "<div class=\"avatar avatar-lg\" aria-hidden=\"true\"></div>"

    # details
    details = p.get('details') if isinstance(p.get('details'), list) else []
    details_html = (
        '<ul style="margin:0;padding-left:18px">' +
        ''.join([f"<li class=\"small\" style=\"margin:6px 0\">{esc(x)}</li>" for x in details]) +
        '</ul>'
    ) if details else '<div class="small">No additional details yet.</div>'

    # timeline
    timeline = p.get('timeline') if isinstance(p.get('timeline'), list) else []
    items = []
    for item in timeline:
        date = esc((item or {}).get('date',''))
        event = esc((item or {}).get('event',''))
        sources = (item or {}).get('sources') or []
        src_html = []
        for s in sources:
            url = esc((s or {}).get('url',''))
            stitle = esc((s or {}).get('title') or (s or {}).get('url',''))
            meta = '  '
            meta_bits = [ (s or {}).get('publisher'), (s or {}).get('type'), (s or {}).get('date') ]
            meta_text = '  '.join([b for b in meta_bits if b])
            meta_text = esc(meta_text)
            src_html.append(
                f"<div class=\"source\">• <a href=\"{url}\" target=\"_blank\" rel=\"noopener noreferrer\">{stitle}</a>" +
                (f" <span class=\"small\">({meta_text})</span>" if meta_text else "") +
                "</div>"
            )
        src_block = ''.join(src_html) if src_html else '<div class="small">No sources listed.</div>'
        items.append(
            "<div class=\"titem\">"
            f"<div class=\"tdate\">{date}</div>"
            f"<div>{event}</div>"
            f"<div class=\"sources\">{src_block}</div>"
            "</div>"
        )
    timeline_html = ''.join(items) if items else '<div class="small">No timeline items yet.</div>'

    # optional image attribution
    img_meta_html = ''
    if (p.get('images') or {}).get('sourceUrl'):
        im = p['images']
        src = esc(im.get('sourceUrl'))
        lic = esc(im.get('license') or '—')
        licu = im.get('licenseUrl')
        lic_link = f"<a href=\"{esc(licu)}\" target=\"_blank\" rel=\"noopener noreferrer\">{lic}</a>" if licu else lic
        attr = esc(im.get('attribution') or '—')
        img_meta_html = (
            "<div class=\"titem\" style=\"margin-top:12px\">"
            "<div class=\"small\"><strong>Image attribution</strong></div>"
            f"<div class=\"small\">{attr}</div>"
            f"<div class=\"small\">{lic_link}</div>"
            f"<div class=\"small\"><a href=\"{src}\" target=\"_blank\" rel=\"noopener noreferrer\">Source</a></div>"
            "</div>"
        )

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{esc(title)}</title>
  <meta name=\"description\" content=\"{esc(desc)}\" />
  <link rel=\"canonical\" href=\"{esc(canonical)}\" />
  <meta property=\"og:title\" content=\"{esc(title)}\" />
  <meta property=\"og:description\" content=\"{esc(desc)}\" />
  <meta property=\"og:url\" content=\"{esc(canonical)}\" />
  <meta property=\"og:type\" content=\"article\" />
  <link rel=\"stylesheet\" href=\"../assets/styles.css?v=20260203a\" />
</head>
<body>
  <div class=\"container\">
    <div class=\"header\">
      <div class=\"brand\">
        <div class=\"brandline\">
          <img class=\"logo\" src=\"../assets/img/logo.png\" alt=\"CryptanamoBay logo\" />
          <h1 style=\"margin:0\"><a href=\"../index.html\" style=\"color:inherit\">CryptanamoBay</a></h1>
        </div>
        <p>Profile details (timeline + sources). If something is wrong, use Contact / Corrections.</p>
      </div>
      <div class=\"nav\">
        <a href=\"../index.html\">Directory</a>
        <a href=\"../pages/methodology.html\">Methodology</a>
        <a href=\"../pages/disclaimer.html\">Disclaimer</a>
        <a href=\"../pages/contact.html\">Contact / Corrections</a>
      </div>
    </div>

    <div class=\"panel\" style=\"margin-top:16px\">
      <div style=\"display:flex;gap:14px;align-items:flex-start\">
        {img_html}
        <div style=\"flex:1;display:flex;flex-direction:column;gap:8px\">
          <div style=\"display:flex;gap:10px;align-items:center;flex-wrap:wrap\">
            <h2 style=\"margin:0;font-size:18px\">{esc(name)}</h2>
            <div><span class=\"pill {esc((p.get('status') or 'charged').lower())}\">{esc(status)}</span></div>
          </div>
          <div class=\"small\">{esc(summary)}</div>
          <div class=\"kv\" style=\"margin-top:6px\">
            <div>Status</div><div>{esc(status) or '—'}</div>
            <div>Jurisdiction</div><div>{esc(juris)}</div>
            <div>Tags</div><div>{esc(tags)}</div>
            <div>Last updated</div><div>{esc(updated_at)}</div>
          </div>
        </div>
      </div>

      <div style=\"margin-top:14px\">
        <h3 style=\"margin:0 0 8px 0\">Details</h3>
        <div class=\"titem\" style=\"background:rgba(15,23,42,.35)\">{details_html}</div>
      </div>

      <div style=\"margin-top:14px\">
        <h3 style=\"margin:0 0 8px 0\">Timeline</h3>
        <div class=\"timeline\">{timeline_html}</div>
      </div>

      {img_meta_html}
    </div>

    <div class=\"footer\">
      <div>Data source: <code>data/profiles.json</code></div>
    </div>
  </div>
</body>
</html>
"""


def main():
    data = json.load(open(DATA_PATH, 'r', encoding='utf-8'))
    updated_at = data.get('updatedAt') or datetime.date.today().isoformat()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    for p in data.get('profiles', []):
        pid = p.get('id')
        if not pid:
            continue
        html = build_page(p, updated_at)
        (OUT_DIR / f"{pid}.html").write_text(html, encoding='utf-8')
        written += 1

    # add a lightweight index redirect page? (optional later)
    print('wrote', written, 'static profile pages to', OUT_DIR)


if __name__ == '__main__':
    main()
