/* Daftar kuis (Kelas > Mapel > Kuis) dan titik mulai aplikasi. */

/* ---------- daftar kuis: Kelas > Mapel > Kuis ---------- */
let LIST = [], QRY = '', LIMIT = 40;
const mk = (tag, cls, text) => { const e = document.createElement(tag); if(cls) e.className = cls; if(text != null) e.textContent = text; return e; };
const nat = (a, b) => a.localeCompare(b, 'id', {numeric: true});
const goto = (kelas, mapel) => '?' + (kelas ? 'kelas=' + encodeURIComponent(kelas) : '') + (mapel ? '&mapel=' + encodeURIComponent(mapel) : '');
const CHEV = '<svg class="i" style="width:20px;height:20px"><use href="#i-right"/></svg>';
// isi kotak kecil di kartu: angka kelas ("Kelas 10" → 10), singkatan ("TKA SMA" → TKA), atau dua huruf awal
const tileOf = s => {
  const m = s.match(/\d+/); if(m) return m[0];
  const w = s.split(/\s+/)[0]; if(/^[A-Z]{2,4}$/.test(w)) return w;
  return s.replace(/[^A-Za-z]/g, '').slice(0, 2) || '?';
};

function setBack(){
  fetch('daftar.json').then(r => r.json()).then(d => {
    const e = (d.kuis || []).find(k => k.path === JSON_PATH);
    if(e){
      document.querySelectorAll('a[data-back]').forEach(a => a.href = goto(e.kelas, e.mapel));
      if(!review) $('badge').textContent = e.kelas + ' · ' + e.mapel;
    }
  }).catch(() => {});
}

function card(href, title, meta){
  const a = mk('a', 'b-card'); a.href = href;
  a.appendChild(mk('div', 'b-tile', tileOf(title)));
  a.appendChild(mk('b', '', title)); a.appendChild(mk('span', '', meta));
  a.insertAdjacentHTML('beforeend', `<span class="b-go">${CHEV}</span>`);
  return a;
}
function row(k, withCtx){
  const a = mk('a', 'b-item');
  a.href = '?kuis=' + k.path.split('/').map(encodeURIComponent).join('/');
  const n = mk('div', 'b-n', k.questions || '–'); n.appendChild(mk('small', '', 'soal')); a.appendChild(n);
  const main = mk('div', 'b-main');
  if(withCtx){ const c = mk('div', 'b-ctx'); c.appendChild(mk('span', '', k.kelas)); c.appendChild(mk('span', '', k.mapel)); main.appendChild(c); }
  main.appendChild(mk('div', 'b-title', k.title));
  const meta = k.topic && !k.title.toLowerCase().includes(k.topic.toLowerCase()) ? k.topic : '';
  if(meta) main.appendChild(mk('div', 'b-meta', meta));
  a.appendChild(main);
  a.insertAdjacentHTML('beforeend', `<span class="b-go">${CHEV}</span>`);
  return a;
}

function draw(){
  const kelas = _P.get('kelas') || '', mapel = _P.get('mapel') || '';
  const scope = LIST.filter(k => (!kelas || k.kelas === kelas) && (!mapel || k.mapel === mapel));
  const term = QRY.trim().toLowerCase();
  const box = $('blist'); box.innerHTML = '';
  $('more').classList.add('hidden'); $('bempty').classList.add('hidden'); $('bcount').classList.add('hidden');

  // jejak
  const cr = $('crumbs'); cr.innerHTML = '';
  cr.classList.toggle('hidden', !kelas);
  if(kelas){
    const add = (t, href) => { if(cr.children.length) cr.appendChild(mk('span', '', '›')); if(href){ const a = mk('a', '', t); a.href = href; cr.appendChild(a); } else cr.appendChild(mk('span', 'cur', t)); };
    add('Semua kelas', '?');
    add(kelas, mapel ? goto(kelas) : null);
    if(mapel) add(mapel, null);
  }
  $('b-h1').textContent = !kelas ? 'Mau latihan apa hari ini?' : !mapel ? kelas : mapel;
  $('b-lead').textContent = !kelas ? 'Pilih kelas, lalu mata pelajaran, lalu kuis yang ingin dikerjakan.'
    : !mapel ? 'Pilih mata pelajaran.' : `Pilih kuis ${mapel} ${kelas} yang ingin dikerjakan.`;
  $('search').placeholder = !kelas ? 'Cari kuis di semua kelas…' : 'Cari kuis di ' + (mapel ? kelas + ' · ' + mapel : kelas) + '…';

  if(kelas && !scope.length){
    $('bempty').textContent = 'Belum ada kuis untuk pilihan ini.'; $('bempty').classList.remove('hidden'); return;
  }

  // pencarian: daftar datar di dalam cakupan yang sedang dibuka
  if(term){
    const hits = scope.filter(k => [k.title, k.topic, k.summary, k.kelas, k.mapel, ...(k.topik || [])].join(' ').toLowerCase().includes(term));
    $('bcount').textContent = hits.length + ' kuis ditemukan'; $('bcount').classList.remove('hidden');
    if(!hits.length){ $('bempty').textContent = 'Tidak ada kuis yang cocok.'; $('bempty').classList.remove('hidden'); return; }
    const ul = mk('div', 'b-list'); ul.style.marginTop = '12px';
    hits.slice(0, LIMIT).forEach(k => ul.appendChild(row(k, !mapel)));
    box.appendChild(ul);
    $('more').classList.toggle('hidden', hits.length <= LIMIT);
    return;
  }

  if(!kelas){                               // langkah 1: kelas
    const g = new Map();
    scope.forEach(k => { if(!g.has(k.kelas)) g.set(k.kelas, {m: new Set(), n: 0}); const o = g.get(k.kelas); o.m.add(k.mapel); o.n++; });
    const grid = mk('div', 'b-cards');
    [...g.keys()].sort(nat).forEach(c => grid.appendChild(card(goto(c), c, g.get(c).m.size + ' mapel · ' + g.get(c).n + ' kuis')));
    box.appendChild(grid);
  } else if(!mapel){                        // langkah 2: mapel
    const g = new Map();
    scope.forEach(k => g.set(k.mapel, (g.get(k.mapel) || 0) + 1));
    const grid = mk('div', 'b-cards');
    [...g.keys()].sort(nat).forEach(m => grid.appendChild(card(goto(kelas, m), m, g.get(m) + ' kuis')));
    box.appendChild(grid);
  } else {                                  // langkah 3: kuis
    $('bcount').textContent = scope.length + ' kuis'; $('bcount').classList.remove('hidden');
    const ul = mk('div', 'b-list'); ul.style.marginTop = '12px';
    scope.slice(0, LIMIT).forEach(k => ul.appendChild(row(k, false)));
    box.appendChild(ul);
    $('more').classList.toggle('hidden', scope.length <= LIMIT);
  }
}

function browse(){
  $('title').textContent = 'Pilih kuis';
  document.title = 'Nalarin Kuis';
  show('browse');
  $('search').oninput = e => { QRY = e.target.value; LIMIT = 40; draw(); };
  $('more').onclick = () => { LIMIT += 40; draw(); };
  fetch('daftar.json', {cache: 'no-cache'})
    .then(r => { if(!r.ok) throw new Error(r.status); return r.json(); })
    .then(d => { LIST = d.kuis || []; if(!LIST.length) throw new Error('kosong'); draw(); })
    .catch(() => {
      ['b-lead','b-h1'].forEach(i => $(i).classList.add('hidden'));
      document.querySelector('.sbox').classList.add('hidden');
      const e = $('berr'); e.classList.remove('hidden');
      e.innerHTML = 'Daftar kuis belum bisa dimuat. Jalankan <code>python3 buat-daftar.py</code> di folder ini, lalu buka halaman lewat server (bukan langsung dari file).';
    });
}

/* ---------- mulai ---------- */
BROWSE ? browse() : load();
