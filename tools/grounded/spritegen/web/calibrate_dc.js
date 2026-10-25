// Kalibratie tegen de pixel-overs uit de Dragonfly Cave-gids (Hitmonchan: zelfde tekening; Vulpix: DC gebruikte de oude art).
// De koppeling tekening -> spriteraster (schaal + verschuiving) is vooraf bepaald op figuur-IoU (align_*.json);
// kleurgroepen krijgen het palet dat de gebruiker zou kiezen (meeste stemmen). Score: figuur, lijnen (±1 px), K/l, toon.
// Gebruik: node calibrate_dc.js tekening.json dc_lab.json palet.json align.json schaal [instellingen.json] [uit.json]
const PO = require('./po_engine.js'), fs = require('fs');
const lumOf = c => 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2];
function makeCase(files, sc, extra) {
const [img, ref, RP, AL] = files.map(f => JSON.parse(fs.readFileSync(f)));
const W = ref.w, H = ref.h, [, fx, fy, cx, cy, scx, scy] = AL;
const names = Object.keys(RP);
let cacheA = null, cacheKey = '';
function render(p) {
  const o = Object.assign({}, PO.DEFAULTS, { k: names.length + 2 }, extra, p);
  o.map = { w: W, h: H, fx: fx * sc, fy: fy * sc, x0: (cx - scx * fx) * sc, y0: (cy - scy * fy) * sc };
  const ak = ['k', 'lineR', 'lineT', 'dark', 'spotMin', 'shadeGap'].map(k => o[k]).join();
  const A = ak === cacheKey ? cacheA : (cacheA = PO.analyse(img, o)); cacheKey = ak;
  // groep -> palet: meeste stemmen van DC-materiaal onder de groep
  const P0 = PO.pixelover(A, o), votes = Array.from({ length: A.k }, () => ({}));
  for (let k = 0; k < W * H; k++) { const v = ref.lab[(k / W) | 0][k % W]; if (P0.fig[k] && P0.mat[k] >= 0 && v && v !== 'K' && v !== 'l') { const m = v.slice(0, -1); votes[P0.mat[k]][m] = (votes[P0.mat[k]][m] || 0) + 1; } }
  const gm = votes.map(v => Object.keys(v).sort((a, b) => v[b] - v[a])[0] || names[0]);
  o.rampLum = gm.map(n => 'hbs'.split('').map(t => lumOf(RP[n][t])));
  const P = PO.pixelover(A, o);
  const lab = new Array(W * H).fill('');
  for (let k = 0; k < W * H; k++) {
    if (!P.fig[k]) continue; const g = gm[P.mat[k]];
    if ((P.edge[k] || P.lin[k]) && !P.pseudo[k]) lab[k] = P.outline[k] === 'K' ? 'K' : 'l:' + g;
    else lab[k] = g + 'hbs'[P.tone[k]];
  }
  for (let k = 0; k < W * H; k++) if (P.inner[k]) {   // overgangspixel binnen de rand
    const i = k % W, j = (k / W) | 0; let ex = 0, ey = 0;
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const ii = i + dx, jj = j + dy; if (ii < 0 || jj < 0 || ii >= W || jj >= H || !P.fig[jj * W + ii]) { ex += dx; ey += dy; } }
    const kk = (j - Math.sign(ey)) * W + i - Math.sign(ex); if (lab[kk] && lab[kk] !== 'K' && !lab[kk].startsWith('l')) lab[kk] = 'l:' + gm[P.mat[kk]];
  }
  return lab;
}
function score(lab) {
  const R = (x, y) => (x < 0 || y < 0 || x >= W || y >= H) ? '' : ref.lab[y][x], O = (x, y) => (x < 0 || y < 0 || x >= W || y >= H) ? '' : lab[y * W + x];
  const isL = v => v === 'K' || v === 'l' || v.startsWith('l:');
  let inter = 0, uni = 0, lp = 0, lr = 0, lph = 0, lrh = 0, kl = 0, kn = 0, sh = 0, st = 0, sm = 0;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const a = O(x, y), b = R(x, y);
    if (a || b) uni++; if (a && b) inter++;
    const near = (F, x, y) => { for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) if (isL(F(x + dx, y + dy))) return true; return false; };
    if (isL(a)) { lp++; if (near(R, x, y)) lph++; } if (isL(b)) { lr++; if (near(O, x, y)) lrh++; }
    if (isL(a) && isL(b)) { kn++; if ((a === 'K') === (b === 'K')) kl++; }
    if (a && b && !isL(a) && !isL(b)) { sh++; if (a.slice(-1) === b.slice(-1)) st++; if (a.slice(0, -1) === b.slice(0, -1)) sm++; }
  }
  const r = { iou: inter / uni, lijn: (lph / lp + lrh / lr) / 2, KvsL: kl / kn, toon: st / sh, groep: sm / sh };
  r.total = 0.2 * r.iou + 0.3 * r.lijn + 0.2 * r.KvsL + 0.3 * r.toon; return r;
}
return { render, score, W, H };
}
module.exports = { makeCase };
if (require.main === module) {
const C = makeCase(process.argv.slice(2, 6), +process.argv[6], process.argv[7] ? JSON.parse(fs.readFileSync(process.argv[7])) : {});
const render = C.render, score = C.score, W = C.W, H = C.H;
const lab = render({});
const r = score(lab); console.log(JSON.stringify(Object.fromEntries(Object.entries(r).map(([k, v]) => [k, +v.toFixed(3)]))));
if (process.argv[8]) fs.writeFileSync(process.argv[8], JSON.stringify({ lab, w: W, h: H }));
}
