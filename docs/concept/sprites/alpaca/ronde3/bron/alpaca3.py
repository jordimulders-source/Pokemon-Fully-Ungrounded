"""Alpaca ronde 3: viervoeter met bokshandschoenen aan de voorpoten.
  python3 alpaca3.py <uitmap>   -> procbase.png (vormen) + normal.pal
Daarna gaat alpaca3.seg (handwerk: gezicht, details) er via segraster.py overheen."""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from shapelib import Canvas, save_indexed, write_jasc, hexpal

PAL = hexpal([
    '#94cd9c',
    '#fffff6', '#f4eee6', '#cec4d2', '#857894',  # 1-4 wol
    '#e0a070', '#b8714a', '#7a3e2c',             # 5-7 vacht
    '#ff7a6e', '#e8383d', '#9e1b32',             # 8-10 handschoenen + kwastjes
    '#f6c445', '#b07a28',                        # 11-12 polsband
    '#d24a5e',                                   # 13 mond
    '#ffffff', '#101010'])
R = {'wol': [1, 2, 3, 4], 'vacht': [5, 6, 7], 'rood': [8, 9, 10], 'goud': [11, 12]}
TH = {'wol': [0.80, 0.05, -0.6], 'vacht': [0.78, 0.0], 'rood': [0.72, 0.0], 'goud': [0.3]}


def puffs(c, items, glob, mix=0.6):
    """Wolbolletjes (x, y, r) van onder naar boven; boogje langs de onderrand."""
    wool = c.part == 'wol'
    y, x = np.mgrid[0:64, 0:64]
    for bx, by, r in sorted(items, key=lambda p: -p[1]):
        m = c.m_ellipse(bx, by, r, r)
        c.fill(m, 'wol', bx, by, r, r, glob=glob, mix=mix, edge=False)
        nb = np.zeros_like(m)
        for oy, ox in ((1, 0), (0, 1), (0, -1)):
            nb |= np.roll(np.roll(wool & ~m, -oy, 0), -ox, 1)
        line = m & ((y - by) > 0.25 * r) & nb
        c.idx[line] = np.where(c.idx[line] >= 3, 4, 3)
        wool = c.part == 'wol'


def glove(c, cx, cy, r, far=False):
    sh = 1 if far else 0
    c.ellipse(cx + 0.5, cy - r + 0.5, r * 0.62, 1.6, 'goud', shift=sh)   # polsband boven
    c.ellipse(cx, cy, r, r * 0.85, 'rood', shift=sh)
    c.ellipse(cx - r * 0.55, cy - r * 0.35, r * 0.4, r * 0.38, 'rood', shift=sh)  # duim naar voren


def leg(c, x0, y0, x1, y1, w, far=False):
    c.poly([(x0 - w / 2, y0), (x0 + w / 2, y0), (x1 + w / 2, y1), (x1 - w / 2, y1)], 'vacht', shift=1 if far else 0)


def frame(f2=False):
    c = Canvas(R, thresholds=TH)
    # achterpoten: korte stompjes met donkere hoefjes
    leg(c, 49, 50, 50, 56, 4.2, far=True); c.ellipse(50, 56.5, 2.5, 1.6, 'vacht', tone=7)
    leg(c, 43, 51, 43, 57, 4.6); c.ellipse(43, 57.5, 2.7, 1.6, 'vacht', tone=7)
    # verre voorpoot met handschoen (staat op de handschoen)
    leg(c, 32, 49, 32, 52, 3.8, far=True)
    glove(c, 32, 55, 4.4, far=True)
    # staart
    puffs(c, [(53, 41, 3.0)], (52, 39, 5, 5), mix=0.4)
    # wollen lijf
    glob = (36, 41, 17, 12)
    c.fill(c.m_ellipse(39, 46, 11, 6.5), 'wol', *glob, edge=False)
    puffs(c, [(29, 49, 3.8), (35, 51, 4.0), (41, 51, 4.0), (47, 49, 3.8), (51, 45, 3.4),
              (33, 44, 4.2), (40, 44, 4.4), (47, 42, 3.8), (36, 39, 3.6), (43, 38, 3.6)], glob)
    # korte, dikke wolhals
    lean = 1 if f2 else 0
    hx, hy = 24 - lean, 27 + lean
    puffs(c, [(29, 43, 4.4), (27, 38, 4.2), (25, 34, 3.8)], (24, 36, 8, 10), mix=0.5)
    # oren + kwastjes
    c.poly([(hx + 4, hy - 5), (hx + 7, hy - 12), (hx + 9, hy - 11), (hx + 7, hy - 4)], 'vacht', shift=1)
    c.poly([(hx - 5, hy - 4), (hx - 7, hy - 11), (hx - 5, hy - 12), (hx - 3, hy - 5)], 'vacht')
    c.ellipse(hx + 8.5, hy - 12.5, 2.2, 2.2, 'rood'); c.ellipse(hx - 6.5, hy - 12.5, 2.2, 2.2, 'rood')
    # grote kop (schattig)
    c.ellipse(hx, hy, 7.8, 6.6, 'vacht')
    c.ellipse(hx - 5.2, hy + 3.0, 3.7, 2.8, 'vacht', tone=5)   # snoet
    # mini-bolhoedje (wolkuif)
    c.ellipse(hx + 0.5, hy - 8.4, 4.0, 2.8, 'wol')
    c.fill(c.m_ellipse(hx + 0.2, hy - 6.2, 6.2, 1.4), 'wol', hx, hy - 8, 7, 4)
    # nabije voorpoot met handschoen
    if f2:   # opgeheven: stoot naar voren
        leg(c, 29, 47, 21, 45, 4.6)
        glove(c, 16, 45, 5.0)
    else:
        leg(c, 27, 48, 25, 51, 4.4)
        glove(c, 24, 54, 5.0)
    c.outline()
    return c, hx, hy


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    fr = [frame(f)[0].idx.astype(np.uint8) for f in (False, True)]
    save_indexed(os.path.join(d, 'procbase.png'), fr, PAL)
    write_jasc(os.path.join(d, 'normal.pal'), PAL)
    print('ok')
