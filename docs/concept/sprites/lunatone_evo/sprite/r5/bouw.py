# r5 = r4 + hooglicht op de bolling (tint 10, eindkeuring) ; variant B = dieper bloedrood (kleur naar het model)
import numpy as np
from PIL import Image
im = Image.open('r4/sprite.png'); a = np.array(im); pal = im.getpalette()[:48]
for y, x0, x1 in ((8, 31, 37), (9, 32, 36)):
    seg = a[y, x0:x1]; seg[seg == 7] = 10
def save(arr, p, fn):
    o = Image.fromarray(arr.astype(np.uint8), 'P'); o.putpalette(p + [0]*(768-len(p)))
    o.save(fn, transparency=0)
    Image.open(fn).convert('RGBA').resize((512, 512), Image.NEAREST).save(fn.replace('.png', '_8x.png'))
save(a, pal, 'r5/sprite.png')
pb = pal[:]
for i in (2, 3, 4, 5, 6, 7, 10):
    r, g, b = pal[i*3:i*3+3]; pb[i*3+1] = round(g*0.82); pb[i*3+2] = round(b*0.74)
save(a, pb, 'r5/sprite_B_bloedrood.png')
