"""Rondom-vel van het evo-model in de pose (kopdraai 20, voorover 15), om de vorm te beoordelen.
Draaien: python3.11 rondom.py  -> rond_v1/rond_XXX.png + rond_v1/vel.png"""
import os, sys
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
import picapau_evo as m
from PIL import Image, ImageDraw
U = os.path.join(HIER, 'rond_v1'); os.makedirs(U, exist_ok=True)
HOEKEN = [0, 45, 90, 180, 270, 315]
for h in HOEKEN:
    m.render(os.path.join(U, f'rond_{h:03d}.png'), lijf=h, kop_draai=20, voorover=15, schaal=0.8)
v = Image.new('RGBA', (384 * 3, 400 * 2), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, h in enumerate(HOEKEN):
    x, y = (i % 3) * 384, (i // 3) * 400
    v.alpha_composite(Image.open(os.path.join(U, f'rond_{h:03d}.png')).resize((384, 384), Image.LANCZOS), (x, y + 14))
    d.text((x + 4, y + 2), f'lijf {h} (kop +20, voorover 15)', fill=(0, 0, 0, 255))
v.convert('RGB').save(os.path.join(U, 'vel.png'))
