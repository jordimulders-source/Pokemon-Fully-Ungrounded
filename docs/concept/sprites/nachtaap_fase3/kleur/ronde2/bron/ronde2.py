# Kleurronde 2: één lichtverdeling (linksboven) over het hele lijf + handpalm.
# Alleen kleurindexen binnen de omtrek van 1s; alpha-diff 0; gezicht/maan/gloed/staart vast.
# Met de hand geschreven: rijpatches (y, x, "tekens") en een blok voor romp/schouder.
import os, sys
import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
CH = '.123456789ABCDEF'
g = [list(r) for r in open(os.path.join(HIER, 'basis_1s.txt')).read().split('\n')[:64]]

def zet(y, x, s):
    for i, c in enumerate(s):
        g[y][x + i] = c

# ---- vuistarm (onderarm: licht boven; bovenarm: licht links, schaduw rechts) ----
zet(19, 12, "22222")
zet(20, 10, "445555522")
zet(21, 10, "2344455552")
zet(22, 10, "23344445552")
zet(23, 10, "113344445551")
zet(24, 12, "1344444551")
zet(25, 13, "1134555431")
zet(26, 15, "24554431")
zet(27, 16, "24554431")

# ---- opgeheven been: band consistent, dij loopt licht in de rug over ----
zet(16, 32, "2554431")
zet(17, 32, "2554431")
zet(22, 32, "2554431")
zet(23, 31, "25544331")

# ---- kop-vacht: bol, licht linksboven, rechterrand schaduw + één rand ----
zet(28, 7, "25555441")
zet(29, 6, "2555554431")
zet(30, 6, "55")
zet(31, 5, "55")
zet(33, 7, "444443")
zet(33, 17, "32")
zet(34, 17, "32")
for y in range(35, 43):
    g[y][18] = '3'
zet(43, 14, "33333")
zet(44, 14, "33332")

# ---- romp + schouder + heup (kol 19..49), één bol: licht linksboven ----
blok = {
 28: "55431......2555544331.....2541.",
 29: "455431....225555444331....2541.",
 30: "24554312225555554444331...2541.",
 31: "24554435555555554444331...2541.",
 32: "345543455555555544444331..2541.",
 33: "145554444345555554444331..2541.",
 34: "1455544432455555554443331.2441.",
 35: "214554443244555555544333224441.",
 36: "214554443244555555544433344331.",
 37: "214554443244555555444433333331.",
 38: "214554443244455554444443333331.",
 39: "21455444324444555444444333331..",
 40: "21455444324444444444444333331..",
 41: "2145544432444444444444443331...",
 42: "2145544432444444444444333331...",
 43: "2125544432444444443333333321...",
 44: "12255444323444433333333333442..",
 45: "222554443233333333333333344552.",
 46: "C225544433111245555554444445552",
}
for y, s in blok.items():
    assert len(s) == 31, (y, len(s), s)
    zet(y, 19, s)

# ---- genezersarm onder de romp: licht links, schaduw rechts, één rand ----
zet(47, 21, "555444331")
zet(48, 22, "55444331")
for y in range(51, 55):
    g[y][28] = '3'
zet(55, 24, "5")
zet(56, 27, "3")
zet(57, 24, "4433")
zet(58, 23, "44331")
zet(59, 23, "3331")

# ---- onderbeen: dij licht boven, onderkant schaduw, geen dubbele rand ----
zet(47, 32, "1125555444444445544222")
zet(48, 34, "1244444444444555444222")
zet(49, 35, "12" + "4"*13 + "555" + "44" + "222")
zet(50, 36, "12333333334444444555422")
zet(51, 37, "1" + "3"*14 + "4444" + "55" + "22")
zet(52, 38, "13333333311111333444522")
zet(53, 39, "1133331 1.....1133444552".replace(' ', ''))
zet(54, 55, "3")
zet(55, 56, "3")
zet(56, 57, "3")

# ---- handpalm (binnen de vaste handomtrek) ----
zet(48, 13, "FD")
zet(49, 13, "DEEFD")
zet(50, 10, "FDEDEEDE2")
zet(51, 10, "DEEDEEDEEDE")
zet(52, 10, "DEEDEEDEEDE")
zet(53, 10, "DDEDDEDEEEE")
zet(54, 10, "DDDDFDDDEEE")
zet(55, 10, "DEDFFDDEEEE")
zet(56, 8,  "FDDDEDDDDEEEE")
zet(57, 8,  "DDEDDEDDEEEE")
zet(58, 10, "EEDEEEEEE")

# losse pixels opgeruimd
zet(32, 19, "4"); zet(32, 24, "4"); zet(33, 28, "4"); zet(46, 33, "5")

out = np.array([[CH.index(c) for c in r] for r in g], dtype=np.uint8)
open(os.path.join(HIER, 'ronde2.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
pal = [tuple(map(int, l.split())) for l in open(os.path.join(HIER, '..', 'normal.pal')).read().split('\n')[3:19]]
im = Image.fromarray(out, 'P')
im.putpalette([v for p in pal for v in p])
im.info['transparency'] = 0
im.save(os.path.join(HIER, '..', 'nachtaap_fase3.png'), transparency=0)
print('ok')
