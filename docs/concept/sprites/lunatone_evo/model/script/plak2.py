# Netter: v11-oog en -neus wegwerken, alleen oog- en neuspixels van v5 erop, kleuren naar v11
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
D, OUT = sys.argv[1], sys.argv[2]
S = float(sys.argv[3]) if len(sys.argv) > 3 else 1.18
v11 = np.array(Image.open(f'{D}/r11/gemini_v11.png').convert('RGB')).astype(int)
v5 = np.array(Image.open(f'{D}/r5/gemini_v5.png').convert('RGB')).astype(int)
H = 1024
def poly(pts, ell=None):
    m = Image.new('L', (H, H), 0); d = ImageDraw.Draw(m)
    if pts: d.polygon(pts, fill=255)
    if ell: d.ellipse(ell, fill=255)
    return np.array(m) > 0
white = lambda a: a.min(-1) > 200
# 1. v11: oog + neus wegwerken
yy, xx = np.mgrid[0:H, 0:H]
body = (xx-560)**2 + (yy-505)**2 < 292**2
old_eye = poly(None, (418, 388, 642, 628))
old_nose = poly([(60,505),(380,432),(415,440),(415,560),(395,560),(80,525)])
gat = old_eye | (old_nose & body)
out = v11.copy()
out[old_nose & ~body] = 255
# vul gat met de dichtstbijzijnde lijfpixel buiten het gat (niet-wit)
# eerst textuur van het lijf rechts van het oog (x+230) waar dat lijf is
sx2 = (xx + 230).clip(0, H-1)
tex = gat & ~white(v11[yy, sx2]) & ~old_eye[yy, sx2]
out[tex] = v11[yy[tex], sx2[tex]]
bron = ~gat & ~white(out)
_, (iy, ix) = ndimage.distance_transform_edt(~bron, return_indices=True)
rest = gat & ~tex
out[rest] = out[iy[rest], ix[rest]]
# 2. v5: oog (zwart + rood iris) en neus
c5 = np.array([597, 515]); c11 = np.array([525, 508])
eye5 = poly(None, (c5[0]-92, c5[1]-86, c5[0]+92, c5[1]+86))
nose5 = poly([(195,495),(330,452),(452,452),(466,520),(452,568),(370,572),(212,538)])
keep = (eye5 | nose5) & ~white(v5)
bx0, by0, bx1, by1 = 190, 425, 700, 610
sub = keep[by0:by1, bx0:bx1]; rgb = v5[by0:by1, bx0:bx1]
w, h = bx1-bx0, by1-by0; W, Hh = round(w*S), round(h*S)
sub = np.array(Image.fromarray((sub*255).astype(np.uint8)).resize((W, Hh), Image.NEAREST)) > 0
rgb = np.array(Image.fromarray(rgb.astype(np.uint8)).resize((W, Hh), Image.NEAREST)).astype(int)
ox = round(c11[0] - (c5[0]-bx0)*S); oy = round(c11[1] - (c5[1]-by0)*S)
ly, lx = np.nonzero(sub); ty, tx = ly + oy, lx + ox
ok = np.ones(len(ty), bool)
cols = rgb[ly, lx]
# 3. kleuren van de neus en het lijf naar het v11-palet (rood van de iris en zwart blijven)
pal_src = v11[body & ~gat & ~white(v11)]
pal = np.unique((pal_src // 8) * 8 + 4, axis=0)
iris = (cols[:,0] > 170) & (cols[:,1] < 90)
dark = cols.sum(1) < 140
m = ~iris & ~dark
if m.any():
    d2 = ((cols[m][:,None,:] - pal[None,:,:])**2).sum(-1)
    cols[m] = pal[d2.argmin(1)]
out[ty[ok], tx[ok]] = cols
# 4. kleine puinstukjes weg
nonw = ~white(out)
lab, n = ndimage.label(nonw)
sizes = ndimage.sum(nonw, lab, range(1, n+1))
main = np.argmax(sizes) + 1
drop = int(sys.argv[4]) if len(sys.argv) > 4 else 2500
for i, s in enumerate(sizes, 1):
    if i != main and s < drop: out[lab == i] = 255
out[white(out)] = 255
Image.fromarray(out.astype(np.uint8)).save(OUT)
