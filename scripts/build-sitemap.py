import json
from pathlib import Path
import datetime

BASE = 'https://cryptanamobay.com'
DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'profiles.json'
OUT_SITEMAP = Path(__file__).resolve().parents[1] / 'sitemap.xml'
OUT_ROBOTS = Path(__file__).resolve().parents[1] / 'robots.txt'


def xml_escape(s: str) -> str:
    return (s.replace('&', '&amp;')
             .replace('<', '&lt;')
             .replace('>', '&gt;')
             .replace('"', '&quot;')
             .replace("'", '&apos;'))


def main():
    data = json.load(open(DATA_PATH, 'r', encoding='utf-8-sig'))
    updated_at = data.get('updatedAt') or datetime.date.today().isoformat()
    profiles = data.get('profiles', [])

    urls = [
        ('/', updated_at),
        ('/pages/methodology.html', updated_at),
        ('/pages/disclaimer.html', updated_at),
        ('/pages/contact.html', updated_at),
    ]

    for p in profiles:
        pid = p.get('id')
        if not pid:
            continue
        # keep JS profile page for compatibility
        urls.append((f'/profile.html?id={pid}', updated_at))
        # prefer static page for indexing
        urls.append((f'/profiles/{pid}.html', updated_at))

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for path, lastmod in urls:
        lines.append('  <url>')
        lines.append(f'    <loc>{xml_escape(BASE + path)}</loc>')
        if lastmod:
            lines.append(f'    <lastmod>{xml_escape(lastmod)}</lastmod>')
        lines.append('  </url>')
    lines.append('</urlset>')

    OUT_SITEMAP.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    robots = """User-agent: *
Allow: /

Sitemap: https://cryptanamobay.com/sitemap.xml
"""
    OUT_ROBOTS.write_text(robots, encoding='utf-8')

    print(f'wrote {OUT_SITEMAP} and {OUT_ROBOTS} ({len(urls)} urls)')


if __name__ == '__main__':
    main()
