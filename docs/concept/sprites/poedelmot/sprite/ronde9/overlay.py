"""Ronde 9: Jordi's rode vormen (jordi_schets_ronde8_vormen.png) exact over een sprite gelegd.
Passing gemeten tegen ronde 8: schaal 10.0, verschuiving (-9, -51) px (sprite-x = (px+9)/10, sprite-y = (py+51)/10),
92,5 % van de niet-rode spritepixels in de schets valt dan op dezelfde kleur. Op 8x: rood geschaald met 0.8."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, '../../referenties/jordi_schets_ronde8_vormen.png')
def rood():
    sk = np.array(Image.open(SK).convert('RGB')).astype(int)
    return (sk[:, :, 0] > 180) & (sk[:, :, 1] < 90) & (sk[:, :, 2] < 90)
def over(spr, z=8):
    im = Image.open(spr).crop((0, 0, 64, 64)).convert('RGB').resize((64 * z, 64 * z), Image.NEAREST)
    a = np.array(im); r = rood(); ys, xs = np.nonzero(r)
    X = ((xs + 9) * z / 10).astype(int); Y = ((ys + 51) * z / 10).astype(int)
    ok = (X >= 0) & (X < 64 * z) & (Y >= 0) & (Y < 64 * z)
    a[Y[ok], X[ok]] = (230, 20, 20)
    return Image.fromarray(a)
def cellen():
    """sprite-cellen waar rood ligt"""
    r = rood(); ys, xs = np.nonzero(r); M = np.zeros((64, 64), int)
    for x, y in zip((xs + 9) // 10, (ys + 51) // 10): M[y, x] += 1
    return M
if __name__ == '__main__':
    import paneel
