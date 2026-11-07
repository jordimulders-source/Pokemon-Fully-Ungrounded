"""Controle bij het typen: vergelijkt het masker van lama_raster.txt met silhouet ronde 6 plus de gemelde afwijkingen."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R6 = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../../../silhouet_r6/ronde6.txt'))]
PLUS = [(48, 23), (49, 23)]; MIN = [(46, 25), (51, 26), (43, 25), (44, 25), (45, 25)]
for x, y in PLUS: R6[y][x] = '#'
for x, y in MIN: R6[y][x] = '.'
g = [l.rstrip('\n') for l in open(os.path.join(HERE, 'lama_raster.txt'))]
for y in range(64):
    bad = [x for x in range(64) if (R6[y][x] == '#') != (g[y][x] != '.')]
    if bad: print('rij', y, 'verschil bij x', bad)
print('klaar')
