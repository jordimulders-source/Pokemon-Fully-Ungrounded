"""Ronde 3: met de hand bijgewerkt vanaf kleur_r2/raster.txt, alleen drie zones:
snavel (N-cellen uit bron_labels), poten (P-cellen + klauwhaakjes), borst-voorrand (+1 px waar de render bolt).
Elke wijziging als (rij, x, tekens); '_' = transparant. Uitvoer: raster.txt."""
G = [list(l.rstrip('\n')) for l in open('../kleur_r2/raster.txt')][:64]
E = [
 # --- snavel: kegel, licht boven, basis midden, donker onder, donkere punt, donkere lijn in het gezicht ---
 (16, 13, '__'),
 (17, 14, 'GG__'),
 (18, 15, 'Ggggg'),
 (19, 16, 'G111'),
 (20, 17, 'ghhG'),
 (21, 17, 'GghG'),
 (22, 18, 'GgG3'),
 (23, 19, 'GG3'),
 # --- poten: nabije poot 2 tenen voor + 1 achter, klauwhaakjes; verre poot donker erachter ---
 (45, 29, 'GgGkkGk'),
 (46, 26, '_GGggG_kGk'),
 (47, 25, '_kggggGGkGGGk_'),
 (48, 24, '_k_GGgG__kkk_k_'),
 (49, 24, '____k__________'),
 # --- borst-voorrand: 1 px naar buiten waar de render bolt (dekking >= 0.36) ---
 (31, 25, '42'),
 (32, 25, '42'),
 (33, 25, '42'),
 (36, 26, '42'),
 (38, 27, '42'),
]
for y, x, s in E:
    for i, ch in enumerate(s):
        G[y][x + i] = '.' if ch == '_' else ch
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in G) + '\n')
