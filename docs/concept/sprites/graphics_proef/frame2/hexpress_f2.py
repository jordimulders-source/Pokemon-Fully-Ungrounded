# Hexpress frame 2 per script (27 nov): losse delen in tegenbeweging. Alleen bestaande pixels verplaatsen.
# Verplaatsen = deel schuift, wat erachter vrijkomt houdt de oude pixels van hetzelfde deel (rek/bol),
# nooit over de trein heen. Wielen: binnenkant 90 graden gedraaid (exact, geen rafels), rand blijft.
import sys, numpy as np
from PIL import Image
sys.path.insert(0, '.')
from f2lib import *
from hexpress_masks import a, pal, GEEST, WOLK, WIEL1, WIEL2, xx, yy

def schuif(x, mask, dx, dy, vrij):
    """mask-pixels dx,dy verplaatsen; alleen landen op transparant of op het eigen deel (vrij)."""
    o = x.copy(); ys, xs = np.where(mask)
    ny, nx = ys+dy, xs+dx
    ok = (ny >= 0) & (ny < 64) & (nx >= 0) & (nx < 64)
    ys, xs, ny, nx = ys[ok], xs[ok], ny[ok], nx[ok]
    land = (x[ny, nx] == 0) | vrij[ny, nx]
    o[ny[land], nx[land]] = x[ys[land], xs[land]]
    return o

def wiel(x, cx, cy, rx, ry):
    """Binnenkant van een (in perspectief ovaal) wiel een halve slag draaien: puntspiegeling rond
    het midden, exact op het raster, ovaal blijft ovaal; de rand erbuiten blijft staan."""
    o = x.copy()
    for y in range(64):
        for c in range(64):
            if ((c-cx)/rx)**2+((y-cy)/ry)**2 <= 1:
                o[y, c] = x[int(round(2*cy-y)), int(round(2*cx-c))]
    return o

V = {}
# h1: geest omhoog (rekt uit de schoorsteen), wolken 1 rechts/1 omlaag
v = schuif(a, GEEST, 0, -1, GEEST)
v = schuif(v, WOLK, 1, 1, WOLK)
V['h1'] = (v, 'ANIM_V_SHAKE')
# h2: als h1 + wielen een halve slag
v2 = wiel(wiel(v, 33.5, 54.5, 5, 7), 48.5, 48, 4, 5)
V['h2'] = (v2, 'ANIM_H_SLIDE')
# h3: geest waait naar achteren (2 rechts, 1 omhoog), wolken 2 naar achteren, wielen een halve slag
v = schuif(a, GEEST, 2, -1, GEEST)
v = schuif(v, WOLK, 2, 0, WOLK)
v = wiel(wiel(v, 33.5, 54.5, 5, 7), 48.5, 48, 4, 5)
V['h3'] = (v, 'ANIM_V_SHAKE_H_SLIDE')

rijen = []
for k, (f2, anim) in V.items():
    save_anim_front(a, f2, pal, f'hexpress_{k}_anim_front.png')
    render_gif(a, f2, pal, anim, f'hexpress_{k}_{anim.lower()}.gif')
    rijen.append((f'hexpress_{k}', a, f2, anim))
vel(rijen, pal, 'hexpress_vel_tmp.png')
