"""Lijf uit silhouet + schaduw, daaroverheen de kop/voorpoten met de hand, daarna handcorrecties."""
import sys, subprocess, os
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from frame1 import F1, write

subprocess.run(['python3', D + '/sil.py', D + '/sil.txt'], check=True)
subprocess.run(['python3', D + '/shade.py', D + '/sil.txt', D + '/sil_sh.txt'], check=True)
rows = [list(l[:64].ljust(64, '.')) for l in open(D + '/sil_sh.txt').read().split('\n')[1:65]]


from cloud import cloud
_cm, _ci = cloud()
_sil = [l[:64].ljust(64, '.') for l in open(D + '/sil.txt').read().split('\n')[:64]]
CH = '.123456789abcdef'
for y in range(64):
    for x in range(64):
        if _sil[y][x] == 'W':
            v = CH[_ci[y, x]]
            if v in 'f4' and any(_sil[y + dy][x + dx] == 'N' for dx, dy in ((-1, 0), (0, -1), (-1, -1), (0, 1), (-1, 1))):
                v = '3'
            rows[y][x] = v


def seg(y, x, s):
    for i, ch in enumerate(s):
        if ch != ' ':
            rows[y][x + i] = ch


# kop
for y, segs in F1.items():
    for x, s in segs:
        if y <= 27 and x < 30:
            seg(y, x, s)
# opgeheven voorpoot met handschoen
for y in range(36, 46):
    for x, s in F1[y]:
        if x < 10:
            seg(y - 4, x, s)
# verre voorpoot met handschoen (staat)
FRONT = {39: [(20, "f766f")], 40: [(20, "f766f")], 41: [(21, "766f")], 42: [(21, "766f")], 43: [(20, "ffffff")],
         44: [(20, "fbbccf")], 45: [(18, "ff9999ff")], 46: [(17, "f99999aaf")], 47: [(16, "f9999999aaf")],
         48: [(16, "f99999aaaaf")], 49: [(17, "faaaaaaaf")], 50: [(18, "fffffff")]}
for y, segs in FRONT.items():
    for x, s in segs:
        seg(y, x, s)

# handcorrecties (komen hierna, per rij)
from fix1 import FIX
for y, segs in FIX:
    for x, s in segs:
        seg(y, x, s)



def selout(rows):
    # zwarte rand linksboven -> donkerste tint van het onderdeel ernaast (Gen 3-selout)
    DARK = {'1': '4', '2': '4', '3': '4', '5': '7', '6': '7', '8': 'a', '9': 'a', 'b': 'c'}
    out = [r[:] for r in rows]
    for y in range(1, 63):
        for x in range(1, 63):
            if rows[y][x] != 'f':
                continue
            up, lf = rows[y - 1][x] == '.', rows[y][x - 1] == '.'
            dn, rt = rows[y + 1][x] == '.', rows[y][x + 1] == '.'
            if (up or lf) and not (dn or rt):
                inner = rows[y + 1][x] if up else rows[y][x + 1]
                if inner in DARK:
                    out[y][x] = DARK[inner]
    return out




def frame2(r1):
    r = [row[:] for row in r1]
    # kop 1 px omlaag (x 0..28), de kin duikt in de wol
    for y in range(27, 2, -1):
        for x in range(0, 32 if y <= 24 else 29):
            r[y + 1][x] = r1[y][x]
    for x in range(0, 32):
        r[3][x] = '.'
    # mond open (schreeuw), met tandje
    for y, x, s in ((24, 2, "fedd7"), (25, 2, "ffdd7"), (26, 3, "ff")):
        for i, ch in enumerate(s):
            r[y][x + i] = ch
    # stoot: handschoen + manchet 2 px naar voren, poot langer (met de hand)
    JAB = {32: "....aaaaf...", 33: "..aa89999afff42", 34: ".f899999999fbffffff",
           35: ".a999999999fbf66666f", 36: ".a999999a9afbf666666f", 37: ".a99999aaaafbf666667f",
           38: ".f999aaaaaafbfffffff", 39: "..f99aaaaafbbf....f", 40: "...f9aaafffff......",
           41: "....ffff............"}
    for y, s in JAB.items():
        for x, ch in enumerate(s):
            r[y][x] = ch
    # staart kwispelt 1 px omhoog
    for y in range(21, 28):
        for x in range(44, 50):
            r[y][x] = r1[y + 1][x] if y + 1 <= 26 or x >= 47 else r1[y][x]
    return r


rows2 = frame2(rows)


def place(r, dx, dy):
    out = [['.'] * 64 for _ in range(64)]
    for y in range(64):
        for x in range(64):
            if 0 <= y - dy < 64 and 0 <= x - dx < 64:
                out[y][x] = r[y - dy][x - dx]
    return out


write(sys.argv[1], [place(selout(rows), 6, 5), place(selout(rows2), 6, 5)])
