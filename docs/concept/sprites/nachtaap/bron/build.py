"""Nachtaap fase 1 (Psychic-starter): bouwt anim_front.png (2 frames) uit vormen.

Vormen (ellips/capsule/lijn) met een normaal -> licht linksboven -> tinten per ramp,
daarna omlijning (selout boven/links, zwart rechts/onder) en gezicht/handen met de hand.
"""
import sys, os, math
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites'); sys.path.insert(0, HERE)
from ramp import gba, write_pal

# ---------------- palet ----------------
PAL = [gba((152, 208, 160))]           # 0 transparant
RAMPS = {
    'fur':   [(230, 213, 197), (180, 164, 148), (139, 123, 123), (98, 82, 98)],     # 1-4 grijsbruine vacht
    'cream': [(255, 246, 222), (222, 205, 172), (164, 148, 123)],                  # 5-7 gezichtsvlekken, vingertoppen, staartkrul
    'belly': [(255, 205, 139), (230, 164, 90), (164, 98, 57)],                     # 8-10 oranje buik/borst
    'iris':  [(255, 238, 148), (238, 172, 49), (164, 90, 24)],                     # 11-13 ogen
}
IDX = {}
for name in ['fur', 'cream', 'belly', 'iris']:
    IDX[name] = list(range(len(PAL), len(PAL) + len(RAMPS[name])))
    PAL += [gba(c) for c in RAMPS[name]]
WHITE = len(PAL); PAL.append((255, 255, 255))   # 14
BLACK = 15; PAL.append((16, 16, 16))
assert len(PAL) == 16, len(PAL)

LIGHT = np.array([-0.55, -0.70, 0.55]); LIGHT /= np.linalg.norm(LIGHT)
# drempels per ramp (dot met licht) van licht naar donker
FRAC = {4: [0.07, 0.53, 0.28, 0.12], 3: [0.10, 0.60, 0.30]}


class Canvas:
    def __init__(s):
        s.part = np.full((64, 64), '', dtype=object)
        s.prim = np.full((64, 64), -1)
        s.dot = np.zeros((64, 64))
        s.prims = []      # (part, z, group, hard)
        s.fixed = {}      # (y,x) -> index (handwerk, na de schaduw)

    def _put(s, mask, nx, ny, part, group=None, hard=False, bias=0.0):
        pid = len(s.prims); s.prims.append((part, pid, group if group is not None else pid, hard))
        nz = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
        d = nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2] + bias
        s.part[mask] = part; s.prim[mask] = pid; s.dot[mask] = d[mask]
        return pid

    def ellipse(s, cx, cy, rx, ry, part, **kw):
        yy, xx = np.mgrid[0:64, 0:64] + 0.5
        nx = (xx - cx) / rx; ny = (yy - cy) / ry
        m = nx ** 2 + ny ** 2 <= 1.0
        return s._put(m, nx, ny, part, **kw)

    def capsule(s, pts, radii, part, **kw):
        """Dikke lijn langs pts met straal per punt (lineair)."""
        yy, xx = np.mgrid[0:64, 0:64] + 0.5
        best = np.full((64, 64), 1e9); NX = np.zeros((64, 64)); NY = np.zeros((64, 64))
        for (x0, y0), (x1, y1), r0, r1 in zip(pts, pts[1:], radii, radii[1:]):
            dx, dy = x1 - x0, y1 - y0; L2 = dx * dx + dy * dy or 1e-9
            t = np.clip(((xx - x0) * dx + (yy - y0) * dy) / L2, 0, 1)
            px = x0 + t * dx; py = y0 + t * dy; r = r0 + t * (r1 - r0)
            ox = xx - px; oy = yy - py
            q = np.sqrt(ox ** 2 + oy ** 2) / r
            upd = q < best
            best = np.where(upd, q, best)
            NX = np.where(upd, ox / r, NX); NY = np.where(upd, oy / r, NY)
        m = best <= 1.0
        return s._put(m, NX, NY, part, **kw)

    def shade(s):
        out = np.zeros((64, 64), dtype=np.uint8)
        filled = s.prim >= 0
        # drempels per ramp als percentielen (Hoenn: ±5% hooglicht, ±40% schaduw)
        for part, idx in IDX.items():
            m = filled & (s.part == part)
            if not m.any(): continue
            d = s.dot[m]
            fr = FRAC[len(idx)]
            th = [np.percentile(d, 100 * (1 - c)) for c in np.cumsum(fr)[:-1]]
            k = np.zeros(d.shape, int)
            for t in th:
                k += d < t
            out[m] = np.array(idx)[k]
        # omlijning
        res = out.copy()
        for y in range(64):
            for x in range(64):
                if not filled[y, x]: continue
                p = s.prim[y, x]; part, z, grp, hard = s.prims[p]
                idx = IDX[part]
                col = None
                for dy, dx, side in ((-1, 0, 'u'), (0, -1, 'l'), (1, 0, 'd'), (0, 1, 'r')):
                    yy, xx = y + dy, x + dx
                    if not (0 <= yy < 64 and 0 <= xx < 64) or not filled[yy, xx]:
                        if side in 'dr':
                            col = BLACK
                        elif col is None:
                            col = idx[-1]
                    else:
                        q = s.prim[yy, xx]
                        if q < p and s.prims[q][2] != grp:      # wij liggen ervoor: contour op onze pixels
                            c = BLACK if (hard and side in 'dr') else idx[-1]
                            if col is None or c == BLACK: col = c
                if col is not None:
                    res[y, x] = col
        for (y, x), v in s.fixed.items():
            if 0 <= y < 64 and 0 <= x < 64:
                res[y, x] = v
        return res


CH = {'k': BLACK, 'w': WHITE, '.': None, ' ': None}
for n, ids in IDX.items():
    for i, v in enumerate(ids):
        CH[n[0] + str(i)] = v


def stamp(cv, x0, y0, rows, legend):
    """rows: strings; legend: char -> index (None = laat staan)."""
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            v = legend.get(ch)
            if v is not None:
                cv.fixed[(y0 + j, x0 + i)] = v


LEG = {'k': BLACK, 'w': WHITE,
       'A': IDX['iris'][0], 'B': IDX['iris'][1], 'C': IDX['iris'][2],
       '1': IDX['fur'][0], '2': IDX['fur'][1], '3': IDX['fur'][2], '4': IDX['fur'][3],
       'q': IDX['cream'][0], 'r': IDX['cream'][1], 's': IDX['cream'][2],
       'x': IDX['belly'][0], 'y': IDX['belly'][1], 'z': IDX['belly'][2]}


def eye(cv, cx, cy, rx, ry, px=-0.6, py=0.4, pr=(2.4, 2.8)):
    """Groot rond oog: zwarte rand, iris donker boven -> licht onder, grote pupil, witte sikkelglans."""
    for y in range(64):
        for x in range(64):
            u = (x + 0.5 - cx) / rx; v = (y + 0.5 - cy) / ry
            r2 = u * u + v * v
            if r2 > 1: continue
            # rand: buur buiten de ellips
            edge = any(((x + 0.5 + dx - cx) / rx) ** 2 + ((y + 0.5 + dy - cy) / ry) ** 2 > 1
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                cv.fixed[(y, x)] = BLACK; continue
            pu = (x + 0.5 - cx - px) / pr[0]; pv = (y + 0.5 - cy - py) / pr[1]
            if pu * pu + pv * pv <= 1:
                cv.fixed[(y, x)] = BLACK; continue
            t = v + 0.35 * u   # boven/links in schaduw van de oogleden
            cv.fixed[(y, x)] = IDX['iris'][2] if t < -0.35 else IDX['iris'][1] if t < 0.45 else IDX['iris'][0]


def pose(f):
    cv = Canvas()
    # staart (achter alles) met Nazca-spiraal
    lift = 2.5 if f == 1 else 0
    tail = [(40, 50), (46, 52), (50.5, 49), (52.5, 43 - lift * 0.5), (52.5, 36 - lift)]
    cx, cy, R0 = 49.6, 30.0 - lift, 4.3
    a0 = math.atan2(36 - lift - cy, 52.5 - cx)
    sp = []
    n = 34
    for i in range(1, n + 1):
        t = i / n
        a = a0 - t * 2 * math.pi * 1.25
        r = R0 * (1 - 0.72 * t)
        sp.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts = tail + sp
    cv.capsule(pts, [1.5] * len(tail) + [1.5 - 0.4 * i / n for i in range(1, n + 1)], 'fur', group=100, bias=0.1)
    # verre dij
    cv.ellipse(39.5, 47.5, 5.3, 6.2, 'fur', group=11, bias=-0.12, hard=True)
    # lijf
    cv.ellipse(31.0, 41.5, 9.0, 10.5, 'fur', group=1)
    cv.ellipse(28.5, 42.0, 4.8, 6.8, 'belly', group=1)
    # nabije dij
    cv.ellipse(22.0, 48.2, 6.6, 5.9, 'fur', group=14, hard=True)
    # oren
    cv.ellipse(16.5, 13.5, 3.2, 3.6, 'fur', group=20)
    cv.ellipse(42.0, 12.5, 2.6, 3.6, 'fur', group=21, bias=-0.1)
    # kop
    cv.ellipse(29.0, 21.5, 13.5, 11.8, 'fur', group=2)
    return cv


def put(cv, rows):
    """rows: lijst (y, x0, tekens); '.' = laat staan, '0' = transparant."""
    for y, x0, chars in rows:
        for i, ch in enumerate(chars):
            if ch == '.': continue
            cv.fixed[(y, x0 + i)] = 0 if ch == '0' else LEG[ch]


EYE_NEAR = [  # x17..26
    (17, 17, "..kkkkkk.."),
    (18, 17, ".kCCCCCCk."),
    (19, 17, "kCBkkkBBCk"),
    (20, 17, "kBkwwkkBBk"),
    (21, 17, "kBkwkkkBBk"),
    (22, 17, "kBkkkkkBBk"),
    (23, 17, "kAkkkkkBAk"),
    (24, 17, "kABkkkBAAk"),
    (25, 17, ".kAAAAAAk."),
    (26, 17, "..kkkkkk.."),
]
EYE_FAR = [  # x29..37
    (17, 29, "..kkkkk.."),
    (18, 29, ".kCCCCCk."),
    (19, 29, "kCBkkBBCk"),
    (20, 29, "kBkwwkBBk"),
    (21, 29, "kBkwkkBBk"),
    (22, 29, "kBkkkkBBk"),
    (23, 29, "kAkkkkBAk"),
    (24, 29, "kABkkBAAk"),
    (25, 29, ".kAAAAAk."),
    (26, 29, "..kkkkk.."),
]
FACE = [
    # witte vlekken boven de ogen, donkere middenstreep, zijstreep aan de verre kant
    (13, 27, "33"),
    (14, 20, "qqqqr..44..rrrs"),
    (15, 18, "qqqrrrrs.44.qrrrss4"),
    (16, 17, "rrs.....s4444rs...ss4"),
    (17, 17, "s.........44.......s4"),
    (18, 27, "32"),
    (19, 27, "32"), (20, 27, "23"), (21, 27, "23"), (22, 27, "23"), (23, 27, "22"),
    # snuit
    (24, 27, "qr"),
    (25, 26, "qqrr"),
    (26, 25, "qrrrrs"),
    (27, 24, "qrkkrrss"),
    (28, 24, "rrrrrrss"),
    (29, 25, "s4444s"),
    (30, 26, "ssss"),
    # lichte wangen onder de ogen
]


LIMBS = [
    # nabije arm (voor het lijf) met de hand over de knie
    (35, 22, "4114"),
    (36, 21, "4124"),
    (37, 20, "4124"),
    (38, 19, "41234"),
    (39, 18, "41234"),
    (40, 18, "41234"),
    (41, 17, "4122234"),
    (42, 16, "412222k"),
    (43, 15, "41k2k2k"),
    (44, 15, "2k2k2k"),
    (45, 15, "q4q4q"),
    (46, 15, "r4r4r"),
    # verre arm naar de verre knie
    (36, 37, "23k"),
    (37, 37, "233k"),
    (38, 38, "233k"),
    (39, 38, "4333k"),
    (40, 38, "42333k"),
    (41, 38, "422333k"),
    (42, 38, "4k3k3k"),
    (43, 38, "r4r4s"),
    (44, 38, "s.s.s"),
    # nabije voet met teenkussentjes
    (54, 15, "4441112222"),
    (55, 13, "qq41122222233"),
    (56, 12, "qrr42222233333k"),
    (57, 12, "kkkkkkkkkkkkkkk"),
    # verre voet
    (54, 38, "4222224"),
    (55, 37, "42222333k"),
    (56, 36, "k3333333srrk"),
    (57, 36, "kkkkkkkkkkk"),
]


def render_hand(f, rows):
    """Staart uit de schets (x>=45, of x>=42 boven y 45), de rest uit de handrijen."""
    base = pose(f).shade()
    out = np.zeros((64, 64), np.uint8)
    for y in range(64):
        for x in range(64):
            if x >= 45 or (x >= 42 and y < 41):
                out[y, x] = base[y, x]
    for y, x0, chars in rows:
        for i, ch in enumerate(chars):
            if ch == '.': continue
            out[y, x0 + i] = 0 if ch == '0' else LEG[ch]
    if f == 1:
        arm = raised_arm().shade()
        out[arm > 0] = arm[arm > 0]
        import f2
        for y, x0, chars in getattr(f2, 'POST', []):
            for i, ch in enumerate(chars):
                if ch == '.': continue
                out[y, x0 + i] = 0 if ch == '0' else LEG[ch]
    return out


def raised_arm():
    """Nabije arm omhoog met gespreide vingers en creme kussentjes."""
    cv = Canvas()
    cv.capsule([(24.0, 35.0), (18.0, 33.5), (14.0, 28.0)], [2.2, 1.9, 1.7], 'fur', group=1)
    for (x0, y0), (x1, y1) in (((11.5, 24.5), (8.5, 19.5)), ((13.0, 24.0), (12.5, 18.5)), ((14.5, 24.5), (16.5, 19.8))):
        cv.capsule([(x0, y0), (x1, y1)], [0.8, 0.8], 'fur', group=1)
    cv.ellipse(13.0, 25.8, 2.7, 2.5, 'fur', group=1)
    for x, y in ((8.3, 19.0), (12.4, 18.0), (16.7, 19.3)):
        cv.ellipse(x, y, 1.25, 1.25, 'cream', group=2)
    return cv


def render(f):
    import importlib
    mod = importlib.import_module('f%d' % (f + 1)) if os.path.exists(os.path.join(HERE, 'f%d.py' % (f + 1))) else None
    if mod: return render_hand(f, mod.ROWS)
    cv = pose(f)
    put(cv, EYE_NEAR); put(cv, EYE_FAR); put(cv, FACE); put(cv, LIMBS)
    return cv.shade()


def dither(a, regions):
    """Schaakbordovergang van 1 px tussen vachttint 2 en 3 op grote ronde vlakken."""
    t2, t3 = IDX['fur'][1], IDX['fur'][2]
    out = a.copy()
    for (x0, y0, x1, y1) in regions:
        for y in range(y0, y1):
            for x in range(x0, x1):
                if a[y, x] == t2 and (x + y) % 2 == 0 and (t3 in (a[y, x + 1], a[y, x + 2], a[y + 1, x], a[y + 2, x])):
                    out[y, x] = t3
    return out


def lighten(a, box, xmax3, xmax4):
    """Binnen box: tint 3 -> 2 links van xmax3, tint 4 -> 3 links van xmax4 (niet op de rand)."""
    t2, t3, t4 = IDX['fur'][1:4]
    out = a.copy(); x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            inner = all(a[y + dy, x + dx] > 0 for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if a[y, x] == t3 and x <= xmax3 and inner: out[y, x] = t2
            elif a[y, x] == t4 and x <= xmax4 and inner and a[y - 1, x] != 0: out[y, x] = t3
    return out


def save():
    fr = [render(0), render(1)]
    fr = [lighten(lighten(lighten(fr[k], (33, 43, 45, 53), 40, 41), (17, 27 - k, 34, 31 - k), 31, 0), (30, 33, 37, 42), 34, 0) for k in range(2)]
    fr = [dither(fr[0], [(17, 10, 41, 31), (15, 43, 45, 53)]), dither(fr[1], [(17, 9, 41, 30), (15, 43, 45, 53)])]
    a = np.vstack(fr)
    im = Image.fromarray(a, 'P'); im.putpalette([v for c in PAL for v in c] + [0] * (768 - 48))
    out = os.path.join(HERE, 'anim_front.png'); im.save(out)
    write_pal(os.path.join(HERE, 'normal.pal'), PAL)
    # voorbeeld: 6x en 1x
    rgb = np.array([PAL[i] for i in range(16)], np.uint8)[a]
    rgb[a == 0] = (200, 200, 200)
    big = Image.fromarray(rgb).resize((64 * 6, 128 * 6), Image.NEAREST)
    from PIL import ImageDraw
    dr = ImageDraw.Draw(big)
    for k in range(0, 129, 4):
        c = (120, 120, 255) if k % 8 == 0 else (190, 190, 230)
        if k <= 64: dr.line([(k * 6, 0), (k * 6, 128 * 6)], fill=c)
        dr.line([(0, k * 6), (64 * 6, k * 6)], fill=c)
    small = Image.fromarray(rgb)
    sheet = Image.new('RGB', (64 * 6 + 80, 128 * 6), 'white'); sheet.paste(big, (0, 0)); sheet.paste(small, (64 * 6 + 8, 0))
    sheet.save(os.path.join(HERE, 'preview.png'))
    return out


if __name__ == '__main__':
    print(save())
