# r3 = r2 met alleen het oog (x10-13, y47-49) anders georiënteerd (Jordi: "hij kijkt naar rechtsboven, hij moet naar linksbeneden kijken").
# Zelfde Sandshrew-kern 4x3 (kolom 19-22 x rij 28-30), alleen gespiegeld/gedraaid; rest pixelgelijk aan r2.
import sys, numpy as np
from PIL import Image
D = __file__.rsplit('/', 1)[0]
r2 = np.load(D + '/r2.npy'); pal = Image.open(D + '/r2.png').getpalette()
SAND = ['fecf', 'ffcc', 'fffe']                     # r2 (wit rechtsboven, zwart linksonder)
VAR = {
    'A_180': [r[::-1] for r in SAND[::-1]],          # 180 graden: wit linksonder, zwart rechtsboven
    'B_hor': [r[::-1] for r in SAND],                # horizontaal gespiegeld: wit linksboven
    'C_ver': SAND[::-1],                             # verticaal gespiegeld: wit rechtsonder
}
MAP = {'f': 1, 'c': 11, 'e': 5}
def bouw(rijen):
    a = r2.copy()
    for j, rij in enumerate(rijen):
        for i, ch in enumerate(rij): a[47 + j, 10 + i] = MAP[ch]
    assert (a != r2)[:, :].sum() <= 12 and (a[:47] != r2[:47]).sum() == 0 and (a[50:] != r2[50:]).sum() == 0
    return a
def opslaan(a, f):
    im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(pal); im.save(f, transparency=0)
for k, v in VAR.items():
    opslaan(bouw(v), D + f'/r3_oog/r3_{k}.png'); print(k, v)
keuze = sys.argv[1] if len(sys.argv) > 1 else 'A_180'
a = bouw(VAR[keuze]); np.save(D + '/r3.npy', a); opslaan(a, D + '/r3.png')
rgb = Image.open(D + '/r3.png').convert('RGBA'); bg = Image.new('RGBA', rgb.size, (255, 255, 255, 255)); bg.alpha_composite(rgb)
bg.resize((512, 512), Image.NEAREST).save(D + '/r3_8x.png')
print('r3 =', keuze, 'diff t.o.v. r2:', (a != r2).sum())
