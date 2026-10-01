"""Project Grounded: grijze stenen standbeelden van Regirock/Regice/Registeel (uit de overworld-sprites),
op een sokkel, als 32x48 RGBA (2x3 metatiles). Gebruikt door snow_tileset.py --town (Ashfrost)."""
import numpy as np
from PIL import Image, ImageDraw

STONE = [(48, 48, 64), (80, 80, 96), (112, 112, 128), (144, 144, 160), (176, 176, 192), (208, 208, 216)]


def statue(species):
    src = Image.open(f'graphics/pokemon/{species}/overworld.png')
    idx = np.array(src)[:32, :32]                       # frame 0 (naar voren)
    rgb = np.array(src.convert('RGB'))[:32, :32].astype(float)
    lum = (rgb[..., 0] * .3 + rgb[..., 1] * .59 + rgb[..., 2] * .11) / 255
    base = Image.new('RGBA', (32, 48), (0, 0, 0, 0))
    g = ImageDraw.Draw(base)                            # sokkel
    g.rectangle((2, 33, 29, 45), fill=STONE[1] + (255,))
    g.rectangle((2, 33, 29, 35), fill=STONE[3] + (255,))
    g.line((2, 33, 29, 33), fill=STONE[4] + (255,))
    g.line((2, 45, 29, 45), fill=STONE[0] + (255,))
    g.rectangle((6, 38, 25, 40), fill=STONE[2] + (255,))
    d = np.array(base)
    ys, xs = np.nonzero(idx)
    lo, hi = lum[idx > 0].min(), lum[idx > 0].max()
    for y, x in zip(ys, xs):
        k = int(round((lum[y, x] - lo) / max(hi - lo, 1e-6) * 5))
        d[y + 3, x] = STONE[k] + (255,)
    return Image.fromarray(d)


if __name__ == '__main__':
    import sys
    o = Image.new('RGBA', (110, 48), (200, 220, 240, 255))
    for i, n in enumerate(['regirock', 'regice', 'registeel']):
        o.alpha_composite(statue(n), (i * 36, 0))
    o.resize((440, 192), Image.NEAREST).save(sys.argv[1])
