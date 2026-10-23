"""Cuyby ronde 2: de hele sprite met de hand per rij getekend.

Per rij van de bol: (y, x links-omlijning, binnenkant als tekst); de rechter-omlijning volgt direct na de tekst.
De contour is een ronde bol (30 breed, 21 hoog boven de zoom) zoals Jigglypuff; de zoom van vijf lokken,
de oren, ogen, neus en mond staan als losse rijen eronder.
"""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from lib import Canvas, save
from cuyby import PAL, KEYS

BALL = [
    (19, 25, "K" + "gGGG" + "ab" + "ooOq" + "K"),
    (20, 23, "K" + "gGGgGG" + "ab" + "ooOOOq" + "K"),
    (21, 22, "gGGGGgGG" + "abc" + "oOOOOqq"),
    (22, 21, "gGGgGGGgG" + "abc" + "oOOOqOqQ"),
    (23, 20, "gGGGGgGGG" + "abbbb" + "oOOOOqqQ"),
    (24, 19, "gGGgGGGgGG" + "bbbbb" + "oOOqOOqqQ"),
    (25, 19, "gGGGGgGGGG" + "bbbbb" + "OOOOOOqqQ"),
    (26, 18, "gGGGGGGgGG" + "bbbbbbb" + "OOOqOOqqQ"),
    (27, 18, "gGGGGGGGG" + "bbbbbbbb" + "OOOOOqqqQ"),
    (28, 17, "gGgEEEgGG" + "bbbbEEEbbb" + "OOOOOqqqQ"),
    (29, 17, "ggEaaEEg" + "bbbbEaaEEbb" + "OOOOqOqqQ"),
    (30, 17, "GgEaaEE" + "bbbbbEaaEEbb" + "OOOOOOqqQ"),
    (31, 17, "GgEEE" + "EE" + "bbbbb" + "EEEEE" + "bc" + "OOOOOqqqQ"),
    (32, 17, "GgE" + "EnnE" + "bbbbb" + "EEnnE" + "bc" + "OOOOqOqqQ"),
    (33, 17, "GG" + "bEEEbbbbbbbEEEbcc" + "OOOOqqqqQ"),
    (34, 17, "bcbbbbbbb" + "pP" + "bbbbbbc" + "cc" + "OOOqqqqQ"),
    (35, 17, "cbcbbbb" + "bbebb" + "bbbbbcc" + "c" + "OOOqqqqQ"),
    (36, 18, "cbbcbbb" + "ebe" + "bbbbbbcc" + "c" + "OOqqqqQ"),
    (37, 18, "ccbcbbbbbbbbcbbcccc" + "OqqqqqQ"),
    (38, 19, "ccbbbcbbbbbcbbcccc" + "OqqqqQ"),
    (39, 19, "bbcbbbbcbbbbbcbbcc" + "OqqqqQ"),
]
TOP = (27, 18, "KKKKKKKKKK")

HEM = [
    (18, 40, "K" + "bbc" + "bbbbb" + "c" + "bbbbbb" + "c" + "bbb" + "OOqqqqQ" + "K"),
    (17, 41, "K" + "bbb" + "c" + "bbbbb" + "c" + "bbbbbb" + "c" + "bbb" + "OO" + "q" + "OqqqQ" + "K"),
    (17, 42, "K" + "bbc" + "K" + "bbbbb" + "c" + "bbbbbb" + "c" + "bbc" + "Oq" + "K" + "OqqqQ" + "K"),
    (16, 43, "K" + "bbcc" + "K" + "bbbbc" + "K" + "bbbbbc" + "K" + "bbc" + "Oq" + "K" + "OqqQ" + "K"),
    (16, 44, "KcK" + ".." + "K" + "bbbc" + "K" + "K" + "bbbbbc" + "K" + "K" + "bcOq" + "K" + ".." + "KQK"),
    (17, 45, "K" + "...." + "K" + "bc" + "K" + "pP" + "K" + "bbbc" + "K" + "pP" + "K" + "bq" + "K" + "...." + "K"),
    (23, 46, "KK" + "." + "KK" + "." + "KbcK" + "." + "KK" + "." + "KK"),
    (30, 47, "KK"),
]

EARS = [
    (21, 16, "KKK"), (20, 17, "KgGGK"), (19, 18, "KGpPGK"), (19, 19, "KGpPGK"), (20, 20, "KGGK"), (20, 21, "KK"),
    (40, 16, "KKK"), (39, 17, "KoOqK"), (38, 18, "KopPqK"), (38, 19, "KopPqK"), (39, 20, "KqQK"), (41, 21, "KK"),
]

# gekleurde omlijning (met de hand gekozen): bruin langs het wit, donkeroranje langs het oranje
SELOUT = {(x, y): 'e' for x, y in [(17, 34), (17, 35), (18, 36), (18, 37), (19, 38), (19, 39), (18, 40), (17, 41),
                                     (17, 42), (16, 43), (21, 42), (21, 43), (27, 43), (34, 43), (31, 18), (32, 18)]}
SELOUT.update({(x, y): 'Q' for x, y in [(33, 18), (34, 18), (35, 18), (36, 18), (37, 19), (40, 42), (40, 43),
                                          (40, 16), (41, 16), (42, 16), (39, 17)]})

# rechterkant (oranje, schaduwzijde): omlijning donkeroranje, de binnenrand een stap lichter
RIGHT_EDGE = [(38, 19), (40, 20), (41, 21), (42, 22), (43, 23), (44, 24), (44, 25), (45, 26), (45, 27), (46, 28), (46, 29),
              (46, 30), (46, 31), (46, 32), (46, 33), (46, 34), (46, 35), (45, 36), (45, 37), (44, 38), (44, 39),
              (45, 40), (46, 41), (46, 42), (45, 43)]

# frame 2: popcornsprongetje: alles een pixel omhoog, mondje open (fluiten)
F2 = [(25, 35, "bKKKb"), (25, 36, "KPPPK"), (26, 37, "KKK")]


def frame(f=0):
    c = Canvas(KEYS)
    dy = -1 if f else 0
    c.put(TOP[0], TOP[1] + dy, [TOP[2]])
    for y, xl, s in BALL:
        c.put(xl, y + dy, ["K" + s + "K"])
    for x, y, s in HEM:
        c.put(x, y + dy, [s])
    for x, y, s in EARS:
        c.put(x, y + dy, [s])
    for (x, y), ch in SELOUT.items():
        if c.px[y + dy][x] == KEYS['K']:
            c.px[y + dy][x] = KEYS[ch]
    for x, y in RIGHT_EDGE:
        if c.px[y + dy][x] == KEYS['K']:
            c.px[y + dy][x] = KEYS['Q']
            if c.px[y + dy][x - 1] == KEYS['Q']:
                c.px[y + dy][x - 1] = KEYS['q']
    if f:
        for x, y, s in F2:
            c.put(x, y + dy, [s])
    return c


if __name__ == '__main__':
    out = sys.argv[1]
    f1, f2 = frame(0), frame(1)
    print('area', f1.area())
    save([f1, f2], PAL, out + '/anim_front.png', out + '/normal.pal')
