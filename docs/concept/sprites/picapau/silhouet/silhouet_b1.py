"""Silhouet uit de B1-render (Jordi koos B1, 5 nov): render 512 = 8x, verkleind met BOX, alpha-drempel.
Uitvoer: silhouet_b1_1x.png (64x64) en silhouet_b1_over_render.png (rode omtrek over de render, 8x)."""
import numpy as np
from PIL import Image
P = 'docs/concept/sprites/picapau/'
im = Image.open(P + 'blender/B1/b1.png').convert('RGBA')
a = np.asarray(im.resize((64, 64), Image.BOX))[..., 3] > 100
ys, xs = np.nonzero(a); print('bbox', xs.min(), xs.max(), ys.min(), ys.max(), 'px', a.sum())
sil = np.zeros((64, 64, 4), np.uint8); sil[a] = (0, 0, 0, 255)
Image.fromarray(sil).save(P + 'silhouet/silhouet_b1_1x.png')
ov = Image.new('RGBA', (512, 512), (225, 225, 225, 255)); ov.alpha_composite(im)
o = np.asarray(ov).copy()
rand = a & ~(np.roll(a, 1, 0) & np.roll(a, -1, 0) & np.roll(a, 1, 1) & np.roll(a, -1, 1))
for y, x in zip(*np.nonzero(rand)):
    o[y*8:y*8+8, x*8:x*8+8] = (230, 20, 20, 255)
Image.fromarray(o).save(P + 'silhouet/silhouet_b1_over_render.png')
