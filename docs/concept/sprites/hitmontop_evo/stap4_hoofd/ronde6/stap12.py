"""Stap 1 (uitsnede) en stap 2 (180 graden + licht terug naar linksboven), als bewerking op Hitmontops pixels."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hulp import *

def stap1():
    d = top_idx(); D = {}
    for (x, y), i in d.items():   # zelfde regel als stap3b KOP: geen blauw lijf, geen handen, polsbanden of armstokjes
        if 12 <= x <= 54 and 34 <= y <= 58 and i not in (6, 7, 8, 9, 12, 13, 14) and not (x <= 17 and y <= 36) \
           and (x - 47) ** 2 + (y - 38) ** 2 > 15 and not (43 <= x <= 48 and y <= 35):
            D[(x, y)] = i
    return D

def stap2(D):
    R = {(63 - x, 63 - y): i for (x, y), i in D.items()}          # 180 graden: hoorn boven
    # ogen: elk oog in zijn eigen 4x4-vak terugdraaien, zodat het witte puntje weer linksboven zit (Hitmontops eigen oog)
    for (ex, ey) in ((27, 18), (36, 20)):
        blok = {(x, y): R[(x, y)] for x in range(ex, ex + 4) for y in range(ey, ey + 4) if (x, y) in R}
        for (x, y), i in blok.items():
            q = (2 * ex + 3 - x, 2 * ey + 3 - y)
            if q in blok: R[(x, y)] = blok[q]
    # licht: de lichtvlek (2) zat na het draaien rechtsonder op het gezicht -> gespiegeld naar linksboven op de schedel
    hl = [p for p, i in R.items() if i == 2 and 32 <= p[0] <= 38 and 22 <= p[1] <= 28]
    for p in hl: R[p] = 3
    for (x, y) in hl:
        q = (x - 9, y - 10)     # verschuiving naar de schedel boven het linkeroog
        if R.get(q) in (3, 4): R[q] = 2
    # flappen: links lag in de schaduw (was rechts), rechts in het licht -> links een toon lichter, rechts een toon donkerder
    for (x, y), i in list(R.items()):
        if x <= 20 and i in (3, 4): R[(x, y)] = i - 1
        if x >= 41 and i in (2, 3): R[(x, y)] = i + 1
    return R
