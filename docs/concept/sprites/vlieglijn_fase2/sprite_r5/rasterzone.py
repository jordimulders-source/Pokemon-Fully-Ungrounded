"""Model (1024) op het spriteraster (verschuiving DX, DY uit tabel.py), zone x22-38, y32-51, met rasterlijnen
en coordinaten; daarnaast r4B en r5 op dezelfde schaal met hetzelfde raster."""
import os
import numpy as np
from PIL import Image, ImageDraw
from celmeting import X0, Y0, sx, sy, BASIS, HIER
from tabel import DX, DY
MI = Image.open(os.path.join(BASIS, 'referenties/gemini_gekozen_r1.png')).convert('RGB')
x0, x1, y0, y1 = 22, 38, 32, 51
Z = 32


def model_zone():
    box = (X0 + (x0 - 4) * sx + DX, Y0 + (y0 - 1) * sy + DY, X0 + (x1 - 4) * sx + DX, Y0 + (y1 - 1) * sy + DY)
    return MI.crop(tuple(int(round(v)) for v in box)).resize(((x1 - x0) * Z, (y1 - y0) * Z), Image.LANCZOS)


def sprite_zone(p):
    im = Image.open(p); a = np.array(im)
    pal = np.array(im.getpalette()[:48]).reshape(16, 3).astype(np.uint8)
    rgb = pal[a]; rgb[a == 0] = (200, 225, 205)
    return Image.fromarray(rgb).crop((x0, y0, x1, y1)).resize(((x1 - x0) * Z, (y1 - y0) * Z), Image.NEAREST)


def grid(im):
    d = ImageDraw.Draw(im)
    for k in range(x1 - x0 + 1):
        d.line([(k * Z, 0), (k * Z, im.height)], fill=(255, 0, 0) if (x0 + k) % 5 == 0 else (150, 150, 150))
    for k in range(y1 - y0 + 1):
        d.line([(0, k * Z), (im.width, k * Z)], fill=(255, 0, 0) if (y0 + k) % 5 == 0 else (150, 150, 150))
    for k in range(x1 - x0):
        d.text((k * Z + 3, 2), str(x0 + k), fill=(255, 0, 0))
    for k in range(y1 - y0):
        d.text((2, k * Z + 12), str(y0 + k), fill=(255, 0, 0))
    return im


def maak(paden, uit):
    ims = [grid(model_zone())] + [grid(sprite_zone(p)) for p in paden]
    v = Image.new('RGB', (sum(i.width for i in ims) + 16 * (len(ims) - 1), ims[0].height), 'white')
    x = 0
    for i in ims:
        v.paste(i, (x, 0)); x += i.width + 16
    v.save(uit)
    return v


if __name__ == '__main__':
    maak([os.path.join(BASIS, 'sprite_r4/mug_r4B.png'), os.path.join(HIER, 'mug_r5.png')], os.path.join(HIER, 'raster_model_r4B_r5.png'))
