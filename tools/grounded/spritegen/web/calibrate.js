// Kalibratie: zoek stijlknoppen waarmee de renderer een echte sprite het best nadoet (zelfde vormen erin).
// Gebruik: node calibrate.js spec.json ref.json   (ref = lijst van 64*64 kleur-sleutels van de echte sprite)
const fs = require('fs'); const R = require('./render.js');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const ref = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
function score(st, light) {
  const s = Object.assign({}, spec, { style: Object.assign({}, spec.style, st), light });
  const { key } = R.render(s);
  let both = 0, same = 0, toneSame = 0, line = 0, lineSame = 0;
  for (let i = 0; i < key.length; i++) {
    const a = key[i], b = ref[i];
    if (!a || !b) continue;
    both++;
    if (a === b) same++;
    const la = a === 'K' || a.endsWith('l'), lb = b === 'K' || b.endsWith('l');
    if (lb) { line++; if (la) lineSame++; }
    if (!la && !lb && a.slice(-1) === b.slice(-1)) toneSame++;
  }
  return { same: same / both, tone: toneSame / both, line: lineSame / line };
}
let best = null;
for (const pillow of [0.5, 0.8, 1.0, 1.3])
  for (const lz of [0.2, 0.4, 0.6])
    for (const hi of [0.5, 0.6, 0.7, 0.8])
      for (const sh of [0.0, 0.15, 0.3, 0.45]) {
        if (sh >= hi) continue;
        const r = score({ pillow, hi, sh }, [-0.55, -0.75, lz]);
        if (!best || r.same > best.r.same) best = { r, pillow, lz, hi, sh };
      }
console.log(JSON.stringify(best));
