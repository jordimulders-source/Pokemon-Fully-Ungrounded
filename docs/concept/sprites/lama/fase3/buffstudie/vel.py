"""Buffstudie fase 3 (5 nov, Jordi: "kijk ook vooral hoe andere sprites dat doen"): Gen 3-sprites die zwaar/buff ogen,
op 3x, met px-telling. Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/fase3/buffstudie/vel.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, '../../../../../../graphics/pokemon')
NAMEN = ['entei', 'raikou', 'arcanine', 'tauros', 'rapidash', 'stantler', 'girafarig', 'camerupt', 'ursaring', 'machamp', 'hariyama', 'swampert']
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
def frame(n):
    im = Image.open(os.path.join(G, n, 'anim_front.png'))
    p = im.convert('P') if im.mode != 'P' else im
    a = np.array(p)[:64, :64]; rgb = np.array(p.convert('RGB'))[:64, :64]
    rgb[a == 0] = 255; return Image.fromarray(rgb), int((a != 0).sum())
cols = 6; im = Image.new('RGB', (12 + 200 * cols, 30 + 220 * 2 + 10), 'white'); d = ImageDraw.Draw(im)
d.text((12, 8), 'Gen 3: hoe sprites massa en kracht tonen (3x)', font=F, fill=(30, 30, 30))
for i, n in enumerate(NAMEN):
    f, px = frame(n); x, y = 12 + 200 * (i % cols), 30 + 220 * (i // cols)
    im.paste(f.resize((192, 192), Image.NEAREST), (x, y)); d.text((x, y + 196), f'{n} ({px} px)', font=F, fill=(60, 60, 60))
im.save(os.path.join(HERE, 'gen3_buff.png'))
