# hulpje: model (box-gemiddelde op spriteraster, en model zelf) naast een sprite-npy, zelfde schaal; uitsnede x0 x1 y0 y1, vergroting k
import sys, json, numpy as np
from PIL import Image, ImageDraw
from meet import a, bg, S, OX, OY
def model_raster(x0, x1, y0, y1, k):
    W = int(round((x1 - x0) * S)); Hh = int(round((y1 - y0) * S))
    ox, oy = int(round(OX + x0 * S)), int(round(OY + y0 * S))
    m = np.full((Hh, W, 3), 235, 'uint8')
    sy0, sx0 = max(oy, 0), max(ox, 0)
    sub = a[sy0:oy + Hh, sx0:ox + W].copy(); sub[bg[sy0:oy + Hh, sx0:ox + W]] = 235
    m[sy0 - oy:sy0 - oy + sub.shape[0], sx0 - ox:sx0 - ox + sub.shape[1]] = sub
    im = Image.fromarray(m).resize(((x1 - x0) * k, (y1 - y0) * k), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    for X in range(0, im.width, k): d.line([(X, 0), (X, im.height)], fill=(180, 180, 200))
    for Y in range(0, im.height, k): d.line([(0, Y), (im.width, Y)], fill=(180, 180, 200))
    return im
def sprite(arr, pal, x0, x1, y0, y1, k):
    rgb = np.array(pal, 'uint8')[arr]; rgb[arr == 0] = (235, 235, 240)
    im = Image.fromarray(rgb[y0:y1, x0:x1]).resize(((x1 - x0) * k, (y1 - y0) * k), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for X in range(0, im.width, k): d.line([(X, 0), (X, im.height)], fill=(180, 180, 200))
    for Y in range(0, im.height, k): d.line([(0, Y), (im.width, Y)], fill=(180, 180, 200))
    return im
if __name__ == '__main__':
    arr = np.load(sys.argv[1]); pal = [tuple(c) for c in json.load(open(sys.argv[2]))]
    x0, x1, y0, y1, k = map(int, sys.argv[4:9])
    A = model_raster(x0, x1, y0, y1, k); Bm = sprite(arr, pal, x0, x1, y0, y1, k)
    W = Image.new('RGB', (A.width * 2 + 40, A.height + 20), (255, 255, 255)); W.paste(A, (0, 20)); W.paste(Bm, (A.width + 40, 20))
    d = ImageDraw.Draw(W)
    for i, x in enumerate(range(x0, x1)):
        for ox in (0, A.width + 40): d.text((ox + i * k + 2, 4), str(x % 100), fill=(0, 0, 0))
    for j, y in enumerate(range(y0, y1)): d.text((A.width + 14, 20 + j * k + k // 2 - 5), str(y), fill=(0, 0, 0))
    W.save(sys.argv[3])
