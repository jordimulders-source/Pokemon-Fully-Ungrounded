// Zoekt schuifknopstanden die op beide DC-pixel-overs tegelijk goed scoren (Hitmonchan telt dubbel: zelfde tekening).
// Gebruik: node search_dc.js <scratchmap> iteraties [start.json] [uit.json]
const { makeCase } = require('./calibrate_dc.js'), fs = require('fs'), G = process.argv[2];
const cases = [[makeCase([G + '/hitmonchan.json', G + '/hm_lab2.json', G + '/hmpal.json', G + '/align_hm.json'], 480 / 657, {}), 2],
  [makeCase([G + '/vulpix.json', G + '/dc_lab.json', G + '/dcpal.json', G + '/align_vu.json'], 480 / 876, {}), 1]];
const SPACE = { lineT: [10, 40], dark: [45, 100], lineCnt: [1, 4, 1], prune: [0, 4, 1], glob: [0, 0.8], artLum: [0, 1.6], artShade: [0, 1.5],
  hiT: [0.6, 1.8], shT: [-0.6, 0.8], round: [0, 3, 1], olK: [-0.3, 0.6], olK2: [-0.3, 0.9], olIn: [1.2, 2.01], lightX: [-0.9, 0], lightY: [-0.9, -0.2] };
let best = null, rs = 777; const rnd = () => (rs = (rs * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
const start = process.argv[4] ? JSON.parse(fs.readFileSync(process.argv[4])) : null;
const evalP = p => { let t = 0, wsum = 0; const parts = cases.map(([c, wt]) => { const r = c.score(c.render(p)); t += r.total * wt; wsum += wt; return r; }); return { total: t / wsum, parts }; };
for (let it = 0; it < +process.argv[3]; it++) {
  const p = {};
  for (const [k, [a, b, step]] of Object.entries(SPACE)) {
    const base = best ? best.p[k] : start && k in start ? start[k] : null;
    let v = base !== null && (it === 0 || rnd() < 0.75) ? base + (it === 0 ? 0 : (rnd() - 0.5) * (b - a) * 0.25) : a + rnd() * (b - a);
    v = Math.max(a, Math.min(b, v)); if (step) v = Math.round(v); p[k] = v;
  }
  if (p.olK2 < p.olK) p.olK2 = p.olK;
  const r = evalP(p);
  if (!best || r.total > best.r.total) { best = { p, r }; console.log(it, r.total.toFixed(4), r.parts.map(x => JSON.stringify(Object.fromEntries(Object.entries(x).map(([k, v]) => [k, +v.toFixed(3)])))).join(' ')); }
}
console.log(JSON.stringify(best.p));
if (process.argv[5]) fs.writeFileSync(process.argv[5], JSON.stringify(best.p));
