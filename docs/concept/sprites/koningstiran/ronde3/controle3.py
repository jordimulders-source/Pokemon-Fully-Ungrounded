"""Ronde 3: diff per zone t.o.v. ronde 2, kleur naast het staf-eind, afstand staartpuntje-poten. Draaien vanuit de repo-root."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
r2 = np.array(Image.open(os.path.join(K, 'ronde2/sapa_inca.png'))); r3 = np.array(Image.open(os.path.join(H, 'sapa_inca.png')))
pal = [ln.split()[1] for ln in open(os.path.join(H, 'sapa_inca.txt')) if ln.startswith('P ')]
C = lambda v: '.' if v == 0 else pal[v - 1]
L2 = np.vectorize(C)(r2); L3 = np.vectorize(C)(r3)
lab = [l[3:].ljust(64, '.') for l in open(os.path.join(K, 'ronde1/labels.txt')).read().split('\n')[:64]]
Z = {}
Z['kroon'] = np.array([[c in 'FP' for c in r] for r in lab]); Z['kroon'][19:23, 22:33] = False
Z['gezicht/kop (x22-33 y19-27)'] = np.zeros((64, 64), bool); Z['gezicht/kop (x22-33 y19-27)'][19:28, 22:34] = True
Z['opgeheven rechtervleugel (x34-54 y18-33)'] = np.zeros((64, 64), bool); Z['opgeheven rechtervleugel (x34-54 y18-33)'][18:34, 34:55] = True
belly = np.isin(L2, list('agy')) & (np.arange(64)[:, None] >= 34) & (np.arange(64)[:, None] <= 52)
Z['buik (goud van ronde 2, y34-52)'] = belly
Z['oude staart (t in ronde 2)'] = (L2 == 't')
legs = np.zeros((64, 64), bool); legs[53:63, 21:35] = True
Z['poten (y53-62, x21-34, zonder staart)'] = legs & ~(L2 == 't')
left = np.zeros((64, 64), bool); left[23:57, 12:25] = True
Z['nieuw: linkervleugel/staf/opvulling (x12-24 y23-56)'] = left
d = r2 != r3
seen = np.zeros_like(d)
print('alpha: erbij', int(((r3 > 0) & (r2 == 0)).sum()), 'eraf', int(((r2 > 0) & (r3 == 0)).sum()), 'totaal px', int((r3 > 0).sum()))
for n, z in Z.items():
    zz = z & ~seen; seen |= z
    pts = [(int(x), int(y)) for y, x in zip(*np.nonzero(d & zz))]
    print(f'{n}: {len(pts)} px', pts if 0 < len(pts) <= 12 else '')
print('rest (lijf/flank):', [(int(x), int(y), L2[y, x], L3[y, x]) for y, x in zip(*np.nonzero(d & ~seen))])
# staf-eind: laatste veerpixel onderaan (rij 50) en zijn buren
for (x, y) in ((19, 50), (18, 49)):
    print(f'staf-eind ({x},{y}) {L3[y, x]}: rechts {L3[y, x + 1]}, onder {L3[y + 1, x]}, rechtsonder {L3[y + 1, x + 1]}')
# staartpuntje: pixels in x26-29 y57-60 die niet bij de poten horen
tip = [(x, y) for y in range(57, 61) for x in range(26, 30) if L3[y, x] != '.' and (x, y) not in ()]
tip = [(x, y) for (x, y) in tip if not (x <= 25 or x >= 29)]
print('staartpuntje:', tip)
for (x, y) in tip:
    lx = max(xx for xx in range(20, x) if L3[y, xx] != '.' and (xx, y) not in tip) if any(L3[y, xx] != '.' for xx in range(20, x)) else None
    rx = min(xx for xx in range(x + 1, 40) if L3[y, xx] != '.' and (xx, y) not in tip)
    print(f'  ({x},{y}): lucht links {x - lx - 1 if lx is not None else "-"} px, rechts {rx - x - 1} px; boven {L3[y-1, x]}')
