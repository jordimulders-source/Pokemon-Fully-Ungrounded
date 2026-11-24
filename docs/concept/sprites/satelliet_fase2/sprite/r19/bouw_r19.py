# r19 op r18. Jordi over r18: "de lijn rechts naast het paneel golft niet genoeg, kijk naar het model".
# Gemeten in het model (1024, panelen_80b; uitsneden rr.png/ll.png in het verslag), buitenrand van de zwarte lijfcontour per rij:
# RECHTS (tussen kap en groot paneel): rij 24 38,1 | 25 37,7 | 26 37,5 | 27-28 37,4 | 29 37,5 | 30 37,6-38,2  -> r18 heeft al x38, 37, 37 ... (0 px verschil).
# LINKS (rechts naast het kleine paneel, de bolling van de lens): rij 27 13,9 | 28 13,6 | 29 13,2 | 30 12,9 | 31 12,8 | 32-37 12,5-12,7 |
#   38-39 12,7 | 40 13,1 | 41 13,4 | 42 13,9 | 43 14,4 | 44 15,1 | 45 16,0. r18 lag op rij 28-29 en 40-45 een pixel naar binnen (vlakkere bolling).
# Rij 32-37 (model 12,5-12,7) blijft x13: daar is de zwarte lensring van oog b zelf de contour (oog b blijft).
import numpy as np
from PIL import Image
im0 = Image.open('../r18/sprite.png'); r18 = np.array(im0).astype(int); a = r18.copy(); pal = im0.getpalette()[:48]
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c != '-': a[y, x + i] = 0 if c == '.' else H.index(c)
put(13, 28, '13')      # contour x14 -> x13, oude contourpixel wordt wit-lila vlak (3, zoals rechts ernaast)
put(13, 29, '13')
put(13, 40, '13')
put(13, 41, '133')
put(14, 43, '15')
put(15, 44, '15')
put(16, 45, '111')
def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal))); im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); m = np.array(im.convert('RGBA')); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
if __name__ == '__main__':
    sla(a, 'sprite.png')
    H2 = '.123456789ABCDEF'
    for y in range(26, 48): print('%2d ' % y + ''.join(H2[v] for v in r18[y, 4:24]) + '   ' + ''.join(H2[v] for v in a[y, 4:24]))
    d = a != r18; print('gewijzigd:', int(d.sum()), ' silhouet:', int(((a == 0) != (r18 == 0)).sum()), ' kleuren:', len(np.unique(a)))
