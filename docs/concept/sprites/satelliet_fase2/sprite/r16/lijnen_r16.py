# Lijnen van het model op het 64-raster: skelet van de zwarte modellijnen (L < 45), elk skeletpunt telt in de spritepixel
# waarin het ligt; pixel = lijn bij >= 3 punten. Binnen de lens (d < 5,0 om (18,9; 34,65)) niet (daar komen iris/ringen uit het model).
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.morphology import skeletonize
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(int)
X0, Y0, s, T = 103, 143, 12.703, 7
L = .299 * M[..., 0] + .587 * M[..., 1] + .114 * M[..., 2]
zw = L < 45
sk = skeletonize(zw)
ys, xs = np.nonzero(sk)
sx = ((xs + .5 - X0) / s).astype(int); sy = ((ys + .5 - Y0) / s + T).astype(int)
cnt = np.zeros((64, 64), int)
ok = (sx >= 0) & (sx < 64) & (sy >= 0) & (sy < 64)
np.add.at(cnt, (sy[ok], sx[ok]), 1)
Lijn = cnt >= 3
yy, xx = np.mgrid[0:64, 0:64]
Lijn &= ~(np.hypot(xx + .5 - 18.9, yy + .5 - 34.65) < 5.0)
np.save('lijnen.npy', Lijn); np.save('lijncnt.npy', cnt)
if __name__ == '__main__':
    print('   ' + ''.join(str(x % 10) for x in range(6, 42)))
    for y in range(10, 52): print('%2d ' % y + ''.join(('#' if Lijn[y, x] else ('+' if cnt[y, x] else '.')) for x in range(6, 42)))
