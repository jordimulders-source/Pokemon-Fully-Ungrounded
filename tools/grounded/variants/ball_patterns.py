#!/usr/bin/env python3
"""Echte Poké Ball-patronen voor Voltorb en Electrode (Jordi 15 okt: de enige
uitzondering op 'alleen een paletwissel').

Per patroon een eigen sprite (anim_front + back) in graphics/pokemon/<soort>/ball_<naam>/.
Patroonpixels liggen alleen op het gekleurde deel van de bal en gebruiken de vrije
paletindexen PAT (donker/midden/licht). In normal.pal en shiny.pal krijgen die indexen
dezelfde tinten als het gekleurde deel, zodat een shiny met zo'n personality er gewoon
als shiny uitziet. De kleuren per variant staan in recipes.py ('pat').

Draai daarna variants.py. De C-kant: src/mon_variants.c (GetVariantMonPic).
"""
import math
import os
import sys

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))
from variants import read_pal, write_pal  # noqa: E402

SPECIES = {
    # gekleurde index-groep (donker -> licht), vrije indexen (donker, midden, licht),
    # flip: het gekleurde deel ligt onderaan (Electrode staat op zijn kop)
    'voltorb': {'ramp': [14, 13, 12, 11, 10, 9], 'pat': [6, 7, 8], 'white': [1, 2, 3, 4]},
    'electrode': {'ramp': [14, 13, 12, 11, 10], 'pat': [6, 7, 8], 'white': [1, 2, 3, 4]},
}

# Volgorde = variant 1..6 (10%, 6%, 4%, 3%, 1,5%, 0,5%).
PATTERNS = ['great', 'ultra', 'quick', 'safari', 'dusk', 'master']


def seg_dist(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def ellipse(u, v, cx, cy, rx, ry):
    return ((u - cx) / rx) ** 2 + ((v - cy) / ry) ** 2 < 1


def polyline(p, pts, width):
    return any(seg_dist(p, a, b) < width for a, b in zip(pts, pts[1:]))


def near(p, c, r):
    n = math.sqrt(sum(x * x for x in c))
    return sum((a - b / n) ** 2 for a, b in zip(p, c)) < r * r


SAFARI_SPOTS = [(-0.6, 0.5, 0.4), (0.2, 0.7, 0.6), (0.75, 0.1, 0.5), (-0.2, -0.6, 0.6),
                (0.6, -0.5, 0.45), (-0.8, -0.2, 0.3), (0.0, 0.1, 0.95), (-0.45, 0.85, 0.15),
                (0.45, 0.35, 0.2)]


def in_pattern(name, sd, fr, up):
    """Punt op de bol in balcoordinaten: sd = zijwaarts, fr = naar de kijker, up = naar de
    pool van de gekleurde helft. Nagetekend naar de Gen 4/5-balsprites (alle draaistanden)
    en de officiële artwork."""
    a = abs(sd)
    if up < 0.06:
        return False
    if name == 'great':
        # twee rode banen van voor naar achter over de flanken: van boven '( )'
        return 0.50 < a < 0.74 and up > 0.12
    if name == 'ultra':
        # gele H op zwart: twee benen van voor naar achter plus een dwarsbalk
        return 0.28 < a < 0.80 or (a <= 0.28 and abs(fr) < 0.20)
    if name == 'quick':
        # gele X van boven gezien over blauw
        return abs(a - abs(fr)) < 0.26 and up > 0.10
    if name == 'safari':
        return any(near((sd, fr, up), c, 0.30) for c in SAFARI_SPOTS)
    if name == 'dusk':
        # groene cirkels op een donkere bal: kap bovenop en vier vlakken rondom
        if up > 0.84:
            return True
        k = math.cos(math.radians(25))
        q = math.sin(math.radians(25))
        return any(near((sd, fr, up), c, 0.40) for c in ((0, k, q), (k, 0, q), (-k, 0, q), (0, -k, q)))
    if name == 'master':
        # twee roze bollen links en rechts van de top
        return near((sd, fr, up), (0.62, 0.35, 0.65), 0.36) or near((sd, fr, up), (-0.62, 0.35, 0.65), 0.36)
    raise ValueError(name)


def ball_geometry(img, x0, y0, w, h):
    """Middelpunt en straal van de bal in een frame (uit de dekking)."""
    xs, ys = [], []
    px = img.load()
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if px[x, y] != 0:
                xs.append(x)
                ys.append(y)
    # De breedte is altijd helemaal zichtbaar; achteraanzichten vallen onderaan uit beeld.
    cx = (min(xs) + max(xs) + 1) / 2
    r = (max(xs) - min(xs) + 1) / 2
    cy = min(ys) + r
    return cx, cy, r


def shade_slot(idx, ramp):
    # donkerste index -> donker, de rest verdeeld over midden/licht
    pos = ramp.index(idx)
    n = len(ramp)
    if pos == 0:
        return 0
    return 1 if pos <= (n - 1) // 2 else 2


def sphere_frame(src, f, cfg):
    """Middelpunt, straal en pool (3D) van de bal in frame f. De pool staat loodrecht op de
    naad tussen gekleurd en wit, zo telt de schuine pose van de sprite mee."""
    cx, cy, r = ball_geometry(src, 0, f * 64, 64, 64)
    px = src.load()
    white = cfg['white']
    seam, colored = [], []

    def p3(x, y):
        X = (x + 0.5 - cx) / r
        Y = -(y + 0.5 - cy) / r
        return (X, Y, math.sqrt(max(0.0, 1 - X * X - Y * Y)))

    for y in range(f * 64, f * 64 + 64):
        for x in range(64):
            i = px[x, y]
            if i in cfg['ramp']:
                colored.append(p3(x, y))
                if any(0 <= x + dx < 64 and px[x + dx, y + dy] in white
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                       if f * 64 <= y + dy < f * 64 + 64):
                    seam.append(p3(x, y))
    # vlak door het middelpunt: kleinste eigenvector van sum p p^T
    import numpy as np
    M = np.zeros((3, 3))
    for p in seam:
        v = np.array(p)
        M += np.outer(v, v)
    w, V = np.linalg.eigh(M)
    n = V[:, 0]
    if np.mean([np.dot(n, c) for c in colored]) < 0:
        n = -n
    return cx, cy, r, n


def make(species, name, picname):
    import numpy as np
    cfg = SPECIES[species]
    src = Image.open(os.path.join(ROOT, 'graphics/pokemon', species, picname))
    img = src.copy()
    px = img.load()
    w, h = img.size
    for f in range(h // 64):
        cx, cy, r, n = sphere_frame(src, f, cfg)
        front = np.array([0.0, 0.0, 1.0]) - n[2] * n
        front /= np.linalg.norm(front)
        side = np.cross(n, front)
        for y in range(f * 64, f * 64 + 64):
            for x in range(64):
                i = px[x, y]
                if i not in cfg['ramp']:
                    continue
                X = (x + 0.5 - cx) / r
                Y = -(y + 0.5 - cy) / r
                p = np.array([X, Y, math.sqrt(max(0.0, 1 - X * X - Y * Y))])
                if in_pattern(name, float(np.dot(p, side)), float(np.dot(p, front)), float(np.dot(p, n))):
                    px[x, y] = cfg['pat'][shade_slot(i, cfg['ramp'])]
    out = os.path.join(ROOT, 'graphics/pokemon', species, 'ball_' + name)
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, picname))


def fill_free_indices(species):
    """Vrije indexen in normal/shiny = tinten van het gekleurde deel (onzichtbaar)."""
    cfg = SPECIES[species]
    ramp = cfg['ramp']
    pick = [ramp[0], ramp[1], ramp[len(ramp) // 2]]
    for palname in ('normal.pal', 'shiny.pal'):
        path = os.path.join(ROOT, 'graphics/pokemon', species, palname)
        pal = read_pal(path)
        for slot, idx in zip(cfg['pat'], pick):
            pal[slot] = pal[idx]
        write_pal(path, pal)


def main():
    for species in SPECIES:
        fill_free_indices(species)
        for name in PATTERNS:
            for pic in ('anim_front.png', 'back.png'):
                make(species, name, pic)
    print('balpatronen klaar')


if __name__ == '__main__':
    main()
