"""Cuyby fase 1, ronde 3: polijstronde van ronde 2 (silhouet en ontwerp ongewijzigd).

De hele sprite staat hieronder als tekstraster (x 14..48, y 16..47), met de hand rij voor rij herschreven vanuit
ronde 2. Geen vormfuncties, geen automatische schaduw of omlijning. Draaien vanuit de repo-root:
    python3 docs/concept/sprites/cuyby/ronde3/bron/cuyby.py docs/concept/sprites/cuyby/ronde3
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../nachtaap/ronde7/bron'))
from lib import Canvas, save, zoom

# Palet: oranje = Vulpix-lijframp (238,156,74 / 205,123,41 / 172,90,8, omlijning 148,49,0), iets lichter
# hooglicht; crème = wit-crème met een warme schaduw; de crème-omlijningsbasis is donkerder dan in ronde 2
# (164,131,90 las als een onderbroken lijn); zwart vlak = basis + glans, schaduw = de omlijning zelf (Scorplack-aanpak).
PAL = [
    (152, 208, 160),  # 0  transparant
    (41, 24, 24),     # 1  K omlijning (schaduwkant)
    (255, 255, 246),  # 2  a crème hooglicht / glans
    (246, 238, 205),  # 3  b crème basis
    (222, 205, 156),  # 4  c crème schaduw
    (139, 106, 65),   # 5  e crème omlijningsbasis
    (255, 197, 123),  # 6  o oranje hooglicht
    (238, 156, 74),   # 7  O oranje basis
    (205, 115, 41),   # 8  q oranje schaduw
    (148, 57, 0),     # 9  Q oranje omlijningsbasis
    (106, 98, 115),   # 10 g zwart vlak: glans
    (49, 41, 57),     # 11 G zwart vlak: basis
    (255, 172, 180),  # 12 p roze
    (222, 106, 123),  # 13 P roze schaduw
    (24, 16, 24),     # 14 E oog
    (156, 98, 74),    # 15 n gekleurde weerkaatsing in het oog
]
KEYS = dict(K=1, a=2, b=3, c=4, e=5, o=6, O=7, q=8, Q=9, g=10, G=11, p=12, P=13, E=14, n=15)

X0, Y0 = 14, 16
GRID = [
    ".......KKK................QqQ......",  # 16 oortoppen (rechts: hooglicht als omlijning)
    "......KgGGK..............QoOqK.....",  # 17
    ".....KgpPGK..KGGKeeQqqQ.KopPqK.....",  # 18 kruin: zachte omlijning op de belichte top
    ".....KGpPGKKKggGGaboooOqQopPqK.....",  # 19 glansband zwart vlak begint; oranje licht bij de scheiding
    "......KGGKGggGgGGabooOOOqKqQK......",  # 20
    "......KKGggGGGGGGabcoOOOOqqQK......",  # 21
    ".......GggGGGGGGGabcooOOqOqqQ......",  # 22 gekartelde vachtgrens in het oranje
    "......GggGGGGgGGaaabboOOOOqqqQ.....",  # 23 voorhoofd crème met hooglicht linksboven
    ".....GgGGGGGGgGGaabbboOOOqOqqqQ....",  # 24 haarstreek in het zwart (g) richting de scheiding
    ".....GgGGGGGGGgGbabbbOOOOqOqqqQ....",  # 25
    "....GgGGGGGGGGGbbbbbbcOOOqOOqqqQ...",  # 26 crème schaduw langs het oranje (de bol draait weg)
    "....KgGgggGGGGbbbbbbbcOOOOqOqqqQ...",  # 27 lichte rand boven het linkeroog
    "...KgGgEEEgGGbbbbEEEbccOOOOqqqqqQ..",  # 28 ogen: lichte rand (g) om het linkeroog
    "...KggEaaEEgbbbbEaaEEbcOOOOqOqqqQ..",  # 29 glans linksboven
    "...KGgEaaEEbbbbbEaaEEbcOOOOOOqqqQ..",  # 30
    "...KGgEEEEEbbbbbEEEEEbcOOOOOqqqqQ..",  # 31
    "...KGgEEnnEbbbbbEEnnEbcOOOOqOqqqQ..",  # 32 gekleurde weerkaatsing rechtsonder
    "...KGGbEEEbbbbbbbEEEbccOOOOqqqqqQ..",  # 33
    "...ebbbbbbbbbpPbbbbbbcccOOOqqqqqQ..",  # 34 neusje
    "...ebbbbbbbbbebbbbbbbcccOOOqqqqqQ..",  # 35 mondje
    "....ebbbbbbbebebbbbbbcccOOqqqqqQ...",  # 36
    "....ebbbbbbbbbbbbbbbccccOqqqqqqQ...",  # 37
    ".....ebbbbbbbbbbbcbbccccOqqqqqQ....",  # 38 haarstrengen beginnen (c) boven de lokscheidingen
    ".....ebbcbbbbcbbbbbcbcccOqqqqqQ....",  # 39
    "....KcbcbbbbbcbbbbbbccccOOqqqqqQ...",  # 40 onder de evenaar: zwarte omlijning aan de schaduwkant
    "...KcbbccbbbbccbbbbbccbcOOqOqqqqQ..",  # 41
    "...KcbcebbbbccbbbbbccbccOqQOqqqqQ..",  # 42 lokscheiding in omlijningsbasis
    "..KcbccKbbbccKbbbbccKbccOqKOqqqQ...",  # 43 ... en onderaan zwart (schaduw)
    "..KcK..KbbbcKKbbbbbcKKbcOqK..KQK...",  # 44 lokpunten
    "...K....KbcKpPKbbbcKpPKbqK....K....",  # 45 voetjes
    ".........KK.KK.KbcK.KK.KK..........",  # 46
    "................KK.................",  # 47
]

# frame 2: popcornsprongetje: alles 1 px omhoog, mondje open (fluiten)
F2 = [(25, 34, "bKKKb"), (25, 35, "KPPPK"), (26, 36, "KKK")]


def frame(f=0):
    c = Canvas(KEYS)
    dy = -1 if f else 0
    c.put(X0, Y0 + dy, GRID)
    if f:
        for x, y, s in F2:
            c.put(x, y, [s])
    return c


if __name__ == '__main__':
    assert all(len(r) == 35 for r in GRID), [i for i, r in enumerate(GRID) if len(r) != 35]
    out = sys.argv[1]
    f1, f2 = frame(0), frame(1)
    print('oppervlak', f1.area())
    save([f1, f2], PAL, os.path.join(out, 'anim_front.png'), os.path.join(out, 'normal.pal'))
    if len(sys.argv) > 2:
        zoom(f1, PAL, sys.argv[2], sc=10)
