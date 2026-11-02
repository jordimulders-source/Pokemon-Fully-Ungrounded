"""8x-weergave om zelf te kijken (licht en donker), met rasternummers."""
import os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
s = int(sys.argv[1]) if len(sys.argv) > 1 else 8
im = Image.open(os.path.join(OUT, 'lama.png')).convert('RGBA')
for name, bg in (('licht', (236, 236, 236, 255)), ('donker', (40, 44, 56, 255))):
    b = Image.new('RGBA', (64, 64), bg); b.alpha_composite(im)
    z = b.resize((64 * s, 64 * s), Image.NEAREST); d = ImageDraw.Draw(z)
    for i in range(0, 64, 5): d.text((i * s + 1, 1), str(i), fill=(255, 0, 0)); d.text((1, i * s + 1), str(i), fill=(255, 0, 0))
    z.save(os.path.join(sys.argv[2] if len(sys.argv) > 2 else HERE, f'zoom_{name}.png'))
