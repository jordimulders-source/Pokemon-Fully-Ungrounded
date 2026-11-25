# Kale reductie r16: modelraster64.png -> palet r15 (dichtstbijzijnde tint), wit binnen het lijf (raster: transparant) terug als wit.
# Achtergrond = vlakvulling vanaf de rand over bijna-wit in het volle model; spritepixel is leeg als > 50 % van zijn blok achtergrond is.
import numpy as np
from PIL import Image
from scipy import ndimage
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(int)
X0, Y0, s, T = 103, 143, 12.703, 7
wit = M.min(2) > 236
lab, n = ndimage.label(wit)
rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(rand))
mr = np.array(Image.open('modelraster64.png')).astype(int)
pal = np.array(Image.open('../r15/sprite.png').getpalette()[:48]).reshape(16, 3)
leeg = np.zeros((64, 64), bool)
for y in range(64):
    for x in range(64):
        ya, yb = int(Y0 + (y - T) * s), int(Y0 + (y + 1 - T) * s); xa, xb = int(X0 + x * s), int(X0 + (x + 1) * s)
        if ya < 0 or yb > 1024 or xb > 1024: leeg[y, x] = True; continue
        leeg[y, x] = bg[ya:yb, xa:xb].mean() > .5
def naar_pal(c):
    d = ((pal[1:] - c) ** 2).sum(1); return 1 + d.argmin()
K = np.zeros((64, 64), int)
for y in range(64):
    for x in range(64):
        if leeg[y, x]: continue
        K[y, x] = naar_pal(mr[y, x, :3]) if mr[y, x, 3] else 2
np.save('kaal.npy', K)
if __name__ == '__main__':
    H = '.123456789ABCDEF'
    r15 = np.array(Image.open('../r15/sprite.png'))
    for y in range(5, 55): print('%2d ' % y + ''.join(H[v] for v in K[y, 4:46]) + '  ' + ''.join(H[v] for v in r15[y, 4:46]))
    im = Image.fromarray(K.astype('uint8'), 'P'); im.putpalette(list(pal.flatten()) + [0] * (768 - 48)); im.save('kaal.png', transparency=0)
