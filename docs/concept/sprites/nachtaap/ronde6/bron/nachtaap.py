"""Nachtaap fase 1, ronde 6: met de hand getekend (ASCII per pixel), skelet Aipom/Abra, palet = Aipom-rampen gedraaid."""
import sys, colorsys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from lib import Canvas, save


def rot(c, dh=0.0, s=1.0, hue=None):
    h, l, ss = colorsys.rgb_to_hls(*[v / 255 for v in c])
    h = hue if hue is not None else (h + dh) % 1
    r, g, b = colorsys.hls_to_rgb(h, l, min(1, ss * s))
    return tuple(int(round(v * 255)) for v in (r, g, b))


def g3(c):  # naar 5-bit GBA-waarden (x8, max 248 -> 255)
    return tuple(min(255, (v >> 3) * 8 + ((v >> 3) * 8 >> 5)) for v in c)


# Aipom normal_gba.pal: paars 213,131,255 / 180,98,230 / 139,57,180 / 82,32,106; creme 255,246,197 / 255,238,164 / 238,197,90
DH = -0.035  # iets blauwer: 'dieper violet' met indigo-rand
PAL = [(152, 208, 160)]
PAL.append((49, 24, 74))                          # 1 K omlijning (donker violet, zoals Aipom)
PAL.append(g3(rot((82, 32, 106), DH, 1.0)))       # 2 d
PAL.append(g3(rot((139, 57, 180), DH)))           # 3 m
PAL.append(g3(rot((180, 98, 230), DH)))           # 4 l
PAL.append(g3(rot((213, 131, 255), DH)))          # 5 h
PAL.append((189, 172, 230))                       # 6 s gezichtsschaduw (lila)
PAL.append((230, 222, 255))                       # 7 f gezicht (bleek lila)
PAL.append((255, 255, 255))                       # 8 w
PAL.append((0, 148, 189))                         # 9 c iris donker
PAL.append((74, 222, 238))                        # 10 C iris
PAL.append((189, 255, 255))                       # 11 B gloed
PAL.append((16, 32, 74))                          # 12 p pupil
PAL.append((205, 98, 156))                        # 13 r roze donker
PAL.append((255, 164, 205))                       # 14 R roze licht
PAL.append((74, 57, 172))                         # 15 i indigo rand

KEYS = dict(K=1, d=2, m=3, l=4, h=5, s=6, f=7, w=8, c=9, C=10, B=11, p=12, r=13, R=14, i=15)

HEAD = [  # x=15, y=11
    ".........KKKKKKKK",
    "......KKK" + "lhhhllmm" + "KKK",
    "....KK" + "lhhhllllllmmmd" + "KK",
    "...K" + "lhhhllllllllllmmmd" + "K",
    "..K" + "lh" + "iiiiii" + "mddm" + "iiiiii" + "md" + "K",
    ".K" + "l" + "ii" + "ffffff" + "i" + "dd" + "i" + "ffffff" + "ii" + "d" + "K",
    ".K" + "i" + "f" * 9 + "ii" + "f" * 9 + "i" + "K",
    "K" + "l" + "i" + "f" * 20 + "i" + "d" + "K",
    "K" + "l" + "i" + "f" * 19 + "s" + "i" + "d" + "K",
    "K" + "l" + "i" + "f" * 19 + "s" + "i" + "d" + "K",
    "K" + "l" + "i" + "f" * 19 + "s" + "i" + "d" + "K",
    "K" + "m" + "i" + "f" * 19 + "s" + "i" + "d" + "K",
    "K" + "m" + "i" + "f" * 19 + "s" + "i" + "d" + "K",
    "K" + "m" + "i" + "f" * 19 + "s" + "i" + "d" + "K",
    "K" + "m" + "i" + "f" * 19 + "s" + "i" + "d" + "K",
    "K" + "m" + "i" + "f" * 19 + "s" + "i" + "d" + "K",
    ".K" + "i" + "f" * 18 + "ss" + "i" + "K",
    ".K" + "i" + "s" + "f" * 16 + "sss" + "i" + "K",
    "..K" + "i" + "s" + "f" * 13 + "ssss" + "i" + "K",
    "...K" + "i" + "ss" + "f" * 9 + "sssss" + "i" + "K",
    "....K" + "ii" + "s" * 12 + "ii" + "K",
    "......KK" + "iissssssii" + "KK",
    "........KKKKKKKKKK",
]

EYE_L = [
    "...KKK...",
    ".KKiiiKK.",
    ".KCCCCCK.",
    "KCwCCCCCK",
    "KCCCCppCK",
    "KCCCCppCK",
    "KCCCCCCCK",
    ".KCCCCCK.",
    ".KBBCBBK.",
    "..KKKKK..",
]
EYE_R = [r.replace('CCCCppCK', 'CCCppCCK') for r in EYE_L]

EAR_L = [
    ".KKK.",
    "KlRrK",
    "KlRrK",
    "KlRrK",
    ".KlrK",
    "..KK.",
]
EAR_R = [
    ".KKK.",
    "KrRdK",
    "KrRdK",
    "KrrdK",
    "KrdK.",
    ".KK..",
]

TORSO = [  # x=21, y=32
    "..KmmmmmmmK",
    ".KlmmmmmmmdK",
    "KlmffffffsmdK",
    "KlfffffffssdK",
    "KmfffffffssdK",
    "KmfffffffsmdK",
    "KmmffffffsmdK",
    "KdmmffffsmmdK",
    ".KdmmsssmmdK",
    "..KddmmmddK",
    "...KKKKKK",
]
LEG_L = [  # x=14, y=37  knie onder de elleboog
    "...KKKKK",
    "..KlhllmK",
    ".KlhllmmdK",
    ".KllmmmmdK",
    ".KlmmmmmdK",
    "..KmmmmddK",
    "...KddddK",
    "....KKKK",
]
FOOT_L = [  # x=9, y=44
    "......KKKKKKK",
    "...KKKlllmmdK",
    "..KRlKllmmmdK",
    ".KRRKRlKmmddK",
    "..KK.KK.KKKK",
]
LEG_R = [  # x=30, y=36  knie omhoog
    "..KKKKK",
    ".KlmmmmK",
    "KlmmmmmdK",
    "KmmmmmmdK",
    "KmmmmmmdK",
    "KmmmmmddK",
    "KdmmmmddK",
    ".KdmmddK",
    "..KKKKK",
]
HAND_R = [  # x=30, y=38  hand over de knie
    "..KKKKK",
    ".KllmmdK",
    ".KRlRlRK",
    ".KRKRKRK",
    "..K.K.K",
]
FOOT_R = [  # x=26, y=44
    "...KKKKKK",
    "..KlmmmmdK",
    ".KllmmmmddK",
    ".KRlRlRmddK",
    "..KRKRKKKK",
]
ARM = [  # x=10, y=28  onderarm omhoog, bovenarm schuin naar de schouder
    ".KlmK",
    ".KlmK",
    ".KlmK",
    ".KlmK",
    ".KlmdK..KKK",
    ".KlmdK.KlmdK",
    "..KlmdKlmdK",
    "..KlmmmmdK",
    "...KddddK",
    "....KKKK",
]
HAND_L = [  # x=11, y=23
    ".KK.KK.KK",
    "KRRKRRKRRK",
    "KlRKlRKlRK",
    ".KlKllKlmK",
    ".KlllllmK",
    "..KlllmK",
]
SPIRAL = [  # x=39, y=28
    "...KKKKK",
    ".KKlllmmKK",
    "KllKKKKKmmK",
    "KlK.....KmdK",
    "KlK.KKK..KdK",
    "KlK.KlmK.KdK",
    "KlK..KmK.KdK",
    ".KmKKmmK.KdK",
    "..KmmdK..KdK",
    "...KKK...KdK",
    ".........KdK",
]
STEM = [  # x=37, y=40
    "...........KdK",
    "...........KdK",
    "..........KmdK",
    "........KKmdK",
    ".....KKKmmdK",
    "..KKKmmmdKK",
    ".KmddddKK",
    ".KKKKKK",
]


def frame(up=0):
    head = HEAD[:13] + HEAD[14:]          # kop 22 hoog
    eye_l = EYE_L[:6] + EYE_L[7:]         # ogen 9 hoog
    eye_r = EYE_R[:6] + EYE_R[7:]
    c = Canvas(KEYS)
    c.put(39, 28 - up, SPIRAL)
    c.put(37, 39, STEM)
    if up:
        c.put(48, 38, ["KdK"])
    c.put(21, 31, TORSO)
    c.put(11, 18, EAR_L)
    c.put(40, 18, EAR_R)
    c.put(15, 11, head)
    c.put(18, 17, eye_l)
    c.put(29, 17, eye_r)
    c.put(27, 26, ["KK"])
    c.put(25, 28, ["i....i", ".iiii."])
    c.put(15, 36, LEG_L)
    c.put(10, 43, FOOT_L)
    c.put(28, 35, LEG_R)
    c.put(25, 43, FOOT_R)
    c.put(28, 37, HAND_R)
    c.put(10, 28 - up, ARM)
    if up:
        c.put(10, 35, ["..KlmmmmdK"])
    c.put(8, 22 - up, HAND_L)
    if up:  # tweede frame: de ogen gloeien op
        c.put(20, 24, ["BBBBB"])
        c.put(31, 24, ["BBBBB"])
        c.put(19, 23, [".BCCCB"])
        c.put(30, 23, [".BCCCB"])
    for x, y, s in DETAIL:
        c.put(x, y - (up if y < 0 else 0), [s])
    # gekleurde omlijning aan de lichtkant (met de hand gekozen punten; alleen waar nu zwart staat)
    for x, y in SELOUT:
        yy = y - up if (x, y) in MOVES_WITH_ARM else y
        if c.px[yy][x] == KEYS['K']:
            c.px[yy][x] = KEYS['m'] if (x, y) in SELOUT_LIGHT else KEYS['d']
    return c


SELOUT = [(21, 12), (22, 12), (23, 12), (19, 13), (20, 13), (18, 14), (17, 15), (16, 16), (16, 17),
          (13, 18), (14, 18), (11, 19), (11, 20), (11, 21),
          (11, 28), (11, 29), (11, 30), (11, 31),
          (39, 31), (39, 32), (39, 33), (39, 34), (43, 28), (44, 28), (45, 28),
          (16, 38), (16, 39), (16, 40), (14, 44), (15, 44), (31, 35), (32, 35), (33, 35)]
SELOUT_LIGHT = {(21, 12), (22, 12), (19, 13), (18, 14), (17, 15), (11, 29), (11, 30), (39, 32), (39, 33), (16, 39), (43, 28), (44, 28)}
SELOUT += [(24, 11), (25, 11), (26, 11), (20, 13), (12, 32), (12, 33), (13, 34), (12, 22), (13, 22), (9, 23), (8, 24)]
MOVES_WITH_ARM = {(11, 28), (11, 29), (11, 30), (11, 31), (43, 28), (44, 28), (45, 28), (39, 31), (39, 32), (39, 33), (39, 34)}

DETAIL = [  # met de hand: vachtaccenten en schaduwclusters
    (19, 13, "KKlhhllllllmlmmdKK"),
    (18, 14, "KlhhlllllmllllmmmddK"),
    (31, 36, "h"),
    (22, 34, "l"),
]


if __name__ == '__main__':
    out = sys.argv[1]
    f1 = frame(0)
    f2 = frame(1)
    print('area', f1.area())
    save([f1, f2], PAL, out + '/anim_front.png', out + '/normal.pal')
