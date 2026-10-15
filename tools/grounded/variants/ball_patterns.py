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
    'voltorb': {'ramp': [14, 13, 12, 11, 10, 9], 'pat': [6, 7, 8], 'flip': False},
    'electrode': {'ramp': [14, 13, 12, 11, 10], 'pat': [6, 7, 8], 'flip': True},
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


def in_pattern(name, u, v):
    """u: -1 links .. 1 rechts, v: -1 bovenkant .. 0 naad (het gekleurde deel).
    Nagetekend naar de officiële artwork (PokeAPI dream-world-items)."""
    au = abs(u)
    if name == 'great':
        # twee rode 'haken' die langs de buitenrand omhoog lopen en bovenin naar binnen buigen
        return polyline((au, v), [(0.58, -0.18), (0.76, -0.48), (0.70, -0.78), (0.52, -0.94)], 0.16)
    if name == 'ultra':
        # gele bovenkant met de zwarte H: brede middenbaan en zwarte flanken
        return au < 0.22 or au > 0.76
    if name == 'quick':
        # gele bliksem-X over een lichtblauwe bovenkant
        bolt = [(-0.62, -0.92), (-0.05, -0.55), (-0.22, -0.46), (0.72, -0.04)]
        return (polyline((u, v), bolt, 0.11) or polyline((-u, v), bolt, 0.11))
    if name == 'safari':
        # donkergroene camouflagevlekken over olijf/kaki
        spots = [(-0.62, -0.30, 0.24, 0.16), (-0.05, -0.78, 0.30, 0.15), (0.55, -0.55, 0.22, 0.18),
                 (-0.30, -0.08, 0.20, 0.10), (0.40, -0.12, 0.22, 0.10), (-0.70, -0.75, 0.14, 0.12),
                 (0.85, -0.25, 0.12, 0.14)]
        return any(ellipse(u, v, x, y, rx, ry) for x, y, rx, ry in spots)
    if name == 'dusk':
        # groene vlekken op een donkere bal: kap bovenop, ovalen op de flanken en voorop
        return (ellipse(u, v, 0, -1.0, 0.42, 0.22) or ellipse(au, v, 0.95, -0.35, 0.22, 0.42)
                or ellipse(u, v, 0, -0.02, 0.42, 0.14))
    if name == 'master':
        # twee roze bollen linksboven en rechtsboven
        return ellipse(au, v, 0.52, -0.62, 0.34, 0.30)
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


def make(species, name, picname):
    cfg = SPECIES[species]
    src = Image.open(os.path.join(ROOT, 'graphics/pokemon', species, picname))
    img = src.copy()
    px = img.load()
    w, h = img.size
    for f in range(h // 64):
        cx, cy, r = ball_geometry(src, 0, f * 64, 64, 64)
        for y in range(f * 64, f * 64 + 64):
            for x in range(64):
                i = px[x, y]
                if i not in cfg['ramp']:
                    continue
                u = (x + 0.5 - cx) / r
                v = (y + 0.5 - cy) / r
                if cfg['flip']:
                    v = -v
                if v < 0 and in_pattern(name, u, v):
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
