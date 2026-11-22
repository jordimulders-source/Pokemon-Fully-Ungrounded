# r3: raster met de hand (rijen_r3.txt, '|' = alleen leesbaarheid). Silhouet moet pixel voor pixel gelijk zijn aan r2.
# Palet: tinten uit het Gemini-model (palet_gemeten.json van r2), ramps teruggebracht tot 3 vultinten + lijn;
# lichtste/donkerste stap iets verlegd voor contrast (keuring r2). Geen nieuwe kleurfamilies.
import sys, numpy as np
from PIL import Image
from bouw_r3_palet import PAL
ORDE = '.krHGFECBApqw'
rows = [ln.rstrip('\n').replace('|','') for ln in open('rijen_r3.txt')]
rows = [r for r in rows if r != '']
assert len(rows) == 63, len(rows)
R2 = np.load('../sprite_r2/raster_r2.npy', allow_pickle=True)
T = np.full((63,63), '.', object)
fout = 0
for y, r in enumerate(rows):
    r = r.ljust(63, '.')
    if len(r) != 63: print('rij', y, 'te lang', len(r)); fout += 1; continue
    for x, ch in enumerate(r):
        assert ch in PAL, (y, x, ch)
        T[y,x] = ch
    a = ''.join('#' if c != '.' else '.' for c in r)
    b = ''.join('#' if c != '.' else '.' for c in R2[y])
    if a != b:
        fout += 1
        print('rij %2d silhouet wijkt af:' % y); print('  r3', a); print('  r2', b)
if fout: sys.exit('silhouet niet gelijk')
for ln in open('patch_r3.txt'):
    ln = ln.split('#')[0].strip()
    if not ln: continue
    y, x, s_ = ln.split(); y, x = int(y), int(x)
    for i, ch in enumerate(s_):
        assert T[y,x+i] != '.', ('patch buiten silhouet', y, x+i)
        T[y,x+i] = ch
img = np.zeros((64,64), 'uint8')
for y in range(63):
    for x in range(63): img[y+1,x] = ORDE.index(T[y,x])
im = Image.fromarray(img, 'P'); pal = []
for c in ORDE: pal += PAL[c]
im.putpalette(pal + [0]*(768-len(pal)))
im.save('kecleon_evo_r3.png', transparency=0)
im.convert('RGBA').resize((512,512), Image.NEAREST).save('kecleon_evo_r3_8x.png')
np.save('raster_r3.npy', T)
print('silhouet gelijk aan r2 (diff 0); kleuren incl. transparant:', len(np.unique(img)))
