"""Lama fase 2, silhouet ronde 1: handreparaties op direct.txt in benoemde zones.
Elke zone is een met de hand getypt tekstraster (# = vorm, . = leeg) dat de rechthoek in direct.txt vervangt.
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/fase2/silhouet/repareer.py [ronde1|ronde1b]
Schrijft ronde1.txt, ronde1_1x.png en print de diff per zone (buiten de zones moet het 0 zijn)."""
import os, sys
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


# Ronde 1b (Claude: A, C, D bevroren; B en de omtrek van het lijf terug). Toegepast op ronde1.txt.
ZONES_1B = {
 # B. Achterpoten, opnieuw: de dij loopt vanuit de buik/het achterwerk geleidelijk over in het been (r41-44 breed,
 #    voorrand schuin 38-39-40), dan twee poten. Nabij: voorrand 47-48-49 (dij schuin naar achteren), hak steekt
 #    naar achteren (x54, r50-51), holte boven de hak (achterrand 49 op r42-43), onderbeen schuin naar voren tot de voet x45-50 r60-61 (= voet van de bron).
 #    Ver (hoger, korter): dezelfde "<" met hak x46 r50-51, onderbeen naar voren, voet x39-44 r57-58.
 #    Overal >= 2 px lucht tussen de poten, ruimte onder de buik (x35-39) leeg.
 'B achterpoten': (37, 41, """
.#############....
..###########.....
...##########.....
...###########....
...#####..#####...
...#####..#####...
....#####..#####..
....#####..#####..
....#####..######.
.....#####..######
.....#####..######
....#####...#####.
....#####...#####.
...#####...#####..
...#####...#####..
...#####...#####..
..######..#####...
..#####...#####...
.........#####....
........######....
........######....
..................
"""),
 # E2 rug: staart als pluim (bol bovenaan r21-23, punt naar achteren, smalle aanzet x50-51 r24), wolpluk op de schoft (x36-37) en
 #    de bolling van de aguayo (x44-45); rij 25 (rug) zelf ongewijzigd.
 'E2 rug+staart': (32, 20, """
.......................
...................##..
..................####.
..................####.
....##......##....##...
"""),
 # E2 achterwerk: twee rustige wolplukken van 2 rijen (r27-28 en r32-33, onderkant als richeltje: hangende wol)
 #    met dalen ertussen (r29-30, r34-37), zodat de massa nauwelijks groeit; daarna de rand van de bron (50).
 'E2 achterwerk': (50, 25, """
###..
###..
####.
####.
##...
##...
###..
####.
####.
##...
##...
##...
##...
#....
#....
#....
"""),
 # E2 borst: wolpluk onder de halsband (r35-36 x20) met een dal erboven (r33-34 x22).
 'E2 borst': (19, 26, """
#####
.####
.####
..###
.####
.####
..###
...##
...##
.####
.####
..###
...##
....#
.....
"""),
}

def apply(src, zones):
    out = src.copy(); mask = np.zeros_like(src); rects = {}
    for name, (x0, y0, txt) in zones.items():
        rows = txt.strip('\n').split('\n')
        w = len(rows[0]); assert all(len(r) == w for r in rows), name
        h = len(rows)
        out[y0:y0 + h, x0:x0 + w] = np.array([[c == '#' for c in r] for r in rows])
        mask[y0:y0 + h, x0:x0 + w] = True
        rects[name] = (x0, y0, w, h)
    return out, mask, rects

def report(src, out, mask, rects, label):
    print(f'diff per zone t.o.v. {label} (bij / weg):')
    for name, (x0, y0, w, h) in rects.items():
        a, b = src[y0:y0+h, x0:x0+w], out[y0:y0+h, x0:x0+w]
        print(f'  {name:16s} rect x{x0}-{x0+w-1} y{y0}-{y0+h-1}: +{(b & ~a).sum()} / -{(a & ~b).sum()}')
    print(f'  buiten de zones gewijzigd t.o.v. {label}:', (src != out)[~mask].sum())

if __name__ == '__main__':
    stem = sys.argv[1] if len(sys.argv) > 1 else 'ronde1'
    direct = load(os.path.join(HERE, 'direct.txt'))
    r1, m1, rects1 = apply(direct, ZONES)
    if stem == 'ronde1':
        save(r1, 'ronde1'); stats(direct, 'direct'); stats(r1, 'ronde1'); report(direct, r1, m1, rects1, 'direct')
    else:
        r1b, m, rects = apply(r1, ZONES_1B)
        save(r1b, 'ronde1b'); stats(direct, 'direct'); stats(r1, 'ronde1'); stats(r1b, 'ronde1b')
        report(r1, r1b, m, rects, 'ronde1')
        for z in ('A voorpoten', 'C oren', 'D snuit'):
            x0, y0, w, h = rects1[z]
            print(f'  bevroren {z}: verschil met ronde1 =', (r1[y0:y0+h, x0:x0+w] != r1b[y0:y0+h, x0:x0+w]).sum())
        print('  ronde1b t.o.v. direct buiten alle zones:', (direct != r1b)[~(m | m1)].sum())
