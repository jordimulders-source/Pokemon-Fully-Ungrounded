"""Ronde 4 (alleen B): reparaties 1-4 uit kleur_r3/KEURING.md, met de hand gekozen, op kleur_r3/raster_B.txt -> raster.txt."""
import os
D = os.path.dirname(os.path.abspath(__file__))
rows = [list(r.rstrip('\n')) for r in open(os.path.join(D, '..', 'kleur_r3', 'raster_B.txt'))][:64]
def zet(y, x0, s):
    for i, c in enumerate(s):
        if c != '_':
            rows[y][x0 + i] = c
# 1. verre poot: gesloten teentjes in G, zwarte onderrand, geen G tegen transparant
zet(46, 34, 'kGGGk')
zet(47, 34, 'kkkkk')
# 2. nabije poot: lichte randpixels zwart
zet(46, 29, 'k'); zet(47, 28, 'k')
# 3. borstlicht: strook langs de voorrand weg, één vlek op de bolling; streepje in de kuifsteel weg
for x, y in [(27, 29), (28, 29), (27, 30), (28, 30), (29, 30), (28, 31), (29, 31), (30, 31), (28, 32), (29, 32), (29, 33)]:
    rows[y][x] = '2'
for x, y in [(30, 29), (29, 30), (30, 30), (31, 30), (29, 31), (30, 31), (31, 31), (30, 32)]:
    rows[y][x] = '1'
rows[10][31] = '2'; rows[11][31] = '2'
open(os.path.join(D, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in rows) + '\n')
