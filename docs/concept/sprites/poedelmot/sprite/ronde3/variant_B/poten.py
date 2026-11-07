"""Ronde 3 variant B: voorpoten naar de foto's + vier achterpoten weggestopt zoals Giratina (half zichtbaar).
Neemt ../../ronde2/raster.txt en vervangt de pootzone (rijen 40-44 voor x<=33 en rijen 45-63 helemaal) door de rijen
hieronder. Die zijn met de hand getypt als stukken (x, tekens). Schrijft raster.txt.
Delen: L = nabije voorpoot, R = verre voorpoot, borstwol tussen de poten, P/Q = achterpoten links (Q half achter L),
R1/S = achterpoten rechts (R1 half achter R)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
R = [list(l.rstrip('\n')) for l in open(os.path.join(HERE, '../../ronde2/raster.txt'))][:64]
def zone(x, y): return (40 <= y <= 44 and x <= 33) or y >= 45
NIEUW = {
 40: [(17, "26655555555545544")],
 41: [(16, "256654566555435443")],
 42: [(15, "2566554365555435543")],
 43: [(14, "25655554355555435543")],
 44: [(14, "25555544355544335443")],
 45: [(12, "223655554435544433355443431")],
 46: [(11, "24356555443334443333554443431")],
 47: [(10, "244355554433343333333544443431")],
 48: [(10, "2444355544", "3344333333", "3554434331")],
 49: [(10, "2444355443", "3114333113", "5444344331")],
 50: [(7, "2225", "44333", "55431"), (23, "1111"), (29, "254433333", "1", "2221")],
 51: [(6, "265543", "111", "255431"), (29, "254431", "111", "255441")],
 52: [(6, "255443", "222", "254431"), (29, "244331", "222", "4544331")],
 53: [(6, "254433", "44", "26655541"), (28, "26554431", "44", "3443331")],
 54: [(6, "143333", "4", "2655555441"), (28, "25554431", "43", "333331")],
 55: [(7, "11111", "3", "2555554431"), (28, "25444331", "33", "11111")],
 56: [(12, "1", "2455544431"), (28, "1443333111")],
 57: [(13, "1444443331"), (29, "133331")],
 58: [(13, "1344433331"), (30, "1111")],
 59: [(14, "13333331")],
 60: [(15, "111111")],
}
for y in range(40, 64):
    for x in range(64):
        if zone(x, y): R[y][x] = '.'
    for x0, *delen in NIEUW.get(y, []):
        for i, c in enumerate(''.join(delen)):
            assert zone(x0 + i, y), (x0 + i, y)
            R[y][x0 + i] = c
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in R) + '\n')
