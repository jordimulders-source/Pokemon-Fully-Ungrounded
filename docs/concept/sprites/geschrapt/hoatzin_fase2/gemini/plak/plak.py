# r2 (Gemini, driekwart) + kop van s12 grof erop geplakt (niets getekend), voor een naad-prompt in Gemini.
import numpy as np
from PIL import Image
r2 = np.array(Image.open('../opknap_r2.png').convert('RGB')).astype(int)
H, W, _ = r2.shape
out = r2.copy()
R, G, B = r2[..., 0], r2[..., 1], r2[..., 2]
yy, xx = np.mgrid[0:H, 0:W]
rood = (R > G + 25) & (R > B + 15)                       # kuif, mond
blauw = (B > R + 40) & (G > R + 10) & (B > 150)          # masker
grijs = (abs(R - G) < 14) & (abs(G - B) < 14) & (R > 90) & (R < 200)  # snavel
zone = (xx < 380) & (yy > 200) & (yy < 640)
donker = (R + G + B < 150) & (abs(R - B) < 40) & (xx < 300) & (yy > 230)
wis = zone & (rood | blauw | grijs | donker | (xx < 235))
wis &= ~((yy > 560) & (xx > 200))                        # nek onderaan laten staan
out[wis] = 255
s = np.array(Image.open('../../sprite2/s12/hoatzin.png').convert('RGBA'))
K, OX, OY = 16, 39, -28
for y in range(16, 38):
    for x in range(0, 17):
        if s[y, x, 3] == 0: continue
        if y < 31 and x > 12: continue                   # vleugel niet meenemen
        out[OY + y*K:OY + (y+1)*K, OX + x*K:OX + (x+1)*K] = s[y, x, :3]
Image.fromarray(out.astype('uint8')).save('r2_plus_s12kop.png')
