"""Alpaca ronde 2 ('Wolbokser'): bouwt anim_front.png + normal.pal.
  python3 alpaca2.py <uitmap>
Vormen via tools/concept/sprites/shapelib.py, gezicht en details als ASCII-rasters."""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from shapelib import Canvas, save_indexed, write_jasc, hexpal

PAL = hexpal([
    '#94cd9c',                                  # 0 transparant
    '#fffffa', '#f4eee6', '#cec4d2', '#857894', # 1-4 wol (licht -> selout; koele lavendel schaduw)
    '#e0a070', '#b8714a', '#7a3e2c',            # 5-7 vacht (gezicht, oren, armen, poten)
    '#ff7a6e', '#e8383d', '#9e1b32',            # 8-10 handschoenen + oorkwastjes
    '#f6c445', '#b07a28',                       # 11-12 polsband (aguayo-goud)
    '#d24a5e',                                  # 13 mond binnenkant
    '#ffffff',                                  # 14 wit (glans, tandje)
    '#101010'])                                 # 15 omlijning
R = {'wol': [1, 2, 3, 4], 'vacht': [5, 6, 7], 'rood': [8, 9, 10], 'goud': [11, 12]}
TH = {'wol': [0.80, 0.05, -0.6], 'vacht': [0.78, 0.0], 'rood': [0.72, 0.0], 'goud': [0.3]}
K = {'w': 14, 'k': 15, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
     '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'm': 13, 'x': 0}


def glove(c, cx, cy, r, far=False, band_dir=(1, 0)):
    """Ronde bokshandschoen met duimbobbel; band = gouden polsband aan de armkant."""
    sh = 1 if far else 0
    bx, by = band_dir
    c.ellipse(cx + bx * (r - 0.5), cy + by * (r - 0.5), r * 0.55, r * 0.75 if bx else r * 0.55, 'goud', shift=sh)
    c.ellipse(cx, cy, r, r * 0.95, 'rood', shift=sh)
    c.ellipse(cx - bx * 0.2 * r + by * 0.6 * r, cy - r * 0.55, r * 0.42, r * 0.38, 'rood', shift=sh)  # duim


def puffs(c, cx, cy, rx, ry, n, br, a0=0.0, glob=None, mix=0.7, curl=(0.15, 2.4)):
    """Wolwolk: kern + bolletjes op de rand, elk met een eigen glans (gemengd met de
    belichting van de hele wolk), en een lavendel krulboogje aan de onderkant van de
    bolletjes in de onderste/rechter helft: een geschulpte rand zoals Wooloo/Altaria."""
    glob = glob or (cx - 2, cy - 3, rx + 2, ry + 2)
    core = c.m_ellipse(cx, cy, rx - br * 0.9, ry - br * 0.9)
    c.fill(core, 'wol', *glob, edge=False)
    cs = []
    for k in range(n):
        a = a0 + 2 * np.pi * k / n
        cs.append((cx + np.cos(a) * (rx - br), cy + np.sin(a) * (ry - br), a))
    allm = core.copy()
    order = sorted(cs, key=lambda p: p[1])
    masks = []
    for bx, by, a in order:
        m = c.m_ellipse(bx, by, br, br)
        c.fill(m, 'wol', bx, by, br, br, glob=glob, mix=mix, edge=False)
        masks.append(m); allm |= m
    return cs


# Wolbolletjes van het lijf (x, y, straal), met de hand geplaatst. Getekend van onder
# naar boven: elk hoger bolletje ligt vóór het lagere, met een lavendel boogje langs
# zijn onderrand (de 'schubben' van Swablu/Altaria/Mareep).
BODY = [(28, 52, 4.4), (34, 53, 4.4), (40, 53, 4.4), (46, 50, 4.4),
        (25, 47, 4.0), (31, 47, 4.6), (38, 47, 4.8), (46, 44, 4.6), (49, 48, 3.6),
        (30, 40, 4.6), (37, 40, 4.8), (44, 38, 4.2),
        (26, 35, 3.4), (31, 34, 3.6), (36, 35, 3.6)]


def body_puffs(c, dx=0):
    glob = (35 + dx, 42, 17, 15)
    c.fill(c.m_ellipse(37 + dx, 45, 12, 9), 'wol', *glob, edge=False)
    wool = c.part == 'wol'
    for bx, by, r in sorted(BODY, key=lambda p: -p[1]):
        bx += dx
        m = c.m_ellipse(bx, by, r, r)
        c.fill(m, 'wol', bx, by, r, r, glob=glob, mix=0.6, edge=False)
        y, x = np.mgrid[0:64, 0:64]
        lower = (y - by) > 0.25 * r
        nb_w = np.zeros_like(m)
        for oy, ox in ((1, 0), (0, 1), (0, -1)):
            nb_w |= np.roll(np.roll(wool & ~m, -oy, 0), -ox, 1)
        line = m & lower & nb_w
        c.idx[line] = np.where(c.idx[line] >= 3, 4, 3)
        wool = c.part == 'wol'


def frame(f2=False):
    c = Canvas(R, thresholds=TH)
    lean = -2 if f2 else 0          # frame 2: naar voren
    # pootjes (achter de wol)
    c.ellipse(30, 56.5, 3, 3, 'vacht'); c.ellipse(42, 56.5, 3, 3, 'vacht', shift=1)
    # achterste arm + handschoen (ver, een tint donkerder) achter het lijf in frame 2
    if f2:
        glove(c, 50, 37, 4.6, far=True, band_dir=(-1, 1))
    # wollen lijf: wolk met geschulpte rand
    body_puffs(c, lean)
    hx, hy = 28 + lean, 27 + (1 if f2 else 0)
    # oren (banaanvorm) met rode wollen kwastjes
    if f2:   # oren plat naar achteren
        c.poly([(hx + 5, hy - 7), (hx + 14, hy - 11), (hx + 15, hy - 9), (hx + 7, hy - 4)], 'vacht', shift=1)
        c.ellipse(hx + 15, hy - 11, 2.6, 2.6, 'rood')
        c.poly([(hx - 3, hy - 7), (hx + 6, hy - 13), (hx + 7, hy - 11), (hx + 1, hy - 5)], 'vacht')
        c.ellipse(hx + 7, hy - 13, 2.6, 2.6, 'rood')
    else:
        c.poly([(hx + 5, hy - 6), (hx + 9, hy - 14), (hx + 11, hy - 13), (hx + 8, hy - 4)], 'vacht', shift=1)
        c.ellipse(hx + 10, hy - 15, 2.6, 2.6, 'rood')
        c.poly([(hx - 6, hy - 4), (hx - 10, hy - 13), (hx - 8, hy - 15), (hx - 3, hy - 6)], 'vacht')
        c.ellipse(hx - 9, hy - 15, 2.6, 2.6, 'rood')
    # kop (groot, schattig)
    c.ellipse(hx, hy, 8.5, 7.5, 'vacht')
    c.ellipse(hx - 6, hy + 3.5, 4.8, 3.6, 'vacht', tone=5)             # snoet licht
    # bolhoedkuif: koepel + krulrand
    c.ellipse(hx + 1, hy - 9.6, 5.4, 3.4, 'wol')
    c.fill(c.m_ellipse(hx + 0.5, hy - 7.2, 7.6, 1.9), 'wol', hx, hy - 9, 9, 5)
    # krulrand: de uiteinden van de rand krullen op (bolhoed)
    c.put([(hx - 7, hy - 8), (hx + 8, hy - 8)], 2)
    # voorste arm + handschoen (jab)
    if f2:
        c.poly([(27, 46), (30, 42), (16, 39), (13, 43)], 'vacht')
        glove(c, 8, 40, 6.4, band_dir=(1, 0.3))
    else:
        c.poly([(30, 46), (32, 42), (21, 39), (18, 43)], 'vacht')
        glove(c, 15, 40, 6.2, band_dir=(1, 0.25))
        # achterste handschoen in de dekking bij de wang
        glove(c, hx + 13, hy + 7, 5.0, far=True, band_dir=(0.3, 1))
    return c, hx, hy


def face(c, hx, hy, f2=False):
    # wollen V-wenkbrauwen + grote ogen met glans; snoet met neus en mondje
    if not f2:
        c.stamp(hx - 7, hy - 5, [
            '1........',
            '21....112',
            '3221.1223',
            '..3213...',
        ], K)
        c.stamp(hx - 6, hy - 1, [
            '.kk...kk',
            'kwwk.kwk',
            'kwkk.kkk',
            'kkkk.kkk',
            '.kk...k.',
        ], K)
        c.stamp(hx - 12, hy + 3, [
            '......',
            '.7....',
            '..6...',
            '...kk.',
        ], K)
    else:
        c.stamp(hx - 7, hy - 5, [
            '11.......',
            '3221..122',
            '..32211.3',
            '....33...',
        ], K)
        c.stamp(hx - 6, hy - 1, [
            '.kk...kk',
            'kwwk.kwk',
            'kkkk.kkk',
            '.kk...k.',
        ], K)
        c.stamp(hx - 12, hy + 2, [
            '.........',
            '.7..kkkk.',
            '...kmmmmk',
            '...kmmwk.',
            '....kkk..',
        ], K)


def build():
    out = []
    for f2 in (False, True):
        c, hx, hy = frame(f2)
        c.outline()
        face(c, hx, hy, f2)
        out.append(c.idx.astype(np.uint8))
    return out


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    fr = build()
    save_indexed(os.path.join(d, 'anim_front.png'), fr, PAL)
    write_jasc(os.path.join(d, 'normal.pal'), PAL)
    print('ok')
