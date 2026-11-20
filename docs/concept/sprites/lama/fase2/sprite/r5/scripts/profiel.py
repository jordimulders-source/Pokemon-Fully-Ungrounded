# Model-omtrek per spritekolom/-rij (subpixel, spriteraster), voor het plaatsen van wolbogen.
# zijde: 'boven' (per kolom eerste modelpixel van boven binnen rijvenster), 'onder', 'links', 'rechts' (per rij binnen kolomvenster)
import numpy as np
from meet import bg, S, OX, OY
fg = ~bg
def _rng(i, o): return int(round(o + i * S)), int(round(o + (i + 1) * S))
def profiel(zijde, idx, lo, hi):
    """idx = kolom (boven/onder) of rij (links/rechts); lo..hi = venster in spritecoordinaten (rij- of kolombereik)"""
    if zijde in ('boven', 'onder'):
        a, b = _rng(idx, OX); r0, r1 = int(OY + lo * S), int(OY + hi * S)
        vals = []
        for c in range(a, b):
            ys = np.nonzero(fg[max(r0, 0):r1, c])[0]
            if len(ys): vals.append((ys[0] if zijde == 'boven' else ys[-1] + 1) + max(r0, 0))
        return (np.median(vals) - OY) / S if vals else None
    a, b = _rng(idx, OY); c0, c1 = int(OX + lo * S), int(OX + hi * S)
    vals = []
    for r in range(max(a, 0), b):
        xs = np.nonzero(fg[r, c0:c1])[0]
        if len(xs): vals.append((xs[0] if zijde == 'links' else xs[-1] + 1) + c0)
    return (np.median(vals) - OX) / S if vals else None
