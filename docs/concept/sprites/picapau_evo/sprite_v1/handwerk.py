"""Handwerk op de eerste overtrek (raster_start.txt) -> raster.txt. Elke stap is een plek met een reden (zie NOTITIES).
Gebruik: python3.11 handwerk.py"""
R = [list(l.rstrip('\n')) for l in open('raster_start.txt')][:64]
P = [list(l.rstrip('\n')) for l in open('onderdelen.txt')][:64]
T = [l.rstrip('\n') for l in open('bron/bron_toon.txt') if not l.startswith('#')]

def zet(y, x, s):
    """schrijf string s vanaf (x, y); ' ' = laat staan"""
    for i, c in enumerate(s):
        if c != ' ': R[y][x + i] = c

# 1. verre vleugel: basis v, schaduw 4 (de automatische toon maakte hem bijna zwart); stippen b (verder weg = donkerder)
for y in range(64):
    for x in range(64):
        if P[y][x] == 'F' and R[y][x] not in 'k':
            R[y][x] = '4' if T[y][x] == '0' else 'v'   # alleen de donkerste toon als schaduw: anders werd hij een zwarte manen-vlek achter de kop
        if P[y][x] == 'S' and x < 34 and y < 28 and any(P[b][a] == 'F' for a, b in ((x-1, y), (x+1, y), (x, y-1), (x, y+1))):
            R[y][x] = 'b'

# 2. kuif + verre vleugeltop: vak x 6-34, rij 6-19 opnieuw (oren met de hand, verre vleugel pas vanaf rij 16)
for y in range(6, 20):
    for x in range(6, 35):
        if P[y][x] in 'UIF' or (P[y][x] == 'S' and x < 34): R[y][x] = '.'
# Raichu Gen 1-oren: driehoek (brede basis op de kop), kastanje rand, gedempt lichte binnenkant (b/e, niet wit);
# de punt loopt zelf smal door in een krul naar buiten-omlaag (haak met gaatje), geen ring op een steeltje.
OOR = ['..kkk',          # rij 9, x vanaf 9 (nabije oor)
       '.k122k',
       'k1kk12k',
       'k2k.k12k',
       '.kk.k412k',
       '....41b2k',
       '....41bb2k',
       '....41bbb2k',
       '....41bbe22k',
       '.....41eee2k']
MASK = {(9 + x, 9 + y) for y, r in enumerate(OOR) for x, c in enumerate(r) if c != '.'}
KLR = {(9 + x, 9 + y): c for y, r in enumerate(OOR) for x, c in enumerate(r) if c != '.'}
def omlijn(mask, kleur):
    """buitenrand opnieuw: selout 4 aan de lichtkant (leeg links/boven), zwart aan de schaduwkant"""
    out = {}
    for (x, y) in mask:
        leeg = [(a, b) for a, b in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)) if (a, b) not in mask and b < 19]   # rij 19+ = kop: daar loopt het oor door
        if leeg:
            licht = all(a < x or b < y for a, b in leeg)
            out[(x, y)] = '4' if licht else 'k'
        else:
            out[(x, y)] = kleur[(x, y)]
    return out
NABIJ = omlijn(MASK, KLR)
# verre oor: zelfde vorm gespiegeld om x = 20.5, schaduw weer rechts (1 <-> 2 wisselen), randen opnieuw
SP = {(41 - x, y): {'1': '2', '2': '1'}.get(c, c) for (x, y), c in KLR.items()}
VER = omlijn(set(SP), SP)
for (x, y), c in {**NABIJ, **VER}.items(): R[y][x] = c
# kop-bovenkant onder de oren (de oude oorbasis en het verre-vleugelstukje ertussen weg)
zet(19, 12, '41111111111222234')
zet(20, 13, '4111111112222334')
zet(21, 13, '4111111112222334')
# verre vleugel bovenrand rechts van het oor: vanaf rij 14 (hij stond tot rij 9 tegen het oor)
zet(14, 31, '4kk')
zet(15, 30, 'k4vvk')
zet(16, 30, 'k4vvvk')
zet(17, 30, 'kvvvv4')
zet(18, 29, 'kvvvvv')
zet(19, 29, 'vvvvv')
# 2b. bliksem opnieuw, met een duidelijke Gen 1-knik: bovenste band smal naar linksboven, onderste band breder en
# naar links verspringend (de render gaf alleen een insnoering); zelfde plek en lengte als in de render
for y in range(36, 60):
    for x in range(0, 24):
        if P[y][x] == 'Z': R[y][x] = '.'
BL = set()
for r in range(37, 50):            # bovenste band: breedte als in de render (3 -> 8 px)
    l = (r - 37) * 0.95; rr = l + 1 + (r - 37) * 0.6
    BL |= {(x, r) for x in range(64) if l - 0.5 <= x <= rr + 0.5}
for r in range(50, 59):            # onderste band: 8 px breed, steekt 3 px links uit (knik), loopt taps naar de koord
    l = 8 + (r - 50) * 1.2; rr = 16 + (r - 50) * 0.8
    BL |= {(x, r) for x in range(64) if l - 0.5 <= x <= rr + 0.5}
BL = {p for p in BL if R[p[1]][p[0]] == '.' or P[p[1]][p[0]] in 'ZT'}
# rand per rij: links (lichtkant) oranje selout 1, rechts en onderkant zwart (niet om en om op één rand)
for (x, y) in BL:
    rij = [a for a, b in BL if b == y]
    leeg = [(a, b) for a, b in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)) if (a, b) not in BL and R[b][a] == '.']
    if len(rij) == 1 or x == max(rij): R[y][x] = 'k'
    elif x == min(rij): R[y][x] = '1'
    elif any(b > y for a, b in leeg): R[y][x] = 'k'
    elif leeg: R[y][x] = '1' if x <= (min(rij) + max(rij)) / 2 else 'k'   # bovenrand: links licht, rechts zwart (geen om-en-om)
    else: R[y][x] = 'y' if y < 50 else ('Y' if y < 56 else '1')
# 3. oog: pixel voor pixel van Picapau (af): glans linksboven, iris onder
for y, r in {23: '.kk.', 24: 'Gwkk', 25: 'kkGk', 26: '.kk.'}.items():
    for i, c in enumerate(r):
        if c != '.': R[y][24 + i] = c
        elif R[y][24 + i] == 'k': R[y][24 + i] = '2'
# 4. beitelsnavel (x 7-17, rij 29-33): crème hoorn, selout e boven, zwart onder, punt naar links (9 px lang)
zet(29, 11, 'eeeee4')
zet(30, 9, 'eaaaaab4')
zet(31, 7, 'eaaaabbbbe4')
zet(32, 8, 'kgbbbeeeek')
zet(33, 10, 'kkkkkkk')
# 5. pootjes: klein, grijs, de verre hoger en donkerder (perspectief)
for y in range(52, 57):
    for x in range(20, 35):
        if P[y][x] == 'P' or R[y][x] in 'gG': R[y][x] = '.'
zet(52, 23, 'gGk'); zet(52, 29, 'GGk')
zet(53, 23, 'gGk'); zet(53, 28, 'kGGGk')
zet(54, 20, 'kgggGGk'); zet(54, 28, 'kkkk')
zet(55, 20, 'kkkkkkk')
# 5b. kop- en lijfrand rechts: de automatische binnenlijn werd 2-4 px breed (donkere 'manen' achter de kop).
# Alleen de pixel die echt aan de vleugel grenst blijft binnenlijn 4; de rest wordt schaduwtint 3 (sikkel rechts).
for y in range(19, 36):
    for x in range(20, 40):
        if P[y][x] in 'KL' and R[y][x] == '4' and not (24 <= x <= 27 and 23 <= y <= 26):
            buren = [P[b][a] for a, b in ((x-1, y), (x+1, y), (x, y-1), (x, y+1))]
            if not any(q in 'FVS.' for q in buren): R[y][x] = '3'
# 5c. kop: licht alleen als ovaal linksboven (de toonkaart gaf een groot vlak licht = plat); rest basis 2
for y in range(19, 34):
    for x in range(10, 30):
        if P[y][x] == 'K' and R[y][x] == '1' and ((x - 16.5) / 7.5) ** 2 + ((y - 23.5) / 6.5) ** 2 > 1: R[y][x] = '2'
# 5d. vleugelstippen rond maken (de render gaf blokjes en scherven): elke stip vervangen door een rond sjabloon van
# vergelijkbare grootte op hetzelfde midden (Picapau: ronde stippen); vrijgekomen pixels worden vleugel v
SJ = {2: ['aa', 'ab'], 3: ['.aa.', 'aaab', '.ab.'], 4: ['.aa.', 'aaaa', 'aabb', '.bb.']}
gezien = set(); stippen = []
for y in range(36):                       # stippen = de stip-onderdelen van de render (labelkaart), niet de tintscherven
    for x in range(29, 64):
        if P[y][x] == 'S' and (x, y) not in gezien:
            st = [(x, y)]; comp = []; gezien.add((x, y))
            while st:
                p = st.pop(); comp.append(p)
                for q in ((p[0]+1, p[1]), (p[0]-1, p[1]), (p[0], p[1]+1), (p[0], p[1]-1)):
                    if 0 <= q[0] < 64 and q[1] < 36 and q not in gezien and P[q[1]][q[0]] == 'S': gezien.add(q); st.append(q)
            stippen.append(comp)
for y in range(36):                       # alle oude lichte pixels in de vleugels weg
    for x in range(29, 64):
        if P[y][x] in 'SVF' and R[y][x] in 'ab': R[y][x] = 'v'
for comp in stippen:
    n = len(comp); maat = 4 if n >= 11 else (3 if n >= 5 else 2)
    cx = round(sum(p[0] for p in comp) / n - (maat - 1) / 2); cy = round(sum(p[1] for p in comp) / n - (maat - 1) / 2)
    ver = sum(P[min(63, y+1)][x] == 'F' or P[y][max(0, x-1)] == 'F' for x, y in comp) > n / 2
    for j, r in enumerate(SJ[maat]):
        for i, c in enumerate(r):
            x, y = cx + i, cy + j
            if c != '.' and R[y][x] in 'v3' and P[y][x] in 'SVF':
                R[y][x] = 'b' if ver else c
# 6. opruimen (controlescript): losse tintpixels in een vlak naar de omringende tint, randen zonder om-en-om
def kleur(lijst, c):
    for x, y in lijst: R[y][x] = c
# krul van de oren in één tint (dunne lijn, 8-verbonden), binnenkant zonder losse schaduwpixel
for x in range(8, 34):
    for y in range(9, 14):
        if R[y][x] in '12' and (x < 16 or x > 25): R[y][x] = '2'
kleur([(17, 17), (24, 17)], 'b')
kleur([(13, 19)], '4')                                   # kop-bovenrand links: selout, geen lichte kleur op de rand
kleur([(47, 7), (47, 10), (48, 10), (34, 21), (35, 22)], 'v')   # vleugel: losse lichte pixels tussen de stippen
kleur([(12, 28), (15, 28)], '1')                         # kop links: restjes van de oude snavelrand
kleur([(34, 28), (34, 29)], 'a')                         # stip op de vleugelaanzet heel maken
kleur([(30, 29)], '3')
kleur([(10, 29), (8, 30)], 'e')                          # snavel-bovenrand doorlopend (selout e)
kleur([(9, 32)], 'k')
kleur([(38, 34)], '4')
kleur([(13, 38), (14, 42), (15, 43)], 'e')               # buikrand links (lichtkant) doorlopend selout e, geen k ertussen
kleur([(18, 46)], 'b')
kleur([(32, 57), (21, 59)], '4')                         # koord-bovenrand selout
kleur([(26, 57)], '.')
kleur([(39, 15)], '3')                                   # lichtlijn op de vleugelvoorrand doorlopend
kleur([(23, 51)], '3')
kleur([(21, 60), (22, 59)], '4')
kleur([(40, 34)], 'k')                                   # gaatje van 1 px tussen vleugelonderrand en lijf dicht
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in R) + '\n')
