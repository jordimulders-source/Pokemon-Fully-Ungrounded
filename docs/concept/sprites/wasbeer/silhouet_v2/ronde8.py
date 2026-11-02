"""Silhouet ronde 8: verre klauw zoals Jordi het zegt: "twee klauwen die even lang zijn met daartussen een kleine inkeping
zoals een koevoet". Pols/steel van ronde 2; daaronder 2 klauwen van 2 px breed tegen elkaar (x 5-6 en 7-8), even lang,
licht naar voren gebogen, alleen in de punt een kleine inkeping. Diff 0 buiten zone 1 t.o.v. ronde2.txt."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
r2 = np.array([[c == '#' for c in r.rstrip('\n')] for r in open(os.path.join(HERE, 'ronde2.txt')) if r.strip()])
a = r2.copy()
a[35:43, 4:12] = False                 # oude klauwkop weg (steel y 33-34 blijft)
KLAUW = {35: range(6, 10), 36: range(6, 10), 37: range(5, 9), 38: range(5, 9), 39: (5, 8)}   # punt: (6,39),(7,39) leeg = inkeping
for y, xs in KLAUW.items():
    for x in xs:
        a[y, x] = True
d = a != r2
ys, xs = np.nonzero(d)
print('gewijzigd', d.sum(), 'buiten zone', sum(1 for x, y in zip(xs, ys) if not (4 <= x <= 13 and 33 <= y <= 42)), 'totaal', a.sum())
open(os.path.join(HERE, 'ronde8.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in a) + '\n')
Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(HERE, 'ronde8_1x.png'))
K = 16
vel = Image.new('RGB', (12 * K + 40 + 64 + 128 + 360, 12 * K), 'white'); px = vel.load()
for y in range(32, 44):
    for x in range(3, 15):
        c = (40, 34, 34) if a[y, x] else (255, 255, 255)
        for dy in range(K):
            for dx in range(K):
                px[(x - 3) * K + dx, (y - 32) * K + dy] = c if (dx and dy) else (205, 205, 215)
one = Image.fromarray(np.where(a, 40, 255).astype(np.uint8)).convert('RGB')
vel.paste(one, (12 * K + 20, 0)); vel.paste(one.resize((128, 128), Image.NEAREST), (12 * K + 90, 0))
foto = Image.open(os.path.join(HERE, '../referenties/foto16_koevoet.webp')).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT)
foto = foto.crop((180, 700, 620, 1100)); foto.thumbnail((340, 190)); vel.paste(foto, (12 * K + 230, 0))
vel.save(os.path.join(HERE, 'vel_ronde8_klauw.png'))
