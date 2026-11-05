"""Projecteer het kené-patroon van het 3D-poppetje naar 64x64 (zelfde schaal/plek als het silhouet),
om te toetsen of het patroon in de sprite in 3D klopt (Jordi: "is het niet teveel naar ons perspectief gevormd?")."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'pop3d'))
import silhouet as S, nachtaap3d as N, pop3d as P

def project(m, fill=0.94, thr=0.35, off=(0, 4)):
    gid, groups = S.gid_render(m, fill)
    k = gid.shape[0] // 64
    g = groups.index('maan')
    frac = (gid == g).reshape(64, k, 64, k).mean(axis=(1, 3))
    mask = frac > thr
    out = np.zeros_like(mask)
    ys, xs = np.nonzero(mask)
    ys2, xs2 = ys + off[1], xs + off[0]
    ok = (ys2 < 64) & (xs2 < 64)
    out[ys2[ok], xs2[ok]] = True
    return out & np.load(os.path.join(HERE, 'silhouet_bevroren.npy'))

if __name__ == '__main__':
    m = N.nachtaap(40, 'omhoog', 'kene', cam=(40, 8))
    mk = project(m)
    np.save(os.path.join(HERE, 'kene_poppetje_64.npy'), mk)
    print('patroonpixels', int(mk.sum()))
