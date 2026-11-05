"""Ronde 2: met de hand bijgewerkt vanaf kleur_r1/raster.txt (alleen snavel, kop-/borst-/buiklicht, voetjes,
achterste kuifpunten). Elke wijziging als (rij, x, tekens); '_' = transparant maken. Uitvoer: raster.txt."""
G = [list(l.rstrip('\n')) for l in open('../kleur_r1/raster.txt')][:64]
E = [
 # --- 2. snavel: lang (punt x13), bleek, taps, donkere onderrand G, korte lijn 4 in het gezicht ---
 (16, 13, 'gg'),
 (17, 14, 'Ggg'),
 (18, 15, 'Ghggh2'),
 (19, 16, 'Ghhh4'),
 (20, 17, 'Ghh4'),
 (21, 17, 'Ggg4'),
 (22, 18, 'Gg3'),
 (23, 19, 'G3'),
 # --- 1. koplicht: één ronde vlek op de bol ---
 (14, 25, '21111'),
 (15, 24, '211111'),
 (16, 25, '21112'),
 # --- 4. achterste kuifpunten: 3 px aan de basis, taps, lichter gevuld ---
 (13, 36, '333'),
 (16, 37, '34'),
 (17, 38, '344'),
 # --- 1. borst: één licht op de bolling linksboven, loopt naar rechtsonder over in de basis ---
 (29, 25, '42112223'),
 (30, 25, '4211112233'),
 (31, 26, '421111222'),
 (32, 26, '422111222'),
 (33, 26, '4221122233'),
 (34, 26, '4222222223'),
 (35, 26, '42222222333'),
 (36, 27, '42222222333'),
 # --- 1. buik/dij: basis links, brede schaduwsikkel langs de onderkant en rechts ---
 (37, 27, '4222222233333333'),
 (38, 28, '422222223333333'),
 (39, 28, '4222222233333333'),
 (40, 28, '4222222333333333'),
 (41, 28, '42222223333333333'),
 (42, 29, '4222223333333333'),
 (43, 29, 'k222233433333333'),
 (44, 29, 'k22333433333333333'),
 # --- 3. voetjes: tenen in pootkleur, zwart alleen onder/schaduwkant, klauwen als haakjes; verre poot donker, achter ---
 (45, 29, 'Ggkk'),          # nabije loopbeen + buikrand ertussen
 (45, 33, 'kGk'),           # verre loopbeen
 (46, 26, 'GGGggk_kGk'),
 (47, 25, 'Gggggggg_kGGGk'),
 (48, 24, 'kGGGGGGGG_kkkk'),
 (49, 24, '_________k____k'),
]
for y, x, s in E:
    for i, ch in enumerate(s):
        G[y][x + i] = '.' if ch == '_' else ch
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in G) + '\n')
