"""Game Freak-studie: per sprite palet, gebruik per index, en waar de donkerste tint staat (rand vs binnen)."""
import os, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *['..'] * 7))
NAMEN = ['taillow', 'starly', 'pidgey', 'fletchling', 'swablu']
def laad(n):
    im = Image.open(os.path.join(R, 'graphics', 'pokemon', n, 'anim_front.png'))
    a = np.array(im)[:64, :64]; pal = im.getpalette()[:48]
    return a, [tuple(pal[i*3:i*3+3]) for i in range(16)]
if __name__ == '__main__':
    tiles = []
    for n in NAMEN:
        a, pal = laad(n); m = a != 0
        rand = m & ~ndimage.binary_erosion(m)
        print(f'== {n}: {m.sum()} px')
        for i in range(1, 16):
            k = (a == i).sum()
            if not k: continue
            r, g, b = pal[i]; lum = int(.3*r+.59*g+.11*b)
            print(f'  {i:2d} {pal[i]} lum {lum:3d}  n {k:3d}  rand {int((rand & (a==i)).sum()):3d}  binnen {int((~rand & (a==i) & m).sum()):3d}')
        im = Image.new('RGB', (64, 64), (236, 236, 240)); px = np.array(im)
        for i in range(1, 16): px[a == i] = pal[i]
        tiles.append((n, Image.fromarray(px).resize((512, 512), Image.NEAREST)))
    vel = Image.new('RGB', (len(tiles) * 520, 540), 'white'); d = ImageDraw.Draw(vel)
    for k, (n, t) in enumerate(tiles):
        vel.paste(t, (k * 520, 24)); d.text((k * 520 + 4, 4), n + ' 8x', fill=(0, 0, 0))
    vel.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'studie.png'))
