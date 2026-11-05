"""Vel: Blender-model rondom (draaien) + 3/4-standen naast Fletchling, Starly, Taillow. python3.11 vel.py"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HIER, '../../../../..'))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
BG = (236, 234, 228)
RONDOM = [0, 45, 90, 135, 180, 225, 270, 315]
DRIEKWART = [('A', 25, 10), ('B', 35, 12), ('C', 45, 15)]
def render_alle():
    code = f"""
import sys; sys.path.insert(0, {HIER!r}); import kolibrie_pre as K, os
for h in {RONDOM}: K.render(os.path.join({HIER!r}, 'rond', f'rond_{{h:03d}}.png'), lijf=h, kop=0, kantel=8)
for n, l, k in {DRIEKWART}: K.render(os.path.join({HIER!r}, 'rond', f'dk_{{n}}.png'), lijf=l, kop=k, kantel=8)
"""
    subprocess.run(['python3.11', '-c', code], check=True, capture_output=True)
def ref(naam):
    im = Image.open(f'{REPO}/graphics/pokemon/{naam}/anim_front.png'); a = np.array(im.crop((0, 0, 64, 64))) != 0
    r = np.array(im.convert('RGBA').crop((0, 0, 64, 64))); r[..., 3] = a * 255
    v = Image.new('RGB', (64, 64), BG); v.paste(Image.fromarray(r), (0, 0), Image.fromarray(r)); return v
def op(p, w=200):
    im = Image.open(p).convert('RGBA').crop((72, 32, 392, 352)).resize((w, w), Image.LANCZOS)
    v = Image.new('RGB', im.size, BG); v.paste(im, (0, 0), im); return v
if __name__ == '__main__':
    if '--geen-render' not in sys.argv: render_alle()
    W = 16 + 8 * 210; V = Image.new('RGB', (W, 44 + 230 + 40 + 290 + 20), 'white'); d = ImageDraw.Draw(V)
    d.text((16, 12), 'Kolibrie pre-evo: echt 3D-model (Blender), één huid; rondom gedraaid', font=FB, fill=(40, 36, 50))
    for i, h in enumerate(RONDOM):
        V.paste(op(f'{HIER}/rond/rond_{h:03d}.png'), (16 + i * 210, 44)); d.text((16 + i * 210, 248), f'{h} gr', font=F, fill=(90, 86, 100))
    y = 44 + 230 + 40
    d.text((16, y - 26), 'Driekwart-standen (lijf / kop naar de kijker) naast Fletchling, Starly, Taillow (4x)', font=FB, fill=(40, 36, 50))
    x = 16
    for n, l, k in DRIEKWART:
        V.paste(op(f'{HIER}/rond/dk_{n}.png', 256), (x, y)); d.text((x, y + 260), f'{n}: lijf {l} gr, kop {l + k} gr', font=F, fill=(90, 86, 100)); x += 270
    for naam in ('fletchling', 'starly', 'taillow'):
        V.paste(ref(naam).resize((256, 256), Image.NEAREST), (x, y)); d.text((x, y + 260), naam.capitalize(), font=F, fill=(90, 86, 100)); x += 270
    V = V.crop((0, 0, max(x, W), V.height))
    V.save(f'{HIER}/vel_blender.png')
