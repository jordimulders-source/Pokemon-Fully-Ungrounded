# Trainer-effect op een paar plekken (Jordi, 25 nov): "ja ik wil dat op een paar plekken zien, maar het mag
# nergens de mond of de ogen overlappen". Binnen een rechthoek schuift elke lijn van 1 px (kolom: omhoog/omlaag,
# rij: links/rechts) als geheel; rechthoeken (+ max verschuiving) blijven buiten het gezicht.
# Gebruik: IN OUT plekken(komma's, uit PLEKKEN) as(kolom|rij|mix) max seed
import sys, random; from PIL import Image; import numpy as np
IN, OUT, namen, AS, m, seed = sys.argv[1], sys.argv[2], sys.argv[3].split(','), sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
GEZICHT = (21, 44, 20, 35)   # x0 x1 y0 y1 (incl.) ogen + mond van r12
PLEKKEN = {'kruin_l': (15, 26, 7, 17), 'kruin_r': (34, 46, 7, 17), 'schouder_r': (48, 59, 18, 32),
           'arm_l': (4, 18, 25, 38), 'kin': (24, 41, 39, 48), 'hand_r': (45, 58, 36, 50), 'hand_l': (2, 17, 40, 52)}
rnd = random.Random(seed)
a = np.asarray(Image.open(IN).convert('RGB')); out = a.copy(); H, W, _ = a.shape
for n in namen:
    x0, x1, y0, y1 = PLEKKEN[n]
    gx0, gx1, gy0, gy1 = GEZICHT
    assert x1 + m < gx0 or x0 - m > gx1 or y1 + m < gy0 or y0 - m > gy1, n + ' raakt het gezicht'
    asje = AS if AS != 'mix' else rnd.choice(('kolom', 'rij'))
    stuk = a[y0:y1 + 1, x0:x1 + 1].copy()
    out[y0 - m:y1 + 1 + m, x0 - m:x1 + 1 + m] = a[y0 - m:y1 + 1 + m, x0 - m:x1 + 1 + m]
    out[y0:y1 + 1, x0:x1 + 1] = 255
    h, w = stuk.shape[:2]
    for i in range(w if asje == 'kolom' else h):
        d = rnd.randint(-m, m)
        if asje == 'kolom':
            col = stuk[:, i]; fg = col.mean(1) < 235
            for j in np.where(fg)[0]: out[y0 + j + d, x0 + i] = col[j]
        else:
            row = stuk[i]; fg = row.mean(1) < 235
            for j in np.where(fg)[0]: out[y0 + i, x0 + j + d] = row[j]
Image.fromarray(out).save(OUT)
