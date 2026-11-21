#!/usr/bin/env python3
"""Mug r5 = r4B + scheiding rechte poot (voor) / knie-poot (achter) binnen de Lambda-driehoek.
Alleen kleur/schaduw/belijning; alpha-diff 0 met r4B (assert). Jordi over r4: "arm en poot lijken nog steeds
verbonden hier, op alle 3" (krabbel sprite_r4/krabbel_jordi_r4.png).
Indexen: 0=. 1=# 2=k 3=d 4=g 5=w 6=P 7=p 8=q 9=L 10=l 11=i 12=Y 13=y 14=E 15=e
"""
import os
import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = os.path.dirname(HIER)
R4B = os.path.join(BASIS, 'sprite_r4', 'mug_r4B.png')
NATIEF = os.path.join(BASIS, 'maat', 'natief.png')
CH = '.#kdgwPpqLliYyEe'
CHI = {c: i for i, c in enumerate(CH)}

# (x, y, van, naar)
WISSELS = [
    # LIJN boven: zwarte lijn tussen schuine knie-poot en rechte poot tot het borststuk
    # (vulpixels van de achterste knie-poot), verlengt de lijn x30 (y38-44) omhoog
    (30, 35, 'i', '#'), (30, 36, 'i', '#'), (30, 37, 'l', '#'),
    # LIJN onder: onderstuk van de knie-poot verdwijnt achter de rechte poot
    (31, 47, 'l', '#'),
    # RECHTE POOT (voor): glans x31 tot de top, onderkant x32 in glans
    (31, 35, 'l', 'i'),
    (32, 45, 'l', 'i'), (32, 46, 'l', 'i'), (32, 47, 'l', 'i'), (32, 48, 'l', 'i'), (32, 49, 'l', 'i'),
    # lange onderpoot = vervolg van de rechte poot (voor): glans links waar 2 breed
    (34, 49, 'l', 'i'), (35, 49, 'k', 'l'), (34, 50, 'l', 'i'), (35, 50, 'k', 'l'),
    (34, 51, 'l', 'i'), (35, 51, 'k', 'l'), (35, 53, 'l', 'i'), (36, 56, 'l', 'i'),
    # KNIE-POOT (achter): hele lengte een stap donkerder, geen glans (i->l, l->k)
    (29, 36, 'i', 'l'), (29, 37, 'i', 'l'),
    (28, 38, 'i', 'l'), (29, 38, 'l', 'k'),
    (27, 39, 'i', 'l'), (28, 39, 'l', 'k'),
    (27, 40, 'i', 'l'), (28, 40, 'l', 'k'),
    (26, 41, 'i', 'l'), (27, 41, 'l', 'k'),
    (25, 42, 'i', 'l'), (26, 42, 'l', 'k'),
    (25, 43, 'i', 'l'), (26, 43, 'l', 'k'),
    (26, 45, 'i', 'l'),
    (26, 46, 'l', 'k'), (27, 46, 'i', 'l'), (28, 46, 'i', 'l'),
    (27, 47, 'l', 'k'), (28, 47, 'l', 'k'), (29, 47, 'l', 'k'), (30, 47, 'l', 'k'),
]


def main():
    im = Image.open(R4B)
    a0 = np.array(im)
    pal = [tuple(im.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    a = a0.copy()
    for x, y, van, naar in WISSELS:
        assert a0[y, x] == CHI[van], (x, y, CH[a0[y, x]], van)
        a[y, x] = CHI[naar]
    assert ((a > 0) == (a0 > 0)).all()
    print('alpha-diff met r4B:', int(((a > 0) != (a0 > 0)).sum()), '| gewisseld:', int((a != a0).sum()), 'px')
    out = Image.fromarray(a.astype(np.uint8), 'P')
    out.putpalette([c for rgb in pal for c in rgb])
    out.save(os.path.join(HIER, 'mug_r5.png'), transparency=0)
    rgb(a, pal).resize((512, 512), Image.NEAREST).save(os.path.join(HIER, 'mug_r5_8x.png'))
    with open(os.path.join(HIER, 'mug_r5.txt'), 'w') as f:
        f.write('# r5, tekens = paletindex: %s\n' % CH)
        for row in a:
            f.write(''.join(CH[v] for v in row) + '\n')
    with open(os.path.join(HIER, 'normal.pal'), 'w') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in pal))
    vel(a0, a, pal)


def rgb(a, pal, bg=(200, 225, 205)):
    p = np.array(pal).astype(np.uint8)
    out = p[a]
    out[a == 0] = bg
    return Image.fromarray(out, 'RGB')


def model64():
    nat = Image.open(NATIEF).convert('RGB')
    na = np.array(nat).astype(int)
    m = np.abs(na - 254).sum(2) > 30
    ys, xs = np.where(m)
    box = nat.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)).resize((56, 63), Image.BOX)
    mod = Image.new('RGB', (64, 64), (254, 254, 254))
    mod.paste(box, (4, 1))
    return mod, nat, (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)


def vel(a0, a, pal):
    """Rij 1: r4B | r5 | model op 8x. Rij 2: driehoek-zone (x22-38, y33-50) op 16x: r4B | r5 | model (natief).
    Rij 3: r4B | r5 op 1x en 2x, op licht en donker."""
    mod, nat, nb = model64()
    gap = 16
    rij1 = [rgb(a0, pal).resize((512, 512), Image.NEAREST), rgb(a, pal).resize((512, 512), Image.NEAREST),
            mod.resize((512, 512), Image.NEAREST)]
    box = (22, 33, 39, 51)
    zw, zh = (box[2] - box[0]) * 16, (box[3] - box[1]) * 16
    sx = (nb[2] - nb[0]) / 56
    sy = (nb[3] - nb[1]) / 63
    nbox = (nb[0] + (box[0] - 4) * sx, nb[1] + (box[1] - 1) * sy, nb[0] + (box[2] - 4) * sx, nb[1] + (box[3] - 1) * sy)
    rij2 = [rgb(a0, pal).crop(box).resize((zw, zh), Image.NEAREST), rgb(a, pal).crop(box).resize((zw, zh), Image.NEAREST),
            nat.crop(tuple(int(round(v)) for v in nbox)).resize((zw, zh), Image.NEAREST)]
    rij3 = []
    for bg in ((200, 225, 205), (40, 44, 56)):
        for arr in (a0, a):
            rij3.append(rgb(arr, pal, bg))
        for arr in (a0, a):
            rij3.append(rgb(arr, pal, bg).resize((128, 128), Image.NEAREST))
    W = 3 * 512 + 2 * gap
    H = 512 + gap + zh + gap + 128
    v = Image.new('RGB', (W, H), (255, 255, 255))
    for i, im in enumerate(rij1):
        v.paste(im, (i * (512 + gap), 0))
    for i, im in enumerate(rij2):
        v.paste(im, (i * (zw + gap), 512 + gap))
    x = 0
    y3 = 512 + gap + zh + gap
    for im in rij3:
        v.paste(im, (x, y3 + (128 - im.height) // 2))
        x += im.width + 8
    v.save(os.path.join(HIER, 'vel.png'))


if __name__ == '__main__':
    main()
