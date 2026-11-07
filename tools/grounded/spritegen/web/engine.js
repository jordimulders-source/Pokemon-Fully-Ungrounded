/* Spritegenerator-motor (JS, zelfde methode als tools/grounded/spritegen/*.py):
   3D-poppetje -> 2D-tekening (vlakke kleuren, lijnen, cel-schaduw) -> pixel-over volgens de Dragonfly Cave-gids:
   1 verkleinen, 2 omlijning overtrekken (1 px, gladde trapjes, geen L-hoeken), 3 vullen: schaduw -> basis -> hooglicht
   in ronde vlakken, 4 omlijning inkleuren (zwart aan de schaduwkant, kleurlijn aan de lichte kant, schaduwtint rond
   hooglicht), 5 details (oog), 6 handwerk (pixels met knopjes). Werkt in de browser en in Node. */
(function (root) {
  'use strict';
  // ---------- 3D ----------
  const rotY = a => { const c = Math.cos(a), s = Math.sin(a); return [[c, 0, s], [0, 1, 0], [-s, 0, c]]; };
  const rotX = a => { const c = Math.cos(a), s = Math.sin(a); return [[1, 0, 0], [0, c, -s], [0, s, c]]; };
  const rotZ = a => { const c = Math.cos(a), s = Math.sin(a); return [[c, -s, 0], [s, c, 0], [0, 0, 1]]; };
  const mm = (A, B) => A.map((r, i) => B[0].map((_, j) => r[0] * B[0][j] + r[1] * B[1][j] + r[2] * B[2][j]));
  const mv = (A, v) => [A[0][0] * v[0] + A[0][1] * v[1] + A[0][2] * v[2], A[1][0] * v[0] + A[1][1] * v[1] + A[1][2] * v[2], A[2][0] * v[0] + A[2][1] * v[1] + A[2][2] * v[2]];
  const T = A => [[A[0][0], A[1][0], A[2][0]], [A[0][1], A[1][1], A[2][1]], [A[0][2], A[1][2], A[2][2]]];
  const I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
  const deg = d => d * Math.PI / 180;
  const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]], sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const scl = (a, k) => [a[0] * k, a[1] * k, a[2] * k], len = a => Math.hypot(a[0], a[1], a[2]);
  const unit = a => scl(a, 1 / (len(a) || 1));

  function qb(a, c, b, n) { const o = []; for (let i = 0; i < n; i++) { const t = i / (n - 1); o.push([0, 1, 2].map(d => (1 - t) * (1 - t) * a[d] + 2 * (1 - t) * t * c[d] + t * t * b[d])); } return o; }

  class Model {
    constructor() { this.parts = []; this.points = {}; this.texture = null; }
    ell(c, r, mat, part, R0) { this.parts.push({ c, r: typeof r === 'number' ? [r, r, r] : r, R0: R0 || I3, mat, part }); }
    chain(pts, mat, part, step = 1.5) {
      for (let k = 0; k + 1 < pts.length; k++) {
        const a = pts[k], b = pts[k + 1];
        const n = Math.max(2, Math.floor(Math.hypot(b[0] - a[0], b[1] - a[1], b[2] - a[2]) / step));
        for (let i = 0; i < n; i++) { const t = i / n; this.ell([0, 1, 2].map(d => a[d] + (b[d] - a[d]) * t), a[3] + (b[3] - a[3]) * t, mat, part); }
      }
      const p = pts[pts.length - 1]; this.ell(p.slice(0, 3), p[3], mat, part);
    }
  }

  function camera(yaw, pitch, sx = 1) { const C = mm(rotX(deg(pitch)), rotY(deg(yaw))); C[0] = C[0].map(v => v * sx); return C; }

  function bbox(m, Rc) {
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    for (const p of m.parts) { const c = mv(Rc, p.c), r = Math.max(...p.r); x0 = Math.min(x0, c[0] - r); x1 = Math.max(x1, c[0] + r); y0 = Math.min(y0, c[1] - r); y1 = Math.max(y1, c[1] + r); }
    return [x0, x1, y0, y1];
  }

  function inv3(A) {
    const [a, b, c] = A[0], [d, e, f] = A[1], [g, h, i] = A[2];
    const det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g);
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det], [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det], [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]];
  }

  function render3d(m, Rc, S, scale, origin) {
    const mats = [...new Set(m.parts.map(p => p.mat))].sort(), parts = [...new Set(m.parts.map(p => p.part))].sort();
    const z = new Float32Array(S * S).fill(-1e9), mat = new Int16Array(S * S).fill(-1), prt = new Int16Array(S * S).fill(-1);
    const nx = new Float32Array(S * S), ny = new Float32Array(S * S), nz = new Float32Array(S * S);
    const ax = new Float32Array(S * S), ay = new Float32Array(S * S), az = new Float32Array(S * S);
    const RcT = T(Rc), Rci = inv3(Rc);
    for (const p of m.parts) {
      const cw = mv(Rc, p.c);
      const M = mm(mm([[1 / p.r[0], 0, 0], [0, 1 / p.r[1], 0], [0, 0, 1 / p.r[2]]], T(p.R0)), Rci);
      const MtM = mm(T(M), M);
      const ext = Math.max(...p.r) * Math.max(1, Math.abs(Rc[0][0]) + Math.abs(Rc[0][2]));
      const xa = Math.max(0, Math.floor((cw[0] - ext - origin[0]) * scale) - 2), xb = Math.min(S, Math.floor((cw[0] + ext - origin[0]) * scale) + 3);
      const ya = Math.max(0, Math.floor((origin[1] - cw[1] - ext) * scale) - 2), yb = Math.min(S, Math.floor((origin[1] - cw[1] + ext) * scale) + 3);
      const b = [M[0][2], M[1][2], M[2][2]], A = b[0] * b[0] + b[1] * b[1] + b[2] * b[2];
      const mi = mats.indexOf(p.mat), pi = parts.indexOf(p.part);
      for (let y = ya; y < yb; y++) {
        const py = origin[1] - (y + 0.5) / scale - cw[1];
        for (let x = xa; x < xb; x++) {
          const px = origin[0] + (x + 0.5) / scale - cw[0];
          const a0 = M[0][0] * px + M[0][1] * py, a1 = M[1][0] * px + M[1][1] * py, a2 = M[2][0] * px + M[2][1] * py;
          const B = 2 * (a0 * b[0] + a1 * b[1] + a2 * b[2]), C = a0 * a0 + a1 * a1 + a2 * a2 - 1;
          const disc = B * B - 4 * A * C; if (disc < 0) continue;
          const zz = (-B + Math.sqrt(disc)) / (2 * A), i = y * S + x;
          if (zz + cw[2] <= z[i]) continue;
          z[i] = zz + cw[2]; mat[i] = mi; prt[i] = pi;
          const q = [px, py, zz], n = mv(MtM, q), l = Math.hypot(n[0], n[1], n[2]) || 1;
          nx[i] = n[0] / l; ny[i] = n[1] / l; nz[i] = n[2] / l;
          const w = [px + cw[0], py + cw[1], zz + cw[2]], an = mv(Rci, w);
          ax[i] = an[0]; ay[i] = an[1]; az[i] = an[2];
        }
      }
    }
    let allMats = mats.slice();
    if (m.texture) {
      const res = m.texture(i => [ax[i], ay[i], az[i]], i => mats[mat[i]], S * S, mat);
      for (const n of res.names) if (!allMats.includes(n)) allMats.push(n);
      for (let i = 0; i < S * S; i++) if (mat[i] >= 0) { const nn = res.out[i]; if (nn) mat[i] = allMats.indexOf(nn); }
    }
    return { S, z, mat, part: prt, nx, ny, nz, mats: allMats, parts };
  }

  // ---------- olinguito-poppetje met schuifknoppen ----------
  function olinguito(P) {
    const m = new Model();
    const LK = P.legK, BL = P.bodyLen, HS = P.headScale, HSH = [-6, P.headLift, 0];
    const bx = x => x > -30 ? -30 + (x + 30) * BL : x;       // lijf langer naar achteren
    const L = pts => pts.map(([x, y, z, r]) => [x, y, z, r * LK]);
    const arch = P.backArch;
    m.ell([-30, 0, 0], 26 * P.bodyThick, 'fur', 'lijf');
    m.ell([bx(2), 6 + arch * 0.5, 0], [34 * BL, 24 * P.bodyThick, 23 * P.bodyThick], 'fur', 'lijf', rotZ(deg(8 + arch)));
    m.ell([bx(34), 12 + arch, 0], 25 * P.bodyThick, 'fur', 'lijf');
    const tl = P.tailLen, tb = [bx(52), 18 + arch, 0];
    const tp = qb(tb, [tb[0] + 36 * tl, tb[1] + 4, 0], [tb[0] + 32 * tl, tb[1] + 56 * tl, 0], 10).slice(0, -1)
      .concat(qb([tb[0] + 32 * tl, tb[1] + 56 * tl, 0], [tb[0] + 28 * tl * P.tailCurl, tb[1] + 98 * tl, 0], [tb[0] - 4 * tl * P.tailCurl, tb[1] + 92 * tl, 0], 8).slice(0, -1))
      .concat(qb([tb[0] - 4 * tl * P.tailCurl, tb[1] + 92 * tl, 0], [tb[0] - 30 * tl * P.tailCurl, tb[1] + 86 * tl, 0], [tb[0] - 26 * tl * P.tailCurl, tb[1] + 66 * tl, 0], 6));
    m.chain(tp.map((q, i) => [q[0], q[1], q[2], (10.5 - 5 * i / (tp.length - 1)) * P.tailThick]), 'fur', 'staart');
    const piv = [-46, -2, 0];
    const H = p => add(add(piv, scl(sub(p, piv), HS)), HSH);
    m.chain([[-36, 0, 0, 22], add(piv, HSH).concat([20])], 'fur', 'lijf');
    let cr = H([-64, -6, 0]);
    m.ell(cr, [25 * HS, 28 * HS * P.headTall, 25 * HS], 'head', 'kop');
    const sn = P.snout;
    m.chain([[-76, -16, 0, 20], [-76 - 12 * sn, -16 - 6 * sn, 0, 14.5], [-76 - 22 * sn, -16 - 12 * sn, 0, 9.5]].map(q => H(q.slice(0, 3)).concat([q[3] * HS])), 'head', 'kop');
    let nose = H([-76 - 29 * sn, -16 - 15 * sn, 0]);
    m.ell(nose, 6 * HS, 'nose', 'kop');
    let eyes = [1, -1].map(s => add(cr, scl(unit([-0.70, -0.28, 0.66 * s]), 25 * HS)));
    for (const s of [1, -1]) {
      const Re = rotY(deg(s > 0 ? 25 : 0)), c = H([-58, 16, 13 * s]), k = (s > 0 ? 1 : 0.6) * P.ear;
      m.ell(c, [4 * HS * k, 12 * HS * k, 11 * HS * k], 'ear', s > 0 ? 'oor_n' : 'oor_v', Re);
      m.ell(add(c, scl(mv(Re, [-1.8, 0.5, 0]), HS * k)), [2.6 * HS * k, 8 * HS * k, 7.5 * HS * k], 'earin', s > 0 ? 'oor_n' : 'oor_v', Re);
    }
    const fl = P.frontLen;
    const fn = [[-34, -2, 13, 16], [-34 - 14 * fl, -2 - 26 * fl, 15, 11.5], [-34 - 28 * fl, -2 - 50 * fl, 17, 9]];
    m.chain(L(fn), 'fur', 'voorpoot_n');
    const pw = fn[2];
    m.ell([pw[0] - 4, pw[1] - 3, 18], [10 * LK, 6 * LK, 8 * LK], 'paw', 'voorpoot_n');
    const cl = P.claw;
    for (const dz of [-3.5, 3.5]) m.chain([[pw[0] - 10, pw[1] - 5, 18 + dz, 3.6 * P.clawThick], [pw[0] - 10 - 8 * cl, pw[1] - 5 - 9 * cl, 18 + dz, 2.6 * P.clawThick], [pw[0] - 10 - 10 * cl, pw[1] - 5 - 21 * cl, 18 + dz, 0.8 * P.clawThick]], 'claw', 'voorpoot_n', 0.8);
    const ff = [[-28, -2, -13, 14], [-28 + 8 * fl, -2 - 26 * fl, -15, 11], [-28 - 6 * fl, -2 - 40 * fl, -17, 8.5]];
    m.chain(L(ff), 'fur', 'voorpoot_v');
    const fw = ff[2];
    m.ell([fw[0] - 4, fw[1] - 3, -17], [9 * LK, 6 * LK, 7.5 * LK], 'paw', 'voorpoot_v');
    for (const dz of [-3.5, 3.5]) m.chain([[fw[0] - 10, fw[1] - 6, -17 + dz, 3.2 * P.clawThick], [fw[0] - 16 * cl, fw[1] - 6 - 9 * cl, -17 + dz, 2.2 * P.clawThick], [fw[0] - 17 * cl, fw[1] - 6 - 18 * cl, -17 + dz, 0.7 * P.clawThick]], 'claw', 'voorpoot_v', 0.8);
    m.chain(L([[bx(30), 10, 18, 20], [bx(6), -20, 21, 13], [bx(30), -42, 21, 9]]), 'fur', 'achterpoot_n');
    m.chain(L([[bx(30), -42, 21, 7.5], [bx(10), -48, 22, 6.5]]), 'paw', 'achterpoot_n');
    m.chain(L([[bx(36), 12, -17, 18], [bx(18), -16, -19, 11.5], [bx(40), -36, -19, 8.5]]), 'fur', 'achterpoot_v');
    m.chain(L([[bx(40), -36, -19, 7], [bx(24), -42, -20, 6]]), 'paw', 'achterpoot_v');
    // kop draait (extra) naar de kijker
    if (P.headTurn) {
      const neck = add(piv, HSH), Rh = rotY(deg(P.headTurn));
      for (const p of m.parts) if (['kop', 'oor_n', 'oor_v'].includes(p.part)) { p.c = add(neck, mv(Rh, sub(p.c, neck))); p.R0 = mm(Rh, p.R0); }
      cr = add(neck, mv(Rh, sub(cr, neck))); nose = add(neck, mv(Rh, sub(nose, neck))); eyes = eyes.map(e => add(neck, mv(Rh, sub(e, neck))));
    }
    m.points.oog = eyes[0];
    const HSc = 25 * HS;
    m.texture = (an, name, n, mat) => {
      const out = new Array(n);
      for (let i = 0; i < n; i++) {
        if (mat[i] < 0 || name(i) !== 'head') continue;
        const q = an(i), u = scl(sub(q, cr), 1 / HSc);
        let nm = 'head';
        if (u[0] * 0.75 + u[1] * 0.66 > 0.72) nm = 'fur';
        if (len(sub(q, nose)) < 9 * HS * P.muzzle) nm = 'muzzle';
        const de = Math.min(...eyes.map(e => len(sub(q, e))));
        const band = Math.abs(u[1] + 0.24) < 0.19 * P.mask && u[0] < -0.50;
        if (de < 9.5 * HS * P.mask || band) nm = 'mask';
        out[i] = nm;
      }
      return { out, names: ['head', 'fur', 'muzzle', 'mask'] };
    };
    return m;
  }

  // ---------- 2D-tekening + maskers ----------
  function makeArt(m, P, S) {
    const Rc = camera(P.yaw, P.pitch);
    const [x0, x1, y0, y1] = bbox(m, Rc);
    const sc = S * 0.94 / Math.max(x1 - x0, y1 - y0);
    const origin = [x0 - (S / sc - (x1 - x0)) / 2, y1 + (S / sc - (y1 - y0)) / 2];
    const R = render3d(m, Rc, S, sc, origin);
    const Lv = unit([-0.6, 0.7, 0.35]);
    const fig = new Uint8Array(S * S), line = new Uint8Array(S * S), tone = new Float32Array(S * S);
    for (let i = 0; i < S * S; i++) if (R.mat[i] >= 0) { fig[i] = 1; tone[i] = (R.nx[i] * Lv[0] + R.ny[i] * Lv[1] + R.nz[i] * Lv[2] + 1) / 2; }
    const jump = 6 * (S / 512) / (sc / (512 * 0.94 / 230)) * 0 + 6;
    for (let y = 0; y < S - 1; y++) for (let x = 1; x < S - 1; x++) {
      const i = y * S + x; if (!fig[i]) continue;
      for (const j of [i + 1, i + S, i + S + 1, i + S - 1]) {
        if (!fig[j] || R.part[j] === R.part[i]) continue;
        if (Math.abs(R.z[i] - R.z[j]) > jump) line[R.z[i] > R.z[j] ? i : j] = 1;
      }
    }
    const w = Math.max(1, Math.round(S / 160));
    for (let k = 1; k < w; k++) { const c = line.slice(); for (let i = S + 1; i < S * S - S - 1; i++) if (c[i] || c[i - 1] || c[i - S]) line[i] = fig[i]; }
    return { R, fig, line, tone, Rc, sc, origin, S };
  }

  // ---------- pixel-over ----------
  function integral(a, S) { const I = new Float64Array((S + 1) * (S + 1)); for (let y = 0; y < S; y++) { let row = 0; for (let x = 0; x < S; x++) { row += a[y * S + x]; I[(y + 1) * (S + 1) + x + 1] = I[y * (S + 1) + x + 1] + row; } } return I; }
  function boxAt(I, S, cx, cy, k) { const h = k / 2; const x0 = Math.max(0, Math.round(cx - h)), x1 = Math.min(S, Math.round(cx + h)), y0 = Math.max(0, Math.round(cy - h)), y1 = Math.min(S, Math.round(cy + h)); const n = Math.max(1, (x1 - x0) * (y1 - y0)); return (I[y1 * (S + 1) + x1] - I[y0 * (S + 1) + x1] - I[y1 * (S + 1) + x0] + I[y0 * (S + 1) + x0]) / n; }

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
  function lCorners(m, w, h) {
    m = m.slice();
    for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
      if (!m[y * w + x]) continue;
      const u = m[(y - 1) * w + x], d = m[(y + 1) * w + x], l = m[y * w + x - 1], r = m[y * w + x + 1];
      if ((u || d) && (l || r) && u + d + l + r === 2) { const dy = u ? -1 : 1, dx = l ? -1 : 1; if (!m[(y - dy) * w + x - dx]) m[y * w + x] = 0; }
    }
    return m;
  }
  function maskCorners(f, w, h) {
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

  function pixelover(A, st) {
    const S = A.S;
    // figuur-kader in de tekening
    let x0 = S, x1 = 0, y0 = S, y1 = 0;
    for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) if (A.fig[y * S + x]) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
    const fw = x1 - x0 + 1, fh = y1 - y0 + 1;
    const f = Math.max(fw / st.maxW, fh / st.maxH);
    const w = Math.max(1, Math.round(fw / f)), h = Math.max(1, Math.round(fh / f));
    const cx = i => x0 + (i + 0.5) * f, cy = j => y0 + (j + 0.5) * f;
    const Ifig = integral(A.fig, S);
    const notLine = new Uint8Array(S * S), toneNL = new Float32Array(S * S);
    for (let i = 0; i < S * S; i++) { notLine[i] = A.fig[i] && !A.line[i] ? 1 : 0; toneNL[i] = notLine[i] ? A.tone[i] : 0; }
    const Inl = integral(notLine, S), Itone = integral(toneNL, S);
    // cel-schaduw zoals een Sugimori-tekening: licht eerst afvlakken (ronde vlakken), dan per materiaal in 3 vlakken
    const Itn = integral(toneNL, S), cel = new Int8Array(S * S).fill(-1);
    const sm = new Float32Array(S * S), kb = Math.max(3, f * st.soft);
    for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) { const i = y * S + x; if (!notLine[i]) continue; const c = boxAt(Inl, S, x, y, kb); sm[i] = c > 0 ? boxAt(Itn, S, x, y, kb) / c : A.tone[i]; }
    for (let q = 0; q < A.R.mats.length; q++) {
      const v = []; for (let i = 0; i < S * S; i += 3) if (notLine[i] && A.R.mat[i] === q) v.push(sm[i]);
      if (v.length < 10) continue; v.sort((a, b) => a - b);
      const qh = v[Math.floor(v.length * (1 - st.hiShare))], qs = v[Math.floor(v.length * st.shShare)];
      for (let i = 0; i < S * S; i++) if (notLine[i] && A.R.mat[i] === q) cel[i] = sm[i] >= qh ? 0 : sm[i] > qs ? 1 : 2;
    }
    const Icel = [0, 1, 2].map(t => { const a = new Uint8Array(S * S); for (let i = 0; i < S * S; i++) a[i] = cel[i] === t ? 1 : 0; return integral(a, S); });
    const lineFig = new Uint8Array(S * S); for (let i = 0; i < S * S; i++) lineFig[i] = A.line[i] && A.fig[i] ? 1 : 0;
    const Iline = integral(lineFig, S);
    const nm = A.R.mats.length;
    const Imat = []; for (let k = 0; k < nm; k++) { const a = new Uint8Array(S * S); for (let i = 0; i < S * S; i++) a[i] = A.R.mat[i] === k && notLine[i] ? 1 : 0; Imat.push(integral(a, S)); }
    let fig = new Uint8Array(w * h), lin = new Uint8Array(w * h);
    const mat = new Int16Array(w * h).fill(-1), tone = new Float32Array(w * h);
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const k = j * w + i, X = cx(i), Y = cy(j);
      if (boxAt(Ifig, S, X, Y, f) > 0.5 + st.rough * (Math.sin(i * 1.7 + j * 2.3) * 0.5)) fig[k] = 1;
      if (boxAt(Iline, S, X, Y, f * st.lineReach) > st.lineCov / f) lin[k] = 1;
      let best = -1, bv = 0; for (let q = 0; q < nm; q++) { const v = boxAt(Imat[q], S, X, Y, f); if (v > bv) { bv = v; best = q; } }
      mat[k] = best;
      let bt = 1, btv = -1; for (let t = 0; t < 3; t++) { const v = boxAt(Icel[t], S, X, Y, f) * (t === 1 ? 1.0 : 1.05); if (v > btv) { btv = v; bt = t; } }
      tone[k] = bt;
    }
    fig = maskCorners(fig, w, h);
    for (let k = 0; k < w * h; k++) lin[k] = lin[k] && fig[k];
    lin = lCorners(prune(thin(lin, w, h), w, h, st.prune), w, h);
    // tonen komen uit de cel-vlakken van de tekening
    const tn = new Int8Array(w * h).fill(2);
    for (let k = 0; k < w * h; k++) if (fig[k]) tn[k] = tone[k];
    for (let it = 0; it < st.round; it++) {
      const c = tn.slice();
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
        const k = j * w + i; if (!fig[k]) continue; const cnt = [0, 0, 0]; let n = 0;
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) { if (!dx && !dy) continue; const ii = i + dx, jj = j + dy; if (ii < 0 || jj < 0 || ii >= w || jj >= h) continue; const kk = jj * w + ii; if (fig[kk] && mat[kk] === mat[k]) { cnt[c[kk]]++; n++; } }
        const mx = Math.max(...cnt); if (mx >= 6 && cnt.indexOf(mx) !== c[k]) tn[k] = cnt.indexOf(mx);
      }
    }
    // omlijning
    const key = new Array(w * h).fill('');
    const L2 = [-0.6, -0.8];
    const F = (i, j) => (i < 0 || j < 0 || i >= w || j >= h) ? 0 : fig[j * w + i];
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const k = j * w + i; if (!fig[k]) continue;
      const mn = mat[k] >= 0 ? A.R.mats[mat[k]] : 'fur';
      key[k] = mn + 'hbs'[tn[k]];
      let ex = 0, ey = 0, edge = false;
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) if (!F(i + dx, j + dy)) { edge = true; ex += dx; ey += dy; }
      if (!edge && !lin[k]) continue;
      if (!edge) { for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) { const ii = i + dx, jj = j + dy; if (F(ii, jj) && !lin[jj * w + ii]) { const t = tn[jj * w + ii]; ex += dx * (2 - t); ey += dy * (2 - t); } } ex = -ex; ey = -ey; }
      const l = Math.hypot(ex, ey) || 1, d = (ex / l) * L2[0] + (ey / l) * L2[1];
      key[k] = edge ? (d > st.lineHi ? mn + 's' : d > st.lineMid ? mn + 'l' : 'K') : (d > st.lineHi ? mn + 's' : mn + 'l');
    }
    return { key, w, h, f, x0, y0 };
  }

  const DEFAULT_PARAMS = { yaw: 52, pitch: 8, headTurn: 0, headScale: 1.35, headTall: 1, headLift: 30, snout: 1, muzzle: 1, mask: 1, ear: 1,
    bodyLen: 1, bodyThick: 1, backArch: 0, legK: 1, frontLen: 1, claw: 1, clawThick: 1, tailLen: 1, tailThick: 1, tailCurl: 1 };
  const DEFAULT_STYLE = { maxW: 56, maxH: 56, soft: 1.5, hiShare: 0.30, shShare: 0.38, round: 2, lineCov: 0.35, lineReach: 0.9, prune: 2, lineHi: 0.75, lineMid: -0.1, rough: 0, eye: 1 };
  const DEFAULT_COLORS = { fur: [139, 90, 65], head: [150, 128, 110], muzzle: [84, 72, 64], nose: [142, 79, 88], paw: [208, 154, 142], claw: [242, 234, 214], ear: [57, 24, 16], earin: [148, 123, 106], mask: [16, 16, 16], eye: [168, 64, 26] };

  // kleurhelling uit één basiskleur (hooglicht lichter en iets warmer, schaduw donkerder en iets koeler)
  function ramp(c, flat) {
    const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
    if (flat) return { h: c, b: c, s: c, l: [16, 16, 16] };
    return { h: mix(c, [255, 236, 200], 0.22), b: c, s: mix(c, [30, 20, 40], 0.32), l: mix(c, [20, 8, 12], 0.62) };
  }
  function palette(colors) {
    // gedeelde tinten houden het palet binnen 15 kleuren (Gen 3): kop-omlijning = vacht-omlijning,
    // binnenoor = kop, voetschaduw = neus, klauwschaduw = kop-hooglicht, oorrand = vacht-omlijning
    const fur = ramp(colors.fur), head = ramp(colors.head), paw = ramp(colors.paw), claw = ramp(colors.claw);
    const pal = { K: [16, 16, 16], w: [255, 255, 255] };
    const set = (m, h, b, s, l) => { pal[m + 'h'] = h; pal[m + 'b'] = b; pal[m + 's'] = s; pal[m + 'l'] = l; };
    set('fur', fur.h, fur.b, fur.s, fur.l);
    set('head', head.h, head.b, head.s, fur.l);
    set('earin', head.h, head.b, head.s, fur.l);
    set('muzzle', colors.muzzle, colors.muzzle, colors.muzzle, [16, 16, 16]);
    set('nose', colors.nose, colors.nose, colors.nose, [16, 16, 16]);
    set('paw', paw.b, paw.b, colors.nose, colors.nose);
    set('claw', claw.b, claw.b, head.h, fur.s);
    set('ear', fur.l, fur.l, fur.l, [16, 16, 16]);
    set('mask', [16, 16, 16], [16, 16, 16], [16, 16, 16], [16, 16, 16]);
    pal.eyed = colors.eye; pal.eyel = colors.nose;
    return pal;
  }

  function generate(params, style, colors, paint) {
    const P = Object.assign({}, DEFAULT_PARAMS, params), st = Object.assign({}, DEFAULT_STYLE, style), C = Object.assign({}, DEFAULT_COLORS, colors);
    const m = olinguito(P), A = makeArt(m, P, 384), po = pixelover(A, st);
    const N = 64, key = new Array(N * N).fill('');
    const ox = Math.floor((N - po.w) / 2), oy = N - po.h - 2;
    for (let j = 0; j < po.h; j++) for (let i = 0; i < po.w; i++) { const y = oy + j, x = ox + i; if (y >= 0 && y < N && x >= 0 && x < N) key[y * N + x] = po.key[j * po.w + i]; }
    // oog-sjabloon op het geprojecteerde punt
    if (st.eye) {
      const p = mv(A.Rc, m.points.oog);
      const ax = (p[0] - A.origin[0]) * A.sc, ay = (A.origin[1] - p[1]) * A.sc;
      const ex = ox + Math.round((ax - po.x0) / po.f - 1), ey = oy + Math.round((ay - po.y0) / po.f - 1);
      const rows = st.eye > 1 ? ['KK.', 'wdK', 'ddK', 'llK'] : ['KK.', 'wdK', 'llK'];
      rows.forEach((r, j) => [...r].forEach((c, i) => { const x = ex + i, y = ey + j; if (c !== '.' && x >= 0 && y >= 0 && x < N && y < N && key[y * N + x]) key[y * N + x] = { K: 'K', w: 'w', d: 'eyed', l: 'eyel' }[c]; }));
    }
    for (const [x, y, k] of paint || []) if (x >= 0 && y >= 0 && x < N && y < N) key[y * N + x] = k;
    return { key, pal: palette(C), art: A, po };
  }

  function check(key, pal) {
    const N = 64; let px = 0, edge = 0, black = 0, open = 0; const cols = new Set();
    const isLine = k => k === 'K' || (k && k.endsWith('l')) || k === 'eyed';
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const k = key[y * N + x]; if (!k) continue; px++; cols.add(String(pal[k]));
      const out = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => { const xx = x + dx, yy = y + dy; return xx < 0 || yy < 0 || xx >= N || yy >= N || !key[yy * N + xx]; });
      if (out) { edge++; if (k === 'K') black++; else if (!isLine(k) && !k.endsWith('s')) open++; }
    }
    // ingesloten gaatjes van 1-2 px
    const seen = new Uint8Array(N * N), st = [0]; seen[0] = 1;
    while (st.length) { const i = st.pop(), x = i % N, y = (i / N) | 0; for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const xx = x + dx, yy = y + dy; if (xx < 0 || yy < 0 || xx >= N || yy >= N) continue; const j = yy * N + xx; if (!seen[j] && !key[j]) { seen[j] = 1; st.push(j); } } }
    let holes = 0; for (let i = 0; i < N * N; i++) if (!key[i] && !seen[i]) holes++;
    return { pixels: px, colors: cols.size, blackShare: edge ? black / edge : 0, open, holes };
  }

  const api = { generate, check, palette, ramp, DEFAULT_PARAMS, DEFAULT_STYLE, DEFAULT_COLORS };
  if (typeof module !== 'undefined') module.exports = api; else root.SpriteGen = api;
})(typeof self !== 'undefined' ? self : this);
