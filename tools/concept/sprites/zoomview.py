"""zoomview.py in.png uit.png [zoom] [--grid]: geïndexeerde sprite vergroot met raster
(alle frames naast elkaar) op een licht geblokte achtergrond, plus 1x en 2x."""
import sys
import numpy as np
from PIL import Image, ImageDraw
src, dst = sys.argv[1], sys.argv[2]
z = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 8
im = Image.open(src); a = np.array(im); p = im.getpalette()
rgb = np.array(p[:48]).reshape(16, 3)
n = a.shape[0] // 64
only = [int(v) for v in sys.argv[4:] if v.isdigit()]
crop = None
W = n * (64 * z + 8) + 64 * 2 + 140
sheet = Image.new('RGB', (W, 64 * z + 8), (200, 200, 200)); d = ImageDraw.Draw(sheet)
for k in range(n):
    f = a[k * 64:(k + 1) * 64]
    img = np.zeros((64, 64, 3), np.uint8)
    yy, xx = np.mgrid[0:64, 0:64]
    img[:] = np.where((((yy // 8) + (xx // 8)) % 2)[..., None] == 0, 236, 224)
    img[f > 0] = rgb[f[f > 0]]
    big = Image.fromarray(img).resize((64 * z, 64 * z), Image.NEAREST)
    x0 = 4 + k * (64 * z + 8)
    sheet.paste(big, (x0, 4))
    if '--grid' in sys.argv:
        for i in range(0, 64, 2):
            d.text((x0 + i * z + 1, 4), str(i), fill=(0, 0, 160))
            d.text((x0 + 1, 4 + i * z + 1), str(i), fill=(0, 0, 160))
        for i in range(0, 65, 8):
            d.line([(x0 + i * z, 4), (x0 + i * z, 4 + 64 * z)], fill=(150, 150, 255))
            d.line([(x0, 4 + i * z), (x0 + 64 * z, 4 + i * z)], fill=(150, 150, 255))
    sm = Image.fromarray(img)
    sheet.paste(sm, (n * (64 * z + 8) + 8, 4 + k * 70))
    sheet.paste(sm.resize((128, 128), Image.NEAREST), (n * (64 * z + 8) + 76, 4 + k * 140))
sheet.save(dst); print(dst)
