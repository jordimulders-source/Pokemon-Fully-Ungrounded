"""Ronde 3: drie varianten van de klauwhand (frame 1) naast elkaar, in kleur en in silhouet.
python3 thumbs.py <uit.png>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import build
from shapepaint import to_rgba
z = 4
names = {'A': 'A haken samen omlaag-voren', 'B': 'B recht hangend, punten gekruld', 'C': 'C naar voren, onder elkaar (gekozen)'}
sheet = Image.new('RGB', (3 * (64 * z + 8), 2 * 64 * z + 40), (240, 238, 230)); d = ImageDraw.Draw(sheet)
for i, k in enumerate('ABC'):
    f = build.frame1(k)
    x = i * (64 * z + 8)
    d.text((x + 4, 2), names[k], fill=(0, 0, 0))
    sheet.paste(to_rgba(f, build.PAL, z, (205, 222, 205, 255)).convert('RGB'), (x, 16))
    a = np.full((64, 64, 3), 240, np.uint8); a[f > 0] = (20, 20, 20)
    sheet.paste(Image.fromarray(a).resize((64 * z, 64 * z), Image.NEAREST), (x, 24 + 64 * z))
sheet.save(sys.argv[1]); print(sys.argv[1])
