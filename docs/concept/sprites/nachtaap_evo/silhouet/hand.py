"""Handreparaties op het verkleinde silhouet, alleen in benoemde zones (SPRITE_WERKWIJZE stap 2).
Zone 'spiraal' (x 46-63, y 6-25): de spiraal liep bij het verkleinen dicht; opnieuw getekend als buis van 3 px
met een open binnenkrul, op dezelfde plek en maat als de render."""
import math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sil = np.load(os.path.join(HERE, 'basis_sil.npy')).copy()
far = np.load(os.path.join(HERE, 'basis_far.npy')).copy()
base = sil.copy()

def disk(a, cx, cy, r):
    yy, xx = np.mgrid[0:64, 0:64]
    a |= (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r

# zone spiraal
Z = (slice(6, 25), slice(46, 64))
sil[6:22, 46:64] = False
cx, cy = 56.0, 14.6
pts = []
for i in range(220):
    t = i / 219
    th = math.radians(180 + 300 * t + 140 * t * t)    # start links, met de klok mee over de top, naar binnen
    r = 6.6 - 4.4 * t
    pts.append((cx + r * math.cos(th), cy - r * math.sin(-th + 2 * math.radians(180)) if False else cy + r * math.sin(th)))
for i, (x, y) in enumerate(pts):
    w = 1.55 - 0.55 * i / len(pts)
    disk(sil, x, y, w)
# stam van de staart sluit aan op het begin van de spiraal (links)
for y in range(16, 25):
    t = (y - 16) / 8
    x = 49.6 + 0.8 * t
    disk(sil, x, y, 1.9)

sil[22, 54:60] = False      # restje van de oude spiraal onder de krul

# zone 'handen' (x 2-14, y 56-62): vingertop-inkeping aan de verre hand, nabije hand los van de verre hand
Z2 = (slice(56, 63), slice(2, 15))
sil[59, 3] = False
sil[60, 9:11] = False

# zone 'nek' (x 11-15, y 34-37): kleine inham tussen kruin en rug, zodat de kop als eigen bol leest
Z3 = (slice(34, 38), slice(11, 16))
sil[36, 12:14] = False
sil[35, 14] = False

np.save(os.path.join(HERE, 'hand_sil.npy'), sil)
np.save(os.path.join(HERE, 'hand_far.npy'), far & sil)
diff = sil ^ base
outside = diff.copy(); outside[Z] = False; outside[Z2] = False; outside[Z3] = False
print('gewijzigd in zones:', int(diff[Z].sum() + diff[Z2].sum() + diff[Z3].sum()), 'buiten zones:', int(outside.sum()), 'totaal px', int(sil.sum()))
for y in range(4, 28):
    print('%2d %s' % (y, ''.join('#' if sil[y, x] else '.' for x in range(40, 64))))
