/* Pixel-over-motor voor de Spritewerkplaats: 2D-tekening -> Gen 3-sprite, stap voor stap volgens de Dragonfly Cave-gids
   (zie tools/grounded/spritegen/METHODE.md, secties C-F). Werkt op ruwe RGBA-data, in de browser en in Node.
   analyse(): figuur, lijnen, kleurgroepen en cel-schaduw van de tekening (eenmalig per tekening + instellingen).
   pixelover(): de spritestappen C1-C8 met alle tussenstappen, zodat de editor elke stap kan tonen. */
(function (root) {
  'use strict';
  const NB4 = [[1, 0], [-1, 0], [0, 1], [0, -1]];

  function integral(a, w, h) {
    const I = new Float64Array((w + 1) * (h + 1));
    for (let y = 0; y < h; y++) { let row = 0; for (let x = 0; x < w; x++) { row += a[y * w + x]; I[(y + 1) * (w + 1) + x + 1] = I[y * (w + 1) + x + 1] + row; } }
    return I;
  }
  function boxAt(I, w, h, cx, cy, k) {
    const r = k / 2;
    const x0 = Math.max(0, Math.round(cx - r)), x1 = Math.min(w, Math.round(cx + r)), y0 = Math.max(0, Math.round(cy - r)), y1 = Math.min(h, Math.round(cy + r));
    const n = Math.max(1, (x1 - x0) * (y1 - y0));
    return (I[y1 * (w + 1) + x1] - I[y0 * (w + 1) + x1] - I[y1 * (w + 1) + x0] + I[y0 * (w + 1) + x0]) / n;
  }
  function rng(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }

  // ---------- analyse van de tekening ----------
  function analyse(img, o) {
    const { w, h, data } = img, n = w * h;
    const lum = new Float32Array(n), sat = new Float32Array(n);
    let hasAlpha = false;
    for (let i = 0; i < n; i++) {
      const r = data[i * 4], g = data[i * 4 + 1], b = data[i * 4 + 2];
      lum[i] = 0.3 * r + 0.59 * g + 0.11 * b;
      const mx = Math.max(r, g, b), mn = Math.min(r, g, b); sat[i] = mx ? (mx - mn) / mx : 0;
      if (data[i * 4 + 3] < 128) hasAlpha = true;
    }
    // 1. figuur: transparantie, of de achtergrond vanaf de rand wegvullen
    const fig = new Uint8Array(n);
    if (hasAlpha) { for (let i = 0; i < n; i++) fig[i] = data[i * 4 + 3] >= 128 ? 1 : 0; }
    else {
      const border = [];
      for (let x = 0; x < w; x++) border.push(x, (h - 1) * w + x);
      for (let y = 0; y < h; y++) border.push(y * w, y * w + w - 1);
      // achtergrondkleuren: de vlakke kleuren die op de rand veel voorkomen (officiële art heeft soms een tweede vlak)
      const hist = {};
      for (const i of border) { const key = (data[i * 4] >> 3) + ',' + (data[i * 4 + 1] >> 3) + ',' + (data[i * 4 + 2] >> 3); hist[key] = (hist[key] || 0) + 1; }
      const modes = Object.entries(hist).filter(([, c]) => c > border.length * 0.03).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([key]) => {
        const kk = key.split(',').map(Number), sel = border.filter(i => (data[i * 4] >> 3) === kk[0] && (data[i * 4 + 1] >> 3) === kk[1] && (data[i * 4 + 2] >> 3) === kk[2]);
        return [0, 1, 2].map(c => sel.reduce((a, i) => a + data[i * 4 + c], 0) / sel.length);
      });
      const isBg = i => modes.some(m => Math.hypot(data[i * 4] - m[0], data[i * 4 + 1] - m[1], data[i * 4 + 2] - m[2]) < o.bgTol);
      const bg = new Uint8Array(n), st = [];
      for (const i of border) if (isBg(i) && !bg[i]) { bg[i] = 1; st.push(i); }
      while (st.length) {
        const i = st.pop(), x = i % w, y = (i / w) | 0;
        for (const [dx, dy] of NB4) { const xx = x + dx, yy = y + dy; if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue; const j = yy * w + xx; if (!bg[j] && isBg(j)) { bg[j] = 1; st.push(j); } }
      }
      // ingesloten achtergrond (bijv. het gat tussen staart en lijf) is ook achtergrond als het vlak groot genoeg is
      const seen2 = new Uint8Array(n);
      for (let s0 = 0; s0 < n; s0++) if (!bg[s0] && !seen2[s0] && isBg(s0)) {
        const comp = [s0], q = [s0]; seen2[s0] = 1;
        while (q.length) { const i = q.pop(), x = i % w, y = (i / w) | 0; for (const [dx, dy] of NB4) { const xx = x + dx, yy = y + dy; if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue; const j = yy * w + xx; if (!bg[j] && !seen2[j] && isBg(j)) { seen2[j] = 1; q.push(j); comp.push(j); } } }
        if (comp.length > n * o.holeMin) for (const i of comp) bg[i] = 1;
      }
      for (let i = 0; i < n; i++) fig[i] = bg[i] ? 0 : 1;
      // grootste samenhangende figuur houden
      const lab = new Int32Array(n); let best = 0, bestN = 0, cur = 0;
      for (let s = 0; s < n; s++) if (fig[s] && !lab[s]) {
        cur++; let cnt = 0; const q = [s]; lab[s] = cur;
        while (q.length) { const i = q.pop(); cnt++; const x = i % w, y = (i / w) | 0; for (const [dx, dy] of NB4) { const xx = x + dx, yy = y + dy; if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue; const j = yy * w + xx; if (fig[j] && !lab[j]) { lab[j] = cur; q.push(j); } } }
        if (cnt > bestN) { bestN = cnt; best = cur; }
      }
      for (let i = 0; i < n; i++) fig[i] = lab[i] === best ? 1 : 0;
    }
    // 2. lijnen van de tekening (C2): donkere streken = veel donkerder dan hun omgeving (zwarte top-hat), plus
    //    absoluut donkere vlakken. Daarna het skelet: één lijn per streek, zoals een spriter die overtrekt.
    let fx0 = w, fx1 = 0, fy0 = h, fy1 = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (fig[y * w + x]) { if (x < fx0) fx0 = x; if (x > fx1) fx1 = x; if (y < fy0) fy0 = y; if (y > fy1) fy1 = y; }
    const fEst = Math.max((fx1 - fx0 + 1) / o.maxW, (fy1 - fy0 + 1) / o.maxH);
    const r = Math.max(2, Math.round(o.lineR || fEst * 0.4));
    const valley = sub(minF(maxF(lum, w, h, r), w, h, r), lum);
    const figE = erode(fig, w, h, 1);
    const line = new Uint8Array(n);
    for (let i = 0; i < n; i++) line[i] = figE[i] && (valley[i] > o.lineT || lum[i] < o.dark) ? 1 : 0;
    const skel = thin(line, w, h);
    // donkere vlakken (riem, pupil): blijven zwart gevuld
    const dk = new Uint8Array(n); for (let i = 0; i < n; i++) dk[i] = fig[i] && lum[i] < o.dark * 0.8 ? 1 : 0;
    const darkFill = dilate(erode(dk, w, h, 2), w, h, 2);
    const darkSpots = [];   // kleine donkere details: minstens één pixel (gids: details niet laten wegvallen)
    { const seen = new Uint8Array(n);
      for (let s0 = 0; s0 < n; s0++) if (figE[s0] && lum[s0] < o.dark && !seen[s0]) {
        const q = [s0]; seen[s0] = 1; let sx = 0, sy = 0, c = 0;
        while (q.length) { const i = q.pop(), x = i % w, y = (i / w) | 0; sx += x; sy += y; c++; for (const [dx, dy] of NB4) { const xx = x + dx, yy = y + dy; if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue; const j = yy * w + xx; if (!seen[j] && figE[j] && lum[j] < o.dark) { seen[j] = 1; q.push(j); } } }
        if (c >= o.spotMin) darkSpots.push([sx / c, sy / c]);
      } }
    // 3. kleurgroepen: k-means op kleurtint (kleur gedeeld door helderheid), zonder lijnpixels
    const R = rng(7), idx = [];
    for (let i = 0; i < n; i++) if (fig[i] && !line[i]) idx.push(i);
    const sample = []; for (let t = 0; t < Math.min(6000, idx.length); t++) sample.push(idx[Math.floor(R() * idx.length)]);
    const chrom = i => { const r = data[i * 4], g = data[i * 4 + 1], b = data[i * 4 + 2], s = r + g + b + 1; return [r / s, g / s, b / s, lum[i] / 255 * o.lumWeight]; };
    const pts = sample.map(chrom), k = Math.max(1, Math.min(o.k, pts.length));
    let cent = [pts[0]];
    while (cent.length < k) { // k-means++ (deterministisch)
      const d = pts.map(p => Math.min(...cent.map(c => dist2(p, c))));
      const tot = d.reduce((a, b) => a + b, 0); let rr = R() * tot, j = 0; while (j < d.length - 1 && (rr -= d[j]) > 0) j++;
      cent.push(pts[j]);
    }
    for (let it = 0; it < 25; it++) {
      const acc = cent.map(() => [0, 0, 0, 0, 0]);
      for (const p of pts) { let bi = 0, bd = 1e9; cent.forEach((c, ci) => { const dd = dist2(p, c); if (dd < bd) { bd = dd; bi = ci; } }); const a = acc[bi]; for (let q = 0; q < 4; q++) a[q] += p[q]; a[4]++; }
      cent = cent.map((c, ci) => acc[ci][4] ? acc[ci].slice(0, 4).map(v => v / acc[ci][4]) : c);
    }
    const mat = new Int8Array(n).fill(-1);
    for (let i = 0; i < n; i++) if (fig[i]) { const p = chrom(i); let bi = 0, bd = 1e9; cent.forEach((c, ci) => { const dd = dist2(p, c); if (dd < bd) { bd = dd; bi = ci; } }); mat[i] = bi; }
    // cel-schaduw van de tekening: per groep duidelijk donkerder dan de mediaan, alleen grotere vlakken
    const med = []; for (let q = 0; q < k; q++) { const v = []; for (let i = 0; i < n; i += 3) if (mat[i] === q && !line[i]) v.push(lum[i]); v.sort((a, b) => a - b); med.push(v.length ? v[v.length >> 1] : 128); }
    const sh0 = new Uint8Array(n);
    for (let i = 0; i < n; i++) if (fig[i] && !line[i] && lum[i] < med[mat[i]] - o.shadeGap) sh0[i] = 1;
    const artShadow = dilate(erode(sh0, w, h, 2), w, h, 2);
    const colors = cent.map(() => ({ r: 0, g: 0, b: 0, n: 0 }));
    for (let i = 0; i < n; i++) if (fig[i] && !line[i]) { const c = colors[mat[i]]; c.r += data[i * 4]; c.g += data[i * 4 + 1]; c.b += data[i * 4 + 2]; c.n++; }
    const matColors = colors.map(c => c.n ? [c.r / c.n, c.g / c.n, c.b / c.n].map(Math.round) : [128, 128, 128]);
    const matSize = colors.map(c => c.n);
    return { w, h, fig, line, skel, darkFill, darkSpots, mat, lum, k, matColors, matSize, artShadow };
  }
  function dist2(a, b) { let s = 0; for (let i = 0; i < a.length; i++) s += (a[i] - b[i]) * (a[i] - b[i]); return s; }
  function sub(a, b) { const r = new Float32Array(a.length); for (let i = 0; i < a.length; i++) r[i] = a[i] - b[i]; return r; }
  function filt1(a, w, h, rad, isMax, horiz) {
    const r = new Float32Array(a.length);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      let v = isMax ? -1e9 : 1e9;
      for (let t = -rad; t <= rad; t++) {
        const xx = horiz ? x + t : x, yy = horiz ? y : y + t; if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue;
        const u = a[yy * w + xx]; v = isMax ? (u > v ? u : v) : (u < v ? u : v);
      }
      r[y * w + x] = v;
    }
    return r;
  }
  const maxF = (a, w, h, r) => filt1(filt1(a, w, h, r, true, true), w, h, r, true, false);
  const minF = (a, w, h, r) => filt1(filt1(a, w, h, r, false, true), w, h, r, false, false);
  const erode = (m, w, h, r) => { const f = minF(Float32Array.from(m), w, h, r); return Uint8Array.from(f, v => v > 0.5 ? 1 : 0); };
  const dilate = (m, w, h, r) => { const f = maxF(Float32Array.from(m), w, h, r); return Uint8Array.from(f, v => v > 0.5 ? 1 : 0); };

  // ---------- spritestappen ----------
  function thin(m, w, h) {
    m = m.slice(); let ch = true;
    const g = (x, y) => (x < 0 || y < 0 || x >= w || y >= h) ? 0 : m[y * w + x];
    while (ch) {
      ch = false;
      for (const step of [0, 1]) {
        const rm = [];
        for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
          if (!m[y * w + x]) continue;
          const p = [g(x, y - 1), g(x + 1, y - 1), g(x + 1, y), g(x + 1, y + 1), g(x, y + 1), g(x - 1, y + 1), g(x - 1, y), g(x - 1, y - 1)];
          const B = p.reduce((a, b) => a + b, 0); let A = 0; for (let i = 0; i < 8; i++) if (!p[i] && p[(i + 1) % 8]) A++;
          const c = step === 0 ? (p[0] * p[2] * p[4] === 0 && p[2] * p[4] * p[6] === 0) : (p[0] * p[2] * p[6] === 0 && p[0] * p[4] * p[6] === 0);
          if (B >= 2 && B <= 6 && A === 1 && c) rm.push(y * w + x);
        }
        if (rm.length) { ch = true; for (const i of rm) m[i] = 0; }
      }
    }
    return m;
  }
  function prune(m, w, h, n) {
    m = m.slice();
    for (let k = 0; k < n; k++) {
      const ends = [];
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        if (!m[y * w + x]) continue; let c = 0;
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) if ((dx || dy) && x + dx >= 0 && y + dy >= 0 && x + dx < w && y + dy < h && m[(y + dy) * w + x + dx]) c++;
        if (c <= 1) ends.push(y * w + x);
      }
      if (!ends.length) break; for (const i of ends) m[i] = 0;
    }
    return m;
  }
  function lCorners(m, w, h) {   // gids D6: 1 px breed, geen L-klonten
    m = m.slice();
    for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
      if (!m[y * w + x]) continue;
      const u = m[(y - 1) * w + x], d = m[(y + 1) * w + x], l = m[y * w + x - 1], r = m[y * w + x + 1];
      if ((u || d) && (l || r) && u + d + l + r === 2) { const dy = u ? -1 : 1, dx = l ? -1 : 1; if (!m[(y - dy) * w + x - dx]) m[y * w + x] = 0; }
    }
    return m;
  }
  function maskCorners(f, w, h) {  // uitwendige traphoeken: 1 px per trede (gids D4)
    const r = f.slice();
    for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
      if (!f[y * w + x]) continue;
      const u = f[(y - 1) * w + x], d = f[(y + 1) * w + x], l = f[y * w + x - 1], rr = f[y * w + x + 1];
      if (u + d + l + rr !== 2 || (u && d) || (l && rr)) continue;
      const dy = u ? -1 : 1, dx = l ? -1 : 1;
      if (f[(y + dy) * w + x + dx] && !f[(y - dy) * w + x - dx]) r[y * w + x] = 0;
    }
    return r;
  }
  function cleanMask(f, w, h) {    // losse uitsteeksels en gaatjes van 1 px
    const r = f.slice();
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      let c = 0; for (const [dx, dy] of NB4) { const xx = x + dx, yy = y + dy; if (xx >= 0 && yy >= 0 && xx < w && yy < h && f[yy * w + xx]) c++; }
      if (f[y * w + x] && c <= 1) r[y * w + x] = 0; else if (!f[y * w + x] && c >= 3) r[y * w + x] = 1;
    }
    return r;
  }

  function pixelover(A, s) {
    const W = A.w, H = A.h;
    let x0 = W, x1 = 0, y0 = H, y1 = 0;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (A.fig[y * W + x]) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    const fw = x1 - x0 + 1, fh = y1 - y0 + 1;
    let f = Math.max(fw / s.maxW, fh / s.maxH);           // C1: verkleinen
    let w = Math.max(2, Math.round(fw / f)), h = Math.max(2, Math.round(fh / f));
    let fx = f, fy = f;
    if (s.exact) { w = s.maxW; h = s.maxH; fx = fw / w; fy = fh / h; f = Math.max(fx, fy); }   // kalibratie: exact op maat
    if (s.map) { w = s.map.w; h = s.map.h; fx = s.map.fx; fy = s.map.fy; x0 = s.map.x0; y0 = s.map.y0; f = Math.max(fx, fy); }
    const N = w * h, NBc = (i, j) => [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]];
    const inb = (i, j) => i >= 0 && j >= 0 && i < w && j < h;
    // ---- per spritepixel: wat ligt er in de tekening onder deze cel
    let fig = new Uint8Array(N); const skc = new Uint16Array(N), dark = new Uint8Array(N), mat = new Int8Array(N).fill(-1);
    const ash = new Float32Array(N), alum = new Float32Array(N);
    const cnt = new Float64Array(A.k);
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const X0 = Math.max(0, Math.round(x0 + i * fx)), X1 = Math.min(W, Math.max(X0 + 1, Math.round(x0 + (i + 1) * fx)));
      const Y0 = Math.max(0, Math.round(y0 + j * fy)), Y1 = Math.min(H, Math.max(Y0 + 1, Math.round(y0 + (j + 1) * fy)));
      if (X0 >= W || Y0 >= H) continue;
      let nf = 0, nt = 0, nd = 0, nsk = 0, ndk = 0, nl = 0, ns = 0, sl = 0; cnt.fill(0);
      for (let y = Y0; y < Y1; y++) for (let x = X0; x < X1; x++) {
        const q = y * W + x; nt++;
        if (!A.fig[q]) continue; nf++;
        if (A.skel[q]) nsk++; if (A.darkFill[q]) nd++; if (A.lum[q] < s.dark) ndk++;
        if (!A.line[q]) { nl++; cnt[A.mat[q]]++; if (A.artShadow[q]) ns++; sl += A.lum[q]; }
      }
      const k = j * w + i;
      fig[k] = nf / nt > 0.5 ? 1 : 0; skc[k] = nsk;
      dark[k] = nd / nt > 0.5 ? 1 : 0;
      if (nl) { let bm = 0; for (let q = 1; q < A.k; q++) if (cnt[q] > cnt[bm]) bm = q; mat[k] = bm; ash[k] = ns / nl; alum[k] = sl / nl; }
    }
    for (const [sx, sy] of A.darkSpots) { const i = Math.floor((sx - x0) / fx), j = Math.floor((sy - y0) / fy); if (inb(i, j)) dark[j * w + i] = 1; }
    const art = { w, h, f, x0, y0, fx, fy };
    // ---- C2: silhouet glad (losse uitsteeksels en gaatjes), één figuur
    fig = cleanMask(cleanMask(fig, w, h), w, h);
    { const lab = new Int32Array(N); let best = 0, bestN = 0, cur = 0;
      for (let s0 = 0; s0 < N; s0++) if (fig[s0] && !lab[s0]) { cur++; let c = 0; const q = [s0]; lab[s0] = cur; while (q.length) { const t = q.pop(); c++; for (const [ii, jj] of NBc(t % w, (t / w) | 0)) if (inb(ii, jj) && fig[jj * w + ii] && !lab[jj * w + ii]) { lab[jj * w + ii] = cur; q.push(jj * w + ii); } } if (c > bestN) { bestN = c; best = cur; } }
      for (let t = 0; t < N; t++) fig[t] = lab[t] === best ? 1 : 0; }
    for (let k = 0; k < N; k++) if (fig[k] && mat[k] < 0) mat[k] = nearestMat(mat, fig, w, h, k);
    const edge = new Uint8Array(N);
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) { const k = j * w + i; if (fig[k] && NBc(i, j).some(([ii, jj]) => !inb(ii, jj) || !fig[jj * w + ii])) edge[k] = 1; }
    // binnenlijnen: cellen waar het skelet van de tekenlijnen doorheen loopt, 1 px dun, korte takjes weg
    let lin = new Uint8Array(N);
    for (let k = 0; k < N; k++) lin[k] = fig[k] && (skc[k] >= s.lineCnt || edge[k]) ? 1 : 0;
    lin = thin(lin, w, h); for (let k = 0; k < N; k++) if (edge[k]) lin[k] = 0;
    for (let it = 0; it < s.prune; it++) {
      const rm = [];
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
        const k = j * w + i; if (!lin[k]) continue; let c = 0;
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) if ((dx || dy) && inb(i + dx, j + dy) && (lin[(j + dy) * w + i + dx] || edge[(j + dy) * w + i + dx])) c++;
        if (c <= 1) rm.push(k);
      }
      if (!rm.length) break; for (const k of rm) lin[k] = 0;
    }
    for (let k = 0; k < N; k++) if (!fig[k]) dark[k] = 0;
    // pseudo-omlijning (C3): delen van 1-2 px breed krijgen geen zwarte lijn maar kleur
    const pseudo = new Uint8Array(N);
    if (s.pseudo) for (let k = 0; k < N; k++) if (edge[k]) {
      const i = k % w, j = (k / w) | 0; let inner = false;
      for (let dy = -1; dy <= 1 && !inner; dy++) for (let dx = -1; dx <= 1; dx++) { const ii = i + dx, jj = j + dy; if (inb(ii, jj) && fig[jj * w + ii] && !edge[jj * w + ii]) { inner = true; break; } }
      if (!inner) pseudo[k] = 1;
    }
    // ---- E3: schaduw per vorm. Elk vlak tussen lijnen is een bol vorm; licht van linksboven.
    const inside = new Uint8Array(N); for (let k = 0; k < N; k++) inside[k] = fig[k] && !edge[k] && !lin[k] && !dark[k] ? 1 : 0;
    // omlijning en lijnen krijgen de groep van het vlak ernaast (randpixels van de tekening zijn gemengd met de achtergrond)
    { const m2 = mat.slice();
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
        const k = j * w + i; if (!fig[k] || inside[k]) continue;
        for (let rr = 1; rr <= 3; rr++) {
          const cn = new Array(A.k).fill(0); let any = false;
          for (let dy = -rr; dy <= rr; dy++) for (let dx = -rr; dx <= rr; dx++) { const ii = i + dx, jj = j + dy; if (inb(ii, jj) && inside[jj * w + ii] && mat[jj * w + ii] >= 0) { cn[mat[jj * w + ii]]++; any = true; } }
          if (any) { m2[k] = cn.indexOf(Math.max(...cn)); break; }
        }
      }
      mat.set(m2); }
    const reg = new Int32Array(N); let nreg = 0;
    for (let s0 = 0; s0 < N; s0++) if (inside[s0] && !reg[s0]) { nreg++; const q = [s0]; reg[s0] = nreg; while (q.length) { const t = q.pop(); for (const [ii, jj] of NBc(t % w, (t / w) | 0)) if (inb(ii, jj) && inside[jj * w + ii] && !reg[jj * w + ii]) { reg[jj * w + ii] = nreg; q.push(jj * w + ii); } } }
    // afstand tot de rand van het eigen vlak (euclidisch) en van het hele figuur
    const dReg = new Float32Array(N), dFig = new Float32Array(N);
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const k = j * w + i; if (!fig[k]) continue;
      let br = 99, bf = 99;
      for (let dy = -14; dy <= 14; dy++) for (let dx = -14; dx <= 14; dx++) {
        const d = Math.hypot(dx, dy); if (d >= bf && d >= br) continue;
        const ii = i + dx, jj = j + dy, out = !inb(ii, jj);
        const kk = jj * w + ii;
        if (inside[k] && d < br && (out || reg[kk] !== reg[k])) br = d;
        if (d < bf && (out || !fig[kk])) bf = d;
      }
      dReg[k] = inside[k] ? br - 0.5 : 0; dFig[k] = bf;
    }
    const blur = (val, sig, same) => {   // gaussisch, alleen binnen dezelfde groep pixels (same(k, kk))
      const rad = Math.ceil(sig * 2.5), out = new Float32Array(N), wt = [];
      for (let t = -rad; t <= rad; t++) wt.push(Math.exp(-t * t / (2 * sig * sig)));
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
        const k = j * w + i; let acc = 0, tw = 0;
        for (let dy = -rad; dy <= rad; dy++) for (let dx = -rad; dx <= rad; dx++) {
          const ii = i + dx, jj = j + dy, ww = wt[dy + rad] * wt[dx + rad]; tw += ww;
          if (inb(ii, jj) && same(k, jj * w + ii)) acc += ww * val[jj * w + ii];
        }
        out[k] = acc / tw;
      }
      return out;
    };
    const dRs = blur(dReg, 1.0, (k, kk) => reg[kk] === reg[k] && reg[k] > 0), dFs = blur(dFig, 2.5, () => true);
    const grad = (a, i, j) => { const g = (ii, jj) => inb(ii, jj) ? a[jj * w + ii] : 0; return [(g(i + 1, j) - g(i - 1, j)) / 2, (g(i, j + 1) - g(i, j - 1)) / 2]; };
    const regMax = new Float32Array(nreg + 1); for (let k = 0; k < N; k++) if (reg[k]) regMax[reg[k]] = Math.max(regMax[reg[k]], dReg[k]);
    let Lx = s.lightX, Ly = s.lightY, Lz = 0.45; { const l = Math.hypot(Lx, Ly, Lz); Lx /= l; Ly /= l; Lz /= l; }
    const rl = s.rampLum;
    const lam = new Float32Array(N);
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const k = j * w + i; if (!inside[k]) continue;
      const [gx, gy] = grad(dRs, i, j), [Gx, Gy] = grad(dFs, i, j);
      let nx = -(1 - s.glob) * gx - s.glob * Gx, ny = -(1 - s.glob) * gy - s.glob * Gy; const nn = Math.hypot(nx, ny) + 1e-6;
      const t = Math.pow(Math.max(0, Math.min(1, 1 - dReg[k] / Math.max(regMax[reg[k]] + 0.5, 1.5))), 1.2);
      const sxy = Math.sqrt(1 - (1 - t) * (1 - t)) * 0.95, Nx = nx / nn * sxy, Ny = ny / nn * sxy, Nz = Math.sqrt(Math.max(0, 1 - Nx * Nx - Ny * Ny));
      // E: de tekening zelf telt mee: hoe licht is deze plek vergeleken met de helling van zijn groep
      let u = 0.5;
      if (rl && rl[mat[k]]) { const [lh, , ls] = rl[mat[k]]; u = (alum[k] - ls) / Math.max(1, lh - ls); }
      lam[k] = (Nx * Lx + Ny * Ly + Nz * Lz) + s.artLum * u - s.artShade * ash[k];
    }
    let tone = new Int8Array(N).fill(1);
    for (let k = 0; k < N; k++) if (inside[k]) tone[k] = lam[k] > s.hiT ? 0 : lam[k] < s.shT ? 2 : 1;
    // ronde vlakken (E3): rafels en losse pixels opnemen in de meerderheid
    for (let it = 0; it < s.round; it++) {
      const c = tone.slice();
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
        const k = j * w + i; if (!inside[k]) continue; const cn = [0, 0, 0];
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) { if (!dx && !dy) continue; const ii = i + dx, jj = j + dy; if (!inb(ii, jj)) continue; const kk = jj * w + ii; if (inside[kk] && mat[kk] === mat[k]) cn[c[kk]]++; }
        const mx = Math.max(...cn); if (mx >= 5 && cn.indexOf(mx) !== c[k]) tone[k] = cn.indexOf(mx);
      }
    }
    // vacht (E7): grens basis/schaduw kartelen met een dambordje
    if (s.fur > 0) {
      const R = rng(11);
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
        const k = j * w + i; if (!inside[k] || tone[k] !== 1) continue;
        if (NBc(i, j).some(([ii, jj]) => inb(ii, jj) && tone[jj * w + ii] === 2 && inside[jj * w + ii] && mat[jj * w + ii] === mat[k]) && (i + j) % 2 === 0 && R() < s.fur) tone[k] = 2;
      }
    }
    // glans (C7, E6): kleine witte vlekjes midden in de grootste hooglichtvlakken
    const shine = [];
    if (s.shine > 0) {
      const seen = new Uint8Array(N), blobs = [];
      for (let k = 0; k < N; k++) if (inside[k] && tone[k] === 0 && !seen[k]) {
        const q = [k], px = []; seen[k] = 1;
        while (q.length) { const c = q.pop(); px.push(c); for (const [ii, jj] of NBc(c % w, (c / w) | 0)) { if (!inb(ii, jj)) continue; const kk = jj * w + ii; if (!seen[kk] && inside[kk] && tone[kk] === 0 && mat[kk] === mat[k]) { seen[kk] = 1; q.push(kk); } } }
        blobs.push(px);
      }
      blobs.sort((a, b) => b.length - a.length);
      for (const b of blobs.slice(0, s.shine)) {
        if (b.length < 6) break;
        let mx = 0, my = 0; for (const c of b) { mx += c % w; my += (c / w) | 0; } mx /= b.length; my /= b.length;
        let best = b[0], bd = 1e9; for (const c of b) { const d = Math.hypot(c % w - (mx - 0.6), ((c / w) | 0) - (my - 0.6)); if (d < bd) { bd = d; best = c; } }
        shine.push(best);
      }
    }
    // ---- F: omlijning inkleuren. Buitenrand: van het licht af zwart, naar het licht omlijningsbasis, met de overgang
    // 'zwart met 1 px omlijningsbasis binnen' ertussen. Binnenlijnen: zwart waar ze aan schaduw grenzen.
    const outline = new Array(N).fill(null), inner = new Array(N).fill(null);
    const l2 = Math.hypot(s.lightX, s.lightY), L2 = [s.lightX / l2, s.lightY / l2];
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const k = j * w + i; if (!fig[k] || pseudo[k]) continue;
      if (edge[k]) {
        let ex = 0, ey = 0;
        for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) { const ii = i + dx, jj = j + dy; if (!inb(ii, jj) || !fig[jj * w + ii]) { ex += dx; ey += dy; } }
        const l = Math.hypot(ex, ey), v = l ? (ex * L2[0] + ey * L2[1]) / l : 0;
        outline[k] = v < s.olK ? 'K' : v < s.olK2 ? 'K' : 'l';
        if (v >= s.olK && v < s.olK2) inner[k] = 'l';
      } else if (lin[k] || dark[k]) {
        let ts = 0, c = 0;
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) { const ii = i + dx, jj = j + dy; if (inb(ii, jj) && inside[jj * w + ii]) { ts += tone[jj * w + ii]; c++; } }
        outline[k] = dark[k] || !c || ts / c >= s.olIn ? 'K' : 'l';
      }
    }
    for (let k = 0; k < N; k++) if (dark[k]) lin[k] = 1;
    return { w, h, f, fig, lin, edge, pseudo, mat, tone, outline, inner, shine, art, lam };
  }
  function nearestMat(mat, fig, w, h, k) {
    const i = k % w, j = (k / w) | 0;
    for (let r = 1; r < 6; r++) for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) { const ii = i + dx, jj = j + dy; if (ii >= 0 && jj >= 0 && ii < w && jj < h && mat[jj * w + ii] >= 0) return mat[jj * w + ii]; }
    return 0;
  }

  // ---------- samenstellen per stap ----------
  // stap: 2 omlijning, 3 schaduwkleur, 4 basis, 5 hooglicht+glans, 6 eind (omlijning ingekleurd), 7 eind + handwerk
  function compose(P, pal, step, overrides, size) {
    const N = size || 64, key = new Array(N * N).fill('');
    const ox = Math.floor((N - P.w) / 2), oy = Math.max(0, N - P.h - 2);
    const put = (i, j, v) => { const x = ox + i, y = oy + j; if (x >= 0 && y >= 0 && x < N && y < N) key[y * N + x] = v; };
    for (let j = 0; j < P.h; j++) for (let i = 0; i < P.w; i++) {
      const k = j * P.w + i; if (!P.fig[k]) continue;
      const m = 'm' + P.mat[k];
      let v;
      if (step >= 3) v = m + (step === 3 ? 's' : step === 4 ? (P.tone[k] === 2 ? 's' : 'b') : 'hbs'[P.tone[k]]);
      const isLine = (P.edge[k] || P.lin[k]) && !P.pseudo[k];
      if (isLine) v = step <= 5 ? 'K' : (P.outline[k] === 'K' ? 'K' : m + P.outline[k]);
      if (step === 2 && !isLine) v = 'W';
      if (P.pseudo[k] && step >= 3) v = m + (P.tone[k] === 0 ? 'h' : 'b');
      put(i, j, v);
    }
    if (step >= 6) {   // binnenpixel van de omlijningsovergang
      for (let j = 0; j < P.h; j++) for (let i = 0; i < P.w; i++) {
        const k = j * P.w + i; const inn = P.inner[k]; if (!inn) continue;
        let ex = 0, ey = 0; for (const [dx, dy] of NB4) { const ii = i + dx, jj = j + dy; if (ii < 0 || jj < 0 || ii >= P.w || jj >= P.h || !P.fig[jj * P.w + ii]) { ex += dx; ey += dy; } }
        const ii = i - Math.sign(ex), jj = j - Math.sign(ey);
        if (ii >= 0 && jj >= 0 && ii < P.w && jj < P.h) { const kk = jj * P.w + ii; if (P.fig[kk] && !P.edge[kk] && !P.lin[kk]) put(ii, jj, 'm' + P.mat[kk] + inn); }
      }
    }
    if (step >= 5) for (const k of P.shine) put(k % P.w, (k / P.w) | 0, 'shine');
    if (step >= 7 && overrides) for (const [pos, v] of Object.entries(overrides)) { const [x, y] = pos.split(',').map(Number); key[y * N + x] = v === '_' ? '' : v; }
    return { key, ox, oy };
  }

  // ---------- controles (gids D en F) ----------
  function checks(key, pal, size) {
    const N = size || 64, res = { pixels: 0, colors: 0, black: 0, open: [], holes: [], clumps: [], lcorner: [], wobble: [] };
    const cols = new Set(); let edgeN = 0, blackN = 0;
    const has = (x, y) => x >= 0 && y >= 0 && x < N && y < N && !!key[y * N + x];
    const isLine = k => k === 'K' || /l$/.test(k) || /s$/.test(k);
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const k = key[y * N + x]; if (!k) continue; res.pixels++; if (pal[k]) cols.add(pal[k].join());
      const e = NB4.some(([dx, dy]) => !has(x + dx, y + dy));
      if (e) { edgeN++; if (k === 'K') blackN++; else if (!isLine(k) && k !== 'shine') res.open.push([x, y]); }
      if (k === 'K' && key[y * N + x + 1] === 'K' && key[(y + 1) * N + x] === 'K' && key[(y + 1) * N + x + 1] === 'K') res.clumps.push([x, y]);
    }
    res.colors = cols.size; res.black = edgeN ? blackN / edgeN : 0;
    // ingesloten gaatjes
    const seen = new Uint8Array(N * N), st = [0]; seen[0] = 1;
    while (st.length) { const i = st.pop(), x = i % N, y = (i / N) | 0; for (const [dx, dy] of NB4) { const xx = x + dx, yy = y + dy; if (xx < 0 || yy < 0 || xx >= N || yy >= N) continue; const j = yy * N + xx; if (!seen[j] && !key[j]) { seen[j] = 1; st.push(j); } } }
    for (let i = 0; i < N * N; i++) if (!key[i] && !seen[i]) res.holes.push([i % N, (i / N) | 0]);
    // curven langs het silhouet: runs langs de omtrek (Moore-tracering)
    const contour = traceContour(key, N);
    const runs = []; // [as ('h'|'v'), lengte, startpunt]
    for (let i = 0; i < contour.length;) {
      const [x, y] = contour[i]; let j = i + 1;
      if (j >= contour.length) break;
      const ax = contour[j][1] === y ? 'h' : contour[j][0] === x ? 'v' : 'd';
      if (ax === 'd') { runs.push(['d', 1, contour[i]]); i = j; continue; }
      while (j + 1 < contour.length && (ax === 'h' ? contour[j + 1][1] === y : contour[j + 1][0] === x)) j++;
      runs.push([ax, j - i + 1, contour[i]]); i = j;
    }
    for (let r = 1; r < runs.length; r++) {
      const a = runs[r - 1], b = runs[r];
      if (a[0] !== 'd' && b[0] !== 'd' && a[0] !== b[0] && a[1] >= 3 && b[1] >= 3) res.lcorner.push(b[2]);    // D4: geen neutraal segment
    }
    for (let r = 2; r < runs.length; r++) {    // D4: besluiteloosheid (lang-kort-lang in dezelfde richting)
      const a = runs[r - 2], b = runs[r - 1], c = runs[r];
      if (a[0] === c[0] && a[0] !== 'd' && b[0] === 'd' && false) res.wobble.push(b[2]);
    }
    return res;
  }
  function traceContour(key, N) {
    let start = -1;
    for (let i = 0; i < N * N && start < 0; i++) if (key[i]) start = i;
    if (start < 0) return [];
    const dirs = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]];
    const has = (x, y) => x >= 0 && y >= 0 && x < N && y < N && !!key[y * N + x];
    let x = start % N, y = (start / N) | 0, d = 6; const out = [[x, y]];
    for (let guard = 0; guard < 4 * N * N; guard++) {
      let found = false;
      for (let t = 0; t < 8; t++) { const nd = (d + 6 + t) % 8, nx = x + dirs[nd][0], ny = y + dirs[nd][1]; if (has(nx, ny)) { x = nx; y = ny; d = nd; found = true; break; } }
      if (!found || (x === out[0][0] && y === out[0][1])) break;
      out.push([x, y]);
    }
    return out;
  }

  // ---------- kleuren (gids B) ----------
  function rgb2hsl(c) { const [r, g, b] = c.map(v => v / 255), mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2; let h = 0, s = 0; if (mx !== mn) { const d = mx - mn; s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn); h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h /= 6; } return [h, s, l]; }
  function lab(c) {
    const f = v => { v /= 255; return v > 0.04045 ? Math.pow((v + 0.055) / 1.055, 2.4) : v / 12.92; };
    const [r, g, b] = c.map(f), X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.9505, Y = 0.2126 * r + 0.7152 * g + 0.0722 * b, Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.089;
    const q = t => t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116;
    return [116 * q(Y) - 16, 500 * (q(X) - q(Y)), 200 * (q(Y) - q(Z))];
  }
  function hsl2rgb([h, s, l]) { const f = n => { const k = (n + h * 12) % 12, a = s * Math.min(l, 1 - l); return Math.round(255 * (l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1)))); }; return [f(0), f(8), f(4)]; }
  // automatische helling: dezelfde tint, schaduw iets richting blauw, omlijningsbasis duidelijk donker (gids B1-B4)
  function autoRamp(c, contrast) {
    const [h, s, l] = rgb2hsl(c), k = contrast;
    const sh = (h + 0.985) % 1, hi = (h + 0.012) % 1;
    return { h: hsl2rgb([hi, Math.max(0, s * 0.92), Math.min(0.93, l + 0.16 * k)]), b: c.map(Math.round), s: hsl2rgb([sh, Math.min(1, s * 1.08), Math.max(0.06, l - 0.17 * k)]), l: hsl2rgb([sh, Math.min(1, s * 1.1), Math.max(0.04, l - 0.40 * k)]) };
  }

  // koppel elke kleurgroep aan een helling (gids B5: kleuren van een echte sprite), op kleurtint en verzadiging,
  // met de beste één-op-één-toewijzing (geen twee groepen op dezelfde helling als het kan)
  function matchRamps(groupColors, ramps) {
    const names = Object.keys(ramps);
    // kosten: verschil in kleurrichting (tinthoek in Lab; Sugimori-kleuren zijn vaak grauwer dan het palet, dus de
    // richting telt, niet de verzadiging), plus een beetje helderheid; bijna-grijs telt vooral op helderheid
    const cost = (g, n) => {
      const a = lab(groupColors[g]); let best = 1e9;
      for (const t of ['h', 'b', 's']) {
        const r = lab(ramps[n][t]), ca = Math.hypot(a[1], a[2]), cr = Math.hypot(r[1], r[2]);
        let dh = Math.abs(Math.atan2(a[2], a[1]) - Math.atan2(r[2], r[1])); if (dh > Math.PI) dh = 2 * Math.PI - dh;
        const wc = Math.min(1, Math.min(ca, cr) / 8);
        best = Math.min(best, wc * dh / Math.PI + (1 - wc) * Math.abs(ca - cr) / 40 + Math.abs(a[0] - r[0]) / 250);
      }
      return best;
    };
    const G = groupColors.length;
    let best = null, bestC = 1e9;
    const perm = (i, used, acc, c) => {
      if (c >= bestC) return;
      if (i === G) { bestC = c; best = acc.slice(); return; }
      for (const n of names) { if (used.has(n) && used.size < names.length) continue; used.add(n); acc.push(n); perm(i + 1, used, acc, c + cost(i, n)); acc.pop(); if (acc.filter(x => x === n).length === 0) used.delete(n); }
    };
    perm(0, new Set(), [], 0);
    return best || groupColors.map(() => names[0]);
  }

  const DEFAULTS = { k: 3, bgTol: 12, holeMin: 0.0015, lumWeight: 0, lineR: 0, lineT: 16, dark: 72, spotMin: 4, shadeGap: 14,
    maxW: 56, maxH: 56, lineCnt: 2, prune: 1, pseudo: true,
    lightX: -0.6, lightY: -0.71, glob: 0.23, artLum: 0.5, artShade: 1.5, hiT: 1.12, shT: 0.35, round: 2, fur: 0, shine: 1,
    olK: 0.17, olK2: 0.3, olIn: 1.8, contrast: 1 };

  const api = { analyse, pixelover, compose, checks, autoRamp, matchRamps, rgb2hsl, hsl2rgb, DEFAULTS };
  if (typeof module !== 'undefined') module.exports = api; else root.PO = api;
})(typeof self !== 'undefined' ? self : this);
