# vergelijkingsvel: model (natief) en sprite-raster op dezelfde schaal met rasterlijnen en coordinaten
# gebruik: python3 grid.py raster.txt uit.png j0 j1 i0 i1   (rasterco's in het 66x66-raster, fase 0,0)
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '.')
from render import load, PAL
txt, uit, j0, j1, i0, i1 = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
lab = load(txt); C = dict(PAL); C['.'] = (255, 255, 255)
nat = np.asarray(Image.open('../natief_zonder_wangoog.png').convert('RGB'))
Z = int(sys.argv[7]) if len(sys.argv) > 7 else 24
w, h = (i1 - i0) * Z, (j1 - j0) * Z
v = Image.new('RGB', (2 * w + 60, h + 30), 'white'); d = ImageDraw.Draw(v)
for j in range(j0, j1):
    for i in range(i0, i1):
        x, y = 30 + (i - i0) * Z, 20 + (j - j0) * Z
        d.rectangle([x, y, x + Z - 1, y + Z - 1], fill=C[lab[j, i]])
        for dy in range(2):
            for dx in range(2):
                c = tuple(int(t) for t in nat[2 * j + dy, 2 * i + dx])
                X = x + w + 20 + dx * Z // 2; Y = y + dy * Z // 2
                d.rectangle([X, Y, X + Z // 2 - 1, Y + Z // 2 - 1], fill=c)
for k, j in enumerate(range(j0, j1 + 1)):
    y = 20 + k * Z
    d.line([30, y, 30 + w, y], fill=(200, 200, 200)); d.line([50 + w, y, 50 + 2 * w, y], fill=(255, 0, 255))
    if j < j1: d.text((2, y + 6), str(j), fill=(0, 0, 0))
for k, i in enumerate(range(i0, i1 + 1)):
    x = 30 + k * Z
    d.line([x, 20, x, 20 + h], fill=(200, 200, 200)); d.line([x + w + 20, 20, x + w + 20, 20 + h], fill=(255, 0, 255))
    if i < i1 and i % 2 == 0: d.text((x + 4, 4), str(i), fill=(0, 0, 0)); d.text((x + w + 24, 4), str(i), fill=(0, 0, 0))
v.save(uit)
