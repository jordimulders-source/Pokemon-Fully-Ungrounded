"""Draai de generator voor een model en maak een vergelijkingsvel (zelfde schaal: 1x en 4x).
Gebruik: python3 tools/grounded/spritegen/run.py <model> [referentie-soort] [uitmap]"""
import importlib
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'models'))
import gen


def ref_img(name):
    im = Image.open(os.path.join('graphics/pokemon', name, 'anim_front.png'))
    a = np.array(im)[:64, :64]
    rgb = np.array(im.convert('RGB'))[:64, :64]
    o = np.zeros((64, 64, 4), np.uint8); o[..., :3] = rgb; o[..., 3] = (a != 0) * 255
    return Image.fromarray(o, 'RGBA')


def main():
    name = sys.argv[1]
    refs = sys.argv[2].split(',') if len(sys.argv) > 2 else []
    outdir = sys.argv[3] if len(sys.argv) > 3 else os.path.join('/tmp')
    os.makedirs(outdir, exist_ok=True)
    mod = importlib.import_module(name)
    grid, info = gen.generate(mod.build(), mod.SPEC)
    img, keys = gen.to_image(grid, mod.SPEC['palette'])
    rep = gen.check(grid, mod.SPEC['palette'])
    print(name, rep)
    img.save(os.path.join(outdir, f'{name}.png'))
    tiles = [(name, img)] + [(r, ref_img(r)) for r in refs]
    k = 4
    W = 10 + len(tiles) * (64 * k + 10)
    sheet = Image.new('RGB', (W, 64 * k + 100), 'white')
    d = ImageDraw.Draw(sheet)
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    for i, (n, t) in enumerate(tiles):
        x = 10 + i * (64 * k + 10)
        b = t.resize((64 * k, 64 * k), Image.NEAREST)
        sheet.paste(b, (x, 10), b)
        sheet.paste(t, (x, 64 * k + 20), t)
        d.text((x + 72, 64 * k + 40), f'{n} ({int((np.array(t)[..., 3] > 0).sum())} px)', font=F, fill=(60, 60, 60))
    sheet.save(os.path.join(outdir, f'{name}_vel.png'))


main()
