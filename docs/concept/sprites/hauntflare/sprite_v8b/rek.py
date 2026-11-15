"""Kandidaat T, stap 1: v7-mond 2 rijen hoger open ZONDER tekenen: per kolom bestaande mondrijen dupliceren.
x20-28: rij 34 (donker) en rij 35 (tong) elk 1x gedupliceerd (+2); x29-33 (rechter mondhoek, ring dichtbij): alleen rij 34 (+1).
Alles eronder schuift mee; de onderste bolrijen vlak boven de ring vallen weg (ring blijft staan)."""
from PIL import Image
import numpy as np, os
H = os.path.dirname(os.path.abspath(__file__))
V7 = os.path.join(H, '..', 'sprite_v7', 'hauntflare_v7.png')
def ringtop(a, x):
    for y in range(38, 45):
        if a[y, x] == 1 and a[y+1, x] in (3, 4, 1): return y
def rek():
    im = Image.open(V7); a = np.array(im); b = a.copy()
    for x in range(20, 34):
        dup = [34, 35] if x <= 28 else [34]
        seq = []
        for y in range(34, 45):
            seq.append(a[y, x])
            if y in dup: seq.append(a[y, x])
        r = ringtop(a, x)
        for i, y in enumerate(range(34, r)): b[y, x] = seq[i]
    return im, b
if __name__ == '__main__':
    im, b = rek()
    print('    '+''.join(str(x%10) for x in range(16,38)))
    for y in range(31, 44): print(y, ''.join('%x'%v if v else '.' for v in b[y,16:38]))
