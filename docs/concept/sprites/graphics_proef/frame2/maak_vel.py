# Overzichtsvel frame2_vel.png (4x): per soort een rij, per variant frame 1 | frame 2 + engine-animatie.
import glob, numpy as np
from PIL import Image, ImageDraw
Z = 4; W = 64*Z
rijen = []
for soort in ('gumfish', 'hexpress'):
    rij = []
    for p in sorted(glob.glob(f'{soort}_*_anim_front.png')):
        k = p.split('_')[1]
        anim = glob.glob(f'{soort}_{k}_anim_*.gif')[0][len(f'{soort}_{k}_'):-4].upper()
        rij.append((f'{soort} {k}', Image.open(p), anim))
    rijen.append(rij)
n = max(len(r) for r in rijen)
sh = Image.new('RGB', (8+n*(2*W+28), len(rijen)*(W+44)+4), 'white'); d = ImageDraw.Draw(sh)
for r, rij in enumerate(rijen):
    for i, (naam, im, anim) in enumerate(rij):
        x0, y0 = 8+i*(2*W+28), 4+r*(W+44)
        rgba = im.convert('RGBA')
        for j in range(2):
            bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(rgba.crop((0, 64*j, 64, 64*j+64)))
            sh.paste(bg.convert('RGB').resize((W, W), Image.NEAREST), (x0+j*(W+4), y0))
            d.rectangle([x0+j*(W+4), y0, x0+j*(W+4)+W-1, y0+W-1], outline=(210, 210, 210))
        d.text((x0, y0+W+6), f'{naam}: frame 1 | frame 2', fill=(0, 0, 0))
        d.text((x0, y0+W+20), anim, fill=(0, 0, 0))
sh.save('frame2_vel.png')
