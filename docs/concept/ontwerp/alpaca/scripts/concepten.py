"""Drie ontwerpconcepten voor de alpaca-lijn (fase 1 + silhouetschets fase 2/3).

Draaien vanuit de repo-root:
    python3 docs/concept/ontwerp/alpaca/scripts/concepten.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from vorm import Drawing, ellipse, circle, bez, wool, curve, LINE  # noqa: E402

DARK = (58, 38, 42)
WHITE = (255, 255, 255)


def eye(d, x, y, rx, ry, iris=None, rot=0):
    """Pokémon-oog: donkere ovaal, eventueel gekleurde iris onderin, één glans."""
    d.part('eye', [ellipse(x, y, rx, ry, rot)], DARK, line=0, sil=False)
    if iris:
        d.part('iris', [ellipse(x, y + ry * 0.45, rx * 0.8, ry * 0.5, rot)], iris,
               line=0, clip='eye', sil=False)
    d.dot(x - rx * 0.25, y - ry * 0.4, max(1.6, rx * 0.38), WHITE)


# ---------------------------------------------------------------- concept A
def concept_a():
    """Wolvuist: bokser. Wolbollen als vuisten, kuif als hoofdbeschermer."""
    CREAM = (255, 234, 166)
    RED = (232, 44, 64)
    CAR = (214, 124, 60)
    d = Drawing()
    # achterste delen
    d.part('tail', wool(212, 140, 14, 13, 7, 6), CREAM)
    d.part('leg_fh', [ellipse(200, 200, 11.5, 15)], CAR)
    d.part('toe_fh', [ellipse(200, 216, 9, 5)], DARK, line=2)
    d.part('leg_ff', [ellipse(146, 192, 10.5, 15)], CAR)
    d.part('wrist_f', wool(146, 200, 9, 8, 6, 5), RED)
    d.part('fist_f', wool(144, 216, 17, 14, 9, 6, start=10), RED)
    # lijf
    d.part('body', wool(168, 162, 44, 36, 13, 11, start=8), CREAM)
    d.part('leg_nh', [ellipse(184, 205, 13.5, 14)], CAR)
    d.part('toe_nh', [ellipse(182, 220, 11, 6)], DARK, line=2)
    # korte rechtopstaande hals met wolkraag
    d.part('neck', wool(114, 134, 22, 26, 10, 9, start=20), CREAM)
    d.part('leg_nf', [ellipse(104, 180, 11.5, 15)], CAR)
    # voorste vuist: wol groeit als een handschoen om de voorpoot
    d.part('wrist_n', wool(100, 194, 11, 9, 7, 6), RED)
    d.part('fist_n', wool(90, 208, 23, 18, 11, 7, start=5), RED)
    d.part('thumb_n', wool(108, 202, 9, 9, 6, 5), RED)
    d.stroke(curve((76, 206), (84, 213), (96, 212), (101, 204)), 2.2, LINE)
    # oren: lange alpacaspeertjes
    d.part('ear_f', [ellipse(60, 34, 6.5, 19, -16)], CAR)
    d.part('ear_n', [ellipse(118, 28, 7.5, 21, 14)], CAR)
    d.part('ear_ni', [ellipse(118, 31, 3.5, 13, 14)], DARK, line=0, clip='ear_n')
    # kop: korte vacht, korte ronde snuit
    d.part('face', [bez(((54, 82), (66, 70), (108, 68), (120, 82)),
                        ((120, 82), (128, 98), (122, 118), (104, 126)),
                        ((104, 126), (88, 134), (60, 136), (46, 126)),
                        ((46, 126), (38, 116), (44, 92), (54, 82)))], CAR)
    d.part('muzzle', [ellipse(60, 120, 19, 13, -10)], CREAM)
    d.part('nose', [ellipse(52, 113, 5, 3)], DARK, line=0)
    d.stroke(curve((46, 123), (50, 127), (55, 127), (58, 123)), 1.6)
    d.stroke(curve((58, 123), (60, 127), (66, 127), (69, 122)), 1.6)
    eye(d, 98, 98, 7.5, 10, iris=(120, 62, 40))
    eye(d, 68, 96, 6, 9, iris=(120, 62, 40))
    # kuif: dikke wolkoepel die als een hoofdbeschermer over het voorhoofd
    # valt; de V-punt zakt tussen de ogen en maakt de frons
    bang = bez(((50, 76), (66, 80), (76, 86), (84, 96)),
               ((84, 96), (92, 86), (108, 80), (126, 80)),
               ((126, 80), (110, 70), (66, 70), (50, 76)))
    d.part('kuif', wool(88, 54, 42, 28, 12, 10, start=5) + [bang], CREAM)
    return d


SIL = (78, 70, 88)       # silhouet
HAT = (26, 22, 30)       # bombín


def lama(d, big=False, kick=False, head=True):
    """Ruw lama-skelet voor de silhouetschetsen (fase 2 en 3)."""
    k = 1.18 if big else 1.0
    bx, by = 168, 128 if big else 132
    d.part('tail', [ellipse(bx + 50 * k, by - 10, 9, 13, 30)], SIL, line=0)
    d.part('lf', [ellipse(bx - 34 * k, by + 58, 8 * k, 36)], SIL, line=0)
    if kick:
        d.part('lk', [ellipse(bx + 60 * k, by + 34, 34, 8 * k, -28)], SIL, line=0)
    else:
        d.part('lh', [ellipse(bx + 34 * k, by + 58, 8 * k, 36)], SIL, line=0)
    d.part('lh2', [ellipse(bx + 22 * k, by + 60, 9 * k, 36)], SIL, line=0)
    d.part('lf2', [ellipse(bx - 22 * k, by + 60, 9 * k, 36)], SIL, line=0)
    d.part('body', [ellipse(bx, by, 48 * k, 28 * k)], SIL, line=0)
    hx, hy = (106, 50) if big else (110, 58)
    d.part('neck', [bez(((bx - 40, by + 10), (hx - 6, by - 20), (hx - 8, hy + 30), (hx - 4, hy + 6)),
                        ((hx - 4, hy + 6), (hx + 14, hy + 4), (hx + 24, hy + 10), (hx + 22, hy + 24)),
                        ((hx + 22, hy + 24), (hx + 22, by - 40), (bx - 10, by - 20), (bx - 10, by - 6)))],
           SIL, line=0)
    if head:
        d.part('head', [ellipse(hx - 2, hy + 2, 22 * k, 17 * k, -8),
                        ellipse(hx - 22, hy + 12, 14, 10, -12)], SIL, line=0)
        d.part('ears', [ellipse(hx - 12, hy - 22, 6, 17, -14),
                        ellipse(hx + 12, hy - 24, 6.5, 18, 16)], SIL, line=0)
    return hx, hy


def bombin(d, hx, hy, w=30):
    d.part('hat', [ellipse(hx, hy - 10, w + 6, 5),
                   bez(((hx - w * 0.62, hy - 10), (hx - w * 0.7, hy - 46),
                        (hx + w * 0.7, hy - 46), (hx + w * 0.62, hy - 10)))], HAT, line=0)


def braid(d, hx, hy, col=SIL):
    d.part('braid', [ellipse(hx + 26, hy + 22, 5, 22, -10), ellipse(hx + 30, hy + 48, 4, 6),
                     ellipse(hx - 20, hy + 20, 4, 18, 10)], col, line=0)


def concept_a_evo():
    RED = (228, 52, 72)
    CREAM = (220, 204, 168)
    d2 = Drawing()
    hx, hy = lama(d2)
    d2.part('kuif', wool(hx - 4, hy - 4, 22, 13, 9, 6), CREAM, line=0)
    d2.part('f1', wool(140, 222, 15, 13, 8, 5), RED, line=0)
    d2.part('f2', wool(122, 204, 20, 18, 9, 6), RED, line=0)
    d3 = Drawing()
    hx, hy = lama(d3, big=True)
    d3.part('poll', wool(184, 152, 52, 20, 14, 9), (150, 60, 72), line=0)
    braid(d3, hx, hy)
    bombin(d3, hx - 4, hy - 8)
    d3.part('f1', wool(146, 222, 19, 16, 9, 6), RED, line=0)
    d3.part('f2', wool(112, 196, 30, 26, 12, 8), RED, line=0)
    return d2, d3


def concept_b_evo():
    CREAM = (230, 214, 182)
    d2 = Drawing()
    hx, hy = lama(d2)
    # de kraag groeit in ringen langs de langere hals
    d2.part('r1', wool(126, 124, 30, 18, 12, 7), CREAM, line=0)
    d2.part('r2', wool(116, 98, 22, 13, 10, 6), CREAM, line=0)
    d3 = Drawing()
    hx, hy = lama(d3, big=True)
    # kraag wordt een manta (omslagdoek) van wol over schouders en borst
    d3.part('manta', [bez(((80, 96), (110, 84), (150, 96), (178, 118)),
                          ((178, 118), (170, 150), (140, 176), (104, 178)),
                          ((104, 178), (84, 160), (76, 130), (80, 96)))] +
            [circle(90 + i * 13, 176 - abs(i - 2) * 3, 8) for i in range(5)], CREAM, line=0)
    braid(d3, hx, hy)
    bombin(d3, hx - 4, hy - 8)
    return d2, d3


def concept_c_evo():
    RED = (234, 76, 72)
    GOLD = (250, 176, 52)
    d2 = Drawing()
    hx, hy = lama(d2, kick=True)
    d2.part('t2', wool(178, 166, 46, 12, 15, 7), GOLD, line=0)
    d2.part('t1', wool(176, 150, 40, 12, 13, 7), RED, line=0)
    d3 = Drawing()
    hx, hy = lama(d3, big=True, kick=True)
    d3.part('t3', wool(176, 182, 62, 13, 18, 8), GOLD, line=0)
    d3.part('t2', wool(174, 164, 56, 13, 16, 8), RED, line=0)
    d3.part('t1', wool(172, 146, 50, 13, 14, 8), (190, 70, 130), line=0)
    braid(d3, hx, hy)
    bombin(d3, hx - 4, hy - 8)
    return d2, d3


# ---------------------------------------------------------------- concept B
def concept_b():
    """Nekkraag: nekworstelaar. Lama's en alpaca's vechten echt met hun nek
    (nekworstelen). De wol rond de hals groeit uit tot een dikke kraag
    die als de nek- en schouderspieren van een worstelaar ligt."""
    RUST = (214, 88, 44)
    WOOL = (255, 242, 206)
    CHOC = (96, 58, 46)
    GOLD = (240, 168, 32)
    d = Drawing()
    d.part('tail', wool(208, 136, 12, 12, 7, 5), WOOL)
    d.part('leg_fh', [ellipse(196, 196, 11, 17)], CHOC)
    d.part('toe_fh', [ellipse(196, 213, 9, 5)], DARK, line=2)
    d.part('leg_ff', [ellipse(140, 200, 11, 17, 10)], CHOC)
    d.part('toe_ff', [ellipse(137, 217, 9, 5)], DARK, line=2)
    d.part('body', wool(172, 162, 36, 28, 11, 9, start=8), RUST)
    d.part('leg_nh', [ellipse(184, 202, 12.5, 16)], CHOC)
    d.part('toe_nh', [ellipse(183, 218, 11, 6)], DARK, line=2)
    d.part('leg_nf', [ellipse(88, 198, 12.5, 18, 18)], CHOC)
    d.part('toe_nf', [ellipse(82, 216, 11, 6)], DARK, line=2)
    # de kraag: een dikke wolring om de hals, breder dan de kop, die tot
    # tegen de kaken opbolt (geen nek, wel nekspieren)
    d.part('ruff_b', wool(148, 124, 28, 28, 10, 10, start=0), WOOL)
    d.part('ruff', wool(100, 150, 50, 32, 16, 11, start=0) +
           [circle(134, 114, 18), circle(60, 126, 15)], WOOL)
    d.stroke(curve((80, 168), (94, 176), (112, 176), (126, 166)), 2.0)
    d.part('ear_f', [ellipse(58, 36, 6, 17, -24)], RUST)
    d.part('ear_n', [ellipse(110, 30, 7, 19, 22)], RUST)
    d.part('ear_ni', [ellipse(110, 33, 3.2, 12, 22)], CHOC, line=0, clip='ear_n')
    d.part('face', [bez(((52, 80), (62, 64), (104, 62), (116, 78)),
                        ((116, 78), (124, 96), (118, 114), (102, 120)),
                        ((102, 120), (86, 128), (58, 130), (44, 120)),
                        ((44, 120), (36, 110), (42, 90), (52, 80)))], RUST)
    d.part('muzzle', [ellipse(58, 114, 19, 13, -10)], WOOL)
    d.part('nose', [ellipse(50, 107, 5, 3)], CHOC, line=0)
    d.stroke(curve((44, 118), (50, 123), (58, 123), (64, 117)), 1.8)
    eye(d, 95, 94, 7, 9.5, iris=GOLD)
    eye(d, 66, 92, 5.6, 8.5, iris=GOLD)
    d.part('brow_n', [ellipse(96, 80, 9, 3, -16)], CHOC, line=0)
    d.part('brow_f', [ellipse(66, 79, 7, 3, 18)], CHOC, line=0)
    d.part('kuif', wool(84, 58, 24, 14, 9, 7, start=0), WOOL)
    return d


# ---------------------------------------------------------------- concept C
def concept_c():
    """Polleratrap: trapper. Alpaca's trappen echt naar achteren als ze boos
    zijn. De wol rond de heupen groeit in gekleurde lagen uit (de pollera
    van de cholita, als vacht); de kracht zit in de achterpoten."""
    TAN = (240, 188, 112)
    RED = (236, 64, 64)
    GOLD = (250, 176, 52)
    BRN = (110, 66, 48)
    CREAM = (255, 246, 226)
    d = Drawing()
    # achterpoot trapt naar achteren (onder de lagen vandaan)
    d.part('leg_kick', [ellipse(214, 176, 26, 8.5, -24)], BRN)
    d.part('hoof', [ellipse(238, 164, 6, 11, -24)], DARK, line=2)
    d.part('leg_ff', [ellipse(140, 196, 10.5, 17, 8)], BRN)
    d.part('toe_ff', [ellipse(138, 214, 9, 5)], DARK, line=2)
    d.part('leg_fh', [ellipse(172, 206, 11.5, 14)], BRN)
    d.part('toe_fh', [ellipse(172, 220, 10, 5)], DARK, line=2)
    d.part('body', wool(150, 150, 34, 26, 10, 9, start=10), TAN)
    # pollera: drie ruches van wol, steeds breder
    d.part('tier3', wool(176, 184, 42, 12, 15, 7, rot=-4), GOLD)
    d.part('tier2', wool(174, 170, 38, 12, 13, 7, rot=-4), RED)
    d.part('tier1', wool(172, 156, 32, 13, 11, 7, rot=-4), TAN)
    d.part('leg_nf', [ellipse(112, 192, 11.5, 17, -8)], BRN)
    d.part('toe_nf', [ellipse(110, 210, 10, 5)], DARK, line=2)
    d.part('chest', wool(118, 140, 22, 24, 9, 8, start=20), CREAM)
    d.part('ear_f', [ellipse(62, 34, 6.5, 19, -18)], TAN)
    d.part('ear_n', [ellipse(118, 30, 7.5, 21, 14)], TAN)
    d.part('ear_ni', [ellipse(118, 33, 3.5, 13, 14)], RED, line=0, clip='ear_n')
    d.part('face', [bez(((54, 82), (66, 70), (108, 68), (120, 82)),
                        ((120, 82), (128, 98), (122, 118), (104, 126)),
                        ((104, 126), (88, 134), (60, 136), (46, 126)),
                        ((46, 126), (38, 116), (44, 92), (54, 82)))], TAN)
    d.part('muzzle', [ellipse(60, 120, 19, 13, -10)], CREAM)
    d.part('nose', [ellipse(52, 113, 5, 3)], BRN, line=0)
    # zelfverzekerde scheve grijns
    d.stroke(curve((48, 124), (56, 129), (64, 128), (72, 120)), 1.8)
    eye(d, 98, 98, 7, 9.5, iris=BRN)
    # verre oog dicht: knipoog, uitdagend
    d.stroke(curve((60, 98), (64, 102), (70, 102), (74, 97)), 2.4)
    d.part('kuif', wool(88, 64, 26, 18, 9, 8, start=0), CREAM)
    return d


TEXT = {
    'A': ('Concept A: Wolvuist (boksen)',
          ['Idee: de wol aan de voorpoten groeit als twee rode bokshandschoenen;',
           'de kuif valt als een hoofdbeschermer over het voorhoofd, met de V als frons.',
           'Type uit het lijf: vuisten en hoofdbeschermer zijn wol, geen kleding.',
           'Lijn: vuisten groeien mee; in fase 3 verhardt de kuif tot de bombín,',
           'de oorwol hangt als vlechten en de heupwol wordt een pollera.']),
    'B': ('Concept B: Nekkraag (nekworstelen)',
          ['Idee: lama\'s en alpaca\'s vechten echt met hun nek. De halswol groeit',
           'uit tot een dikke kraag die als de nek- en schouderspieren van een',
           'worstelaar ligt; strenge wenkbrauwen, brede stand. Alleen vacht.',
           'Lijn: de kraag groeit in ringen langs de hals; in fase 3 wordt hij',
           'de manta (omslagdoek) van de cholita, met bombín-kuif en vlechten.']),
    'C': ('Concept C: Polleratrap (trappen)',
          ['Idee: alpaca\'s trappen naar achteren als ze boos zijn. De wol rond',
           'de heupen groeit in gekleurde ruches (de pollera van de cholita als',
           'vacht); de kracht zit in de achterpoten. Knipoog: uitdagend.',
           'Lijn: elke fase een laag erbij; fase 3 trapt met een volle pollera',
           'en draagt de bombín als verharde kuif.']),
}


def font(sz, bold=False):
    from PIL import ImageFont
    name = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/' + name, sz)


def concept_sheet(key, d1, d2, d3, path):
    from PIL import Image, ImageDraw
    title, lines = TEXT[key]
    W, H = 768, 256 + 40 + 24 + 18 * len(lines) + 16
    im = Image.new('RGB', (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.text((12, 10), title, fill=(40, 30, 40), font=font(18, True))
    y = 40
    im.paste(d1.result(), (0, y))
    im.paste(d2.result(), (256, y))
    im.paste(d3.result(), (512, y))
    for i, lab in enumerate(['fase 1 (modeltekening)', 'fase 2 (silhouetschets)',
                             'fase 3 (silhouetschets)']):
        dr.text((i * 256 + 12, y + 256), lab, fill=(110, 100, 110), font=font(12))
    dr.line([(256, y), (256, y + 256)], fill=(225, 225, 225))
    dr.line([(512, y), (512, y + 256)], fill=(225, 225, 225))
    ty = y + 256 + 24
    for ln in lines:
        dr.text((12, ty), ln, fill=(40, 30, 40), font=font(13))
        ty += 18
    im.save(path)


def to_sprite(d, area=900):
    """Verklein naar 64x64 zodat het silhouetoppervlak ~area px is."""
    from PIL import Image
    import numpy as np
    sil = d.sil
    a_full = (np.asarray(sil) > 127).sum()
    scale = (area / a_full) ** 0.5           # lineaire factor t.o.v. 1024
    bbox = sil.getbbox()
    crop_img = d.img.crop(bbox)
    crop_sil = sil.crop(bbox)
    w = max(1, round(crop_img.width * scale))
    h = max(1, round(crop_img.height * scale))
    small = crop_img.resize((w, h), Image.LANCZOS)
    smask = crop_sil.resize((w, h), Image.LANCZOS).point(lambda v: 255 if v > 110 else 0)
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    ox, oy = (64 - w) // 2, 64 - h - 4
    out.paste(small.convert('RGBA'), (ox, oy), smask)
    return out


def real_sprite(name):
    from PIL import Image
    b = os.path.join(REPO, 'graphics/pokemon', name)
    f = os.path.join(b, 'anim_front_gba.png')
    if not os.path.exists(f):
        f = os.path.join(b, 'anim_front.png')
    im = Image.open(f)
    pal = im.getpalette()
    im = im.crop((0, 0, 64, 64))
    rgba = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    px = im.load()
    for y in range(64):
        for x in range(64):
            i = px[x, y]
            if i:
                rgba.putpixel((x, y), tuple(pal[i * 3:i * 3 + 3]) + (255,))
    return rgba


def silhouette(img):
    from PIL import Image
    a = img.split()[3].point(lambda v: 255 if v > 0 else 0)
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.paste((30, 30, 40, 255), mask=a)
    return out


def comparison(drawings, path):
    from PIL import Image, ImageDraw
    import numpy as np
    refs = ['torchic', 'mudkip', 'treecko', 'mareep', 'growlithe', 'chimchar']
    items = [(n.capitalize() + ('*' if n == 'chimchar' else ''), real_sprite(n)) for n in refs]
    items += [('Concept ' + k, to_sprite(d)) for k, d in drawings]
    n = len(items)
    cw = 136
    W = 16 + n * cw
    H = 560
    im = Image.new('RGB', (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.text((16, 10), 'Alpaca-concepten naast echte Gen 3-starters (2x, 1x kleur, 1x silhouet)',
            fill=(40, 30, 40), font=font(16, True))
    dr.text((16, 32), 'Concepten zijn verkleinde tekeningen (geen sprite), geschaald tot een '
            'oppervlak van ~900 px op 64x64. * Chimchar = DS-sprite (geen Gen 3).',
            fill=(110, 100, 110), font=font(12))
    for i, (lab, spr) in enumerate(items):
        x = 16 + i * cw
        if i == 6:
            dr.line([(x - 6, 56), (x - 6, H - 10)], fill=(200, 80, 80), width=2)
        big = spr.resize((128, 128), Image.NEAREST)
        im.paste(big, (x, 64), big)
        area = int((np.asarray(spr.split()[3]) > 0).sum())
        dr.text((x, 196), lab, fill=(40, 30, 40), font=font(13, True))
        dr.text((x, 214), str(area) + ' px', fill=(110, 100, 110), font=font(12))
        im.paste(spr, (x + 32, 250), spr)
        sil = silhouette(spr)
        im.paste(sil, (x + 32, 330), sil)
        # 1x op een gevechtsachtergrond-achtige grijsgroene grond
        bg = Image.new('RGB', (64, 64), (200, 216, 176))
        bg.paste(spr, (0, 0), spr)
        im.paste(bg, (x + 32, 410))
    dr.text((16, 236), '1x', fill=(110, 100, 110), font=font(12))
    dr.text((16, 316), '1x silhouet', fill=(110, 100, 110), font=font(12))
    dr.text((16, 396), '1x op gras', fill=(110, 100, 110), font=font(12))
    dr.text((16, 490), 'Gemiddeld oppervlak fase-1-starters Gen 3: ~808 px (Treecko 967). '
            'Concepten bewust op ~900 geschaald;', fill=(110, 100, 110), font=font(12))
    dr.text((16, 506), 'de echte sprite wordt per pixel getekend op een Gen 3-skelet '
            '(Mareep + Growlithe), niet verkleind.', fill=(110, 100, 110), font=font(12))
    im.save(path)


REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'docs/concept/ontwerp/alpaca')
    a, b, c = concept_a(), concept_b(), concept_c()
    concept_sheet('A', a, *concept_a_evo(), os.path.join(out, 'concept_A.png'))
    concept_sheet('B', b, *concept_b_evo(), os.path.join(out, 'concept_B.png'))
    concept_sheet('C', c, *concept_c_evo(), os.path.join(out, 'concept_C.png'))
    comparison([('A', a), ('B', b), ('C', c)], os.path.join(out, 'vergelijking.png'))
