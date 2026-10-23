"""Alpaca-lijn: modeltekeningen fase 2 en fase 3 (twee varianten) bij concept A.

Zelfde tekenaar en stijl als concepten.py (vlakke kleuren, donkere omlijning,
basisvormen, 256x256, 3/4 naar links). Draaien vanuit de repo-root:
    python3 docs/concept/ontwerp/alpaca/scripts/lijn.py
Maakt fase2.png, fase3_A.png, fase3_B.png en lijn.png in docs/concept/ontwerp/alpaca/.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from vorm import Drawing, ellipse, circle, bez, wool, curve, LINE  # noqa: E402
from concepten import concept_a, eye, font, DARK, REPO  # noqa: E402

CREAM = (255, 234, 166)
RED = (232, 44, 64)
CAR = (214, 124, 60)
FELT = (78, 52, 50)        # vilt: verharde kuifwol (bombín)
GOLD = (250, 182, 50)
IRIS = (120, 62, 40)


class Drawing(Drawing):
    """Zelfde tekenaar, met een verschuiving (fase 2/3 zijn hoger dan het vel)."""
    def __init__(self, dx=0, dy=0, **kw):
        super().__init__(**kw)
        self.dx, self.dy = dx, dy

    def _t(self, pts):
        return [(x + self.dx, y + self.dy) for x, y in pts]

    def _mask(self, polys, grow=0.0):
        return super()._mask([self._t(p) for p in polys], grow)

    def stroke(self, pts, *a, **kw):
        return super().stroke(self._t(pts), *a, **kw)

    def dot(self, x, y, r, col):
        return super().dot(x + self.dx, y + self.dy, r, col)


def hoof(d, name, x, y, rx=8, ry=5):
    d.part(name, [ellipse(x, y, rx, ry)], DARK, line=2)


def collar(d, name, x, y, rx, ry, col=RED, bumps=9, br=5.5, start=0):
    """Wolkraag om een poot: een platte ring van wolbolletjes."""
    d.part(name, wool(x, y, rx, ry, bumps, br, start=start), col)


def lama_head(d, hx, hy, k=1.0, kuif='wool', frown=0.0):
    """Lamakop, langer dan de alpacakop van fase 1. hx, hy = midden van de schedel.
    kuif: 'wool' (fase 2, verdichtende koepel) of None (fase 3: bombín apart)."""
    def P(x, y):
        return (hx + x * k, hy + y * k)
    # oren: lange gebogen bananenoren
    d.part('ear_f', [ellipse(*P(-26, -30), 6 * k, 21 * k, -22)], CAR)
    d.part('ear_n', [ellipse(*P(22, -36), 7.5 * k, 24 * k, 12)], CAR)
    d.part('ear_ni', [ellipse(*P(22, -33), 3.4 * k, 15 * k, 12)], DARK, line=0, clip='ear_n')
    d.part('face', [bez((P(-24, -12), P(-10, -24), P(26, -22), P(34, -8)),
                        (P(34, -8), P(40, 8), P(30, 26), P(12, 32)),
                        (P(12, 32), P(-6, 40), P(-36, 44), P(-50, 36)),
                        (P(-50, 36), P(-60, 28), P(-46, 2), P(-24, -12)))], CAR)
    d.part('muzzle', [ellipse(*P(-40, 32), 18 * k, 12 * k, -14)], CREAM)
    d.part('nose', [ellipse(*P(-49, 25), 5 * k, 3 * k, -10)], DARK, line=0)
    d.stroke(curve(P(-52, 34), P(-46, 39), P(-38, 38), P(-32, 33)), 1.7)
    # ogen: groot, laag, met een strakke bovenrand (vastberaden)
    eye(d, *P(10, 6), 7 * k, 9.5 * k, iris=IRIS, rot=8)
    eye(d, *P(-20, 6), 5.6 * k, 8.5 * k, iris=IRIS, rot=-8)
    d.stroke([P(1, -2 - frown), P(10, -6), P(20, -4)], 2.4 * k)
    d.stroke([P(-27, -3), P(-20, -5 - frown), P(-13, -3)], 2.2 * k)
    if kuif == 'wool':
        bang = bez((P(-30, -14), P(-16, -10), P(-10, -6), P(-4, 2)),
                   (P(-4, 2), P(4, -6), P(16, -12), P(34, -12)),
                   (P(34, -12), P(16, -24), P(-14, -24), P(-30, -14)))
        # de kuif verdicht al: grotere, gladdere bollen en een randje als een hoedrand
        d.part('kuif', wool(*P(0, -30), 34 * k, 20 * k, 9, 11 * k, start=10) + [bang], CREAM)
        d.stroke(curve(P(-28, -16), P(-10, -12), P(16, -14), P(34, -14)), 1.6)


# ---------------------------------------------------------------- fase 2
def fase2():
    """Lama: de vuisten gaan open en worden wolkragen om de voorpoten
    (boksbandages van wol). Langere hals en poten, kuif verdicht."""
    d = Drawing(dy=12)
    d.part('tail', wool(220, 104, 12, 12, 7, 5), CREAM)
    # verre poten
    d.part('leg_fh', [ellipse(206, 178, 8.5, 30)], CAR)
    hoof(d, 'hoof_fh', 206, 208)
    d.part('leg_ff', [ellipse(142, 182, 8, 30)], CAR)
    collar(d, 'col_ff', 142, 190, 13, 7, bumps=9, br=5)
    hoof(d, 'hoof_ff', 142, 212)
    # lijf: wol, slanker dan fase 1 (lama's hebben minder wol)
    d.part('body', wool(176, 132, 46, 28, 13, 9, start=8), CREAM)
    d.part('leg_nh', [ellipse(192, 184, 10, 30)], CAR)
    hoof(d, 'hoof_nh', 192, 214, 9.5, 6)
    # hals: rechtop, wol in een lange wolk
    d.part('neck', wool(118, 106, 20, 38, 11, 8, rot=-12, start=30), CREAM)
    # voorste voorpoot iets opgetild in dekking; de kraag zit om het onderbeen
    d.part('leg_nf', [ellipse(108, 176, 9.5, 30, 14)], CAR)
    collar(d, 'col_nf', 103, 186, 17, 9, bumps=11, br=6.5, start=10)
    d.stroke(curve((90, 186), (98, 192), (110, 192), (118, 186)), 1.6)
    hoof(d, 'hoof_nf', 98, 208, 9.5, 6)
    lama_head(d, 96, 62, k=1.0, kuif='wool', frown=2)
    return d


# ---------------------------------------------------------------- fase 3
def bombin(d, x, y, k=1.0, tilt=-10):
    """De kuif is verhard tot vilt: een kleine bolhoed bovenop de kop (zoals
    cholita's hem dragen, hoog en klein), de laatste wol krult als pony onder de rand uit (bangs)."""
    import math
    a = math.radians(tilt)

    def R(px, py):
        return (x + (px * math.cos(a) - py * math.sin(a)) * k,
                y + (px * math.sin(a) + py * math.cos(a)) * k)
    d.part('brim', [ellipse(*R(0, 0), 23 * k, 5.5 * k, tilt)], FELT)
    d.part('crown', [bez((R(-14, 1), R(-17, -30), R(17, -30), R(14, 1)))], FELT)
    d.part('shine', [ellipse(*R(-6, -14), 2.6 * k, 7 * k, tilt - 8)], (130, 92, 84), line=0, clip='crown')


def braid(d, name, pts, w, tassel):
    """Vlecht van oorwol: dicht op elkaar liggende schuine streng-ovalen (een
    vlechtpatroon) die naar onder smaller worden, met een wollen kwast (tullma)."""
    import math
    seq = []
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 7))
        for j in range(n):
            t = j / n
            seq.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t,
                        math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90))
    polys = []
    for i, (x, y, ang) in enumerate(seq):
        ww = w * (1 - 0.35 * i / len(seq))
        polys.append(ellipse(x, y, ww, ww * 0.75, ang + (28 if i % 2 else -28)))
    d.part(name, polys, CAR)
    for i, (x, y, ang) in enumerate(seq[1:], 1):
        ww = w * (1 - 0.35 * i / len(seq))
        sgn = 1 if i % 2 else -1
        d.stroke([(x - ww * 0.8, y - sgn * ww * 0.35), (x + ww * 0.8, y + sgn * ww * 0.35)], 1.3)
    tx, ty = pts[-1]
    d.part(name + '_t', wool(tx, ty + 7, 6.5, 8.5, 7, 3.8), tassel)


def bangs(d, x, y, k=1.0):
    """Het laatste stukje kuif dat onder de hoedrand uit krult (pony)."""
    d.part('bangs', [circle(x + (i - 2) * 7.5 * k, y + (2 if i in (1, 3) else 0) + (3 if i == 2 else 0), 5.2 * k)
                     for i in range(5)], CREAM)


def pollera(d, cx, cy, rx, tiers, k=1.0):
    """Heupwol in ruches (pollera): van boven naar onder steeds breder."""
    for i, (col, dy, grow) in reversed(list(enumerate(tiers))):
        d.part('tier%d' % i, wool(cx + grow * 0.2, cy + dy, rx + grow, 11 * k, 13 + i * 2, 6.5 * k, rot=-6), col)


def fase3a():
    """Variant A: blijft op vier poten. Bombín (verharde kuif), vlechten
    (oorwol), manta (halswol over de schouders), pollera (heupwol) en
    dubbele wolkragen om de voorpoten."""
    d = Drawing(dy=14)
    d.part('tail', wool(230, 98, 11, 12, 7, 5), CREAM)
    d.part('leg_fh', [ellipse(208, 190, 8.5, 34)], CAR)
    collar(d, 'col_fh', 208, 202, 11, 6, col=CREAM, bumps=8, br=4.5)
    hoof(d, 'hoof_fh', 208, 224)
    d.part('leg_ff', [ellipse(140, 192, 9, 34)], CAR)
    collar(d, 'col_ff', 140, 198, 15, 9, bumps=10, br=5.5)
    hoof(d, 'hoof_ff', 140, 226)
    d.part('body', wool(180, 124, 48, 28, 13, 9, start=8), CREAM)
    # pollera: rood met gouden zoom en een crème onderrok
    pollera(d, 186, 132, 40, [(RED, 0, 0), (GOLD, 13, 4), (CREAM, 24, 7)])
    d.part('leg_nh', [ellipse(194, 196, 10, 34)], CAR)
    collar(d, 'col_nh', 194, 210, 13, 7, col=CREAM, bumps=9, br=5)
    hoof(d, 'hoof_nh', 194, 230, 10, 6)
    # hals
    d.part('neck', wool(116, 98, 18, 40, 11, 7, rot=-10, start=30), CREAM)
    # manta: de halswol valt als een omslagdoek over de schouders, met een
    # rand van wolkwastjes (de franje)
    d.part('manta', wool(126, 128, 38, 25, 13, 6.5, rot=22, start=0), CREAM)
    zz = [(126 - 44 + i * 8, 128 + 6 + (6 if i % 2 else 0) + i * 1.2) for i in range(12)]
    d.part('manta_zz', [zz + [(p[0], p[1] + 7) for p in reversed(zz)]], RED, line=1.4, clip='manta')
    # voorste voorpoot met dubbele kraag
    d.part('leg_nf', [ellipse(108, 190, 10, 36, 6)], CAR)
    collar(d, 'col_nf', 106, 198, 20, 12, bumps=12, br=7, start=4)
    d.stroke(curve((90, 200), (98, 207), (112, 207), (122, 200)), 1.6)
    hoof(d, 'hoof_nf', 103, 228, 10, 6)
    # vlecht achter (verre oor) en voor (nabije oor)
    braid(d, 'braid_f', [(66, 64), (60, 80), (60, 96), (64, 112)], 5, RED)
    lama_head(d, 92, 56, k=1.0, kuif=None, frown=3)
    braid(d, 'braid_n', [(116, 48), (122, 66), (124, 84), (122, 102), (118, 118)], 5.6, RED)
    bangs(d, 90, 34)
    bombin(d, 96, 24, k=0.92, tilt=-8)
    return d


def fase3b():
    """Variant B: staat rechtop als luchadora (Incineroar-stap). Voorpoten
    worden armen met de kragen als polsbanden; de pollera is de heupwol."""
    d = Drawing(dy=12)
    d.part('tail', wool(184, 166, 10, 11, 7, 5), CREAM)
    # benen
    d.part('leg_f', [ellipse(152, 210, 10, 22, -6)], CAR)
    hoof(d, 'hoof_f', 156, 230, 10, 6)
    d.part('leg_n', [ellipse(118, 212, 11, 22, 8)], CAR)
    hoof(d, 'hoof_n', 112, 232, 11, 6.5)
    # lijf (rechtop) en pollera
    d.part('body', wool(136, 150, 32, 40, 12, 9, start=0), CREAM)
    pollera(d, 136, 176, 34, [(RED, 0, 0), (GOLD, 12, 5), (CREAM, 22, 9)])
    # verre arm: vuist in de zij
    d.part('arm_f', [ellipse(176, 136, 8, 24, -30)], CAR)
    collar(d, 'col_af', 184, 150, 12, 9, bumps=9, br=5)
    hoof(d, 'hoof_af', 188, 160, 7, 6)
    # manta
    d.part('manta', wool(132, 126, 38, 25, 13, 6.5, rot=14, start=0), CREAM)
    zz = [(132 - 44 + i * 8, 126 + 6 + (6 if i % 2 else 0) + i * 1.2) for i in range(12)]
    d.part('manta_zz', [zz + [(p[0], p[1] + 7) for p in reversed(zz)]], RED, line=1.4, clip='manta')
    # nabije arm: geheven in dekking, dubbele kraag
    d.part('arm_n', [ellipse(86, 130, 9, 26, 24)], CAR)
    collar(d, 'col_an2', 84, 128, 14, 9, bumps=10, br=5.5)
    collar(d, 'col_an', 78, 116, 15, 10, bumps=10, br=6)
    hoof(d, 'hoof_an', 74, 102, 8, 6.5)
    braid(d, 'braid_f', [(80, 62), (74, 78), (74, 94), (78, 108)], 5, RED)
    lama_head(d, 108, 54, k=0.95, kuif=None, frown=3)
    braid(d, 'braid_n', [(130, 46), (138, 64), (140, 82), (138, 100), (134, 116)], 5.6, RED)
    bangs(d, 106, 34, 0.95)
    bombin(d, 112, 24, k=0.88, tilt=-8)
    return d


def lijn_sheet(path, d1, d2, d3a, d3b):
    """Fase 1-3 op schaal op één grondlijn (fase 1 ±0,7 m, fase 2 ±1,2 m, fase 3 ±1,7 m)."""
    from PIL import Image, ImageDraw
    import numpy as np
    W, H = 1100, 470
    im = Image.new('RGB', (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.text((14, 10), 'Alpaca-lijn (concept A): fase 1-3 op schaal', fill=(40, 30, 40), font=font(20, True))
    ground = 380
    items = [('fase 1: alpaca (Wolvuist)', d1, 0.50, 'vuisten van wol'),
             ('fase 2: lama (Wolkraag)', d2, 0.80, 'vuisten openen tot kragen'),
             ('fase 3, variant A (vier poten)', d3a, 1.10, 'bombín, vlechten, manta, pollera'),
             ('fase 3, variant B (rechtop)', d3b, 1.10, 'idem, als luchadora op twee benen')]
    x = 20
    for lab, d, s, sub in items:
        img = d.result()
        sil = (np.asarray(d.sil.resize((256, 256))) > 100)
        ys = np.where(sil.any(1))[0]
        xs = np.where(sil.any(0))[0]
        crop = img.crop((xs[0] - 2, ys[0] - 2, xs[-1] + 3, ys[-1] + 3))
        w, h = int(crop.width * s), int(crop.height * s)
        crop = crop.resize((w, h), Image.LANCZOS)
        cw = max(w, 230)
        im.paste(crop, (x + (cw - w) // 2, ground - h))
        dr.text((x, ground + 16), lab, fill=(40, 30, 40), font=font(13, True))
        dr.text((x, ground + 34), sub, fill=(110, 100, 110), font=font(12))
        x += cw + 36
    dr.line([(14, ground + 2), (W - 14, ground + 2)], fill=(200, 200, 200), width=2)
    dr.text((14, 40), 'Kleurrollen: crème = wol, karamel = vacht, rood = de vechtwol (vuist > kraag > manta/pollera), '
            'donkerbruin = vilt (bombín) en hoeven, goud = zoom.', fill=(110, 100, 110), font=font(12))
    im.save(path)


def single(path, d, title, lines):
    from PIL import Image, ImageDraw
    W, H = 256 + 380, 280
    im = Image.new('RGB', (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    im.paste(d.result(), (0, 12))
    dr.text((268, 16), title, fill=(40, 30, 40), font=font(16, True))
    y = 46
    for ln in lines:
        dr.text((268, y), ln, fill=(40, 30, 40), font=font(12))
        y += 18
    im.save(path)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'docs/concept/ontwerp/alpaca')
    d1, d2, d3a, d3b = concept_a(), fase2(), fase3a(), fase3b()
    single(os.path.join(out, 'fase2.png'), d2, 'Fase 2: lama (Wolkraag)',
           ['De vuisten gaan open: de rode wol ligt nu als een', 'kraag om de onderbenen (bandages van wol).',
            'Langere hals en poten, voorpoot in dekking.', 'De kuif verdicht tot een koepel met een randje:',
            'het zaadje van de bombín.', 'Kleuren gelijk aan fase 1.'])
    single(os.path.join(out, 'fase3_A.png'), d3a, 'Fase 3, variant A: op vier poten',
           ['Bombín = verharde kuif (vilt), klein en hoog', 'zoals cholita\'s hem dragen, met een wolring.',
            'Vlechten = oorwol, met rode wolkwasten (tullma).', 'Manta = halswol over de schouders, met franje.',
            'Pollera = heupwol in ruches (rood, goud, crème).', 'Dubbele rode kragen om de voorpoten,',
            'crème kragen om de achterpoten.'])
    single(os.path.join(out, 'fase3_B.png'), d3b, 'Fase 3, variant B: rechtop',
           ['Zelfde onderdelen, maar staand als luchadora', '(de Incineroar-stap): voorpoten worden armen,',
            'de kragen polsbanden, de pollera een rok van wol.', 'Sterker als vechter, maar dichter bij',
            '\'dier in kostuum\'.'])
    lijn_sheet(os.path.join(out, 'lijn.png'), d1, d2, d3a, d3b)
    print('ok')
