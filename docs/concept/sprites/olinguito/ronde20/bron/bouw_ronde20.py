#!/usr/bin/env python3
"""Olinguito ronde 20: alle verbeterpunten in een keer, op basis van stap 1b.
Lagen (van achter naar voor): lijf, verre achterpoot, verre voorpoot + verre klauwen,
nabije achterpoot, nabije voorpoot + nabije klauwen, staart (letterlijk), kop (letterlijk + masker).
Tekens = paletindex (hex), '.' = niet schilderen. Alles met de hand per rij uitgeschreven;
de klauwen zijn de Sandslash-klauwen (graphics/pokemon/sandslash, x4-14 y34-45) in onze kleuren.
Frame 2: kop en voorpoten 1 rij hoger, staart 1 rij lager (zoals in stap 1b); lijf en achterpoten blijven."""
from PIL import Image
import os
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..')
ST1B = os.path.join(R, 'stap1b_kop', 'anim_front.png')
SAND = os.path.join(R, '..', '..', '..', '..', 'graphics', 'pokemon', 'sandslash', 'anim_front.png')
TAIL_DX = -6

# ---------- masker-correctie (kop), frame-1-coordinaten ----------
MASKER = {  # y: (x0, rij)
    # punt 1a: masker boven de neus 1-2 rijen lager (bovenrand zakt van y28 naar y29/y30 voor x15-18)
    28: (15, '5543'),          # x15-18: vacht in plaats van masker/glans
    29: (14, '4332'),          # x14-17: vacht, glans zakt mee naar de nieuwe bovenrand
    # punt 1b: onderste uiteinde van het masker (onderlob) 5 px mee naar voren, zoals oog en bovenlob
    33: (28, '24444'),         # x28-32: lob eindigt nu bij x28 (was x32); erachter wang
    34: (30, '4444'),          # x30-33: oude lobpunt wordt wang
    35: (31, '33'),            # x31-32: los kaaklijntje -> schaduw (geen zwevende donkere streep)
}

# ---------- lijf ----------
LIJF = {
    32: (40, '22222'),
    33: (38, '22555522'),
    34: (39, '55555522'),
    35: (38, '3445555442'),
    36: (38, '344444444432'),
    37: (38, '44444444431'),
    38: (37, '4444444433'),
    39: (34, '3444444444433'),
    40: (29, '4444444444255554431'),
    41: (29, '4444444444245554431'),
    42: (29, '444444444332455443'),
    43: (29, '44444433332244544'),
    44: (30, '3333333311'),
}
VERRE_ACHTERPOOT = {
    44: (33, '2333'),
    45: (32, '23333'),
    46: (32, '23331'),
    47: (32, '23331'),
    48: (31, '23331'),
    49: (30, '233331'),
    50: (30, '123121'),
    51: (31, '11.11'),
}
VERRE_VOORPOOT = {
    41: (32, '2333'),
    42: (31, '23331'),
    43: (30, '23331'),
    44: (30, '23331'),
    45: (29, '23331'),
    46: (29, '23331'),
    47: (29, '23331'),
    48: (29, '21111'),
}
NABIJE_ACHTERPOOT = {
    42: (44, '431'),
    43: (38, '24454431'),
    44: (38, '2444431'),
    45: (37, '2444311'),
    46: (37, '24431'),
    47: (37, '244331'),
    48: (37, '244331'),
    49: (37, '24331'),
    50: (36, '24431'),
    51: (35, '244431'),
    52: (34, '2444331'),
    53: (34, '1231331'),
    54: (35, '11.111'),
}
NABIJE_VOORPOOT = {
    40: (25, '22455433'),
    41: (25, '2455433'),
    42: (24, '245543331'),
    43: (23, '24544331'),
    44: (22, '2444331'),
    45: (21, '2444331'),
    46: (21, '244331'),
    47: (21, '23331'),
    48: (21, '23331'),
    49: (21, '2331'),
    50: (21, '111'),
}
# Sandslash-klauwkleuren -> ons palet. Nabij: wit/creme/grijs; ver: een stap donkerder.
SAND_NABIJ = {6: 0xc, 7: 0xa, 9: 0x9, 0xa: 0x9, 0xf: 0x1}
SAND_VER = {6: 0xa, 7: 0x9, 9: 0x9, 0xa: 0x1, 0xf: 0x1}
SAND_BOX = (4, 34, 14, 45)   # x0, y0, x1, y1 (incl.) van de nabije hand van Sandslash
KLAUW_NABIJ = (8, 10)        # verschuiving: punt (x5,y45) -> (x13,y55)
KLAUW_VER = (17, 8)          # 9 px naar rechts, 2 rijen hoger

def head_mask(x, y):
    """Kopzone in stap 1b (frame 1): achterste omlijning per rij."""
    if y < 19 or y > 39 or x < 9:
        return False
    lim = {33: 37, 34: 38, 35: 37, 36: 37, 37: 37, 38: 36, 39: 33}.get(y, 39)
    return x <= lim

def tail_mask(x, y):
    """Staart (J met haak) in stap 1b (frame 1), voor verschuiving."""
    return (x >= 53 and 33 <= y <= 53) or (50 <= x <= 52 and 46 <= y <= 52)

def sand_claws():
    s = Image.open(SAND)
    x0, y0, x1, y1 = SAND_BOX
    pts = []
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            v = s.getpixel((x, y))
            if v not in SAND_NABIJ:
                continue
            # alleen de klauwen zelf (niet de gele arm en zijn omlijning rechts)
            if x >= 13 and v == 0xf and y <= 40:
                pass
            if v == 0xf and x >= 14:
                continue
            pts.append((x, y, v))
    return pts

def paint(g, rows, dy=0):
    for y, (x0, s) in rows.items():
        for i, c in enumerate(s):
            if c != '.':
                g[(x0 + i, y + dy)] = int(c, 16)

def bouw_frame(src, f):
    """f = 0 (frame 1) of 1 (frame 2)."""
    g = {}
    up = -1 if f else 0          # kop en voorpoten
    paint(g, LIJF)
    if f:   # frame 2: borst onder de kop gaat mee omhoog (voorkomt een gat onder de kin)
        paint(g, {y: (x0, ''.join(c if x0 + i <= 39 else '.' for i, c in enumerate(r)))
                  for y, (x0, r) in LIJF.items()}, -1)
    paint(g, VERRE_ACHTERPOOT)
    claws = sand_claws()
    dx, dy = KLAUW_VER
    for x, y, v in claws:
        if y >= 38:              # van de verre poot steken alleen de punten uit
            g[(x + dx, y + dy + up)] = SAND_VER[v]
    paint(g, VERRE_VOORPOOT, up)
    paint(g, NABIJE_ACHTERPOOT)
    paint(g, NABIJE_VOORPOOT, up)
    dx, dy = KLAUW_NABIJ
    for x, y, v in claws:
        g[(x + dx, y + dy + up)] = SAND_NABIJ[v]
    # staart: letterlijk uit stap 1b, zelfde frame (frame 2 staat daar 1 rij lager)
    for y in range(64):
        for x in range(64):
            if 0 <= y - f and tail_mask(x, y - f):
                v = src.getpixel((x, y + 64 * f))
                if v:
                    g[(x + TAIL_DX, y)] = v
    # kop: letterlijk uit stap 1b, zelfde frame (frame 2 staat 1 rij hoger), dan de maskercorrectie
    for y in range(64):
        for x in range(64):
            if y + f < 64 and head_mask(x, y + f):
                v = src.getpixel((x, y + 64 * f))
                if v:
                    g[(x, y)] = v
                else:
                    g.pop((x, y), None)
    paint(g, MASKER, up)
    return g

def bouw():
    src = Image.open(ST1B)
    out = Image.new('P', (64, 128), 0)
    out.putpalette(src.getpalette())
    for f in (0, 1):
        g = bouw_frame(src, f)
        for (x, y), v in g.items():
            if 0 <= x < 64 and 0 <= y < 64:
                out.putpixel((x, y + 64 * f), v)
    return src, out

if __name__ == '__main__':
    src, out = bouw()
    out.save(os.path.join(H, '..', 'anim_front.png'), transparency=0)
    a = sum(1 for y in range(64) for x in range(64) if out.getpixel((x, y)))
    xs = [x for y in range(64) for x in range(64) if out.getpixel((x, y))]
    ys = [y for y in range(64) for x in range(64) if out.getpixel((x, y))]
    print('frame 1: %d px, box x%d-%d (%d) y%d-%d (%d)' % (a, min(xs), max(xs), max(xs) - min(xs) + 1, min(ys), max(ys), max(ys) - min(ys) + 1))
