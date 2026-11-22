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

# (x, y, van, naar, modelcel) - modelcel = wat het model (1024, op het spriteraster, tabel.py) in die cel toont:
# zwart% / helderheid van het niet-zwarte deel. Pootpalet: i ~130-140 (glans), l ~80, k ~45, # lijn.
WISSELS = [
    # BOVENARM borstarm (schouder -> elleboog geel 35,36-37): glans links zoals de onderarm, model x33/x34 licht
    (33, 28, 'l', 'i', '0/124'), (33, 29, 'l', 'i', '8/113'), (33, 30, 'l', 'i', '20/113'), (33, 31, 'l', 'i', '50/75*'),
    (34, 32, 'l', 'i', '0/123'), (34, 33, 'l', 'i', '4/127'), (34, 34, 'l', 'i', '22/117'), (34, 35, 'l', 'i', '17/99'),
    (35, 35, 'k', 'l', '0/82'),
    # ELLEBOOG -> ONDERARM: verbinding elleboog met de rechte poot is in het model vulling, geen lijn (r4 maakte er # van)
    (33, 36, '#', 'i', '16/104'), (33, 37, '#', 'l', '2/72'), (33, 38, '#', 'l', '34/70'),
    (34, 37, 'k', 'l', '1/69'), (34, 38, 'k', 'l', '2/72'), (35, 38, 'k', 'l', '0/67'),
    (34, 36, 'k', '#', '79/59'),            # lijn tussen bovenarm en onderarm (Jordi's bovenlijn)
    (32, 37, 'l', 'k', '71/71'),            # model hier grotendeels zwart; k i.p.v. # zodat de poot niet breekt
    # ONDERARM = rechte poot (Jordi's lus x30-33, y34-51): top x30 in glans, linkerrand lijn op x29
    (30, 35, 'i', 'i', '11/113'), (30, 36, 'i', 'i', '0/113'), (30, 37, 'l', 'i', '6/113'),
    (31, 37, 'i', 'l', '2/78'),
    (29, 36, 'i', '#', '76/102'),
    # onderkant: onderstuk knie-poot verdwijnt achter de rechte poot
    (31, 47, 'l', '#', '43/70'),
    # KNIE-POOT (achter): een stap donkerder dan de rechte poot, geen glans (i->l, l->k)
    (29, 37, 'i', 'l', '0/109'),
    (28, 38, 'i', 'l', '0/116'), (29, 38, 'l', 'k', '0/109'),
    (27, 39, 'i', 'l', '1/110'), (28, 39, 'l', 'k', '0/110'),
    (27, 40, 'i', 'l', '0/109'), (28, 40, 'l', 'k', '0/72'),
    (26, 41, 'i', 'l', '0/110'), (27, 41, 'l', 'k', '0/71'),
    (25, 42, 'i', 'l', '1/102'), (26, 42, 'l', 'k', '0/84'),
    (25, 43, 'i', 'l', '0/105'), (26, 43, 'l', 'k', '0/72'),
    (26, 45, 'i', 'l', '44/75'),
    (26, 46, 'l', 'k', '0/71'), (27, 46, 'i', 'l', '0/70'), (28, 46, 'i', 'l', '8/69'),
    (27, 47, 'l', 'k', '44/67'), (28, 47, 'l', 'k', '0/71'), (29, 47, 'l', 'k', '0/72'), (30, 47, 'l', 'k', '0/69'),
]
# (30,35) en (30,36) zijn in r4B al i: staan alleen in de lijst als modelcontrole, tellen niet als wissel.


def main():
    im = Image.open(R4B)
    a0 = np.array(im)
    pal = [tuple(im.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    a = a0.copy()
    regels = []
    for x, y, van, naar, mod in WISSELS:
        assert a0[y, x] == CHI[van], (x, y, CH[a0[y, x]], van)
        a[y, x] = CHI[naar]
        if van != naar:
            regels.append('(%d,%d) %s -> %s   model %s' % (x, y, van, naar, mod))
    with open(os.path.join(HIER, 'diff.txt'), 'w') as f:
        f.write('# r5 t.o.v. r4B, per pixel: oud -> nieuw, model zwart%/helderheid in die cel (* = cel deels buiten de poot)\n')
        f.write('\n'.join(regels) + '\n')
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
    Rij 3: r4B | r5 op 1x en 2x, op licht en donker. Rij 4: model op het spriteraster | r4B | r5."""
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
    # rij 4: model op het spriteraster | r4B | r5 (rasterzone.py)
    import rasterzone
    r = rasterzone.maak([R4B, os.path.join(HIER, 'mug_r5.png')], os.path.join(HIER, 'raster_model_r4B_r5.png'))
    r = r.resize((W, int(r.height * W / r.width)), Image.LANCZOS)
    v2 = Image.new('RGB', (W, H + gap + r.height), (255, 255, 255))
    v2.paste(v, (0, 0)); v2.paste(r, (0, H + gap))
    v2.save(os.path.join(HIER, 'vel.png'))


if __name__ == '__main__':
    main()
