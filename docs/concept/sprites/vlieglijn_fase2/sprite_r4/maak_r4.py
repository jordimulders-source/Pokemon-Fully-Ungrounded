#!/usr/bin/env python3
"""Mug r4: alleen kleur, schaduw en belijning op sprite_r3/mug_r3.png (alpha-diff 0, bewezen onderaan).

Indexen: 0=. 1=# 2=k 3=d 4=g 5=w 6=P 7=p 8=q 9=L (selout vleugels + midden schaal) 10=l 11=i 12=Y 13=y 14=E 15=e
Gebruik: python3 maak_r4.py  -> mug_r4A.png, mug_r4B.png (+ _8x, .txt, normal_A/B.pal), vel.png
"""
import os
import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = os.path.dirname(HIER)
R3 = os.path.join(BASIS, 'sprite_r3', 'mug_r3.png')
CH = '.#kdgwPpqLliYyEe'

r3img = Image.open(R3)
R3A = np.array(r3img)
PAL3 = np.array(r3img.getpalette()[:48]).reshape(16, 3)
H, W = R3A.shape

CHI = {c: i for i, c in enumerate(CH)}


def zet(a, lijst, groep, log):
    """lijst: (x, y, teken). Alleen bestaande figuurpixels; telt per groep."""
    n = 0
    for x, y, c in lijst:
        assert R3A[y, x] != 0, (x, y)
        v = CHI[c]
        if a[y, x] != v:
            a[y, x] = v
            n += 1
    log[groep] = log.get(groep, 0) + n


def rij(y, x0, tekens):
    return [(x0 + i, y, c) for i, c in enumerate(tekens) if c != ' ']


# ---------- POTEN: drie tinten k (schaduw) / l (midden) / i (glans linksboven) ----------
# Voor: Lambda-been (top, linkertak, knie, voet, rechtertak x31-32), arm naar de naald, poot over het achterlijf,
# lange rechterpoot. Achter (een stap donkerder, geen i): arm uit het borststuk (x33-36, y27-38),
# onderkant borststuk (x30-32, y29-32) en het lange linkeronderbeen (x34-38, y49-59).
POTEN_A = []
# arm naar de naald: bovenkant i, onderkant l
POTEN_A += [(14, 33, 'i'), (15, 33, 'i'), (16, 34, 'i'), (17, 34, 'i')] + rij(35, 18, 'iiii')
POTEN_A += [(25, 31, 'i'), (25, 32, 'i'), (24, 33, 'i')]
# Lambda: top + linkertak (i links, l midden, k rechts = binnenkant driehoek)
POTEN_A += rij(35, 30, 'i') + rij(36, 29, 'iiil') + rij(37, 29, 'ilil')
POTEN_A += rij(38, 28, 'il') + rij(39, 27, 'ilk') + rij(40, 27, 'ilk') + rij(41, 26, 'ilk') + rij(42, 25, 'ilk') + rij(43, 25, 'il')
# knie/voet: bovenrij i, onderrij l
POTEN_A += [(26, 45, 'i'), (26, 46, 'l'), (27, 46, 'i'), (28, 46, 'i')] + rij(47, 27, 'llllll')
# rechtertak (x31 glans, x32 midden) blijft zoals r3; scheidingslijn x33 (zie LIJN)
# achter: onderkant borststuk k, arm uit het borststuk l (licht) + k (schaduw)
POTEN_A += rij(29, 31, 'kk') + rij(30, 31, 'kk') + rij(31, 30, 'kkk') + rij(32, 30, 'kkk')
POTEN_A += [(33, 27, 'l'), (33, 28, 'l')] + rij(29, 33, 'llk') + rij(30, 33, 'llk') + rij(31, 33, 'llk')
POTEN_A += [(34, 32, 'l'), (34, 33, 'l'), (34, 34, 'l'), (35, 34, 'k'), (34, 35, 'l'), (35, 35, 'k'), (34, 37, 'l'), (34, 38, 'k')]
# lang linkeronderbeen (achter): l links, k rechts
POTEN_A += rij(49, 34, 'lk') + rij(50, 34, 'lk') + rij(51, 34, 'lk') + rij(53, 35, 'lk') + rij(56, 36, 'lk')
# poot over het achterlijf (voor): i links, l midden, k rechts
POTEN_A += rij(36, 38, 'ilk') + rij(37, 38, 'illk') + rij(38, 39, 'ilk') + rij(39, 39, 'ilk')
POTEN_A += rij(40, 40, 'ilk') + rij(41, 40, 'ilk') + rij(42, 41, 'il') + rij(43, 41, 'ilk')
# lange rechterpoot (voor): i links, l rechts, k waar 3 breed
POTEN_A += rij(47, 43, 'iill') + rij(48, 45, 'llk') + rij(49, 46, 'ilk') + rij(51, 48, 'il')
for y, x in ((52, 49), (53, 49), (54, 50), (55, 50), (56, 51), (57, 51), (58, 52), (59, 52)):
    POTEN_A.append((x, y, 'i')); POTEN_A.append((x + 1, y, 'l'))
POTEN_A += [(53, 61, 'i'), (54, 61, 'l')]
# losse spikkels (eigen controle): top rechtertak, eind achterarm, glans rechterpoot, achterbeen
POTEN_A += [(31, 35, 'l'), (34, 37, 'k'), (45, 48, 'i'), (36, 53, 'l'), (37, 56, 'l')]

# ---------- LIJN: arm/Lambda-scheiding, verlengt de rechterlijn van de rechtertak (x33, y39+) omhoog ----------
LIJN = [(33, 36, '#'), (33, 37, '#'), (33, 38, '#')]

# ---------- PAARS: borststuk q links (lichtkant, zoals het model), P-sikkel rechtsonder ----------
PAARS_A = [(30, 30, 'q'), (35, 25, 'P'), (35, 26, 'P'), (36, 27, 'P'), (36, 28, 'P'), (29, 31, 'P'),
           # achterlijf rechterpaneel: P-sikkel rechtsonder
           (46, 43, 'P'), (46, 44, 'P')]

# ---------- SCHAAL achterlijf: d hooglicht, L midden (slot 9, ook vleugelselout), k schaduw ----------
SCHAAL_A = [(41, 34, 'd'), (42, 34, 'd'), (43, 34, 'L'), (44, 35, 'L'), (42, 35, 'L'), (43, 35, 'L'), (43, 36, 'L'), (43, 37, 'L'),
            (44, 38, 'L'), (44, 39, 'L'), (44, 40, 'L'), (39, 31, 'd')]

# ---------- GRIJS: spikkels weg ----------
GRIJS_A = [(28, 12, 'g'),            # linkervleugel: losse d onderaan -> g (ader blijft x26)
           (24, 26, 'd'), (23, 27, 'd')]  # kop rechtsonder: d-k-d-dambord -> een d-vlak, nek blijft k
SCHAAL_B = SCHAAL_A + [(45, 38, 'L'), (45, 39, 'L'), (45, 40, 'L')]
PAARS_B = PAARS_A + [(35, 27, 'P'), (35, 28, 'P'), (38, 40, 'P'), (37, 41, 'P')]

EXTRA = {
    'A': [('poten', POTEN_A), ('lijn', LIJN), ('paars', PAARS_A), ('schaal', SCHAAL_A), ('grijs', GRIJS_A)],
    'B': [('poten', POTEN_A), ('lijn', LIJN), ('paars', PAARS_B), ('schaal', SCHAAL_B), ('grijs', GRIJS_A)],
}


def main():
    for naam in ('A', 'B'):
        a = R3A.copy()
        log = {}
        for groep, lijst in EXTRA[naam]:
            zet(a, lijst, groep, log)
        print(naam, log)
        schrijf(a, PAL[naam], naam)
    vel()


def schrijf(a, pal, naam):
    assert ((a > 0) == (R3A > 0)).all(), 'alpha-diff niet 0'
    im = Image.fromarray(a.astype(np.uint8), 'P')
    flat = [c for rgb in pal for c in rgb]
    im.putpalette(flat)
    im.save(os.path.join(HIER, f'mug_r4{naam}.png'), transparency=0)
    rgb(a, pal).resize((512, 512), Image.NEAREST).save(os.path.join(HIER, f'mug_r4{naam}_8x.png'))
    with open(os.path.join(HIER, f'mug_r4{naam}.txt'), 'w') as f:
        f.write('# r4%s, tekens = paletindex: %s\n' % (naam, CH))
        for row in a:
            f.write(''.join(CH[v] for v in row) + '\n')
    with open(os.path.join(HIER, f'normal_{naam}.pal'), 'w') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple(c) for c in pal))
    diff = int((a != R3A).sum())
    print(naam, 'alpha-diff', int(((a > 0) != (R3A > 0)).sum()), '| index-diff met r3', diff)


def rgb(a, pal, bg=(200, 225, 205)):
    p = np.array(pal).astype(np.uint8)
    out = p[a]
    out[a == 0] = bg
    return Image.fromarray(out, 'RGB')



PAL = {
    # A: r3-palet, k donker indigo-grijs (ook schaduw van de poten), poten l/i een stap lichter
    'A': [(0, 0, 0), (16, 16, 24), (48, 44, 66), (118, 118, 132), (164, 164, 176), (214, 214, 222),
          (86, 48, 102), (124, 76, 136), (168, 108, 182), (92, 92, 108), (80, 76, 114), (128, 124, 164),
          (168, 156, 56), (222, 212, 100), (150, 56, 196), (240, 172, 255)],
    # B: gespreider (donkerder schaduw, lichter hooglicht per groep)
    'B': [(0, 0, 0), (16, 16, 24), (46, 42, 66), (112, 112, 130), (162, 162, 178), (226, 226, 234),
          (76, 36, 94), (122, 68, 140), (182, 118, 198), (82, 82, 102), (84, 78, 122), (142, 136, 182),
          (176, 150, 36), (238, 222, 96), (150, 56, 196), (240, 172, 255)],
}


def vel():
    """Rij 1: r3 | r4A | r4B op 8x. Rij 2: arm/been-kruising (x22-40, y26-50) op 12x, r3 | A | B.
    Rij 3: r3 | A | B op 1x en 2x, op licht en op donker."""
    ims = [rgb(R3A, [tuple(c) for c in PAL3])]
    arrs = [R3A]
    for n in ('A', 'B'):
        a = np.array(Image.open(os.path.join(HIER, f'mug_r4{n}.png')))
        arrs.append(a)
        ims.append(rgb(a, PAL[n]))
    gap = 16
    rij1 = [im.resize((512, 512), Image.NEAREST) for im in ims]
    box = (22, 26, 41, 51)
    rij2 = [im.crop(box).resize(((box[2] - box[0]) * 12, (box[3] - box[1]) * 12), Image.NEAREST) for im in ims]
    rij3 = []
    for bg in ((200, 225, 205), (40, 44, 56)):
        for a, pal in zip(arrs, [[tuple(c) for c in PAL3], PAL['A'], PAL['B']]):
            rij3.append(rgb(a, pal, bg))
        for a, pal in zip(arrs, [[tuple(c) for c in PAL3], PAL['A'], PAL['B']]):
            rij3.append(rgb(a, pal, bg).resize((128, 128), Image.NEAREST))
    Wt = 3 * 512 + 2 * gap
    Ht = 512 + gap + rij2[0].height + gap + 128 + gap
    v = Image.new('RGB', (Wt, Ht), (255, 255, 255))
    for i, im in enumerate(rij1):
        v.paste(im, (i * (512 + gap), 0))
    y2 = 512 + gap
    for i, im in enumerate(rij2):
        v.paste(im, (i * (im.width + gap), y2))
    y3 = y2 + rij2[0].height + gap
    x = 0
    for im in rij3:
        v.paste(im, (x, y3 + (128 - im.height) // 2))
        x += im.width + 8
    v.save(os.path.join(HIER, 'vel.png'))


if __name__ == '__main__':
    main()
