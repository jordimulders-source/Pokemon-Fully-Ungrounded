# Rug van v2_r4 gladmaken: binnen een polygoon (rug) textuur en binnenlijnen weg, 3 tinten uit de rug zelf,
# volume uit de sterk vervaagde originele helderheid. Omtrek, stekels (dicht bij de achtergrond) en schouder blijven.
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as nd
src = Image.open('gemini/v2_r4.webp').convert('RGB')
a = np.array(src).astype(float)
H, W = a.shape[:2]
L = a @ [0.3, 0.59, 0.11]
POLY = [(578,298),(700,318),(800,372),(848,432),(858,560),(820,612),(700,640),(640,600),(626,520),(614,430),(578,402)]
pm = Image.new('L', (W, H), 0); ImageDraw.Draw(pm).polygon(POLY, fill=1); poly = np.array(pm).astype(bool)
bg = a.min(2) > 225
dist = nd.distance_transform_edt(~bg)
zone = poly & (dist > 28)            # stekels en buitenlijn blijven
fill = zone & (L > 60)               # bruine pixels in de zone
# 3 tinten uit de rug zelf (kwantielen van de bruine pixels)
cols = a[fill]; Lf = L[fill]
tones = []
for lo, hi in [(0, 33), (33, 66), (66, 100)]:
    q0, q1 = np.percentile(Lf, [lo, hi]); sel = (Lf >= q0) & (Lf <= q1)
    tones.append(np.median(cols[sel], 0))
tones = np.array([(113,91,70),(145,120,92),(168,143,112)])  # lijftinten van schouder/dij (gemeten), niet de donkere rugtextuur
# volume: helderheid met lijnen vervangen door buurt, dan sterk vervagen, plus licht linksboven
Lb = L.copy(); Lb[zone & (L <= 60)] = np.nan
m = np.where(np.isnan(Lb), 0, Lb); w = (~np.isnan(Lb)).astype(float)
g = ndimage_s = nd.gaussian_filter(m, 30) / np.maximum(nd.gaussian_filter(w * 1.0, 30), 1e-6)
yy, xx = np.mgrid[0:H, 0:W]
g = -0.5 * (xx - 700) - 1.0 * (yy - 450)  # licht langs de bovenrand (ruggengraat), schaduw rechtsonder naar de staart
g = nd.gaussian_filter(g * zone, 8)
v = g[zone]; t1, t2 = np.percentile(v, [30, 78])
idx = np.where(g < t1, 0, np.where(g < t2, 1, 2))
out = a.copy(); out[zone] = tones[idx[zone]]
# terug naar Gemini-pixelraster (±10,24): blokmodus in de zone
o = Image.fromarray(out.astype('uint8'))
o.save('rug_glad/v2_r4_rug_glad.png')
print(tones.round())
