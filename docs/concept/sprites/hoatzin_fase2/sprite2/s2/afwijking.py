# afwijking.py: per zone het aantal pixels dat afwijkt van de kale reductie (onderlaag op het palet).
# Soorten: lijn (buiten-/binnenlijn of selout gezet), silhouet (erbij/eraf), tint (andere tint dan de reductie).
import numpy as np
from klassen import ZONE
from palet import MAP
K = np.load('onderlaag.npy'); A = np.load('alpha.npy'); S = np.array(__import__('PIL.Image', fromlist=['Image']).open('hoatzin.png'))
kaal = np.where(A >= 0.45, np.vectorize(lambda k: MAP.get(k, 0))(K), 0)
tel = {}
for j in range(64):
    for i in range(64):
        a, b = kaal[j, i], S[j, i]
        if a == b: continue
        z = ZONE[K[j, i]] if A[j, i] >= 0.12 else 'buiten'
        soort = 'silhouet' if (a == 0) != (b == 0) else 'lijn' if b == 1 else 'tint/selout'
        t = tel.setdefault(z, {}); t[soort] = t.get(soort, 0) + 1
tot = sum(sum(t.values()) for t in tel.values())
for z, t in sorted(tel.items()): print('%-8s' % z, t, sum(t.values()))
hand = int((np.load('auto.npy') != S).sum())
print('totaal', tot, 'van', int((S > 0).sum()), 'pixels; met de hand gezet:', hand, '(oog, Jordi)')
