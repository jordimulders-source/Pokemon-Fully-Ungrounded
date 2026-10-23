"""Cuyby-evolutie (fase 2), ronde 1: de wandelende hooiberg (pol Stipa ichu). Pixel-over van modeltekening A.

Elk deel staat hieronder als handgeschreven tekstraster: (y, x, "pixels") per rij, achterste deel eerst.
Geen vormfuncties, geen automatische schaduw of omlijning. Draaien vanuit de repo-root:
    python3 docs/concept/sprites/cuyby_evo/ronde1/bron/cuyby_evo.py docs/concept/sprites/cuyby_evo/ronde1 [zoom.png]
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../nachtaap/ronde7/bron'))
from lib import Canvas, save, zoom

PAL = [
    (152, 208, 160),  # 0  transparant
    (41, 24, 24),     # 1  K omlijning (schaduwkant), oog
    (255, 255, 246),  # 2  a glans
    (246, 238, 205),  # 3  b crème (snuit)
    (222, 205, 156),  # 4  c crème schaduw
    (255, 238, 156),  # 5  y stro hooglicht
    (238, 205, 106),  # 6  Y stro basis
    (205, 164, 74),   # 7  s stro schaduw
    (139, 98, 32),    # 8  S stro omlijningsbasis (ook rond de snuit)
    (238, 156, 74),   # 9  O roest basis (Cuyby's oranje)
    (205, 115, 41),   # 10 q roest schaduw
    (148, 57, 0),     # 11 Q roest omlijningsbasis
    (106, 98, 115),   # 12 g zwart vlak: glans
    (49, 41, 57),     # 13 G zwart vlak: basis
    (255, 172, 180),  # 14 p roze
    (205, 106, 115),  # 15 n roze schaduw / gekleurde weerkaatsing in het oog
]
KEYS = dict(K=1, a=2, b=3, c=4, y=5, Y=6, s=7, S=8, O=9, q=10, Q=11, g=12, G=13, p=14, n=15)

PARTS = {}

# ---------------------------------------------------------------- achterste plukken (schaduwtint)
PARTS['achter'] = [
    # b0: links buiten
    (23, 10, "K"), (24, 10, "SK"), (25, 11, "SsK"), (26, 12, "SsK"), (27, 12, "SYsK"), (28, 13, "SYsK"),
    (29, 14, "SYsK"), (30, 14, "SYssK"),
    # b1: links, leunt naar links
    (19, 14, "K"), (20, 14, "SK"), (21, 14, "SsK"), (22, 15, "SsK"), (23, 15, "SYsK"), (24, 16, "SYsK"),
    (25, 16, "SYsK"), (26, 17, "SYssK"), (27, 17, "SYssK"), (28, 18, "SYssK"), (29, 18, "SYssK"),
    # b2: midden-links
    (12, 21, "S"), (13, 21, "SS"), (14, 21, "SsS"), (15, 22, "SsS"), (16, 22, "SYsS"), (17, 22, "SYsS"),
    (18, 23, "SYsS"), (19, 23, "SYssK"), (20, 23, "SYssK"), (21, 24, "SYssK"), (22, 24, "SYssK"), (23, 24, "SYssK"),
    (24, 24, "SYsssK"), (25, 25, "SYsssK"), (26, 25, "SYsssK"),
    # b3: midden-rechts, leunt naar rechts
    (11, 36, "S"), (12, 35, "SS"), (13, 35, "SsS"), (14, 34, "SsS"), (15, 34, "SYsS"), (16, 33, "SYsS"),
    (17, 33, "SYsS"), (18, 33, "SYssS"), (19, 32, "SYssK"), (20, 32, "SYssK"), (21, 32, "SYssK"),
    # b4: rechts (stro in schaduw)
    (15, 45, "S"), (16, 44, "SS"), (17, 44, "SsS"), (18, 43, "SsS"), (19, 43, "SYsK"), (20, 42, "SYsK"),
    (21, 42, "SYsK"), (22, 41, "SYssK"), (23, 41, "SYssK"), (24, 40, "SYssK"), (25, 40, "SYssK"),
    # b5: rechts buiten, roest
    (23, 53, "K"), (24, 52, "QK"), (25, 51, "QqK"), (26, 50, "QqqK"), (27, 49, "QOqK"), (28, 48, "QOqqK"),
    (29, 48, "QOqqK"), (30, 47, "QOqqK"),
]

PARTS['lijf'] = [
    (27, 25, "YssssYYYYYYOOO"),
    (28, 21, "SSSSyyYYYYYYYYYYOOQQQQ"),
    (29, 18, "SSSyyYYYYYYYYYYYYYYOOOOOQQQK"),
    (30, 16, "SSyyYYYYYYYYYYYYYYYYYYOOOOOOqQQK"),
    (31, 15, "SyyYYyYYYYYYYYYYYYYYYYYYY" "OOOOOqqQK"),
    (32, 14, "SyyYyYYYYYYYYYYYYYYYYYYYYY" "OOOOOqqqQK"),
    (33, 13, "SyYyYYYyYYYYYYYYYYYYYYYYYYY" "OOOOOqqqqqK"),
    (34, 13, "SyYYyYYYyYYYYYYYYYYYYYYYYYY" "sOOOOqqqqqK"),
    (35, 12, "SyYYYyYYYyYYYYYYYYYYYYYYYYYY" "sOOOOOqqqqqK"),
    (36, 12, "SysYYYsYYYs" "YYYYYYYYYYYYYYYYY" "ssOOOOqqqqqK"),
    (37, 12, "SYsYYYsYYYs" "YYYYYYYYYYYYYYYYY" "sOOOOOqqqqqK"),
    (38, 11, "SYYYsYYYsYYYs" "YYYYYYYYYYYYYYYY" "sOOOOOqOqqqqK"),
    (39, 11, "KYYYsYYYs" "YYYYYYYYYYYYYYYYYYYY" "ssOOOOqOqqqqK"),
    (40, 11, "KYYYYsYYYs" "YYYYYYYYYYYYYYYYYYY" "sqOOOqOqqqqqK"),
    (41, 11, "KyYYYsYYYs" "YYYYYYYYYYYYYYYYYYY" "sqOOOqqOqqqqK"),
    (42, 12, "KsYYYsYYYs" "YYYYYYYYYYYYYYYYYY" "qOOOqqOqqqqK"),
    (43, 12, "KsYYYsYYYs" "YYYYYYYYYYYYYYYYYY" "qOOqqOqqqqqK"),
    (44, 12, "KYsYYYsYYYs" "YYYYYYYYYYYYYYYYY" "qqOqqOqqqqqK"),
    (45, 13, "KsYYYsYYYs" "YYYYYYYYYYYYYYYYY" "qqqqOqqqqqK"),
    (46, 13, "KssYYYsYYYs" "YYYYYYYYYYYYYYYY" "qqqqqqqqqqK"),
    (47, 14, "KsssssYssYsss" "sssssssssssss" "qqqqqqqqqK"),
    (48, 15, "KKssssSsssSsss" "sssssssssss" "qqqqqqqqK"),
    (49, 16, "KKsSssssSsssSsss" "ssssssss" "qqqqqqKK"),
    (50, 17, "KsssKsK" "KKKKKK" "sssK" "KKKKKK" "qqqKqK"),
]

PARTS['zoom'] = [
    (46, 11, "KYsK"), (47, 11, "KYsK"), (48, 11, "KssK"), (49, 10, "KsK"), (50, 10, "KK"),
    (45, 49, "KqqK"), (46, 49, "KqqK"), (47, 49, "KqqK"), (48, 50, "KqK"), (49, 51, "KK"),
    (51, 18, "KsK"), (51, 22, "K"), (52, 19, "K"),
    (51, 30, "KsK"), (52, 31, "K"),
    (51, 40, "KqK"), (51, 44, "K"), (52, 41, "K"),
]

PARTS['poten'] = [
    (51, 15, "KnnK"), (52, 16, "KK"),
    (51, 45, "KnnK"), (52, 46, "KK"),
    (51, 24, "KpppK"), (52, 24, "KppnK"), (53, 25, "KKK"),
    (51, 34, "KpnnK"), (52, 34, "KpnnK"), (53, 35, "KKK"),
]

PARTS['buiten'] = [
    # f1 links buiten: leunt sterk naar links (45 graden), recht als een grasspriet
    (25, 8, "K"), (26, 8, "SK"), (27, 9, "SyK"), (28, 10, "SyYK"), (29, 10, "SyYsK"), (30, 11, "SyYsK"),
    (31, 11, "SyYYsK"), (32, 12, "SyYYs"), (33, 12, "SyYYY"), (34, 12, "SyYYY"),
    # f6 rechts buiten (roest): idem naar rechts, iets langer en vlakker dan f1 (geen spiegelbeeld)
    (24, 55, "K"), (25, 54, "QK"), (26, 53, "QqK"), (27, 52, "QOqK"), (28, 51, "QOqK"), (29, 50, "QOqqK"),
    (30, 48, "QOOqqK"), (31, 47, "QOOqK"), (32, 46, "OOOqK"),
]

PARTS['kruin'] = [
    # f2 links
    (15, 17, "S"), (16, 17, "SS"), (17, 17, "SyS"), (18, 17, "SyS"), (19, 18, "SyK"), (20, 18, "SyK"),
    (21, 18, "SyYK"), (22, 18, "SyYK"), (23, 19, "SyYK"), (24, 19, "SyYK"), (25, 19, "SyYsK"), (26, 19, "SyYsK"),
    (27, 20, "SyYsK"), (28, 20, "SyYsK"), (29, 20, "yYYYsK"), (30, 20, "YYYYsK"),
    # f5 rechts (roest)
    (17, 48, "S"), (18, 47, "QQ"), (19, 46, "QOK"), (20, 46, "QOK"), (21, 45, "QOK"), (22, 45, "QOK"),
    (23, 44, "QOqK"), (24, 44, "QOqK"), (25, 43, "QOqK"), (26, 43, "QOqK"), (27, 42, "QOOqK"), (28, 42, "QOOqK"),
    (29, 41, "OOOqK"), (30, 41, "OOOqqK"),
    # f3 midden
    (10, 28, "S"), (11, 28, "SS"), (12, 28, "SyS"), (13, 28, "SyS"), (14, 28, "SyYS"), (15, 29, "SyYS"),
    (16, 29, "SyYS"), (17, 29, "SyYsS"), (18, 29, "SyYsS"), (19, 29, "SyYYsK"), (20, 30, "SyYYsK"),
    (21, 30, "SyYYsK"), (22, 30, "SyYYsK"), (23, 30, "SyYYsK"), (24, 30, "SyYYYsK"), (25, 30, "yYYYYsK"),
    (26, 30, "YYYYYsK"),
    # f4 midden-rechts
    (13, 40, "S"), (14, 39, "SS"), (15, 38, "SyS"), (16, 38, "SyS"), (17, 37, "SyS"), (18, 37, "SyS"),
    (19, 36, "SyYK"), (20, 36, "SyYK"), (21, 35, "SyYK"), (22, 35, "SyYK"), (23, 34, "SyYsK"), (24, 34, "SyYsK"),
    (25, 33, "SyYsK"), (26, 33, "SyYsK"), (27, 32, "yYYYsK"), (28, 32, "YYYYsK"),
]

PARTS['strepen'] = [
    # streng A
    (28, 20, "ys"), (29, 21, "ys"), (30, 22, "ys"), (31, 22, "ys"), (32, 23, "ys"), (33, 24, "ys"), (34, 25, "ys"), (35, 25, "ys"),
    # streng D (midden)
    (31, 29, "ys"), (32, 29, "ys"), (33, 29, "ys"), (34, 29, "ys"), (35, 30, "ys"), (36, 30, "ys"),
    # streng E
    (29, 34, "ys"), (30, 33, "ys"), (31, 33, "ys"), (32, 33, "ys"), (33, 32, "ys"), (34, 32, "ys"), (35, 32, "ys"), (36, 31, "ys"),
    # streng F
    (29, 39, "Oq"), (30, 38, "Oq"), (31, 38, "Oq"), (32, 37, "Oq"), (33, 37, "Oq"), (34, 36, "ys"), (35, 36, "ys"), (36, 35, "ys"),
]

PARTS['gezicht'] = [
    (38, 25, "SSbbbbbbbbbbSS"),
    (39, 24, "SbbbbbbbbbbbbbbS"),
    (40, 23, "SbbbbbbbbbbbbbbbbS"),
    (41, 23, "SbbbbbbbbbbbbbbbcS"),
    (42, 23, "SbbbbbbbbbbbbbbbcK"),
    (43, 23, "SbbbbbbbbbbbbbbccK"),
    (44, 24, "SbbbbbbbbbbbbbcK"),
    (45, 24, "KbbbbbbbbbbbbccK"),
    (46, 25, "KcbbbbbbbbbccK"),
    (47, 26, "KKccccccccKK"),
    (48, 28, "KKKKKKKK"),
    # zwart vlak om het linkeroog met een zwart hangoor links ervan (Cuyby's kenmerk); blok x16..30
    (36, 16, "......KKK......"),
    (37, 16, "...KKgggGGGK..."),
    (38, 16, "..KgggGGGGGGG.."),
    (39, 16, ".KgGGGGGGGGGGG."),
    (40, 16, "KgGGGGGGGgggGG."),
    (41, 16, "KGGGGKGGGgaKgG."),
    (42, 16, "KGGGKsKGGgKKgG."),
    (43, 16, ".KGGKsKGGgKngG."),
    (44, 16, ".KGKssKGGGggG.."),
    (45, 16, "..KKss.KGGGGG.."),
    (46, 16, "........KGGG..."),
    # roest hangoor rechts, over de rechterwang
    (38, 39, "QQK"), (39, 39, "QOOqK"), (40, 39, "QOOqqK"), (41, 39, "KOOqqK"), (42, 40, "KOqqK"), (43, 40, "KqqqK"),
    (44, 41, "KqqK"), (45, 42, "KK"),
    # rechteroog
    (41, 35, "aK"), (42, 35, "KK"), (43, 35, "Kn"),
    # neus en mond
    (44, 31, "pn"), (45, 31, "S"), (46, 30, "S.S"),
    # pony: twee korte plukken over het voorhoofd (rechts van het zwarte vlak)
    (37, 28, "YYYYYYY"),
    (38, 29, "SyYYsK"), (39, 30, "SYsK"), (40, 31, "KK"),
]

ORDER = ['achter', 'lijf', 'zoom', 'poten', 'buiten', 'kruin', 'strepen', 'gezicht']

# frame 2: de sprieten wiegen: de kruin (bovenste rijen van de plukken) 1 px opzij, de rest blijft staan
WIND_Y = 20


def frame(f=0):
    c = Canvas(KEYS)
    for part in ORDER:
        for y, x, s in PARTS[part]:
            dx = 1 if (f and part in ('achter', 'kruin', 'buiten') and y <= WIND_Y) else 0
            c.put(x + dx, y, [s])
    return c


if __name__ == '__main__':
    out = sys.argv[1]
    f1 = frame(0)
    f2 = frame(1)
    print('oppervlak', f1.area())
    save([f1, f2], PAL, os.path.join(out, 'anim_front.png'), os.path.join(out, 'normal.pal'))
    if len(sys.argv) > 2:
        zoom(f1, PAL, sys.argv[2], sc=8)
