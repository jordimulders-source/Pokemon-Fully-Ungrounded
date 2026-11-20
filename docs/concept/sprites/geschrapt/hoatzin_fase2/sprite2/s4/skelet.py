# skelet.py: modellijnen als verbonden paden op hoge resolutie (skelet van de zwarte lijnen in MODEL.png),
# zonder de buitenomtrek. Per pad: lengte (modelpx) en zone eromheen. Uit: skelet.npz (labels + info), skelet.png
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from skimage.morphology import skeletonize
kl = np.load('modelklas.npy')
fig = kl >= 0
lijn = (kl == 0)
# buitenomtrek weg: lijnpixels binnen 10 px van de achtergrond
binnen = nd.binary_erosion(fig, iterations=10)
sk = skeletonize(lijn) & binnen
# vertakkingen knippen zodat elk pad apart telt
nb = nd.convolve(sk.astype(int), np.ones((3, 3), int), mode='constant') - 1
knoop = sk & (nb >= 3)
paden = sk & ~nd.binary_dilation(knoop, iterations=1)
lab, n = nd.label(paden, structure=np.ones((3, 3)))
lengte = nd.sum(paden, lab, range(1, n + 1))
np.savez_compressed('skelet.npz', lab=lab.astype(np.int32), lengte=lengte, sk=sk)
print('paden', n, 'langer dan 60:', int((lengte >= 60).sum()), '100:', int((lengte >= 100).sum()))
a = np.array(Image.open('../../MODEL.png').convert('RGB')) // 3 + 170
rng = np.random.default_rng(1)
for i in np.argsort(-lengte)[:80]:
    a[lab == i + 1] = rng.integers(0, 200, 3)
Image.fromarray(a.astype(np.uint8)).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/c799a334-5afa-5ce2-a1de-fd8513506124/scratchpad/skelet.png')
