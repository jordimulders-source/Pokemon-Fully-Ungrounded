"""Stap 4 hoofd, ronde 6 (6 nov). Jordi: "ik heb liever dat je hitmontops hoofd pakt en daarmee gaat spelen".
Niet opnieuw tekenen: Hitmontops eigen kop (graphics/pokemon/hitmontop/anim_front.png) stap voor stap bewerkt.
 1 uitsnede (regel van stap3b KOP)             2 180 graden; licht terug naar linksboven (ogen in hun eigen vak terug,
                                                 lichtvlek gespiegeld, flappen een toon om)
 3 zijflappen weg (hun binnenrand = de omtrek); de afgeronde bovenhoek van de linkerflap = de knot (plooien eruit);
   hoorn nog op ware grootte                    4 hoorn kleiner: middelste rijen eruit, tip zakt (vorm blijft)
 5 Hitmontops rand boven de ogen 1 rij hoger, f->5/4 en los van de omtrek (fade); flapschaduw van de lichte wang;
   mond = streepje van 5 met de hoeken 1 hoger   6 maat: A 25, B 23 px breed -> niets weg
 7 27 graden tegen de klok in: omtrek uit het gedraaide masker, daarna per pixel met de hand (ogen 1:1 terug, licht
   opnieuw linksboven, mond en fade opnieuw gelegd)
Varianten: A = knot achterop (linksboven, achter de kruin), B = knot bovenop, rond de punt.
Rasters: Hitmontops palet-indices (1 wit, 2/3/4/5 huid licht->donker, f omlijning), x0=14, y0=7.
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde6/stap4_r6.py"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from hulp import *
from stap12 import stap1, stap2
from PIL import Image, ImageDraw

X0, Y0 = 14, 7
# oude gezicht = stap 2 zonder zijflappen (rijen y15-29); rand boven de ogen, mond en flapschaduw nog van Hitmontop
OUD = """
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
""".strip('\n').split('\n')
# stap 5, rechtop (y7-29)
S5 = {'A': """
..............................
..........ff..................
.........f34f.................
.......fff34fff...............
......f22333334f..............
.....f2333333344f.............
.....f3333333444fffff.........
.......f333344fff3333f........
.......f32223455433333f.......
......f32334433334333334f.....
.....f3333333333333334433f....
.....f33333333ff333333334f....
.....f3333333f1ff333333334f...
.....f3333333ffff333333ff34f..
.....f33333333ff333333f1ff4f..
.....f3333333333333333ffff4f..
......f3333333333333333ff34f..
......f33333333333333333344f..
......f33333333353335333444f..
......f3333333333555333344f...
.......f444433333333334444f...
........f4444444444445555f....
.........ffffffffffffffff.....
""", 'B': """
.................ff...........
................f34f..........
..............fff34fff........
.............f22333334f.......
............f2333333344f......
............f3333333444f......
..............f333344f........
........ffffff333333334f......
.......f322234554333333f......
......f32334433334333334f.....
.....f3333333333333334433f....
.....f33333333ff333333334f....
.....f3333333f1ff333333334f...
.....f3333333ffff333333ff34f..
.....f33333333ff333333f1ff4f..
.....f3333333333333333ffff4f..
......f3333333333333333ff34f..
......f33333333333333333344f..
......f33333333353335333444f..
......f3333333333555333344f...
.......f444433333333334444f...
........f4444444444445555f....
.........ffffffffffffffff.....
"""}
S5 = {k: v.strip('\n').split('\n') for k, v in S5.items()}
# hoorn op ware grootte (stap 3): Hitmontops hoorn uit stap 2, 3 rijen langer, voet 4 breed in de knot
HOORN_GROOT = {'B': (31, 7, ["ff", "f34f", "f34f", "f3234f", "f3334f"], (28, 9, "ff3334ff")),
               'A': (24, 8, ["ff", "f34f", "f34f", "f3234f", "f3334f"], (21, 10, "ff3334ff"))}


def rows_d(rows, y0=Y0):
    return uit_tekst('\n'.join(rows), X0, y0)


def rechtop(v, stap):
    """het rechtopstaande hoofd na stap 3, 4 of 5/6 (dict pos -> index)."""
    rows = list(S5[v])
    if stap <= 4:   # rijen y15-29 nog Hitmontops oude gezicht (rand boven de ogen, mond, flapschaduw)
        for y in range(15, 30):
            rows[y - Y0] = OUD[y - 15]
    d = rows_d(rows)
    if stap == 3:
        tx, ty, horn, (bx, by, voet) = HOORN_GROOT[v]
        for p in [p for p in d if p[1] < by]:
            del d[p]
        for (x, y) in [(x, by) for x in range(bx, bx + len(voet))]:
            d.pop((x, y), None)
        for i, c in enumerate(voet): d[(bx + i, by)] = CH.index(c)
        for j, r in enumerate(horn):
            yy = by - len(horn) + j
            xx = tx + 1 - len(r) // 2
            for i, c in enumerate(r): d[(xx + i, yy)] = CH.index(c)
    return d


# ---------------- stap 7: gedraaid, met de hand ----------------
def pad_naar_masker(pad):
    m = set(pad); xs = [p[0] for p in pad]; ys = [p[1] for p in pad]
    # binnen = vullen vanaf het midden
    st = [(31, 21)]; binnen = set()
    while st:
        p = st.pop()
        if p in binnen or p in m: continue
        assert min(xs) <= p[0] <= max(xs) and min(ys) <= p[1] <= max(ys), ('lek', p)
        binnen.add(p)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): st.append((p[0] + dx, p[1] + dy))
    return m, binnen


ONDER = ([(41, 16), (41, 17)] + [(42, y) for y in range(18, 25)] +
         [(41, 25), (40, 25), (39, 26), (38, 26), (37, 27), (36, 27), (35, 28), (34, 28), (33, 29), (32, 29), (31, 30),
          (30, 30), (29, 31), (28, 31), (27, 31), (26, 30), (25, 30), (24, 29), (23, 28), (22, 27), (21, 26), (21, 25)] +
         [(20, y) for y in range(19, 25)])
PAD = {
    'B': [(29, 7), (30, 7), (28, 8), (31, 8), (27, 9), (28, 9), (31, 9), (32, 9), (25, 10), (26, 10), (33, 10), (24, 11),
          (33, 11), (23, 12), (23, 13), (34, 12), (35, 13), (36, 13), (37, 13), (38, 14), (39, 14), (40, 15)] + ONDER +
         [(21, 18), (22, 17), (23, 16), (24, 15), (24, 14)],
    'A': [(20, 11), (21, 11), (19, 12), (22, 12), (19, 13), (22, 13), (23, 13), (24, 13), (25, 13), (26, 13), (26, 14),
          (26, 15), (27, 16), (28, 15), (29, 15), (30, 14), (31, 14), (32, 13), (33, 13), (34, 13), (35, 13), (36, 13),
          (37, 13), (38, 14), (39, 14), (40, 15)] + ONDER +
         [(19, 19), (18, 19), (17, 18), (17, 17), (18, 16), (18, 15), (19, 14)],
}
OOG_L = [".ff.", "f1ff", "ffff", ".ff."]          # Hitmontops oog, pixel voor pixel (stap 2, wit linksboven)
GEZICHT_7 = {   # hand: ogen, mond, fade, licht (gelijk voor A en B; het gezicht is hetzelfde)
    'oog': [(27, 19), (36, 16)],
    'mond': [(33, 24), (34, 25), (35, 25), (36, 24), (37, 23)],
    'licht': [(22, 19), (23, 18), (22, 20), (23, 19)],
}
FADE = {'B': {(24, 18): 4, (25, 17): 4, (26, 17): 5, (27, 16): 5, (28, 16): 5, (29, 15): 4, (30, 15): 4},
        'A': {(24, 19): 4, (25, 18): 4, (26, 18): 5, (27, 17): 5, (28, 17): 5, (29, 16): 4, (30, 16): 4}}
TOP = {'B': {(29, 8): 3, (30, 8): 4, (29, 9): 3, (30, 9): 4,                         # hoorn
             (27, 10): 2, (28, 10): 2, (26, 11): 2, (27, 11): 2, (25, 12): 2,        # knot licht
             (32, 10): 4, (32, 11): 4, (31, 11): 4, (33, 12): 4},                    # knot schaduw rechts
       'A': {(20, 12): 3, (21, 12): 4, (20, 13): 3, (21, 13): 4,
             (20, 14): 2, (21, 14): 2, (19, 15): 2, (20, 15): 2, (19, 16): 2,
             (25, 14): 4, (25, 15): 4, (26, 16): 4, (24, 15): 4}}


def gedraaid(v):
    m, binnen = pad_naar_masker(PAD[v])
    d = {p: 15 for p in m}
    for p in binnen: d[p] = 3
    # schaduwsikkel: binnenpixels naast de omtrek rechts (x>=39) en onder (y>=27) -> 4, tweede laag rechtsonder 4/5
    rand = [p for p in binnen if any((p[0] + a, p[1] + b) in m for a, b in ((1, 0), (0, 1), (1, 1), (-1, 1)))]
    for (x, y) in rand:
        if x >= 39 or y >= 27: d[(x, y)] = 4
    for (x, y) in binnen:
        if (x, y) in d and d[(x, y)] == 3 and any(d.get((x + a, y + b)) == 4 for a, b in ((1, 0), (0, 1), (1, 1))) \
           and x + y >= 63:
            d[(x, y)] = 4
    for (x, y) in rand:
        if x + y >= 66 and y >= 25: d[(x, y)] = 5
    for (ex, ey) in GEZICHT_7['oog']:
        for j, r in enumerate(OOG_L):
            for i, c in enumerate(r):
                if c != '.': d[(ex + i, ey + j)] = CH.index(c)
    for p in GEZICHT_7['mond']: d[p] = 5
    for p in GEZICHT_7['licht']: d[p] = 2
    d.update(FADE[v]); d.update(TOP[v])
    return d


def verschuif(d, dx, dy):
    return {(x + dx, y + dy): i for (x, y), i in d.items()}


def x8(d, Z=8, bg=(152, 208, 160)):
    im = beeld(d, bg=bg); bb = beeld(d).getchannel('A').getbbox()
    bb = (bb[0] - 1, bb[1] - 1, bb[2] + 1, bb[3] + 1)
    c = im.crop(bb); return c.resize((c.width * Z, c.height * Z), Image.NEAREST)


def tel(d, ref):
    gelijk = sum(1 for p, i in d.items() if ref.get(p) == i)
    plek = sum(1 for p in d if p in ref)
    return gelijk, plek, len(d)


def main():
    D1 = stap1(); D2 = stap2(D1)
    stappen = {'1_uitsnede': D1, '2_gedraaid_licht': D2}
    for v in 'AB':
        stappen['3%s_flappen_knot' % v] = rechtop(v, 3)
        stappen['4%s_hoorn_klein' % v] = rechtop(v, 4)
        stappen['5%s_fade_mond' % v] = rechtop(v, 5)
        stappen['6%s_maat' % v] = rechtop(v, 5)
        stappen['7%s_gedraaid' % v] = gedraaid(v)
    regels = []
    for n, d in stappen.items():
        x8(d).save(os.path.join(HERE, 'stap%s.png' % n))
        if n[0] in '3456':
            g, p, t = tel(d, D2)
            xs = [q[0] for q in d]
            regels.append('%s: %d px, breed %d; %d%% exact Hitmontop (zelfde plek en tint als stap 2), %d%% op een plek waar '
                          'Hitmontop huid had' % (n, t, max(xs) - min(xs) + 1, 100 * g // t, 100 * p // t))
        if n[0] == '7':
            xs = [q[0] for q in d]
            regels.append('%s: %d px, breed %d (gedraaid en met de hand gelegd; ogen 1:1 Hitmontop)' % (n, len(d), max(xs) - min(xs) + 1))
    # losse hoofden op de schermplek (zelfde plek als ronde 5b: midden ~ (14,35))
    for v in 'AB':
        d = verschuif(stappen['7%s_gedraaid' % v], -17, 16)
        assert all(0 <= x < 64 and 0 <= y < 64 for x, y in d)
        beeld(d).save(os.path.join(HERE, 'hoofd_%s.png' % v))
        stappen['los' + v] = d
    # controle: gesloten omtrek (geen huid naast leegte), geen losse tintpixels
    for v in 'AB':
        d = stappen['los' + v]
        open_ = [p for p, i in d.items() if i != 15 and any((p[0] + a, p[1] + b) not in d for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        regels.append('controle %s: open randen %d' % (v, len(open_)))
    open(os.path.join(HERE, 'controle.txt'), 'w').write('\n'.join(regels) + '\n')
    print('\n'.join(regels))
    # vel: per variant 8x | 2x | 1x; daaronder Hitmontop (kop) 8x | 2x | 1x; rechts de anime; stappenstrook
    top = SRC.convert('RGBA').crop((0, 0, 64, 64))
    topkop = Image.new('RGBA', (64, 64), (152, 208, 160, 255)); topkop.alpha_composite(top)
    topkop = topkop.crop((10, 26, 56, 58))
    anime = Image.open(os.path.join(HERE, '../../referenties/hitmontop_anime.webp')).convert('RGB').crop((320, 40, 1000, 500))
    anime = anime.resize((anime.width * 300 // anime.height, 300))
    BG = (152, 208, 160)
    def schaal(im, z): return im.resize((im.width * z, im.height * z), Image.NEAREST)
    kop = {v: beeld(stappen['7%s_gedraaid' % v], bg=BG).crop((15, 5, 45, 34)) for v in 'AB'}
    rijen = [('A: knot achterop', kop['A']), ('B: knot bovenop, rond de punt', kop['B']), ('Hitmontop (sprite, kop)', topkop)]
    W = 20 + 46 * 8 + 20 + 46 * 2 + 20 + 46 + 30 + anime.width + 20
    H = 20 + sum(k.height * 8 + 40 for _, k in rijen) + 0
    v_ = Image.new('RGB', (W, H), (235, 235, 240)); dr = ImageDraw.Draw(v_); y = 20
    for t, k in rijen:
        dr.text((20, y), t + '   (8x | 2x | 1x)', fill=(0, 0, 0)); y += 14
        v_.paste(schaal(k, 8), (20, y)); v_.paste(schaal(k, 2), (20 + 46 * 8 + 20, y)); v_.paste(k, (20 + 46 * 8 + 20 + 46 * 2 + 20, y))
        y += k.height * 8 + 26
    v_.paste(anime, (W - anime.width - 20, 34)); dr.text((W - anime.width - 20, 20), 'anime (referentie)', fill=(0, 0, 0))
    # 1x naast elkaar op de schermplek: A, B, Hitmontop
    xx = W - anime.width - 20; yy = 360
    dr.text((xx, yy), '1x en 2x op de spriteplek: A | B | Hitmontop', fill=(0, 0, 0))
    for i, im in enumerate([beeld(stappen['losA'], bg=BG), beeld(stappen['losB'], bg=BG), topkop]):
        v_.paste(im, (xx + i * 70, yy + 16)); v_.paste(schaal(im, 2), (xx + i * 140, yy + 90))
    v_.save(os.path.join(HERE, 'vel_hoofd.png'))
    # stappenvel per variant (alle stappen 8x op een rij, in twee rijen)
    for v in 'AB':
        ns = ['1_uitsnede', '2_gedraaid_licht', '3%s_flappen_knot' % v, '4%s_hoorn_klein' % v, '5%s_fade_mond' % v, '7%s_gedraaid' % v]
        ims = [x8(stappen[n], Z=6) for n in ns]
        Wt = sum(i.width for i in ims) + 20 * (len(ims) + 1); Ht = max(i.height for i in ims) + 50
        st = Image.new('RGB', (Wt, Ht), (235, 235, 240)); dd = ImageDraw.Draw(st); x = 20
        for n, im in zip(ns, ims):
            dd.text((x, 8), 'stap ' + n, fill=(0, 0, 0)); st.paste(im, (x, 26)); x += im.width + 20
        st.save(os.path.join(HERE, 'vel_stappen_%s.png' % v))


main()
