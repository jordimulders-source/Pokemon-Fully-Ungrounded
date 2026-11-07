"""Stap 4 hoofd, ronde 7 (6 nov). Jordi (letterlijk): "De V-vorm tussen zijn ogen, die lijn gaan we naar achter trekken,
die haren komen samen in een soort knot, dat mag gewoon een rondje zijn met een witte band, bijna zoals zijn handen.
en de stekel bovenop mag kleiner, makkelijker kan ik het echt neit maken". Referentie: referenties/hitmontop_3d.webp.
Alles op Hitmontops eigen pixels (anim_front.png), vanaf stap 2 van ronde 6 (kop rechtop, ogen terug, licht linksboven):
 a  V-lijn (voorrand van de flappen: (22,18)..(30,16)..(31,17),(32,18) | tip (35,19) | (36-37,18)) 3 rijen omhoog
    geschoven: de flappen zijn naar achteren gekamd, voorhoofd tussen en boven de ogen = vrij gezicht (flapschaduw weg);
    de neerhangende zijflappen weg (hun binnenrand = de wang/kaaklijn)
 b  knot = Hitmontops linkerhand (anim_front x9-16, y28-35), 1:1; witte band = zijn polsband (x8-12, y24-25), 1:1
    of 90 graden gedraaid; de band zit tussen knot en kop zoals tussen hand en arm
 c  stekel: zijn eigen stekel, middelste rijen eruit (6 -> 3 rijen + voet)
Ogen en mond: Hitmontops eigen pixels, onveranderd. Varianten: 1 = knot achter op de kruin, 2 = knot achterop/opzij.
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde7/stap4_r7.py"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from hulp import *
from stap12 import stap1, stap2
from PIL import Image, ImageDraw

X0 = 14
# Basis = ronde 6 stap 2 (Hitmontops kop rechtop, ogen terug, licht linksboven) met de neerhangende zijflappen weg
# (hun binnenrand werd de wang/kaaklijn): x14-43, y7-29. Hierop alleen de drie bewerkingen van Jordi.
BASIS = """
.................ff...........
................f34f..........
................f34f..........
...............f3234f.........
...............f3334f.........
..............f333344f........
..........ffff3333334f........
........ff332223333344f.......
.......f333332223333334f......
......f33333355ff3333344f.....
.....f3333ff53344f3333334f....
.....f33ff4443ff333333554f....
.....f3344444f1ff333333333f...
.....f3344444ffff333333ff34f..
.....f34444433ff433333f1ff4f..
.....f3444433333333333ffff4f..
......f4443333333555333ff34f..
......f44433333553335333344f..
......f44443335333333333444f..
......f4444443333333333344f...
.......f444444443333333344f...
........f4444444444445555f....
.........ffffffffffffffff.....
"""
OUDE_V = {(22, 18): 15, (23, 18): 15, (24, 17): 15, (25, 17): 15, (26, 17): 5, (27, 16): 5, (28, 16): 5, (29, 16): 15,
          (30, 16): 15, (31, 17): 15, (32, 18): 4, (35, 19): 5, (36, 18): 5, (37, 18): 5}   # Hitmontops V (voorrand flappen)
OMHOOG = 2


def laad_kop(stap=3):
    d = uit_tekst(BASIS, X0, 7)
    if stap >= 1:   # a: V naar achteren getrokken
        for p in OUDE_V: d[p] = 3                                   # waar de V zat: vrij gezicht
        for (x, y), i in list(d.items()):                           # flapschaduw op wang/voorhoofd weg
            if 20 <= x <= 26 and 17 <= y <= 24 and i == 4: d[(x, y)] = 3
        d[(29, 17)] = 3; d[(30, 17)] = 3
        for (x, y), i in OUDE_V.items(): d[(x, y - OMHOOG)] = i      # dezelfde lijn, 2 rijen hoger
        d[(33, 17)] = 4; d[(34, 17)] = 5                            # V-punt dicht (in het origineel 2 px open)
    if stap >= 3:   # c: stekel kleiner: Hitmontops stekel, 3 middelste rijen eruit, tip zakt
        for y in range(7, 13):
            for x in range(26, 37): d.pop((x, y), None)
        d.update({(31, 9): 15, (32, 9): 15, (30, 10): 15, (31, 10): 3, (32, 10): 4, (33, 10): 15, (29, 11): 15, (30, 11): 3,
                  (31, 11): 2, (32, 11): 3, (33, 11): 4, (34, 11): 15, (28, 12): 15, (29, 12): 3, (30, 12): 3, (31, 12): 3,
                  (32, 12): 3, (33, 12): 4, (34, 12): 4, (35, 12): 15})
    return d


SRCD = top_idx()
HAND = {(x, y): SRCD[(x, y)] for x in range(9, 17) for y in range(28, 36) if (x, y) in SRCD
        and not (x == 16 and y == 29) and not (x == 16 and y == 28)}   # linkerhand, zonder het armstokje
BAND = {(x, y): SRCD[(x, y)] for x in range(8, 13) for y in range(24, 26) if (x, y) in SRCD}  # polsband c11cf / d1cff


def plaats(d, blok, dx, dy, draai90=False):
    xs = [p[0] for p in blok]; ys = [p[1] for p in blok]; x0, y0 = min(xs), min(ys)
    for (x, y), i in blok.items():
        if draai90:      # 90 graden: rij wordt kolom (band staand)
            q = (dx + (y - y0), dy + (x - x0))
        else:
            q = (dx + (x - x0), dy + (y - y0))
        d[q] = i
    return d


# Polsband in Hitmontops eigen kleuren en schikking (wit 1 in het midden, lichtgrijs c / grijs d aan de randen)
BAND_RIJ = ['c11c', 'dccd']


def variant(n, stap=3):
    d = laad_kop(stap)
    if stap < 2: return d
    if n == 1:   # knot achter op de kruin: band liggend op de kruin (vervangt daar de omtrek), knot erbovenop
        plaats(d, HAND, 20, 4)                          # knot = Hitmontops hand, 1:1
        for j, r in enumerate(BAND_RIJ):
            for i, c in enumerate(r): d[(22 + i, 12 + j)] = CH.index(c)
        for y in (12, 13): d[(21, y)] = 15; d[(26, y)] = 15
    else:        # knot achterop/opzij: band staand tussen knot en achterhoofd, waar de V-lijn uitkomt
        plaats(d, HAND, 10, 13)
        for j, r in enumerate(BAND_RIJ):
            for i, c in enumerate(r): d[(18 + j, 15 + i)] = CH.index(c)
        for x in (18, 19): d[(x, 14)] = 15; d[(x, 19)] = 15
        d[(20, 14)] = 15; d[(21, 14)] = 15; d[(20, 15)] = 3; d[(21, 15)] = 3
    return d


def scale2x(grid):
    h = len(grid); w = len(grid[0]); out = [[0] * (2 * w) for _ in range(2 * h)]
    g_ = lambda x, y: grid[y][x] if 0 <= x < w and 0 <= y < h else None
    for y in range(h):
        for x in range(w):
            P = g_(x, y); A = g_(x, y - 1); B = g_(x + 1, y); C = g_(x - 1, y); D = g_(x, y + 1)
            e = [P, P, P, P]
            if C == A and C != D and A != B: e[0] = A
            if A == B and A != C and B != D: e[1] = B
            if D == C and D != B and C != A: e[2] = C
            if B == D and B != A and D != C: e[3] = D
            out[2 * y][2 * x], out[2 * y][2 * x + 1], out[2 * y + 1][2 * x], out[2 * y + 1][2 * x + 1] = [q or 0 for q in e]
    return out


def draai(d, hoek, cx, cy):
    """rotsprite (3x scale2x, draaien, terug naar 1x) als gids; daarna: omtrek dicht, ogen 1:1 terug."""
    grid = [[d.get((x, y), 0) for x in range(64)] for y in range(64)]
    for _ in range(3): grid = scale2x(grid)
    Z = 8; big = Image.new('P', (64 * Z, 64 * Z), 0); big.putdata([v for r in grid for v in r])
    big = big.rotate(hoek, resample=Image.NEAREST, center=(cx * Z, cy * Z)); px = big.load()
    out = {}
    for y in range(64):
        for x in range(64):
            cnt = {}
            for yy in range(y * Z + 2, y * Z + 6):
                for xx in range(x * Z + 2, x * Z + 6):
                    cnt[px[xx, yy]] = cnt.get(px[xx, yy], 0) + 1
            k = max(cnt, key=cnt.get)
            if k: out[(x, y)] = k
    a = math.radians(hoek)
    rot = lambda x, y: (cx + (x - cx) * math.cos(a) + (y - cy) * math.sin(a), cy - (x - cx) * math.sin(a) + (y - cy) * math.cos(a))
    # ogen: zwart/wit uit het gezicht, Hitmontops 4x4-oog 1:1 op de gedraaide plek
    oog = [".ff.", "f1ff", "ffff", ".ff."]
    for (ex, ey) in ((27, 18), (36, 20)):
        mx, my = rot(ex + 2, ey + 2)
        for p in [p for p in out if abs(p[0] + 0.5 - mx) < 3 and abs(p[1] + 0.5 - my) < 3 and out[p] in (1, 15)]:
            out[p] = 3
        bx, by = round(mx - 2), round(my - 2)
        for j, r in enumerate(oog):
            for i, c in enumerate(r):
                if c != '.': out[(bx + i, by + j)] = CH.index(c)
    # losse pixels weg, omtrek dicht
    N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for p in [p for p in out if sum((p[0] + a_, p[1] + b_) in out for a_, b_ in N4) <= 1]: del out[p]
    for p in list(out):
        if out[p] not in (15, 1, 12, 13) and any((p[0] + a_, p[1] + b_) not in out for a_, b_ in N4): out[p] = 15
    return out


def x8(d, Z=8, bg=(152, 208, 160), box=None):
    im = beeld(d, bg=bg)
    if box is None:
        bb = beeld(d).getchannel('A').getbbox(); box = (bb[0] - 1, bb[1] - 1, bb[2] + 1, bb[3] + 1)
    c = im.crop(box); return c.resize((c.width * Z, c.height * Z), Image.NEAREST)


HOEK = 15


def main():
    BG = (152, 208, 160)
    stappen = {'0_basis_stap2_zonder_zijflappen': laad_kop(0), '1_V_naar_achteren': laad_kop(1)}
    koppen = {}
    for n in (1, 2):
        stappen['2_knot_variant%d' % n] = variant(n, 2)
        stappen['3_stekel_kleiner_variant%d' % n] = variant(n, 3)
        rechtop = variant(n, 3)
        cx, cy = 30.5, 20.5
        gedraaid = draai(rechtop, HOEK, cx, cy)
        stappen['4_gedraaid_variant%d' % n] = gedraaid
        koppen[n] = (rechtop, gedraaid)
    for k, d in stappen.items():
        x8(d).save(os.path.join(HERE, 'stap%s.png' % k))
    for n, (r, g_) in koppen.items():
        beeld(r).save(os.path.join(HERE, 'hoofd_%d_rechtop.png' % n)); beeld(g_).save(os.path.join(HERE, 'hoofd_%d_gedraaid.png' % n))
    # telling: hoeveel pixels zijn Hitmontops eigen pixels (zelfde tint, op de plek van stap 2 of als hand/band 1:1)
    D2 = stap2(stap1()); regels = []
    for n, (r, _) in koppen.items():
        hand = {}
        plaats(hand, HAND, *((20, 4) if n == 1 else (10, 13)))
        eigen = sum(1 for p, i in r.items() if D2.get(p) == i or hand.get(p) == i)
        regels.append('variant %d rechtop: %d px, %d eigen Hitmontop-pixels (%d%%), breed %d' % (
            n, len(r), eigen, 100 * eigen // len(r), max(p[0] for p in r) - min(p[0] for p in r) + 1))
    open(os.path.join(HERE, 'controle.txt'), 'w').write('\n'.join(regels) + '\n'); print('\n'.join(regels))
    # vel: per variant rechtop 8x | gedraaid 8x | 2x | 1x ; onderaan Hitmontop ; rechts de 3D-referentie
    top = SRC.convert('RGBA').crop((0, 0, 64, 64)); tk = Image.new('RGBA', (64, 64), BG + (255,)); tk.alpha_composite(top)
    tk = tk.crop((8, 22, 56, 58))
    ref = Image.open(os.path.join(HERE, '../../referenties/hitmontop_3d.webp')).convert('RGB')
    ref = ref.crop((0, 0, 1080, 760)); ref = ref.resize((ref.width * 330 // ref.height, 330))
    alles = [p for r_, g2 in koppen.values() for p in list(r_) + list(g2)]
    box = (min(p[0] for p in alles) - 1, min(p[1] for p in alles) - 1, max(p[0] for p in alles) + 2, max(p[1] for p in alles) + 2)
    bw, bh = box[2] - box[0], box[3] - box[1]
    sch = lambda im, z: im.resize((im.width * z, im.height * z), Image.NEAREST)
    W = 20 + 2 * (bw * 8 + 20) + bw * 2 + 20 + bw + 30 + ref.width + 20; H = 20 + 2 * (bh * 8 + 40) + 36 * 4 + 60
    v = Image.new('RGB', (W, H), (235, 235, 240)); dr = ImageDraw.Draw(v); y = 20
    namen = {1: 'variant 1: knot achter op de kruin', 2: 'variant 2: knot achterop/opzij'}
    for n, (r, g_) in koppen.items():
        dr.text((20, y), namen[n] + '   (rechtop 8x | %d graden tegen de klok in 8x | 2x | 1x)' % HOEK, fill=(0, 0, 0)); y += 14
        a_ = beeld(r, bg=BG).crop(box); b_ = beeld(g_, bg=BG).crop(box)
        v.paste(sch(a_, 8), (20, y)); v.paste(sch(b_, 8), (20 + bw * 8 + 20, y)); x = 20 + 2 * (bw * 8 + 20)
        v.paste(sch(a_, 2), (x, y)); v.paste(sch(b_, 2), (x, y + bh * 2 + 10)); v.paste(a_, (x + bw * 2 + 20, y)); v.paste(b_, (x + bw * 2 + 20, y + bh * 2 + 10))
        y += bh * 8 + 26
    dr.text((20, y), 'Hitmontop (sprite)  4x | 1x', fill=(0, 0, 0)); v.paste(sch(tk, 4), (20, y + 14)); v.paste(tk, (20 + tk.width * 4 + 20, y + 14))
    v.paste(ref, (W - ref.width - 20, 34)); dr.text((W - ref.width - 20, 20), 'referentie: hitmontop_3d.webp', fill=(0, 0, 0))
    v.save(os.path.join(HERE, 'vel_hoofd.png'))
    ims = [(k, x8(d, Z=5)) for k, d in stappen.items()]
    Wt = sum(i.width for _, i in ims) + 20 * (len(ims) + 1); Ht = max(i.height for _, i in ims) + 50
    st = Image.new('RGB', (Wt, Ht), (235, 235, 240)); dd = ImageDraw.Draw(st); x = 20
    for k, im in ims:
        dd.text((x, 8), k.replace('_', ' ')[:28], fill=(0, 0, 0)); st.paste(im, (x, 26)); x += im.width + 20
    st.save(os.path.join(HERE, 'vel_stappen.png'))


main()
