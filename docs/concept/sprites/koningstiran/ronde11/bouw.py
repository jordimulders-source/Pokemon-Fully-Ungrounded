"""Sapa Inca ronde 1: tekstraster -> geindexeerde PNG + controles.
Raster: sapa_inca.txt. Regels 'P <letter> R G B' = palet (volgorde = index 1..15).
Regels 'y x0 tekens' = met de hand getekende pixels (meerdere regels per y mogen; '.' = laat staan/transparant, '_' = expliciet transparant).
Draaien vanuit de repo-root: python3 docs/concept/sprites/koningstiran/ronde1/bouw.py"""
import os
import sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.dirname(HERE)


def lees(path):
    pal, rows = [], {}
    for ln in open(path):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.startswith('#'):
            continue
        p = ln.split()
        if p[0] == 'P':
            pal.append((p[1], tuple(int(v) for v in p[2:5])))
            continue
        y, x0, s = int(p[0]), int(p[1]), p[2]
        rows.setdefault(y, []).append((x0, s))
    return pal, rows


def bouw(path):
    pal, rows = lees(path)
    letters = {c: i + 1 for i, (c, _) in enumerate(pal)}
    g = np.zeros((64, 64), np.uint8)
    for y, segs in rows.items():
        for x0, s in segs:
            for i, ch in enumerate(s):
                if ch == '.':
                    continue
                g[y, x0 + i] = 0 if ch == '_' else letters[ch]
    return pal, letters, g


def controle(pal, letters, g):
    sil = np.array(Image.open(os.path.join(K, 'silhouet_v1_1x.png'))) > 128
    fig = g > 0
    plus = fig & ~sil
    min_ = sil & ~fig
    print(f'pixels {fig.sum()} (silhouet {sil.sum()}); erbij {plus.sum()}, eraf {min_.sum()}')
    zA = np.zeros((64, 64), bool); zA[17:24, 39:56] = True
    zB = np.zeros((64, 64), bool); zB[53:63, 28:39] = True
    d = plus | min_
    print(f'  zone a: {(d & zA).sum()} px, zone b: {(d & zB).sum()} px, buiten zones: {(d & ~zA & ~zB).sum()} px')
    for (y, x) in zip(*np.nonzero(d)):
        print('   diff', x, y, '+' if plus[y, x] else '-')
    inv = {v: c for c, v in letters.items()}
    # open randen: lichte/basistinten naast transparant; selout l/m alleen aan de lichtkant (links/boven)
    # strenge definitie (keuring ronde 10): alleen K, d (donkerste bruin) en p (donker lavendel) mogen naast transparant
    # ronde 11: K, d, p overal; aan de lichtkant (transparant links/boven) ook de gekleurde lichte selout l en de rode selout r
    outline = set('Kdp')
    litonly = set('lr')
    opens = []
    for y in range(64):
        for x in range(64):
            if not g[y, x]:
                continue
            c = inv[g[y, x]]
            for dx, dy, lit in ((-1, 0, True), (0, -1, True), (1, 0, False), (0, 1, False)):
                X, Y = x + dx, y + dy
                if 0 <= X < 64 and 0 <= Y < 64 and g[Y, X]:
                    continue
                if c in outline or (c in litonly and lit):
                    continue
                opens.append((x, y, c))
                break
    print(f'open randen: {len(opens)}', opens[:40])
    # losse pixels: geen enkele 4-buur van dezelfde kleur en alle buren een andere kleur (alleen info)
    loners = []
    for y in range(1, 63):
        for x in range(1, 63):
            v = g[y, x]
            if not v:
                continue
            nb = [g[y + a, x + b] for a, b in ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1))]
            if all(n != v for n in nb) and all(n for n in nb[:4]):
                loners.append((x, y, inv[v]))
    print(f'losse pixels (geen buur in dezelfde kleur): {len(loners)}', loners)
    used = sorted(set(g[g > 0].ravel()))
    print('kleuren gebruikt:', len(used), '+ transparant;', ''.join(inv[u] for u in used))
    dark = np.isin(g, [letters['K']]).sum() / max(1, fig.sum())
    print(f'aandeel zwart K: {dark:.2f}')


def save(pal, g, out):
    im = Image.fromarray(g, 'P')
    flat = [152, 208, 160]
    for _, rgb in pal:
        flat += list(rgb)
    flat += [0, 0, 0] * (256 - len(flat) // 3)
    im.putpalette(flat)
    im.save(out, transparency=0)


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'sapa_inca.txt')
    pal, letters, g = bouw(src)
    controle(pal, letters, g)
    save(pal, g, os.path.join(HERE, 'sapa_inca.png'))
    inv = {v: c for c, v in letters.items()}
    with open(os.path.join(HERE, 'dump.txt'), 'w') as f:
        f.write('   ' + ''.join(str(x // 10) for x in range(64)) + '\n   ' + ''.join(str(x % 10) for x in range(64)) + '\n')
        for y in range(64):
            f.write('%2d ' % y + ''.join(inv.get(v, '.') for v in g[y]) + '\n')
