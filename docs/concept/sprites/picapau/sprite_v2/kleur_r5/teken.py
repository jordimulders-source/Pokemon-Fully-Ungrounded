"""Ronde 5 vanaf r4 (afwerken). Zie NOTITIES.md voor de uitleg per zone.
1. Kop rechts (kuif, kruin, achterkant tot de nek) = r2 (de versie van Jordi's krabbel), plus alleen de
   aanpassingen op de plekken van zijn twee lijnen, volgens de render/toonkaart.
2. Lijfvolume (r29-43) volgens blender/B1/toonkaart_1x.png: licht op de bolling, basis, brede schaduw rechts/onder, dij-bult.
3. Tenen korter en ronder.
Vleugel, oog, wang, snavel, borstomtrek, staart: r4 (0 px)."""
R4 = [l.rstrip('\n') for l in open('../kleur_r4/raster.txt')][:64]
R2 = [l.rstrip('\n') for l in open('../kleur_r2/raster.txt')][:64]
G = [list(r) for r in R4]
# --- 1. kop rechts uit r2 ---------------------------------------------------------------
ZONE = set()
for y in range(3, 12):            # kuif (beide kegels, zwarte toppen) hele rij
    ZONE |= {(x, y) for x in range(64)}
ZONE |= {(x, 12) for x in range(25, 64)}      # kruin onder de kegelbasis
for y in range(13, 25):           # rechts van het oog (r2-oog x25-28, dus vanaf x29) tot de nek
    ZONE |= {(x, y) for x in range(29, 64)}
for x, y in ZONE:
    if R4[y][x] in 'cC':          # wang blijft r4 (bevroren)
        continue
    G[y][x] = R2[y][x]
# Jordi's lijn 1 (schuin, (34,9)->(30,13)): naad voorste kegel / achterste kegel volgens de render
LIJN1 = {(35, 9): '2', (32, 10): '3', (34, 10): '2', (31, 11): '3', (30, 12): '3'}
# Jordi's lijn 2 (verticaal, x35-36 r10-15): donkere achterrand van kop/achterste kegel, lob A licht ernaast
LIJN2 = {(36, 13): '4', (36, 14): '4'}
for (x, y), c in {**LIJN1, **LIJN2}.items():
    G[y][x] = c
# naad r4-voorhoofd | r2-kop: hooglicht doorlopend maken (anders losse 1-pixel)
G[14][28] = '1'; G[15][27] = '1'; G[15][28] = '1'
# --- 2. lijfvolume ------------------------------------------------------------------------
WING = {29: 33, 30: 33, 31: 33, 32: 34, 33: 35, 34: 36, 35: 41, 36: 43, 37: 44, 38: 44, 39: 44,
        40: 45, 41: 45, 42: 45, 43: 46}
LIJF = {
 29: (25, '4' + '3333' + '222'),
 30: (24, '4' + '2222' + '111' + '2'),
 31: (24, '4' + '222' + '11111'),
 32: (24, '4' + '222' + '11111' + '2'),
 33: (24, '4' + '222' + '11111' + '22'),
 34: (24, '4' + '2222' + '1111' + '222'),
 35: (24, '4' + '22222' + '111' + '222222' + '33'),
 36: (25, '4' + '2'*14 + '333'),
 37: (25, '4' + '2'*14 + '3333'),
 38: (26, '4' + '2'*13 + '3333'),
 39: (26, '4' + '2'*13 + '3'*4),
 40: (27, '4' + '33' + '222' + '1' + '22222' + '3'*6),
 41: (27, '4' + '33' + '22' + '111' + '22' + '3'*8),
 42: (28, 'k' + '3' + '222' + '11' + '2' + '3'*9),
 43: (29, 'k' + '22222' + '3'*11),
}
for y, (x0, s) in LIJF.items():
    assert x0 + len(s) == WING[y], (y, x0 + len(s), WING[y])
    assert G[y][x0] in '4k' and G[y][x0 - 1] == '.', y      # omtrek ongewijzigd
    for i, c in enumerate(s):
        G[y][x0 + i] = c
# --- 3. tenen -----------------------------------------------------------------------------
for y in (47, 48, 49):
    for x in range(20, 40):
        if y == 47 and x in (31, 32):   # nabij been blijft
            continue
        G[y][x] = '.'
VOET = {47: [(34, 'GGGk')], 48: [(27, 'ggGggG')], 49: [(26, 'kGG'), (30, 'GGGk')]}
for y, segs in VOET.items():
    for x0, s in segs:
        for i, c in enumerate(s):
            G[y][x0 + i] = c
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in G) + '\n')
print('\n'.join('%2d ' % y + ''.join(G[y][14:54]) for y in range(2, 58)))
