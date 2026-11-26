# Fase 2: armen van Gemini r12 in de stijl van het hoofd (alleen inkleuring en lijnen; silhouet blijft).
# Grijzen in de armen krijgen via rangorde-matching de toonverdeling van het hoofd (met echte hoofdkleuren);
# zwarte lijnen in de armen worden de donkerste veelvoorkomende hoofdkleur.
import sys; from PIL import Image; import numpy as np
IN, OUT, metkin = sys.argv[1], sys.argv[2], (len(sys.argv) > 3 and sys.argv[3] == 'kin')
a = np.asarray(Image.open(IN).convert('RGB')).astype(int); H, W, _ = a.shape
L = a.mean(2); fg = L < 235
sat = a.max(2) - a.min(2)
grijs = fg & (sat < 40)
yy, xx = np.mgrid[0:H, 0:W]
arm = ((xx <= 22) & (yy >= 33)) | ((xx <= 25) & (yy >= 40)) | ((xx >= 46) & (yy >= 30))
if metkin: arm |= (xx >= 26) & (xx <= 42) & (yy >= 36)
arm &= grijs
hoofd = grijs & (yy >= 14) & (yy <= 33) & (xx >= 21) & (xx <= 45)
hk = a[hoofd]; hl = L[hoofd]; order = np.argsort(hl); hk = hk[order]; hl = hl[order]
lijnkleur = hk[int(len(hk) * 0.12)]          # donker maar geen zwart, zoals de hoofdrand
out = a.copy()
zwart = arm & (L < 30)
rest = arm & ~zwart
rl = L[rest]; rank = rl.argsort().argsort() / max(1, len(rl) - 1)
out[rest] = hk[np.clip((rank * (len(hk) - 1)).round().astype(int), 0, len(hk) - 1)]
out[zwart] = lijnkleur
im = Image.fromarray(out.astype('uint8')); im.save(OUT)
