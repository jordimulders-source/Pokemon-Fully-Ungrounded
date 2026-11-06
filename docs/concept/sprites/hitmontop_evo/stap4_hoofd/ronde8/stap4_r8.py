"""Stap 4 hoofd, ronde 8 (6 nov). Bron: Hitmontops OVERWORLD-sprite (frame 1): de kop staat daar rechtop en van voren,
zoals referenties/hitmontop_3d.webp (koepel, stekel bovenop, flappen opzij, V boven de ogen).
 1 uitsnede (regel van stap3b KOP_OW), OW-palet -> frontpalet, buitenrand zwart
 2 groter met de hand: kolommen 7, 9, 15, 21, 23 en rijen 13-15 verdubbeld (vlakke delen) -> 24 px breed
 3 glad + frontsprite-gezicht: de trapjes van het verdubbelen eruit (koepelomtrek per rij hieronder), ogen = Hitmontops
   frontsprite-oog 1:1 (zwart rondje, wit puntje linksboven), mond = zijn streepje; licht linksboven, sikkel rechtsonder
 4 Jordi: V naar achteren (flappen niet meer opzij, naar achteren gekamd; voorhoofd vrij)
 5 knot = Hitmontops linkerhand (anim_front x9-16, y28-35) 1:1, achter de kop; zijn polsband tussen knot en kop
 6 stekel kleiner: Jordi "zorg ervoor dat het wel een stekel wordt en niet een ingedeukt weetikveelwat" -> zelfde
   rechte kegel met spitse tip (1-3-3-5-5), alleen korter dan de grote (1-3-3-3-5-5-7)
 7 12 graden tegen de klok in: omtrek, licht, ogen, mond, V en knot opnieuw op de gedraaide vorm gelegd (geen
   gedraaide pixels, dus geen trapjes of rafels): ogen en hand 1:1, V en mond als rechte lijnstukken.
Varianten: 1 = knot achter op de kruin (linksboven achter de koepel), 2 = knot achterop/opzij (laag, achter de wang).
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde8/stap4_r8.py"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from hulp import *
from ow import stap1, dubbel
from PIL import Image, ImageDraw

OX, OY = 22, 12                      # plek van het raster in het 64-vak
CX, CY = 10.5, 10.0                  # midden van de koepel (draaipunt, lichtberekening)
HOEK = 12
OOG = [".ff.", "f1ff", "ffff", ".ff."]       # Hitmontops frontsprite-oog, pixel voor pixel
KOEPEL = {1: (5, 16), 2: (3, 18), 3: (2, 19), 4: (1, 20), 5: (0, 21), 6: (0, 21), 7: (0, 21), 8: (0, 21), 9: (0, 21),
          10: (0, 21), 11: (0, 21), 12: (0, 21), 13: (0, 21), 14: (0, 21), 15: (1, 20), 16: (1, 20), 17: (2, 19),
          18: (3, 18), 19: (5, 16)}
STEKEL_GROOT = {-6: (10, 10), -5: (9, 11), -4: (9, 11), -3: (9, 11), -2: (8, 12), -1: (8, 12), 0: (7, 13)}
STEKEL_KLEIN = {-4: (10, 10), -3: (9, 11), -2: (9, 11), -1: (8, 12), 0: (8, 12)}
FLAPPEN = {y: [(-2, -1), (22, 23)] for y in range(6, 15)}              # Hitmontops flappen opzij (stap 3)
# V-lijn: binnen de kop, donkerste huidtint (5), uiteinden 4; vervormt de omtrek niet (Jordi: "bovenkant smooth")
V_OUD = [((3, 7), 4), ((4, 7), 5), ((5, 8), 5), ((6, 8), 5), ((7, 8), 5), ((8, 9), 5), ((9, 9), 5), ((10, 10), 5),
         ((11, 10), 5), ((12, 9), 5), ((13, 9), 5), ((14, 8), 5), ((15, 8), 5), ((16, 8), 5), ((17, 7), 5), ((18, 7), 4)]
V_NIEUW = [((4, 3), 4), ((5, 4), 5), ((6, 4), 5), ((7, 5), 5), ((8, 5), 5), ((9, 6), 5), ((10, 7), 5), ((11, 7), 5),
           ((12, 6), 5), ((13, 5), 5), ((14, 5), 5), ((15, 4), 5), ((16, 4), 5), ((17, 3), 4)]
MOND = ((8, 15), (13, 15))
OGEN = ((5, 10), (13, 10))
SRCD = top_idx()
HAND = {(x - 9, y - 28): SRCD[(x, y)] for x in range(9, 17) for y in range(28, 36) if (x, y) in SRCD
        and not (x == 16 and y in (28, 29))}
BAND = ['c11c', 'dccd']
KNOT = {1: ((-4, -4), (2, -1)),      # (linksboven van de hand, linksboven van de staande band 2x4) in rechtop-coordinaten
        2: ((-6, 11), (-1, 12))}
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def T(x, y, hoek):
    a = math.radians(hoek); dx, dy = x - CX, y - CY
    return CX + dx * math.cos(a) + dy * math.sin(a), CY - dx * math.sin(a) + dy * math.cos(a)


def masker(stekel, flappen=False):
    rij = dict(KOEPEL); rij.update(stekel); m = set()
    for y, (a, b) in rij.items():
        for x in range(a, b + 1): m.add((x, y))
    if flappen:
        for y, segs in FLAPPEN.items():
            for a, b in segs:
                for x in range(a, b + 1): m.add((x, y))
    return m


def draai_masker(m, hoek):
    if not hoek: return set(m)
    out = set()
    for y in range(-12, 32):
        for x in range(-12, 34):
            ux, uy = T(x + 0.5, y + 0.5, -hoek)
            if (math.floor(ux), math.floor(uy)) in m: out.add((x, y))
    for _ in range(2):   # bultjes/gaatjes van 1 px weg
        for p in [p for p in out if sum((p[0] + a, p[1] + b) in out for a, b in N4) <= 1]: out.discard(p)
        for y in range(-12, 32):
            for x in range(-12, 34):
                if (x, y) not in out and sum((x + a, y + b) in out for a, b in N4) >= 3: out.add((x, y))
    return out


def kleur(m, stekel_m):
    """omlijning zwart; licht linksboven en schaduw rechtsonder als sikkel langs de omtrek (richting t.o.v. het midden)."""
    d = {p: 3 for p in m}
    rand = {p for p in m if any((p[0] + a, p[1] + b) not in m for a, b in N4)}
    for p in rand: d[p] = 15
    L = (-1 / math.sqrt(2), -1 / math.sqrt(2))
    def dot(p):
        dx, dy = p[0] + 0.5 - CX, p[1] + 0.5 - CY - 2; n = math.hypot(dx, dy) or 1
        return (dx * L[0] + dy * L[1]) / n
    laag1 = {p for p in m if p not in rand and any((p[0] + a, p[1] + b) in rand for a, b in N4 + ((1, 1), (-1, -1)))}
    laag2 = {p for p in m if p not in rand and p not in laag1 and any((p[0] + a, p[1] + b) in laag1 for a, b in N4)}
    for p in laag1:
        if p in stekel_m: continue
        k = dot(p)
        if k > 0.55: d[p] = 2
        elif k < -0.2: d[p] = 4
        if k < -0.8: d[p] = 5
    for p in laag2:
        if p not in stekel_m and dot(p) < -0.6: d[p] = 4
    return d


def lijn(a, b):
    (x0, y0), (x1, y1) = a, b; pts = []; n = max(abs(x1 - x0), abs(y1 - y0)) or 1
    for i in range(n + 1):
        pts.append((round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)))
    return pts


def hoofd(stap, var=1, hoek=0):
    stekel = STEKEL_KLEIN if stap >= 6 else STEKEL_GROOT
    m = draai_masker(masker(stekel, flappen=stap < 4), hoek)
    sm = draai_masker({(x, y) for y, (a, b) in stekel.items() if y < 0 for x in range(a, b + 1)}, hoek)
    d = kleur(m, sm)
    for p in sm:                                       # stekel: links licht (3), rechts schaduw (4)
        if d.get(p) == 3:
            d[p] = 4 if (p[0] + 1, p[1]) in sm and d.get((p[0] + 1, p[1])) == 15 and (p[0] - 1, p[1]) in sm and d.get((p[0] - 1, p[1])) != 15 else 3
    R = lambda x, y: T(x, y, hoek)
    for (ex, ey) in OGEN:                              # ogen 1:1
        cx, cy = R(ex + 2, ey + 2); bx, by = round(cx - 2), round(cy - 2)
        for j, r in enumerate(OOG):
            for i, c in enumerate(r):
                if c != '.': d[(bx + i, by + j)] = CH.index(c)
    a, b = MOND                                        # mondstreepje: recht lijnstuk
    mond = lijn(tuple(map(math.floor, R(a[0] + 0.5, a[1] + 0.5))), tuple(map(math.floor, R(b[0] + 0.5, b[1] + 0.5))))
    for p in mond:                                     # rondom de mond geen schaduwtint, zodat het streepje leest
        for q in ((p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] + 1, p[1] + 1)):
            if d.get(q) in (4, 5): d[q] = 3
    for p in mond: d[p] = 5
    if not hoek:
        for x in range(a[0], b[0] + 1): d[(x, a[1])] = 5
    V = V_OUD if stap < 4 else V_NIEUW
    if not hoek:
        for p, c in V: d[p] = c
    else:   # V als aaneengesloten lijnstukken op de gedraaide vorm
        pts = [(tuple(map(lambda v: math.floor(v), R(p[0] + 0.5, p[1] + 0.5))), c) for p, c in V]
        for (p, c), (q, c2) in zip(pts, pts[1:]):
            for r in lijn(p, q): d[r] = max(c, c2) if 15 in (c, c2) and r in (p, q) else (c if r == p else c2 if r == q else min(5, max(c, c2)))
        for p, c in pts: d[p] = c
    if stap >= 5:
        (hx, hy), (bx, by) = KNOT[var]
        hcx, hcy = R(hx + 4, hy + 4); ox, oy = round(hcx - 4), round(hcy - 4)
        bcx, bcy = R(bx + 1, by + 2); bx2, by2 = round(bcx - 1), round(bcy - 2)
        band = {}
        for j in range(2):
            for k in range(4): band[(bx2 + j, by2 + k)] = CH.index(BAND[j][k])
        for j in range(2): band[(bx2 + j, by2 - 1)] = 15; band[(bx2 + j, by2 + 4)] = 15
        for p, i in band.items():                      # band achter de kop: alleen waar de kop er niet is
            if p not in d: d[p] = i
        for (x, y), i in HAND.items():                 # knot achter band en kop
            q = (ox + x, oy + y)
            if q not in d: d[q] = i
        for p in [p for p, i in d.items() if i not in (15, 1, 12, 13) and any((p[0] + a, p[1] + b) not in d for a, b in N4)]:
            d[p] = 15 if p not in {(ox + x, oy + y) for (x, y) in HAND} else d[p]
    return d


def schuif(d, dx=OX, dy=OY): return {(x + dx, y + dy): i for (x, y), i in d.items()}


def x8(d, Z=8, bg=(152, 208, 160)):
    im = beeld(d, bg=bg); bb = beeld(d).getchannel('A').getbbox()
    c = im.crop((bb[0] - 1, bb[1] - 1, bb[2] + 1, bb[3] + 1)); return c.resize((c.width * Z, c.height * Z), Image.NEAREST)


def main():
    BG = (152, 208, 160)
    s1 = stap1(); s2 = dubbel(s1, (7, 9, 15, 21, 23), (13, 14, 15))
    stappen = {'1_uitsnede_overworld': s1, '2_verdubbeld_24px': s2, '3_glad_frontgezicht': schuif(hoofd(3)),
               '4_V_naar_achteren': schuif(hoofd(4))}
    koppen = {}
    for v in (1, 2):
        stappen['5_knot_variant%d' % v] = schuif(hoofd(5, v))
        stappen['6_stekel_kleiner_variant%d' % v] = schuif(hoofd(6, v))
        stappen['7_gedraaid_variant%d' % v] = schuif(hoofd(6, v, HOEK))
        koppen[v] = (stappen['6_stekel_kleiner_variant%d' % v], stappen['7_gedraaid_variant%d' % v])
    for k, d in stappen.items():
        assert all(0 <= x < 64 and 0 <= y < 64 for x, y in d), k
        x8(d).save(os.path.join(HERE, 'stap%s.png' % k))
    regels = []
    for v, (r, g) in koppen.items():
        beeld(r).save(os.path.join(HERE, 'hoofd_%d_rechtop.png' % v)); beeld(g).save(os.path.join(HERE, 'hoofd_%d_gedraaid.png' % v))
        for naam, d in (('rechtop', r), ('gedraaid', g)):
            open_ = [p for p, i in d.items() if i not in (15,) and any((p[0] + a, p[1] + b) not in d for a, b in N4)]
            xs = [p[0] for p in d]
            regels.append('variant %d %s: %d px, %d breed (met knot), open randen %d %s' % (
                v, naam, len(d), max(xs) - min(xs) + 1, len(open_), open_[:6]))
    open(os.path.join(HERE, 'controle.txt'), 'w').write('\n'.join(regels) + '\n'); print('\n'.join(regels))
    # vel
    owk = Image.open(os.path.join(ROOT, 'graphics/pokemon/hitmontop/overworld.png')).convert('RGBA').crop((0, 0, 32, 32))
    top = Image.new('RGBA', (64, 64), BG + (255,)); top.alpha_composite(SRC.convert('RGBA').crop((0, 0, 64, 64)))
    ref = Image.open(os.path.join(HERE, '../../referenties/hitmontop_3d.webp')).convert('RGB').crop((0, 0, 1080, 760))
    ref = ref.resize((ref.width * 330 // ref.height, 330))
    alles = [p for r_, g_ in koppen.values() for p in list(r_) + list(g_)]
    box = (min(p[0] for p in alles) - 1, min(p[1] for p in alles) - 1, max(p[0] for p in alles) + 2, max(p[1] for p in alles) + 2)
    bw, bh = box[2] - box[0], box[3] - box[1]
    sch = lambda im, z: im.resize((im.width * z, im.height * z), Image.NEAREST)
    W = 20 + 2 * (bw * 8 + 20) + bw * 2 + 20 + bw + 30 + ref.width + 20; H = 40 + 2 * (bh * 8 + 40) + 140
    v_ = Image.new('RGB', (W, H), (235, 235, 240)); dr = ImageDraw.Draw(v_); y = 20
    namen = {1: 'variant 1: knot achter op de kruin', 2: 'variant 2: knot achterop/opzij'}
    for v, (r, g) in koppen.items():
        dr.text((20, y), namen[v] + '   (rechtop 8x | %d graden tegen de klok in 8x | 2x | 1x)' % HOEK, fill=(0, 0, 0)); y += 14
        a = beeld(r, bg=BG).crop(box); b = beeld(g, bg=BG).crop(box)
        v_.paste(sch(a, 8), (20, y)); v_.paste(sch(b, 8), (20 + bw * 8 + 20, y)); x = 20 + 2 * (bw * 8 + 20)
        v_.paste(sch(a, 2), (x, y)); v_.paste(sch(b, 2), (x, y + bh * 2 + 10)); v_.paste(a, (x + bw * 2 + 20, y)); v_.paste(b, (x + bw * 2 + 20, y + bh * 2 + 10))
        y += bh * 8 + 26
    dr.text((20, y), 'Hitmontop: overworld 4x | frontsprite 2x | 1x', fill=(0, 0, 0))
    o = Image.new('RGBA', (32, 32), BG + (255,)); o.alpha_composite(owk)
    v_.paste(sch(o, 4), (20, y + 14)); v_.paste(sch(top, 2), (170, y + 14)); v_.paste(top, (310, y + 14)); v_.paste(o, (390, y + 14))
    v_.paste(ref, (W - ref.width - 20, 34)); dr.text((W - ref.width - 20, 20), 'referentie: hitmontop_3d.webp', fill=(0, 0, 0))
    v_.save(os.path.join(HERE, 'vel_hoofd.png'))
    ims = [(k, x8(d, Z=5)) for k, d in stappen.items()]
    Wt = sum(i.width for _, i in ims) + 20 * (len(ims) + 1); Ht = max(i.height for _, i in ims) + 50
    st = Image.new('RGB', (Wt, Ht), (235, 235, 240)); dd = ImageDraw.Draw(st); x = 20
    for k, im in ims:
        dd.text((x, 8), k.replace('_', ' ')[:30], fill=(0, 0, 0)); st.paste(im, (x, 26)); x += im.width + 20
    st.save(os.path.join(HERE, 'vel_stappen.png'))


main()
