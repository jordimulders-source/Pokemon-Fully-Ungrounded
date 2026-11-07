/* Sprite-renderer (Gen 3, 64x64) volgens de Dragonfly Cave-regels (docs/lessen/SPRITING.md).
   Invoer: een spec met vormen (gesloten curven op spritegrootte), materialen (kleurhellingen) en stijlknoppen.
   Werkt in de browser (editor) en in Node (repo, kalibratie). Geen afhankelijkheden.

   Stappen per vorm: curve -> masker (8x) -> kussen-normalen (afstand tot de rand = bolling) -> licht per vlak
   -> tonen (hooglicht/basis/schaduw) -> omlijning per kleurgroep (zwart aan de schaduwkant, kleurlijn aan de
   lichte kant, schaduwtint als lijn-hooglicht) -> binnenlijnen waar een vorm vóór een andere ligt
   -> 'pixel-perfect' hoeken -> detailsjablonen -> handlaag (pixels met knopjes). */
(function (root) {
  const N = 64, SS = 8, H = N * SS;

  // ---------- curven ----------
  function catmull(pts, perSeg) {
    const out = [], n = pts.length;
    for (let i = 0; i < n; i++) {
      const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      for (let j = 0; j < perSeg; j++) {
        const t = j / perSeg, t2 = t * t, t3 = t2 * t;
        out.push([0, 1].map(d => 0.5 * ((2 * p1[d]) + (-p0[d] + p2[d]) * t + (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * t2 + (-p0[d] + 3 * p1[d] - 3 * p2[d] + p3[d]) * t3)));
      }
    }
    return out;
  }

  function fillPoly(poly, W, scale) {     // scanline-vulling, pixelmiddens
    const m = new Uint8Array(W * W);
    const P = poly.map(p => [p[0] * scale, p[1] * scale]);
    for (let y = 0; y < W; y++) {
      const yc = y + 0.5, xs = [];
      for (let i = 0; i < P.length; i++) {
        const a = P[i], b = P[(i + 1) % P.length];
        if ((a[1] <= yc && b[1] > yc) || (b[1] <= yc && a[1] > yc)) xs.push(a[0] + (yc - a[1]) / (b[1] - a[1]) * (b[0] - a[0]));
      }
      xs.sort((u, v) => u - v);
      for (let k = 0; k + 1 < xs.length; k += 2) {
        const x0 = Math.max(0, Math.ceil(xs[k] - 0.5)), x1 = Math.min(W - 1, Math.floor(xs[k + 1] - 0.5));
        for (let x = x0; x <= x1; x++) m[y * W + x] = 1;
      }
    }
    return m;
  }

  // afstand tot de rand (chamfer 3-4), in hoge-resolutiepixels
  function distance(m, W) {
    const d = new Float32Array(W * W), INF = 1e9;
    for (let i = 0; i < W * W; i++) d[i] = m[i] ? INF : 0;
    const at = (x, y) => (x < 0 || y < 0 || x >= W || y >= W) ? 0 : d[y * W + x];
    for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) {
      const i = y * W + x; if (!d[i]) continue;
      d[i] = Math.min(d[i], at(x - 1, y) + 3, at(x, y - 1) + 3, at(x - 1, y - 1) + 4, at(x + 1, y - 1) + 4);
    }
    for (let y = W - 1; y >= 0; y--) for (let x = W - 1; x >= 0; x--) {
      const i = y * W + x; if (!d[i]) continue;
      d[i] = Math.min(d[i], at(x + 1, y) + 3, at(x, y + 1) + 3, at(x + 1, y + 1) + 4, at(x - 1, y + 1) + 4);
    }
    for (let i = 0; i < W * W; i++) d[i] /= 3;
    return d;
  }

  // waarde-ruis (deterministisch) voor gekartelde schaduwgrenzen / grillige omtrek
  function noise(seed, scale) {
    const g = (ix, iy) => { let h = (ix * 374761393 + iy * 668265263 + seed * 2147483647) | 0; h = (h ^ (h >>> 13)) * 1274126177 | 0; return ((h ^ (h >>> 16)) & 0xffff) / 32768 - 1; };
    return (x, y) => {
      x /= scale; y /= scale; const x0 = Math.floor(x), y0 = Math.floor(y), fx = x - x0, fy = y - y0;
      const s = t => t * t * (3 - 2 * t), a = g(x0, y0), b = g(x0 + 1, y0), c = g(x0, y0 + 1), e = g(x0 + 1, y0 + 1);
      return (a * (1 - s(fx)) + b * s(fx)) * (1 - s(fy)) + (c * (1 - s(fx)) + e * s(fx)) * s(fy);
    };
  }

  function render(spec) {
    const st = Object.assign({ hi: 0.55, sh: 0.15, lineHi: 0.75, lineMid: -0.05, jag: 0, rough: 0, pillow: 0.55, cast: 1, seed: 1 }, spec.style || {});
    const L = norm3(spec.light || [-0.55, -0.75, 0.6]);       // schermcoördinaten: x rechts, y omlaag, z naar de kijker
    const L2 = norm2([L[0], L[1]]);
    const parts = spec.parts.map((p, i) => Object.assign({ z: i, line: true, group: p.name }, p)).sort((a, b) => a.z - b.z);
    const nz = noise(st.seed, SS * 2.2), nj = noise(st.seed + 9, SS * 1.3);
    // 1. maskers per vorm (hoge resolutie) + zichtbaarheid
    const owner = new Int16Array(H * H).fill(-1);
    const full = [];
    parts.forEach((p, k) => {
      let poly = p.poly ? p.pts : catmull(p.pts, 16);
      if (st.rough) poly = poly.map(q => { const r = st.rough * 1.2 * nz(q[0] * SS, q[1] * SS); return [q[0] + r, q[1] + r * 0.7]; });
      const m = fillPoly(poly, H, SS);
      full.push(m);
      for (let i = 0; i < H * H; i++) if (m[i]) owner[i] = k;
    });
    // 2. per spritepixel: eigenaar op het pixelmidden
    const own = new Int16Array(N * N).fill(-1);
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) own[y * N + x] = owner[(y * SS + SS / 2) * H + x * SS + SS / 2];
    pixelPerfect(own);
    // 3. kussen-normalen en licht per vorm
    const lit = new Float32Array(N * N).fill(0), nrm = new Float32Array(N * N * 2);
    parts.forEach((p, k) => {
      const d = distance(full[k], H);
      let maxd = 0; for (let i = 0; i < H * H; i++) if (d[i] > maxd) maxd = d[i];
      const R = Math.max(2, maxd * (p.pillow || st.pillow));
      const h = new Float32Array(H * H);
      for (let i = 0; i < H * H; i++) { const t = Math.min(d[i] / R, 1); h[i] = Math.sqrt(Math.max(0, 1 - (1 - t) * (1 - t))); }
      for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
        if (own[y * N + x] !== k) continue;
        const cx = x * SS + SS / 2, cy = y * SS + SS / 2;
        const gx = (h[cy * H + Math.min(H - 1, cx + 2)] - h[cy * H + Math.max(0, cx - 2)]) / 4 * R;
        const gy = (h[Math.min(H - 1, cy + 2) * H + cx] - h[Math.max(0, cy - 2) * H + cx]) / 4 * R;
        const n = norm3([-gx, -gy, 1.0]);
        let v = n[0] * L[0] + n[1] * L[1] + n[2] * L[2];
        if (st.jag) v += st.jag * nj(cx, cy);
        v += (p.tone || 0);
        lit[y * N + x] = v;
        // naar buiten gerichte randnormaal (voor de lijnkleur)
        const ex = -(full[k][cy * H + Math.min(H - 1, cx + SS)] - full[k][cy * H + Math.max(0, cx - SS)]);
        const ey = -(full[k][Math.min(H - 1, cy + SS) * H + cx] - full[k][Math.max(0, cy - SS) * H + cx]);
        nrm[(y * N + x) * 2] = ex || -n[0]; nrm[(y * N + x) * 2 + 1] = ey || -n[1];
      }
    });
    // 4. tonen + slagschaduw (achterste vorm direct onder/rechts van een voorste vorm)
    const key = new Array(N * N).fill('');
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const k = own[y * N + x]; if (k < 0) continue;
      const p = parts[k]; let v = lit[y * N + x];
      let t = p.flat ? 'b' : (v > st.hi ? 'h' : v > st.sh ? 'b' : 's');
      if (st.cast && !p.flat) {
        const ux = x - Math.round(L2[0]), uy = y - Math.round(L2[1]);
        const kk = (ux >= 0 && uy >= 0 && ux < N && uy < N) ? own[uy * N + ux] : -1;
        if (kk >= 0 && kk !== k && parts[kk].z > p.z && parts[kk].group !== p.group) t = 's';
      }
      key[y * N + x] = p.mat + t;
    }
    // 5. omlijning
    const isLine = new Uint8Array(N * N);
    const nb4 = [[1, 0], [-1, 0], [0, 1], [0, -1]];
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const k = own[y * N + x]; if (k < 0) continue;
      const p = parts[k];
      let edge = false, ix = 0, iy = 0;
      for (const [dx, dy] of nb4) {
        const xx = x + dx, yy = y + dy;
        const kk = (xx >= 0 && yy >= 0 && xx < N && yy < N) ? own[yy * N + xx] : -1;
        if (kk < 0) { edge = true; ix += dx; iy += dy; }
        else if (kk !== k && p.line && parts[kk].z < p.z && parts[kk].group !== p.group) { edge = true; ix += dx; iy += dy; }
      }
      if (!edge) continue;
      isLine[y * N + x] = 1;
      const n = norm2([ix || nrm[(y * N + x) * 2], iy || nrm[(y * N + x) * 2 + 1]]);
      const f = n[0] * L2[0] + n[1] * L2[1];       // >0: naar het licht
      key[y * N + x] = f > st.lineHi ? p.mat + 's' : f > st.lineMid ? p.mat + 'l' : 'K';
    }
    // 6. details en handlaag
    for (const d of spec.details || []) d.rows.forEach((row, j) => [...row].forEach((ch, i) => {
      const x = d.at[0] + i, y = d.at[1] + j; if (ch !== '.' && x >= 0 && y >= 0 && x < N && y < N) key[y * N + x] = d.colors[ch];
    }));
    for (const [x, y, k] of spec.paint || []) key[y * N + x] = k;
    return { key, own, parts };
  }

  // uitwendige trap-hoeken (L-vormen) van het silhouet weghalen: 1 px per trede
  function pixelPerfect(own) {
    const at = (x, y) => (x < 0 || y < 0 || x >= N || y >= N) ? -1 : own[y * N + x];
    const kill = [];
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      if (own[y * N + x] < 0) continue;
      const u = at(x, y - 1) >= 0, d = at(x, y + 1) >= 0, l = at(x - 1, y) >= 0, r = at(x + 1, y) >= 0;
      if (u + d + l + r !== 2 || (u && d) || (l && r)) continue;
      const dy = u ? -1 : 1, dx = l ? -1 : 1;
      if (at(x + dx, y + dy) >= 0 && at(x - dx, y - dy) < 0) kill.push(y * N + x);
    }
    for (const i of kill) own[i] = -1;
  }

  function palette(spec) {
    const pal = { K: spec.black || [16, 16, 16] };
    for (const [m, c] of Object.entries(spec.materials)) for (const t of ['h', 'b', 's', 'l']) pal[m + t] = c[t] || c.b;
    Object.assign(pal, spec.extra || {});
    return pal;
  }

  function check(key, pal) {
    const cols = new Set(); let px = 0;
    key.forEach(k => { if (k) { px++; cols.add(String(pal[k])); } });
    return { pixels: px, kleuren: cols.size };
  }

  function norm3(v) { const l = Math.hypot(...v) || 1; return v.map(a => a / l); }
  function norm2(v) { const l = Math.hypot(...v) || 1; return v.map(a => a / l); }

  const api = { render, palette, check, catmull, N };
  if (typeof module !== 'undefined') module.exports = api; else root.SpriteRender = api;
})(this);
