"""Silhouet-overlay: gegenereerd (rood) vs referentie (blauw), overlap paars. Gebruik: overlay.py gen.png soort uit.png"""
import sys
import numpy as np
from PIL import Image
a = np.array(Image.open(sys.argv[1]).convert('RGBA'))[..., 3] > 0
im = Image.open(f'graphics/pokemon/{sys.argv[2]}/anim_front.png')
b = np.array(im)[:64, :64] != 0
o = np.full((64, 64, 3), 255, np.uint8)
o[a & ~b] = (230, 60, 60); o[b & ~a] = (60, 90, 230); o[a & b] = (150, 90, 170)
print('overlap', int((a & b).sum()), 'alleen gen', int((a & ~b).sum()), 'alleen ref', int((b & ~a).sum()))
Image.fromarray(o).resize((384, 384), Image.NEAREST).save(sys.argv[3])
