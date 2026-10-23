"""Cuyby fase 1, ronde 2: met de hand getekend (ASCII per pixel), skelet Jigglypuff (bol) + Skitty (ogen),
palet = rampen van Jigglypuff/Skitty, alleen de tint gedraaid (gekleurde omlijning per kleurvlak)."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from lib import Canvas, save

# Jigglypuff-roze 255,205,197 / 255,172,164 / 230,115,98 / 164,49,16 -> oranje (zelfde helderheidsstappen)
PAL = [
    (152, 208, 160),   # 0 transparant
    (49, 32, 32),      # 1 K omlijning
    (255, 255, 255),   # 2 a wit / glans
    (246, 238, 213),   # 3 b vacht wit-creme
    (222, 205, 164),   # 4 c vachtschaduw
    (164, 131, 90),    # 5 e vacht donker / gekleurde lijn
    (255, 213, 139),   # 6 o oranje licht
    (246, 156, 65),    # 7 O oranje
    (213, 106, 32),    # 8 q oranje schaduw
    (139, 57, 16),     # 9 Q oranje donker / lijn
    (98, 90, 106),     # 10 g zwartvlak licht
    (41, 36, 49),      # 11 G zwartvlak
    (255, 172, 180),   # 12 p roze
    (222, 106, 123),   # 13 P roze donker
    (24, 16, 24),      # 14 E oog
    (131, 82, 65),     # 15 n oog onder (bruine weerglans)
]
KEYS = dict(K=1, a=2, b=3, c=4, e=5, o=6, O=7, q=8, Q=9, g=10, G=11, p=12, P=13, E=14, n=15)

# bol: per rij (y, x-links-omlijning, x-rechts-omlijning, einde zwartvlak, begin oranje)
BALL = [
    (19, 27, 35, 28, 34), (20, 25, 37, 28, 34), (21, 23, 39, 28, 34), (22, 21, 41, 28, 34), (23, 20, 42, 28, 34),
    (24, 19, 43, 28, 34), (25, 18, 44, 28, 35), (26, 18, 44, 28, 35), (27, 17, 45, 27, 36), (28, 17, 45, 27, 36),
    (29, 17, 45, 27, 36), (30, 17, 45, 27, 36), (31, 17, 45, 26, 36), (32, 17, 45, 26, 37), (33, 17, 45, 25, 37),
    (34, 17, 45, 23, 37), (35, 17, 45, 20, 37), (36, 17, 45, 0, 37), (37, 17, 45, 0, 37), (38, 17, 45, 0, 37),
    (39, 18, 44, 0, 37), (40, 18, 44, 0, 37), (41, 19, 43, 0, 37),
]


def ball(c):
    for y, xl, xr, be, os_ in BALL:
        row = {}
        row[xl] = 'K'
        row[xr] = 'K'
        for x in range(xl + 1, xr):
            if x <= be:
                ch = 'G'
            elif x >= os_:
                ch = 'O'
            else:
                ch = 'b'
            row[x] = ch
        for x, ch in row.items():
            c.put(x, y, [ch])


# Met de hand: schaduw, lichtrand, haarlokken (korte strengen), middenscheiding
SHADE = [
    # middenscheiding en kruinglans
    (31, 20, "c"), (31, 21, "c"), (30, 20, "a"), (29, 21, "aa"), (32, 21, "a"),
    (30, 22, "a"), (33, 22, "c"), (29, 23, "a"),
    # zwartvlak: lichtrand linksboven + strengen
    (26, 20, "gG"), (24, 21, "gg"), (22, 22, "g"), (21, 23, "g"), (20, 24, "g"), (19, 25, "g"), (19, 26, "g"),
    (18, 27, "g"), (18, 28, "g"), (25, 23, "g"), (24, 24, "g"), (23, 25, "g"), (27, 24, "g"), (26, 25, "g"),
    # oranje: licht bij de scheiding, schaduw rechts
    (34, 20, "oo"), (34, 21, "oo"), (34, 22, "o"), (35, 22, "o"), (34, 23, "o"), (35, 24, "o"),
    (36, 25, "o"), (36, 26, "o"),
    (38, 20, "q"), (39, 21, "qq"), (40, 22, "q"), (41, 23, "Q"), (40, 23, "q"), (41, 24, "qQ"), (42, 25, "qQ"),
    (42, 26, "qQ"), (43, 27, "qQ"), (43, 28, "qQ"), (42, 29, "qqQ"), (42, 30, "qqQ"), (42, 31, "qqQ"),
    (42, 32, "qqQ"), (41, 33, "qqqQ"), (41, 34, "qqqQ"), (40, 35, "qqqqQ"), (40, 36, "qqqqQ"),
    (39, 37, "qqqqqQ"), (39, 38, "qqqqqQ"), (39, 39, "qqqqQ"), (38, 40, "qqqqqQ"),
    (38, 26, "q"), (39, 27, "q"), (39, 30, "q"), (38, 33, "q"), (37, 23, "q"), (38, 24, "q"),
    # wit: schaduw onderaan en langs het oranje
    (35, 30, "c"), (35, 31, "c"), (36, 32, "c"), (35, 33, "cc"), (35, 34, "cc"), (35, 35, "cc"),
    (34, 36, "ccc"), (33, 37, "cccc"), (18, 37, "c"), (18, 38, "cc"), (31, 38, "cccccc"),
    (19, 39, "cc"), (28, 39, "ccccccccc"), (19, 40, "c"), (24, 40, "ccccccccccccc"),
]

EYE = [
    ".EEE.",
    "EaaEE",
    "EaaEE",
    "EEEEE",
    "EEnnE",
    ".EEE.",
]

# zoom van lokken onder de bol (wit links, oranje rechts), punten krullen naar buiten
HEM = [  # x=14, y=39
    "....K.........................K",
    "...KbK......................KqQK",
    "..KbbcKb..................bKqqqQK",
    ".KbbbcKbbc..............qqOKqqqQK",
    "KbbbcK.KbcK..KK..KK..KqqK.KqqqQK",
    "KbbcK..KbbcKKbcKKbqKKqqK...KqqQK",
    "KbcK....KbcKKbcK.KqqKqqK....KqQK",
    "KcK.....KccKKccK.KqQKqQK.....KQK",
    ".K.......KK.KKK...KKK.KK......K",
]
FEET = [  # x=22, y=46
    "..........",
    "KpPK..KpPK",
    "KPK....KPK",
]

EAR_L = [  # x=16, y=15
    "..KKK",
    ".KgGGK",
    "KGpPGK",
    "KGpPK",
    ".KKK",
]
EAR_R = [  # x=40, y=14
    ".KKK",
    "KoOqK",
    "KpPqQK",
    "KpPqK",
    ".KKK",
]


def frame(f=0):
    c = Canvas(KEYS)
    c.put(16, 15 + f, EAR_L)
    c.put(40, 14 + f, EAR_R)
    ball(c)
    for x, y, s in SHADE:
        c.put(x, y, [s])
    c.put(14, 39, HEM)
    # ogen: links in het zwarte vlak met een witte ring, rechts op wit
    c.put(19, 27, [".bbbbb.", "bb...bb", "b.....b", "b.....b", "b.....b", "bb...bb", ".bbbbb."])
    c.put(20, 28, EYE)
    c.put(31, 28, EYE)
    # neusje en omega-mondje
    c.put(26, 34, ["pP"])
    c.put(25, 35, ["e.e.e"]) if False else c.put(25, 35, [".K.K"])
    c.put(24, 36, ["K.K.K"])
    return c


if __name__ == '__main__':
    out = sys.argv[1]
    f1 = frame(0)
    f2 = frame(1)
    print('area', f1.area())
    save([f1, f2], PAL, out + '/anim_front.png', out + '/normal.pal')
