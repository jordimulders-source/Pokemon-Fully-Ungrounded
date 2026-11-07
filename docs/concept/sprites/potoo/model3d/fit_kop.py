"""Fit de kopmaten (KP) op de verhoudingen van de 3/4-foto (meten.py), door coördinaat-afdaling: elke maat stap
voor stap groter/kleiner zolang het totale verschil kleiner wordt. Geen giswerk: het doel zijn de gemeten lijnen.
Oogbreedte-doel iets groter dan de foto (Pokémon, Jordi: "grote ogen")."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import potoo3d
from potoo3d import potoo
from meten import FOTO, ratios, meet_model

YAWS = (40, 45, 50)
DOEL = ratios(FOTO); DOEL['oog breedte'] = 0.23
W = {'oog vanaf achterkant': 3, 'oog vorm (h/b, onbedekt)': 3, 'oog hoogte vanaf kruin': 2}   # oog half onder een 'klep' telde eerst niet mee


def kost(kp):
    t = 0
    for y in YAWS:
        try:
            r = ratios(meet_model(potoo(0, kp=kp), y))
        except Exception:
            return 1e9
        t += sum(W.get(k, 1) * (r[k] - DOEL[k]) ** 2 for k in DOEL)
    return t / len(YAWS)


def vlak(kp):
    return [(k, i) for k, v in kp.items() for i in (range(len(v)) if isinstance(v, (tuple, list)) else [None])]


def zet(kp, k, i, d):
    kp = {a: (list(b) if isinstance(b, (tuple, list)) else b) for a, b in kp.items()}
    if i is None: kp[k] += d
    else: kp[k][i] += d
    return kp


kp = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kp_fit.json'))) if len(sys.argv) > 1 else {a: (list(b) if isinstance(b, (tuple, list)) else b) for a, b in potoo3d.KP.items()}
best = kost(kp); print('start', round(best, 4))
for stap in (4, 2, 1):
    beter = True
    while beter:
        beter = False
        for k, i in vlak(kp):
            for d in (stap, -stap):
                c = zet(kp, k, i, d); s = kost(c)
                if s < best - 1e-5:
                    kp, best, beter = c, s, True
                    break
    print('stap', stap, round(best, 4))
json.dump(kp, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kp_fit.json'), 'w'), indent=1)
print(kp)
