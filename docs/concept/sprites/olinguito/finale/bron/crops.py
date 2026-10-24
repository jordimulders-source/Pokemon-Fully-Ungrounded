#!/usr/bin/env python3
"""crops.py : uitsneden per onderdeel op 14x (frame 1) in keuring/."""
import tools as T
from PIL import Image
g = T.read_txt(T.H + '/werk_f1.txt')
for n, box in [('kop', (6, 15, 42, 40)), ('voorpoten', (6, 36, 34, 56)), ('achterpoten', (28, 34, 52, 56)), ('staart', (44, 28, 60, 54))]:
    im = T.rgba(g, (205, 220, 205, 255)).crop(box)
    im.resize((im.size[0] * 14, im.size[1] * 14), Image.NEAREST).save(T.H + '/keuring/%s_14x.png' % n)
