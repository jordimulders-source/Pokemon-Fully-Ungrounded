"""Vergelijking: hetzelfde poppetje Y onder lijfhoek 55 (C), 45 en 38 graden, als 64-px-silhouet (50%) + render.
Draaien vanuit deze map: python3 hoeken.py"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../ontwerp'))
import pop3d_lama as L
import fase3_r4 as F4
P = L.P
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
L.set_vacht('bont (foto 4)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#C9A982'
def sil64(m, yaw, fill=0.99):
    Rc = P.rot_x(math.radians(8)) @ P.rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = L.R * fill / max(x1 - x0, y1 - y0)
    c = ((x0 + x1) / 2, (y0 + y1) / 2 + (1 - fill) * L.R / scale * 0.5)
    zb, gid, nrm, gr = L.render(m, yaw, 8, scale, c)
    und, a = L.shade(zb, gid, nrm, gr, out=256)
    a = np.asarray(a, float); k = a.shape[0] // 64
    return und, a.reshape(64, k, 64, k).mean((1, 3)) >= 0.5
opts = [(55, 10, 'C (gekozen): lijf 55°'), (45, 18, 'C2: lijf 45°'), (38, 24, 'C3: lijf 38°')]
im = Image.new('RGB', (12 + 266 * 3, 44 + 290 + 300), 'white'); d = ImageDraw.Draw(im)
d.text((12, 12), 'Lama fase 3 (Y): hoe leest de pose op 64 px? Zelfde poppetje, lijf iets minder frontaal', font=FB, fill=(30, 30, 30))
for i, (yaw, hy, lab) in enumerate(opts):
    F4.HEAD_YAW = hy; m = F4.fase3_r4('Y')
    und, S = sil64(m, yaw)
    im.paste(und, (12 + 266 * i, 44)); d.text((16 + 266 * i, 304), lab, font=F, fill=(60, 60, 60))
    s = np.full((64, 64, 3), 255, np.uint8); s[S] = (40, 30, 30); s = Image.fromarray(s)
    im.paste(s.resize((256, 256), Image.NEAREST), (12 + 266 * i, 330)); im.paste(s, (12 + 266 * i + 190, 330 + 190))
    ys, xs = np.nonzero(S)
    d.text((16 + 266 * i, 592), f'{int(S.sum())} px, box {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}', font=F, fill=(60, 60, 60))
im.save(os.path.join(HERE, 'vel_hoeken.png'))
