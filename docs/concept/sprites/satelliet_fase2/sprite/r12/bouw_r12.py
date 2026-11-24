# r12: (1) rode lijn: lijfcontour linksboven als bolle boog (model), (2) afwerking. Basis: ../r11/var_a.png (Jordi koos A).
# Draaien vanuit deze map: python3 bouw_r12.py
import numpy as np
from PIL import Image
im0 = Image.open('../r11/var_a.png'); a = np.array(im0).astype(int); pal = im0.getpalette()[:48]
va = a.copy()
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c == '-': continue
        a[y, x + i] = 0 if c == '.' else H.index(c)

# ================= 1. rode lijn =================
# contour (1 px, kleur 1) per rij: trapjes 1-1-1-1-2-2-3-2 (bol, steiler naar onder zoals de ronding in het model)
NIEUW = {18: 20, 19: 19, 20: 18, 21: 17, 22: 16, 23: 16, 24: 15, 25: 15, 26: 14, 27: 14, 28: 14}
for y, xl in NIEUW.items():
    oud = [x for x in range(10, 23) if va[y, x] == 1][0]
    a[y, xl] = 1
    a[y, xl - 1] = 11                         # lichte paneelrand (B) loopt mee
    for x in range(xl + 1, max(oud, xl) + 1):  # wat lijf wordt: wit
        a[y, x] = 2
# lijf langs de contour: geen lavendel strook, lichtkant = wit
for y in range(18, 29):
    for x in range(12, 24):
        if a[y, x] == 3: a[y, x] = 2
# kraaghoek: rand loopt 2 px tot tegen de nieuwe contour
put(21, 18, '762')

# ================= 2. afwerking (geen vormen veranderd) =================
# lijf rechts: 4|5-grens zonder hobbel (r24 x35 en r26 x35 zijn al 5)
a[25, 35] = 5
# lijf tussen koepellijn en bolletje: 2-wig houdt op bij r30, r31 helemaal 3 (geen 2-zakje onder een 3)
a[31, 30] = 3; a[31, 31] = 3
# binnenwitte ring om de lens: boven lichter dan rechts (r29 had 3 boven een 2)
a[29, 22] = 2; a[29, 23] = 2
# onderkant binnenring: bovenste rij 3, onderste rij 4 (geen losse 4 tussen 3-en)
a[40, 16] = 3; a[41, 16] = 4
# koepelrand linksonder: dubbele zwarte lijn -> 1 px (buitenste silhouetpixel blijft, binnenste krijgt de vulling ernaast)
a[40, 14] = 3; a[41, 15] = 3; a[42, 15] = 7; a[43, 16] = 4; a[44, 17] = 4
# koepellijn rechtsonder: dubbele pixels eruit (lijn loopt diagonaal door)
a[42, 25] = 4; a[41, 27] = 5
# onderrand: dubbele pixel waar de bocht in de bodemlijn overgaat
a[46, 21] = 5

# ======== OPSLAAN
def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); rgba = im.convert('RGBA'); m = np.array(rgba); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
sla(a, 'sprite.png'); np.save('r12.npy', a)
d = a != va
print('afwijkend t.o.v. var_a:', d.sum(), ' kleuren', len(np.unique(a)))
for nm, (x0, x1, y0, y1) in {'rode lijn': (4, 24, 16, 31), 'boven': (21, 51, 5, 21), 'koepel': (8, 31, 26, 48), 'lijf rechts': (24, 40, 18, 47), 'groot paneel': (36, 64, 8, 56), 'klein paneel': (0, 21, 12, 43)}.items():
    print('  %-12s %d' % (nm, d[y0:y1, x0:x1].sum()))
