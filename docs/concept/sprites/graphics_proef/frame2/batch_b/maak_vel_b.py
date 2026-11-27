# Overzichtsvel batch_b_vel.png (4x): per soort frame 1 | frame 2 + naam + animId.
import os, numpy as np
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
Z = 4; W = 64*Z; K = 3
rij = [l.split() for l in open('animids.txt') if l.strip()]
n = len(rij); R = (n+K-1)//K
sh = Image.new('RGB', (8+K*(2*W+28), R*(W+40)+4), 'white'); d = ImageDraw.Draw(sh)
for i, (s, anim) in enumerate(rij):
    x0, y0 = 8+(i % K)*(2*W+28), 4+(i//K)*(W+40)
    im = Image.open(f'{s}_anim_front.png').convert('RGBA')
    for j in range(2):
        bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(im.crop((0, 64*j, 64, 64*j+64)))
        sh.paste(bg.convert('RGB').resize((W, W), Image.NEAREST), (x0+j*(W+4), y0))
        d.rectangle([x0+j*(W+4), y0, x0+j*(W+4)+W-1, y0+W-1], outline=(210, 210, 210))
    d.text((x0, y0+W+4), f'{s}: frame 1 | frame 2', fill=(0, 0, 0))
    d.text((x0, y0+W+18), anim, fill=(0, 0, 0))
sh.save('batch_b_vel.png')
