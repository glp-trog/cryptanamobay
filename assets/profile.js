/* CryptanamoBay — profile page
   Loads data/profiles.json and renders one profile by id (query param).
*/

const $ = (sel) => document.querySelector(sel);

function escapeHtml(str){
  return String(str ?? '')
    .replaceAll('&','&amp;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;')
    .replaceAll('"','&quot;')
    .replaceAll("'",'&#039;');
}

function statusLabel(status){
  const s = (status||'').toLowerCase();
  const map = {
    alleged: 'Alleged',
    charged: 'Charged',
    convicted: 'Convicted',
    pleaded: 'Pleaded guilty',
    wanted: 'Wanted',
    settled: 'Settled',
    sanctioned: 'Sanctioned'
  };
  return map[s] || status;
}

function statusClass(status){
  const s = (status||'').toLowerCase();
  if(['alleged','charged','convicted','pleaded','wanted','sanctioned','settled'].includes(s)) return s;
  return 'charged';
}

function qs(name){
  return new URLSearchParams(location.search).get(name);
}

async function load(){
  const id = qs('id');
  if(!id){
    $('#pError').style.display = 'inline-flex';
    $('#pError').textContent = 'Missing profile id.';
    return;
  }

  const res = await fetch('./data/profiles.json', { cache: 'no-store' });
  const data = await res.json();
  const p = (data.profiles||[]).find(x => x.id === id);

  if(!p){
    $('#pError').style.display = 'inline-flex';
    $('#pError').textContent = 'Profile not found.';
    return;
  }

  document.title = `CryptanamoBay — ${p.name}`;

  // header
  $('#pName').textContent = p.name;
  $('#pStatus').innerHTML = `<span class="pill ${statusClass(p.status)}">${escapeHtml(statusLabel(p.status))}</span>`;
  $('#pSummary').textContent = p.summary || '';

  // avatar (blank if none)
  if(p.images?.path){
    $('#pAvatar').outerHTML = `<img class="avatar avatar-lg" src="./${escapeHtml(p.images.path)}" alt="${escapeHtml(p.images.caption || p.name)}" loading="lazy" />`;
  } else {
    // keep the blank avatar div
    $('#pAvatar').classList.add('avatar-lg');
  }

  // meta
  const meta = [
    ['Status', statusLabel(p.status) || '—'],
    ['Jurisdiction', (p.jurisdiction||[]).join(', ') || '—'],
    ['Tags', (p.tags||[]).join(', ') || '—'],
  ];

  // optional image attribution block
  if(p.images?.sourceUrl){
    meta.push(['Image source', `<a href="${escapeHtml(p.images.sourceUrl)}" target="_blank" rel="noopener noreferrer">Source</a>`]);
    meta.push(['Image license', p.images.licenseUrl
      ? `<a href="${escapeHtml(p.images.licenseUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(p.images.license || 'License')}</a>`
      : escapeHtml(p.images.license || '—')
    ]);
    meta.push(['Attribution', escapeHtml(p.images.attribution || '—')]);
  }

  $('#pMeta').innerHTML = meta.map(([k,v])=>`<div>${escapeHtml(k)}</div><div>${typeof v === 'string' && v.startsWith('<a ') ? v : escapeHtml(v)}</div>`).join('');

  // timeline
  const items = (p.timeline||[]).map(item=>{
    const srcs = (item.sources||[]).map(s=>{
      const title = s.title || s.url;
      const meta = [s.publisher, s.type, s.date].filter(Boolean).join(' • ');
      return `<div class="source">• <a href="${escapeHtml(s.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(title)}</a>${meta?` <span class="small">(${escapeHtml(meta)})</span>`:''}</div>`;
    }).join('') || '<div class="small">No sources listed.</div>';

    return `
      <div class="titem">
        <div class="tdate">${escapeHtml(item.date || '')}</div>
        <div>${escapeHtml(item.event || '')}</div>
        <div class="sources">${srcs}</div>
      </div>
    `;
  }).join('') || '<div class="small">No timeline items yet.</div>';

  $('#pTimeline').innerHTML = items;
}

load().catch(err=>{
  console.error(err);
  $('#pError').style.display = 'inline-flex';
  $('#pError').textContent = 'Error loading profile.';
});
