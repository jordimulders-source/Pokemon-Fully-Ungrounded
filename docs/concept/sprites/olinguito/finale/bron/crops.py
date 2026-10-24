#!/usr/bin/env python3
"""crops.py : uitsneden per onderdeel op 14x (frame 1) in keuring/."""
import tools as T
from PIL import Image
g = T.read_txt(T.H + '/werk_f1.txt')
for n, box in [('kop', (6, 14, 42, 38)), ('voorpoten', (6, 34, 34, 56)), ('achterpoten', (28, 30, 50, 56)), ('staart', (40, 26, 60, 52))]:
    im = T.rgba(g, (205, 220, 205, 255)).crop(box)
    im.resize((im.size[0] * 14, im.size[1] * 14), Image.NEAREST).save(T.H + '/keuring/%s_14x.png' % n)
