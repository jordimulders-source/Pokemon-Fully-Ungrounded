#!/usr/bin/env python3
"""Project Grounded: gedeelde 'film'-encoder voor cinematische gevechtsintro's (Steven, Wally, Rayquaza).

Een film is een reeks RGB-beelden van 240x160 (één per gameframe; gelijke opeenvolgende beelden kosten niets extra).
De encoder zet elk beeld om naar BG0-tiles met drie paletten (BG 13, 14 en 15; per tile het beste palet) en ontdubbelt
de tiles (ook gespiegeld, over de hele film). VRAM is een cache van SLOTS tiles: bij elk nieuw beeld worden alleen de
tiles geladen die er nog niet staan, in plekken die het getoonde beeld niet gebruikt (de langst ongebruikte eerst). De
C-speler zet elke nieuwe tilemap in het schermblok dat niet getoond wordt (31 of 27) en wisselt BG0CNT in de VBlank.
Zo is het getoonde beeld nooit half beschreven (geen scheuren), en een stilstaande achtergrond wordt maar één keer
geladen. Past een beeld niet in MAX_TILES tiles, dan worden de meest gelijkende tiles samengevoegd (verliesgevend).

Uitvoer (graphics/battle_transitions/):
- film_<naam>_pal.bin: de paletsets als GBA-kleuren (per set 3 x 16: BG 13, 14, 15)
- film_<naam>_tiles.bin: per laadactie een LZ77-blok met de nieuwe tiles (4bpp), 4-byte uitgelijnd
- film_<naam>_loads.bin: per laadactie u32 offset in _tiles.bin, u16 aantal runs, u16 eerste run in _runs.bin
- film_<naam>_runs.bin: runs van u16 doeltile, u16 aantal (de tiles staan in die volgorde in het blok)
- film_<naam>_maps.bin + _mapofs.bin: LZ77-tilemaps van 32x20 (u16, tile | flip | palet; kolom 30/31 = kopie van
  29/0 voor HOFS-trillen) en per tilemap de u32 offset
- film_<naam>_seq.bin: per gameframe 8 bytes: u16 tilemap (0xFFFF = leeg), u16 laadactie (0xFFFF = geen),
  u8 paletset, 3 x 0
"""
import os, struct
import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'graphics/battle_transitions/')
W, H = 240, 160
SLOTS = 702           # tiles 1..702 van charblock 2 (tile 0 = leeg, 704-767 = schermblok 27)
MAX_TILES = 351       # per beeld, zodat het vorige en het nieuwe beeld samen altijd in VRAM passen
BANK = MAX_TILES
BLANK = 0xFFFF


def gba(c):
    """8-bit RGB naar de GBA-kleur (5 bit per kanaal, terug naar 8 bit)."""
    return tuple((int(v) >> 3) << 3 for v in c)


def pad15(cols):
    """Een palet van max. 15 kleuren -> 16 (index 0 = doorzichtig, zwart)."""
    cols = [gba(c) for c in cols]
    assert len(cols) <= 15, len(cols)
    return [(0, 0, 0)] + cols + [cols[-1]] * (15 - len(cols))


class Film:
    def __init__(self, name):
        self.name = name
        self._budget = {}
        self.ref = None            # paletset waartegen de beelden gekwantiseerd worden (de 'echte' kleuren)
        self.palsets = []          # [ [pal13, pal14, pal15] ], elk 16 kleuren
        self.frames = []           # (beeld of None, paletset)
        self._palkey = {}

    def palset(self, p13, p14, p15):
        """Registreert een paletset (drie lijsten van max. 15 kleuren) en geeft het nummer."""
        ps = [pad15(p13), pad15(p14), pad15(p15)]
        key = tuple(tuple(c) for p in ps for c in p)
        if key not in self._palkey:
            self._palkey[key] = len(self.palsets)
            self.palsets.append(ps)
        return self._palkey[key]

    def add(self, img, palset, n=1, q=None, budget=None):
        """Voegt n gameframes met dit beeld toe (img: numpy HxWx3 uint8, of None = leeg/doorzichtig). q = paletset
        waartegen het beeld gekwantiseerd wordt (standaard self.ref, en anders palset zelf)."""
        if q is None:
            q = self.ref if self.ref is not None else palset
        for _ in range(n):
            self.frames.append((img, palset, q))
        if budget is not None and img is not None:
            self._budget[id(img)] = budget     # max. tiles voor dit beeld (minder = sneller laden, iets grover)

    # ------------------------------------------------------------------ omzetten
    def _quantize(self, img, ps):
        """Beeld -> (indexen per tile [600,64], palet per tile [600], rgb-fout)."""
        t = img.reshape(20, 8, 30, 8, 3).transpose(0, 2, 1, 3, 4).reshape(600, 64, 3).astype(np.int32)
        best_err = np.full(600, 1 << 60, np.int64)
        best_idx = np.zeros((600, 64), np.uint8)
        best_pal = np.zeros(600, np.uint8)
        for k in range(3):
            pal = np.array(ps[k][1:], np.int32)                       # 15 kleuren (index 1..15)
            d = ((t[:, :, None, :] - pal[None, None, :, :]) ** 2 * np.array([3, 6, 2])).sum(3)
            idx = d.argmin(2)
            err = d.min(2).sum(1)
            better = err < best_err
            best_err[better] = err[better]
            best_idx[better] = (idx[better] + 1).astype(np.uint8)
            best_pal[better] = k
        return best_idx, best_pal

    def encode(self, preview_dir=None):
        frame_maps = []            # per uniek beeld: (cellen [600] als (tilekey, flip), paletten [600])
        frame_of = []              # per gameframe: index in frame_maps of -1
        seen = {}
        keep = []
        for img, ps, q in self.frames:
            if img is None:
                frame_of.append(-1)
                continue
            key = (id(img), q)
            if key in seen:
                frame_of.append(seen[key])
                continue
            ref = self.palsets[q]
            idx, pal = self._quantize(img, ref)
            frame_maps.append(self._reduce(idx, pal, ref, self._budget.get(id(img), MAX_TILES)))
            seen[key] = len(frame_maps) - 1
            keep.append(img)
            frame_of.append(seen[key])

        # VRAM als cache: per beeldwissel de ontbrekende tiles laden in plekken die het getoonde beeld niet gebruikt
        slot_of = {}               # tilekey -> slot
        key_of = {}                # slot -> tilekey
        last_use = {}              # slot -> gameframe waarop hij voor het laatst nodig was
        shown = set()              # slots van het getoonde beeld
        map_cache = {}             # (beeld, slots) -> tilemapnummer
        maps, loads, seq = [], [], []
        new_tiles_total = 0
        prev_fm = None
        for gi, ((img, ps, q), fm) in enumerate(zip(self.frames, frame_of)):
            if fm < 0:
                seq.append((BLANK, BLANK, ps))
                shown = set()
                prev_fm = None
                continue
            if fm == prev_fm:
                seq.append((seq[-1][0], BLANK, ps))
                continue
            cells, pals = frame_maps[fm]
            need = set(k for k, f in cells)
            missing = [k for k in sorted(need) if k not in slot_of]
            for k in need:
                if k in slot_of:
                    last_use[slot_of[k]] = gi
            # vrije plekken: nooit gebruikt, of gebruikt door tiles die nu en in het getoonde beeld niet nodig zijn
            cand = [sl for sl in range(1, SLOTS + 1) if sl not in shown and key_of.get(sl) not in need]
            cand.sort(key=lambda sl: (sl in key_of, last_use.get(sl, -1)))
            assert len(cand) >= len(missing), (self.name, gi, len(cand), len(missing))
            new = []
            for k, sl in zip(missing, cand):
                old = key_of.get(sl)
                if old is not None:
                    del slot_of[old]
                key_of[sl] = k
                slot_of[k] = sl
                last_use[sl] = gi
                new.append((sl, k))
            new_tiles_total += len(new)
            load = BLANK
            if new:
                new.sort()
                runs = []
                for sl, k in new:
                    if runs and runs[-1][0] + runs[-1][1] == sl:
                        runs[-1][1] += 1
                    else:
                        runs.append([sl, 1])
                loads.append(([k for sl, k in new], runs))
                load = len(loads) - 1
            tm = [int(slot_of[k]) | (int(f) << 10) | ((13 + int(p)) << 12) for (k, f), p in zip(cells, pals)]
            key = (fm, tuple(tm))
            if key not in map_cache:
                rows = []
                for r in range(20):
                    row = tm[r * 30:(r + 1) * 30]
                    rows += row + [row[29], row[0]]
                maps.append(rows)
                map_cache[key] = len(maps) - 1
            seq.append((map_cache[key], load, ps))
            shown = set(slot_of[k] for k in need)
            prev_fm = fm

        loads, seq = self._spread(loads, seq)
        self._save(loads, maps, seq)
        size = self.rom_size
        mg = getattr(self, '_merged', [])
        print('%s: %d gameframes, %d tilemaps, %d laadacties, %d tiles geladen, %.0f KB ROM; %d beelden samengevoegd '
              '(max %d tiles)' % (self.name, len(seq), len(maps), len(loads), new_tiles_total, size / 1024.0, len(mg),
                                  max(mg) if mg else 0))
        if preview_dir:
            self._preview(loads, maps, seq, preview_dir)
        return size

    @staticmethod
    def _spread(loads, seq):
        """Verdeelt elke laadactie over de frames sinds de vorige beeldwissel (het getoonde beeld blijft dan hetzelfde,
        dus de gekozen plekken blijven veilig). Zo hoeft de GBA nooit honderden tiles in één frame uit te pakken."""
        out_loads, out_seq = [], [list(x) for x in seq]
        last_switch = 0
        for f, (m, l, p) in enumerate(seq):
            if f > 0 and m != seq[f - 1][0]:
                if l != BLANK:
                    keys, runs = loads[l]
                    items = []
                    i = 0
                    for sl, c in runs:
                        for j in range(c):
                            items.append((sl + j, keys[i]))
                            i += 1
                    frames = list(range(last_switch + 1, f + 1))
                    n = len(frames)
                    for ci, fr in enumerate(frames):
                        part = items[len(items) * ci // n:len(items) * (ci + 1) // n]
                        if not part:
                            out_seq[fr][1] = BLANK
                            continue
                        rr = []
                        for sl, k in part:
                            if rr and rr[-1][0] + rr[-1][1] == sl:
                                rr[-1][1] += 1
                            else:
                                rr.append([sl, 1])
                        out_loads.append(([k for sl, k in part], rr))
                        out_seq[fr][1] = len(out_loads) - 1
                last_switch = f
            elif f == 0 and l != BLANK:
                out_loads.append(loads[l])
                out_seq[f][1] = len(out_loads) - 1
        return out_loads, [tuple(x) for x in out_seq]

    def _reduce(self, idx, pal, ps, lim=MAX_TILES):
        """Ontdubbelt de tiles van één beeld (ook gespiegeld) en voegt de meest gelijkende samen tot er max. BANK zijn."""
        keys = [bytes(r) for r in idx]
        canon = {}
        cells = []
        for k in keys:
            a = np.frombuffer(k, np.uint8).reshape(8, 8)
            vs = [a.tobytes(), a[:, ::-1].tobytes(), a[::-1, :].tobytes(), a[::-1, ::-1].tobytes()]
            c = min(vs)
            canon[c] = True
            cells.append((c, vs.index(c)))
        uniq = list(canon.keys())
        self._merged = getattr(self, '_merged', [])
        if len(uniq) > lim:
            self._merged.append(len(uniq) - lim)
        if len(uniq) <= lim:
            return cells, list(pal)
        # samenvoegen: per unieke tile de rgb onder het palet van zijn eerste cel
        first_pal = {}
        count = {}
        for (k, f), p in zip(cells, pal):
            first_pal.setdefault(k, p)
            count[k] = count.get(k, 0) + 1
        n = len(uniq)
        rgb = np.zeros((n, 64, 3), np.float64)
        for i, k in enumerate(uniq):
            pp = np.array(ps[first_pal[k]], np.float64)
            rgb[i] = pp[np.frombuffer(k, np.uint8)]
        flat = rgb.reshape(n, -1) * np.repeat(np.sqrt([3, 6, 2]), 1)[None, :].repeat(64, 0).reshape(1, -1)
        sq = (flat ** 2).sum(1)
        D = sq[:, None] + sq[None, :] - 2 * flat @ flat.T
        cnt = np.array([count[k] for k in uniq], np.float64)
        cost = D * np.minimum(cnt[:, None], cnt[None, :])
        np.fill_diagonal(cost, np.inf)
        alive = np.ones(n, bool)
        target = list(range(n))
        for _ in range(n - lim):
            i, j = np.unravel_index(np.argmin(cost), cost.shape)
            # de minst gebruikte gaat op in de meest gebruikte
            if cnt[i] > cnt[j]:
                i, j = j, i
            target[i] = j
            alive[i] = False
            cnt[j] += cnt[i]
            cost[i, :] = np.inf
            cost[:, i] = np.inf
            cost[j, alive] = D[j, alive] * np.minimum(cnt[j], cnt[alive])
            cost[alive, j] = cost[j, alive]
            cost[j, j] = np.inf
        def root(i):
            while target[i] != i:
                i = target[i]
            return i
        pos = {k: i for i, k in enumerate(uniq)}
        out_cells, out_pal = [], []
        for (k, f), p in zip(cells, pal):
            r = root(pos[k])
            if r == pos[k]:
                out_cells.append((k, f))
                out_pal.append(p)
            else:
                out_cells.append((uniq[r], 0))
                out_pal.append(first_pal[uniq[r]])
        return out_cells, out_pal

    def _save(self, loads, maps, seq):
        """Schrijft de film. Tiles (per laadactie) en tilemaps zijn LZ77-gecomprimeerd met gbagfx; de C-speler pakt ze
        uit met FastLZ77UnCompWram in een buffer en kopieert ze naar VRAM."""
        import subprocess, tempfile
        n = self.name
        gfx = os.path.join(ROOT, 'tools/gbagfx/gbagfx')

        def lz(raw):
            with tempfile.TemporaryDirectory() as d:
                a, b = os.path.join(d, 'x.bin'), os.path.join(d, 'x.bin.lz')
                open(a, 'wb').write(raw)
                subprocess.run([gfx, a, b], check=True)
                out = open(b, 'rb').read()
            return out + bytes((-len(out)) % 4)

        tile_blob, load_rows, run_rows = b'', [], []
        for keys, runs in loads:
            raw = b''.join(self._tile4bpp(k) for k in keys)
            load_rows.append(struct.pack('<IHH', len(tile_blob), len(runs), len(run_rows)))
            run_rows += [struct.pack('<HH', sl, c) for sl, c in runs]
            tile_blob += lz(raw)
        map_blob, map_ofs = b'', []
        for m in maps:
            map_ofs.append(len(map_blob))
            map_blob += lz(struct.pack('<640H', *m))
        if len(run_rows) % 2:
            run_rows.append(struct.pack('<HH', 0, 0))
        open(OUT + 'film_%s_tiles.bin' % n, 'wb').write(tile_blob)
        open(OUT + 'film_%s_loads.bin' % n, 'wb').write(b''.join(load_rows))
        open(OUT + 'film_%s_runs.bin' % n, 'wb').write(b''.join(run_rows))
        open(OUT + 'film_%s_maps.bin' % n, 'wb').write(map_blob)
        open(OUT + 'film_%s_mapofs.bin' % n, 'wb').write(struct.pack('<%dI' % len(map_ofs), *map_ofs))
        with open(OUT + 'film_%s_seq.bin' % n, 'wb') as fp:
            for m, l, p in seq:
                fp.write(struct.pack('<HHBBH', m, l, p, 0, 0))
        # paletten direct als GBA-kleuren (gbagfx kent max. 256 kleuren per .pal)
        with open(OUT + 'film_%s_pal.bin' % n, 'wb') as fp:
            for ps in self.palsets:
                for p in ps:
                    for c in p:
                        fp.write(struct.pack('<H', (c[0] >> 3) | ((c[1] >> 3) << 5) | ((c[2] >> 3) << 10)))
        pth = OUT + 'film_%s_segs.bin' % n
        if os.path.exists(pth):
            os.remove(pth)
        self.rom_size = len(tile_blob) + len(map_blob) + len(load_rows) * 8 + len(run_rows) * 4 + \
            len(map_ofs) * 4 + len(seq) * 8 + len(self.palsets) * 96

    @staticmethod
    def _tile4bpp(t):
        a = np.frombuffer(t, np.uint8)
        return bytes((a[0::2] | (a[1::2] << 4)).astype(np.uint8))

    def _preview(self, loads, maps, seq, d):
        """Speelt de film na zoals de GBA hem toont (VRAM-cache + tilemaps + paletten): GIF en self.preview_frames."""
        os.makedirs(d, exist_ok=True)
        vram = {0: np.zeros((8, 8), np.uint8)}
        out = []
        cache = {}
        for gi, (m, l, p) in enumerate(seq):
            if l != BLANK:
                keys, runs = loads[l]
                i = 0
                for sl, c in runs:
                    for j in range(c):
                        vram[sl + j] = np.frombuffer(keys[i], np.uint8).reshape(8, 8)
                        i += 1
                cache = {}
            if m == BLANK:
                out.append(np.zeros((H, W, 3), np.uint8))
                continue
            key = (m, p)
            if key not in cache:
                img = np.zeros((H, W, 3), np.uint8)
                ps = [np.array(x, np.uint8) for x in self.palsets[p]]
                for r in range(20):
                    for c in range(30):
                        v = maps[m][r * 32 + c]
                        t = vram[v & 0x3FF]
                        if v & 0x400:
                            t = t[:, ::-1]
                        if v & 0x800:
                            t = t[::-1, :]
                        img[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = ps[(v >> 12) - 13][t]
                cache[key] = img
            out.append(cache[key])
        self.preview_frames = out
        ims = [Image.fromarray(f) for f in out[::2]]
        ims[0].save(os.path.join(d, '%s_preview.gif' % self.name), save_all=True, append_images=ims[1:],
                    duration=33, loop=0)
        return out


# ------------------------------------------------------------------ kleine 3x5-pixelletters (plaatjes, VHS-schermtekst)
_F35_ROWS = {
    'A': ('.#.', '#.#', '###', '#.#', '#.#'), 'B': ('##.', '#.#', '##.', '#.#', '##.'),
    'C': ('.##', '#..', '#..', '#..', '.##'), 'D': ('##.', '#.#', '#.#', '#.#', '##.'),
    'E': ('###', '#..', '##.', '#..', '###'), 'F': ('###', '#..', '##.', '#..', '#..'),
    'G': ('.##', '#..', '#.#', '#.#', '.##'), 'H': ('#.#', '#.#', '###', '#.#', '#.#'),
    'I': ('###', '.#.', '.#.', '.#.', '###'), 'J': ('..#', '..#', '..#', '#.#', '.#.'),
    'K': ('#.#', '#.#', '##.', '#.#', '#.#'), 'L': ('#..', '#..', '#..', '#..', '###'),
    'M': ('#...#', '##.##', '#.#.#', '#...#', '#...#'), 'N': ('##.', '#.#', '#.#', '#.#', '#.#'),
    'O': ('.#.', '#.#', '#.#', '#.#', '.#.'), 'P': ('##.', '#.#', '##.', '#..', '#..'),
    'Q': ('.#.', '#.#', '#.#', '##.', '.##'), 'R': ('##.', '#.#', '##.', '#.#', '#.#'),
    'S': ('.##', '#..', '.#.', '..#', '##.'), 'T': ('###', '.#.', '.#.', '.#.', '.#.'),
    'U': ('#.#', '#.#', '#.#', '#.#', '###'), 'V': ('#.#', '#.#', '#.#', '#.#', '.#.'),
    'W': ('#...#', '#...#', '#.#.#', '##.##', '#...#'), 'X': ('#.#', '#.#', '.#.', '#.#', '#.#'),
    'Y': ('#.#', '#.#', '.#.', '.#.', '.#.'), 'Z': ('###', '..#', '.#.', '#..', '###'),
    '0': ('###', '#.#', '#.#', '#.#', '###'), '1': ('.#.', '##.', '.#.', '.#.', '###'),
    '2': ('##.', '..#', '.#.', '#..', '###'), '3': ('##.', '..#', '.#.', '..#', '##.'),
    '4': ('#.#', '#.#', '###', '..#', '..#'), '5': ('###', '#..', '##.', '..#', '##.'),
    '6': ('.##', '#..', '###', '#.#', '###'), '7': ('###', '..#', '.#.', '.#.', '.#.'),
    '8': ('###', '#.#', '###', '#.#', '###'), '9': ('###', '#.#', '###', '..#', '##.'),
    ':': ('...', '.#.', '...', '.#.', '...'), '.': ('...', '...', '...', '...', '.#.'),
    '(': ('.#.', '#..', '#..', '#..', '.#.'), ')': ('.#.', '..#', '..#', '..#', '.#.'),
    '?': ('##.', '..#', '.#.', '...', '.#.'), '!': ('.#.', '.#.', '.#.', '...', '.#.'),
    '-': ('...', '...', '###', '...', '...'), ' ': ('...', '...', '...', '...', '...'),
    '/': ('..#', '..#', '.#.', '#..', '#..'), "'": ('.#.', '.#.', '...', '...', '...'),
    '=': ('...', '###', '...', '###', '...'), '+': ('...', '.#.', '###', '.#.', '...'),
    '<': ('..#', '.#.', '#..', '.#.', '..#'), '>': ('#..', '.#.', '..#', '.#.', '#..'),
    '%': ('#.#', '..#', '.#.', '#..', '#.#'), ',': ('...', '...', '...', '.#.', '#..'),
}


def text35(draw_px, x, y, text, scale=1):
    """Tekent tekst in 3x5-letters; draw_px(x, y) wordt per 'aan'-pixel aangeroepen. Geeft de eindpositie x."""
    for ch in text:
        rows = _F35_ROWS.get(ch.upper(), _F35_ROWS[' '])
        for j, row in enumerate(rows):
            for i, v in enumerate(row):
                if v == '#':
                    for sy in range(scale):
                        for sx in range(scale):
                            draw_px(x + i * scale + sx, y + j * scale + sy)
        x += (len(rows[0]) + 1) * scale
    return x


def text35_width(text, scale=1):
    return sum(len(_F35_ROWS.get(c.upper(), _F35_ROWS[' '])[0]) + 1 for c in text) * scale - scale


def auto_palettes(imgs, fixed, n_free=12, iters=8, seed=1):
    """Kiest drie paletten (elk: de vaste kleuren + n_free eigen kleuren) voor een reeks beelden, zo dat elke tile met
    één palet goed te tekenen is: tiles worden over de drie paletten verdeeld (k-means op tiles), per palet een k-means op
    de kleuren van zijn tiles, en dat een paar keer herhaald. Geeft drie lijsten van kleuren."""
    rng = np.random.RandomState(seed)
    wts = np.array([3.0, 6.0, 2.0])
    tl = {}
    for img in imgs:
        t = img.reshape(20, 8, 30, 8, 3).transpose(0, 2, 1, 3, 4).reshape(600, 64, 3)
        for row in t:
            k = row.tobytes()
            tl[k] = tl.get(k, 0) + 1
    T = np.array([np.frombuffer(k, np.uint8).reshape(64, 3) for k in tl], np.float64)
    cnt = np.array(list(tl.values()), np.float64)
    fx = np.array([gba(c) for c in fixed], np.float64).reshape(-1, 3)
    # begin: verdeel de tiles naar hun gemiddelde kleur
    mean = T.mean(1)
    cent = mean[rng.choice(len(mean), 3, replace=len(mean) < 3)]
    for _ in range(10):
        d = (((mean[:, None, :] - cent[None]) ** 2) * wts).sum(2)
        grp = d.argmin(1)
        for g in range(3):
            if (grp == g).any():
                cent[g] = np.average(mean[grp == g], axis=0, weights=cnt[grp == g])
    pals = [None] * 3
    for it in range(iters):
        for g in range(3):
            sel = grp == g
            if not sel.any():
                sel = rng.rand(len(T)) < 0.1
            px = T[sel].reshape(-1, 3)
            w = np.repeat(cnt[sel], 64)
            # unieke kleuren met gewicht
            keys, inv = np.unique(px.astype(np.int64) @ np.array([1, 256, 65536]), return_inverse=True)
            cols = np.stack([keys % 256, (keys // 256) % 256, keys // 65536], 1).astype(np.float64)
            cw = np.bincount(inv, weights=w)
            k = min(n_free, len(cols))
            c = cols[np.argsort(-cw)[:k]].copy() if pals[g] is None else pals[g][len(fx):].copy()
            for _ in range(12):
                allc = np.concatenate([fx, c]) if len(fx) else c
                d = (((cols[:, None, :] - allc[None]) ** 2) * wts).sum(2)
                a = d.argmin(1)
                for j in range(len(c)):
                    m = a == len(fx) + j
                    if m.any():
                        c[j] = np.average(cols[m], axis=0, weights=cw[m])
            pals[g] = np.concatenate([fx, c]) if len(fx) else c
        # tiles opnieuw verdelen
        err = np.zeros((len(T), 3))
        for g in range(3):
            P = np.array([gba(x) for x in pals[g]], np.float64)
            d = (((T[:, :, None, :] - P[None, None]) ** 2) * wts).sum(3).min(2).sum(1)
            err[:, g] = d
        grp = err.argmin(1)
    return [[tuple(int(v) for v in gba(x)) for x in p] for p in pals]


def sheet(frames, idxs, path, scale=2, cols=4):
    """Contactvel van gekozen gameframes (vergroot)."""
    rows = (len(idxs) + cols - 1) // cols
    S = Image.new('RGB', (W * cols * scale + (cols - 1) * 4, H * rows * scale + (rows - 1) * 4), (40, 40, 40))
    for n, i in enumerate(idxs):
        im = Image.fromarray(frames[i]).resize((W * scale, H * scale), Image.NEAREST)
        S.paste(im, ((n % cols) * (W * scale + 4), (n // cols) * (H * scale + 4)))
    S.save(path)
