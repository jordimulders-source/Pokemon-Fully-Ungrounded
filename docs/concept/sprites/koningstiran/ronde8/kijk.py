"""Kijkvel voor eigen controle: sprite 8x + 1x/2x op licht en donker (scratch). Arg: uitvoerpad."""
import os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(HERE, 'sapa_inca.png')).convert('RGBA')
W = Image.new('RGB', (512 + 20 + 200, 512), (200, 200, 200))
bg = Image.new('RGBA', (512, 512), (236, 232, 222, 255)); bg.alpha_composite(im.resize((512, 512), Image.NEAREST))
W.paste(bg.convert('RGB'), (0, 0))
for i, col in enumerate(((248, 248, 240), (40, 44, 52))):
    for k, z in enumerate((1, 2)):
        b = Image.new('RGBA', (64 * z, 64 * z), col + (255,)); b.alpha_composite(im.resize((64 * z, 64 * z), Image.NEAREST))
        W.paste(b.convert('RGB'), (530 + k * 70 if z == 1 else 530, 10 + i * 220 + (0 if z == 1 else 70)))
W.save(sys.argv[1])
