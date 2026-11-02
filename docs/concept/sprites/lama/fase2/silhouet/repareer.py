"""Lama fase 2, silhouet ronde 1: handreparaties op direct.txt in benoemde zones.
Elke zone is een met de hand getypt tekstraster (# = vorm, . = leeg) dat de rechthoek in direct.txt vervangt.
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/fase2/silhouet/repareer.py
Schrijft ronde1.txt, ronde1_1x.png en print de diff per zone (buiten de zones moet het 0 zijn)."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))

# zone: (x0, y0, raster)
ZONES = {
 # A. Voorpoten: opgetilde nabije voorpoot (knie naar voren r46-47, pols r50, handschoen r50-56, vrij van de grond)
 #    en dragende verre voorpoot (5 px, eigen kolom, handschoen op de grond r57-62); lucht ertussen 2 kolommen.
 'A voorpoten': (18, 41, """
.......##########..
......###########..
.....######.#####..
....######..#####..
...######...#####..
..######....#####..
..######....#####..
...######...#####..
....######..#####..
...#######..#####..
..########..#####..
.#########..#####..
.#########..#####..
.#########..#####..
..########..#####..
...######...#####..
...........######..
..........########.
.........#########.
.........#########.
.........#########.
..........#######..
"""),
 # B. Achterpoten: verre achterpoot (5 px) en nabije achterpoot
 #    (5 px, hak naar achteren r49-51, onderbeen 1 px naar voren onder de hak, voet r60-61 = voet van de bron);
 #    verre poot ook met knik onder de hak (r53), voet r58-59 (1 rij hoger dan de bron: perspectief); inkeping vanaf r45, 2 kolommen lucht vanaf r47.
 'B achterpoten': (39, 41, """
...#########....
...##########...
...##########...
...##########...
..#####.######..
..#####.######..
..#####..#####..
..#####..#####..
..#####..######.
..#####..######.
..#####..######.
..#####..#####..
.#####..#####...
.#####..#####...
.#####..#####...
.#####..#####...
.#####..#####...
######..#####...
######..#####...
.......######...
.......######...
................
"""),
 # C. Oren: blad-/banaanvorm (breedst bij de kwast, punt naar achteren), geen knop op een steel; V ertussen.
 'C oren': (11, 2, """
............
...##....##.
..###...###.
.####...###.
.####...###.
..###..###..
..###.####..
"""),
 # D. Snuit: bobbel van het verre oog weg (r14-15), neus steekt naar voren-onder (r19-21),
 #    ronde kin (r22-23) met een keelinkeping vóór de hals (kop = eigen onderdeel).
 'D snuit': (10, 13, """
..########
..########
..########
..########
..########
..########
.#########
.#########
.#########
..########
...###..##
"""),
 # E. Wol: één wolbobbel op het achterwerk (rechte rand r28-36 breken).
 'E wol': (52, 31, """
#
#
#
"""),
}

def load(p):
    return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(p) if l.strip()], dtype=bool)

def save(sil, stem):
    open(os.path.join(HERE, stem + '.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in sil) + '\n')
    im = Image.fromarray(sil.astype(np.uint8), 'P')
    im.putpalette([255, 255, 255, 40, 32, 48] + [0] * 762)
    im.save(os.path.join(HERE, stem + '_1x.png'), transparency=0)

def stats(sil, name):
    ys, xs = np.nonzero(sil)
    print(f'{name}: px {sil.sum()}, box {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}, x {xs.min()}-{xs.max()}, y {ys.min()}-{ys.max()}')

if __name__ == '__main__':
    src = load(os.path.join(HERE, 'direct.txt'))
    out = src.copy()
    mask = np.zeros_like(src)
    rects = {}
    for name, (x0, y0, txt) in ZONES.items():
        rows = [r for r in txt.strip('\n').split('\n')]
        w = len(rows[0]); assert all(len(r) == w for r in rows), name
        blk = np.array([[c == '#' for c in r] for r in rows])
        h = len(rows)
        out[y0:y0 + h, x0:x0 + w] = blk
        mask[y0:y0 + h, x0:x0 + w] = True
        rects[name] = (x0, y0, w, h)
    save(out, 'ronde1')
    stats(src, 'direct'); stats(out, 'ronde1')
    print('diff per zone (bij / weg):')
    for name, (x0, y0, w, h) in rects.items():
        a, b = src[y0:y0+h, x0:x0+w], out[y0:y0+h, x0:x0+w]
        print(f'  {name:14s} rect x{x0}-{x0+w-1} y{y0}-{y0+h-1}: +{(b & ~a).sum()} / -{(a & ~b).sum()}')
    print('buiten de zones gewijzigd:', (src != out)[~mask].sum())
