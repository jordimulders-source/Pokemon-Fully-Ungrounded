# Variant 2: binnen de rug alleen textuur weg. Binnenlijnen -> buurtkleur, dan grote mediaan op de helderheid
# (houdt het volume van het origineel), posteriseren naar 3 gemeten lijftinten; rand van de zone zacht laten overlopen.
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
a = np.array(Image.open('gemini/v2_r4.webp').convert('RGB')).astype(float)
H, W = a.shape[:2]; L = a @ [0.3, 0.59, 0.11]
POLY = [(578,298),(700,318),(800,372),(848,432),(858,560),(820,612),(700,640),(640,600),(626,520),(614,430),(578,402)]
pm = Image.new('L', (W, H), 0); ImageDraw.Draw(pm).polygon(POLY, fill=1); poly = np.array(pm).astype(bool)
bg = a.min(2) > 225
zone = poly & (nd.distance_transform_edt(~bg) > 28)
lines = zone & (L <= 70)
# lijnen vullen met dichtstbijzijnde niet-lijnpixel
idx = nd.distance_transform_edt(lines, return_distances=False, return_indices=True)
Lf = L[idx[0], idx[1]]
Lm = nd.median_filter(Lf, size=41)
Lm = nd.gaussian_filter(Lm, 6)
tones = np.array([(113,91,70),(145,120,92),(168,143,112)], float)
edge0 = nd.distance_transform_edt(poly)
msel = zone & (edge0 >= 18)
t1, t2 = np.percentile(Lm[msel], [30, 75])
k = np.where(Lm < t1, 0, np.where(Lm < t2, 1, 2))
new = tones[k]
# zachte overgang: binnen 18 px van de polygoonrand de originele pixels houden
edge = nd.distance_transform_edt(poly)
keep_orig = edge < 18
mask = zone & ~keep_orig
out = a.copy(); out[mask] = new[mask]
Image.fromarray(out.astype('uint8')).save('rug_glad/v2_r4_rug_glad2.png')
v = Lm[mask]; print(np.percentile(v,[10,30,50,70,90]).round())
