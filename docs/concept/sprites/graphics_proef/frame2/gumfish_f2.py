# Gumfish frame 2 per script (27 nov). Alleen bestaande pixels verschuiven/draaien; vrijgekomen
# plekken dicht met de aangrenzende kleur van hetzelfde deel. Draaien = nearest zoals de engine.
import sys, numpy as np
from PIL import Image
sys.path.insert(0, '.')
from f2lib import *
B = '../../'
im = Image.open(B+'blobfish/af/blobfish.png'); a = np.array(im); pal = im.getpalette()
H, W = a.shape
yy, xx = np.mgrid[0:H, 0:W]
# Onderdelen
STAART = (a > 0) & (xx >= 49) & (yy <= 37)                       # staartvin rechtsboven
VIN = np.isin(a, [10, 11]) & (xx >= 28) & (xx <= 40) & (yy >= 39) & (yy <= 51)  # roze borstvin-strepen
VIN |= (a == 2) & (xx >= 33) & (xx <= 37) & (yy == 39)            # bovenrand borstvin
LIJFKLEUR = 4

def rij_weg(x, r):      # squash: rij r verdwijnt, alles erboven 1 px omlaag
    o = x.copy(); o[1:r+1] = x[0:r]; o[0] = 0; return o
def rij_dubbel(x, r):   # stretch: rij r dubbel, alles erboven 1 px omhoog
    o = x.copy(); o[0:r] = x[1:r+1]; return o

def draai_deel(x, mask, hoek, piv):
    """Deel (mask) draaien rond piv; eerst het deel weghalen, gaten binnen het oude deel dichtmaken
    met de kleur van het deel zelf (dichtstbijzijnde oude pixel van het deel aan de lijfkant)."""
    deel = np.where(mask, x, 0).astype(np.uint8)
    D = Image.fromarray(deel, 'P'); D.putpalette(pal)
    R = np.array(D.rotate(hoek, resample=Image.NEAREST, center=piv, fillcolor=0))
    o = np.where(mask, 0, x)
    o = np.where(R > 0, R, o)
    return o

def buig_deel(x, mask, x0, k):
    """Deel buigen: kolom x (>= x0) schuift (x-x0)*k px verticaal (k<0 = omhoog). Elke kolom blijft
    heel (omlijning gaat mee); wat vrijkomt binnen het oude deel wordt transparant (buitenkant)."""
    o = np.where(mask, 0, x)
    for c in range(x0, x.shape[1]):
        d = int(round((c-x0)*k))
        ys = np.where(mask[:, c])[0]
        for y in ys:
            if 0 <= y+d < x.shape[0]:
                o[y+d, c] = x[y, c]
    return o

def schuif_vin(x, mask, dx, dy):
    o = x.copy()
    o[mask] = LIJFKLEUR
    ys, xs = np.where(mask)
    o[ys+dy, xs+dx] = x[ys, xs]
    return o

def staart_dicht(o, orig_mask):
    # gaten in de staartvin-zone die nu leeg zijn maar binnen het lijf liggen: vullen met linkerbuur
    return o

R = 38
varianten = {}
# v1: squash (lijf 1 px lager), staartvin tip omhoog (tegen), borstvin 1 px omhoog
v = rij_weg(a, R); st = np.zeros_like(STAART); st[1:R+1] = STAART[0:R]
v = buig_deel(v, st, 49, -0.25)
v = schuif_vin(v, VIN, 0, -1)
varianten['v1'] = (v, 'ANIM_V_SQUISH_AND_BOUNCE')
# v2: stretch (lijf 1 px hoger), staartvin tip omlaag, borstvin 1 px omlaag
v = rij_dubbel(a, R); st = np.zeros_like(STAART); st[0:R] = STAART[1:R+1]
v = buig_deel(v, st, 49, 0.25)
v = schuif_vin(v, VIN, 0, 1)
varianten['v2'] = (v, 'ANIM_V_SLIDE')
# v3: staartslag: staartvin sterk omhoog, borstvin 1 px naar achteren, lijf gelijk
v = buig_deel(a, STAART, 49, -0.45)
v = schuif_vin(v, VIN, 1, 0)
varianten['v3'] = (v, 'ANIM_H_SLIDE_WOBBLE')

rijen = []
for k, (f2, anim) in varianten.items():
    save_anim_front(a, f2, pal, f'gumfish_{k}_anim_front.png')
    render_gif(a, f2, pal, anim, f'gumfish_{k}_{anim.lower()}.gif')
    rijen.append((f'gumfish_{k}', a, f2, anim))
vel(rijen, pal, 'gumfish_vel_tmp.png')
