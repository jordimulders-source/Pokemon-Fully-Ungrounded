"""Ronde 5A: zet het lijf van ronde 2b (met de hand gekleurd) op het kleinere silhouet A.
Geen tint- of vormlogica: alleen een vaste, met de hand gekozen rij-/kolomtoewijzing (3 rijen en 2 kolommen van 2b vallen weg
in egale vlakken, de rest schuift 3 rijen omlaag / 1 kolom naar rechts). Daarna met de hand gerepareerd in bron/lijf_reparaties.txt.
Uitvoer: bron/lijf_overgezet.txt (64 rijen, alleen y>=26)."""
import os
H = os.path.dirname(os.path.abspath(__file__))
b = [l for l in open(os.path.join(H, '../../ronde2b/ronde2b.txt')).read().split('\n')[:64]]
DROP_Y = {34, 44, 48}; DROP_X = {20, 44}
ys = [y for y in range(23, 64) if y not in DROP_Y]          # 2b-rijen -> A-rijen 26..63
xs = [x for x in range(12, 52) if x not in DROP_X]          # 2b-kolommen -> A-kolommen 13..50
assert len(ys) == 38, len(ys)
out = [['.'] * 64 for _ in range(64)]
for ay, by in zip(range(26, 64), ys):
    for ax, bx in zip(range(13, 13 + len(xs)), xs):
        out[ay][ax] = b[by][bx]
open(os.path.join(H, 'lijf_overgezet.txt'), 'w').write('\n'.join(''.join(r) for r in out) + '\n')
