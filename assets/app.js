/* CryptAnamoBay — static directory (no login)
   Data: /data/profiles.json
*/

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

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

function escapeHtml(str){
  return String(str ?? '')
    .replaceAll('&','&amp;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;')
    .replaceAll('"','&quot;')
    .replaceAll("'",'&#039;');
}

function matchesQuery(p, q){
  if(!q) return true;
  q = q.trim().toLowerCase();
  if(!q) return true;
  const blob = [p.name, p.summary, (p.tags||[]).join(' '), (p.jurisdiction||[]).join(' '), p.type, p.status]
    .filter(Boolean).join(' ').toLowerCase();
  return blob.includes(q);
}

function matchesFilters(p, filters){
  if(filters.status && filters.status !== 'any' && (p.status||'').toLowerCase() !== filters.status) return false;
  if(filters.type && filters.type !== 'any' && (p.type||'').toLowerCase() !== filters.type) return false;
  if(filters.tag && filters.tag !== 'any') {
    const tags = (p.tags||[]).map(t=>String(t).toLowerCase());
    if(!tags.includes(filters.tag)) return false;
  }
  return true;
}

function buildTagOptions(profiles){
  const tags = new Set();
  for(const p of profiles){
    for(const t of (p.tags||[])) tags.add(String(t).toLowerCase());
  }
  return Array.from(tags).sort();
}

function renderCounts(total, shown){
  $('#counts').innerHTML = `${shown} shown <span class="small">(of ${total})</span>`;
}

function renderTable(rows){
  const tbody = $('#tbody');
  tbody.innerHTML = rows.map(p=>{
    const tags = (p.tags||[]).slice(0,3).map(t=>`<span class="badge"><strong>#</strong>${escapeHtml(t)}</span>`).join(' ');
    const more = (p.tags||[]).length > 3 ? `<span class="badge">+${(p.tags||[]).length-3}</span>` : '';
    const imgPath = p.images?.path ? `./${p.images.path}` : './assets/img/profiles/placeholder-person.svg';
    const altText = (p.images?.caption || p.name || 'Profile image');
    const avatar = `<img class="avatar" src="${escapeHtml(imgPath)}" alt="${escapeHtml(altText)}" loading="lazy" />`;

    return `
      <tr>
        <td>
          <div style="display:flex;gap:12px;align-items:flex-start">
            ${avatar}
            <div style="display:flex;flex-direction:column;gap:6px">
              <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
                <strong>${escapeHtml(p.name)}</strong>
                <span class="pill ${statusClass(p.status)}">${escapeHtml(statusLabel(p.status))}</span>
              </div>
              <div class="small">${escapeHtml(p.summary||'')}</div>
              <div class="badges">${tags}${more}</div>
            </div>
          </div>
        </td>
        <td>${escapeHtml((p.jurisdiction||[]).join(', ') || '—')}</td>
        <td>
          <div class="row-actions">
            <button class="button" data-open="${escapeHtml(p.id)}">View</button>
          </div>
        </td>
      </tr>
    `;
  }).join('');

  $$('button[data-open]').forEach(btn=>{
    btn.addEventListener('click', ()=> openModal(btn.getAttribute('data-open')));
  });
}

let DATA = null;
let PROFILE_MAP = new Map();

function openModal(id){
  const p = PROFILE_MAP.get(id);
  if(!p) return;
  $('#modalTitle').textContent = p.name;
  $('#modalStatus').innerHTML = `<span class="pill ${statusClass(p.status)}">${escapeHtml(statusLabel(p.status))}</span>`;

  const kv = [
    ['Status', statusLabel(p.status) || '—'],
    ['Jurisdiction', (p.jurisdiction||[]).join(', ') || '—'],
    ['Tags', (p.tags||[]).join(', ') || '—'],
  ];

  const imgPath = p.images?.path ? `./${p.images.path}` : './assets/img/profiles/placeholder-person.svg';
  const altText = (p.images?.caption || p.name || 'Profile image');
  const hasMeta = !!p.images?.sourceUrl;
  const imgHtml = `<div style="display:flex;gap:12px;align-items:flex-start;margin-top:10px">
         <img class="avatar avatar-lg" src="${escapeHtml(imgPath)}" alt="${escapeHtml(altText)}" loading="lazy" />
         <div class="small">
           <div><strong>Image</strong></div>
           ${hasMeta ? `
             <div>${escapeHtml(p.images.attribution || '—')}</div>
             <div>${p.images.licenseUrl ? `<a href="${escapeHtml(p.images.licenseUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(p.images.license || 'License')}</a>` : escapeHtml(p.images.license || '—')}</div>
             <div><a href="${escapeHtml(p.images.sourceUrl)}" target="_blank" rel="noopener noreferrer">Source</a></div>
           ` : `<div>Placeholder</div>`}
         </div>
       </div>`;

  $('#modalKV').innerHTML = kv.map(([k,v])=>`<div>${escapeHtml(k)}</div><div>${escapeHtml(v)}</div>`).join('') + imgHtml;

  const timeline = (p.timeline||[]).map(item=>{
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

  $('#modalTimeline').innerHTML = timeline;

  $('#modalBackdrop').style.display = 'flex';
}

function closeModal(){
  $('#modalBackdrop').style.display = 'none';
}

function wireModal(){
  $('#modalClose').addEventListener('click', closeModal);
  $('#modalBackdrop').addEventListener('click', (e)=>{
    if(e.target.id === 'modalBackdrop') closeModal();
  });
  window.addEventListener('keydown', (e)=>{
    if(e.key === 'Escape') closeModal();
  });
}

function apply(){
  const q = $('#q').value;
  const filters = {
    status: $('#status').value,
    type: $('#type').value,
    tag: $('#tag').value,
  };

  const all = DATA.profiles || [];
  const rows = all
    .filter(p=>matchesFilters(p, filters))
    .filter(p=>matchesQuery(p, q))
    .sort((a,b)=> (a.name||'').localeCompare(b.name||''));

  renderCounts(all.length, rows.length);
  renderTable(rows);
}

async function main(){
  wireModal();
  const res = await fetch('./data/profiles.json', { cache: 'no-store' });
  DATA = await res.json();
  const profiles = DATA.profiles || [];
  PROFILE_MAP = new Map(profiles.map(p=>[p.id, p]));

  // tag options
  const tags = buildTagOptions(profiles);
  const tagSel = $('#tag');
  tagSel.innerHTML = ['<option value="any">Any</option>']
    .concat(tags.map(t=>`<option value="${escapeHtml(t)}">${escapeHtml(t)}</option>`))
    .join('');

  // events
  ['q','status','type','tag'].forEach(id=>{
    $('#'+id).addEventListener('input', apply);
    $('#'+id).addEventListener('change', apply);
  });

  apply();
}

main().catch(err=>{
  console.error(err);
  $('#tbody').innerHTML = `<tr><td colspan="3" class="small">Failed to load data. Check console.</td></tr>`;
});
