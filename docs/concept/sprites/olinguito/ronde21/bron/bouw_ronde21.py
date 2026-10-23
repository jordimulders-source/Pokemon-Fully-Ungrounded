#!/usr/bin/env python3
"""Olinguito ronde 21: poten en klauwen, op basis van ronde 20.
Kop (met masker), oren, staart en romp komen letterlijk uit ronde 20 (zelfde frame).
Alleen de pootzone (y>=40, x<=48, zonder staart) wordt opnieuw getekend, plus de kaaklijn (KAAK, <=6 px).
Tekens = paletindex (hex), '.' = niet schilderen. Met de hand per rij uitgeschreven.
Lagen (achter -> voor): romp, verre achterpoot, verre voorpoot + klauwen, nabije achterpoot (ronde 20, dx +2),
nabije voorpoot + klauwen, staart, kop, kaaklijn.
Frame 2: kop en voorpoten 1 rij hoger (zoals ronde 20); romp, achterpoten en staart uit ronde 20 frame 2."""
from PIL import Image
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..')
R20 = os.path.join(R, 'ronde20', 'anim_front.png')
sys.path.insert(0, os.path.join(R, 'ronde20', 'bron'))
import bouw_ronde20 as B20

HIND_DX = 2   # punt 3: nabije achterpoot als geheel 2 px naar achteren (richting stap 1b / Galar-Linoone)

def in_zone(x, y):
    """Pootzone (frame-1-coordinaten van de romp): alles onder de borst links van de staart."""
    return y >= 40 and 12 <= x <= 48

def tail_px(x, y, f):
    """Staartpixel in ronde 20 (frame f): stap-1b-staartmasker met dx -6 en de frame-2-rij."""
    return 0 <= y - f and B20.tail_mask(x - B20.TAIL_DX, y - f)

# ---------- verre voorpoot (schaduwtint 3), eigen kolom x29-32, voet 2 rijen hoger dan de nabije ----------
VERRE_VOOR = {
    44: (30, '2331'),
    45: (30, '2331'),
    46: (30, '2331'),
    47: (29, '2331'),
    48: (29, '2331'),
    49: (28, '23331'),
    50: (28, '23331'),
    51: (29, '1111'),
}
# ---------- buik + verre achterpoot (x34-37, lucht op x33) ----------
BUIK = {
    43: (31, '33333333'),
    44: (34, '11111'),
}
VERRE_ACHTER = {
    45: (36, '233'),
    46: (36, '2331'),
    47: (35, '2331'),
    48: (35, '2331'),
    49: (34, '2331'),
    50: (33, '23331'),
    51: (33, '11111'),
}
# ---------- nabije voorpoot: schouderbolling onder de borst, poot bijna loodrecht ----------
NABIJ_VOOR = {
    40: (24, '22455433'),
    41: (23, '224554331'),
    42: (23, '2455443311'),
    43: (23, '24554431'),
    44: (22, '2455431'),
    45: (21, '2445431'),
    46: (21, '244431'),
    47: (20, '244431'),
    48: (20, '244331'),
    49: (19, '2444331'),
    50: (19, '2444331'),
    51: (20, '244331'),
    52: (21, '11111'),
}
# Klauwen in Sandslash-vorm (2 per poot), verkleind tot de pootdikte. Blok: (x0, y0) linksboven, rijen.
KLAUW_NABIJ = ((14, 48), [
    '...991..',
    '..9cca1.',
    '.9ca9cc1',
    '.9a9cca1',
    '9a9caa1.',
    '9a9ca1..',
    '19a91...',
    '.111....',
])
KLAUW_VER = ((24, 49), [
    '..991.',
    '.9aa91',
    '9a99a1',
    '9a9a1.',
    '191...',
    '.1....',
])
# ---------- kaaklijn (A6): onderkant van de kaak licht gebogen, frame-1-coordinaten ----------
KAAK = {
    39: (23, '33'),     # x23-24: was zwarte rechte rand; wordt kaakschaduw
    40: (23, '1'),      # x23: de rand zakt hier 1 rij (boog naar de keel)
}

def paint(g, rows, dy=0, dx=0):
    for y, (x0, s) in rows.items():
        for i, c in enumerate(s):
            if c != '.':
                g[(x0 + i + dx, y + dy)] = int(c, 16)

def paint_block(g, blok, dy=0):
    (x0, y0), rows = blok
    paint(g, {y0 + i: (x0, r) for i, r in enumerate(rows)}, dy)

def bouw_frame(r20, f):
    up = -1 if f else 0
    g = {}
    # 1. alles uit ronde 20 buiten de pootzone (en de staart, ook binnen de zone)
    for y in range(64):
        for x in range(64):
            v = r20.getpixel((x, y + 64 * f))
            if v and (not in_zone(x, y) or tail_px(x, y, f)):
                g[(x, y)] = v
    # 2. romp-onderkant binnen de zone: rijen y40-43 letterlijk uit ronde 20 waar geen poot komt
    paint(g, {y: r for y, r in B20.LIJF.items() if y >= 40})
    # 3. poten
    paint(g, BUIK)
    paint(g, VERRE_ACHTER)
    paint(g, VERRE_VOOR, up)
    paint_block(g, KLAUW_VER, up)
    paint(g, B20.NABIJE_ACHTERPOOT, 0, HIND_DX)
    paint(g, NABIJ_VOOR, up)
    paint_block(g, KLAUW_NABIJ, up)
    # 4. staart en kop letterlijk terug (bovenop)
    for y in range(64):
        for x in range(64):
            v = r20.getpixel((x, y + 64 * f))
            if tail_px(x, y, f) and v:
                g[(x, y)] = v
            if y + f < 64 and B20.head_mask(x, y + f):
                if v:
                    g[(x, y)] = v
                else:
                    g.pop((x, y), None)
    paint(g, KAAK, up)
    return g

def bouw(paths=(R20,)):
    r20 = Image.open(R20)
    out = Image.new('P', (64, 128), 0)
    out.putpalette(r20.getpalette())
    for f in (0, 1):
        g = bouw_frame(r20, f)
        for (x, y), v in g.items():
            if 0 <= x < 64 and 0 <= y < 64:
                out.putpixel((x, y + 64 * f), v)
    return r20, out

if __name__ == '__main__':
    r20, out = bouw()
    out.save(os.path.join(H, '..', 'anim_front.png'), transparency=0)
    for f in (0, 1):
        px = [(x, y) for y in range(64) for x in range(64) if out.getpixel((x, y + 64 * f))]
        xs = [p[0] for p in px]; ys = [p[1] for p in px]
        print('frame %d: %d px, box %dx%d' % (f + 1, len(px), max(xs)-min(xs)+1, max(ys)-min(ys)+1))
