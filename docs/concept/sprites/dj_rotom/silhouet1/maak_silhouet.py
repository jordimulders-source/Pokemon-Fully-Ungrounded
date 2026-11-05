"""Silhouet DJ Rotom: de bron (Pokopia-render) direct verkleind naar 64x64.
Gebruik: python3 maak_silhouet.py <bron> <uitmap> [breedte]"""
import sys
from PIL import Image
import numpy as np
bron, uit = sys.argv[1], sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 60
im = Image.open(bron).convert('RGBA')
a = np.array(im)[..., 3]
ys, xs = np.where(a > 128)
box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
crop = im.crop(box)
s = W / crop.width
H = round(crop.height * s)
small = crop.resize((W, H), Image.BOX)
al = np.array(small)[..., 3] > 127
out = np.zeros((64, 64), bool)
ox, oy = (64 - W) // 2, 64 - H - 1  # onderaan, 1 px marge
out[oy:oy + H, ox:ox + W] = al
under = Image.new('RGBA', (64, 64)); under.paste(small, (ox, oy))
under.save(f'{uit}/onderlaag.png')
sil = Image.new('P', (64, 64)); sil.putpalette([0, 0, 0, 40, 40, 48] + [0] * 762)
sil.putdata(out.flatten().astype(int).tolist()); sil.save(f'{uit}/silhouet.png', transparency=0)
print('breedte', W, 'hoogte', H, 'px', int(out.sum()))
