"""Test: pose C met open stand (voorpoten verder uit elkaar in x, onderbenen slanker), zodat de poten op 64 px los lezen.
Draaien vanuit deze map: python3 open_stand.py"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../ontwerp'))
import pop3d_lama as L, fase3_r3 as F3, fase3_r4 as F4, hoeken as H
F3.POSES3['C_open'] = [
    ('leg', [(-34, -12, 16, 9.5), (-48, -40, 21, 6.6), (-56, -64, 23, 5.8)], 'wrap'),
    ('far', [(-18, -12, -16, 9.5), (-10, -40, -21, 6.6), (-4, -64, -23, 5.8)], 'wrap'),
    ('leg', [(32, -10, 16, 11), (36, -38, 21, 6.6), (34, -64, 23, 5.8)], None),
    ('far', [(40, -10, -16, 11), (52, -38, -21, 6.6), (62, -62, -23, 5.8)], None)]
src = open(os.path.join(HERE, '../../ontwerp/fase3_r4.py')).read()
assert "F3.POSES3['W_breed']" in src
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
im = Image.new('RGB', (12 + 266 * 2, 44 + 290 + 300), 'white'); d = ImageDraw.Draw(im)
d.text((12, 12), 'Pose C: nu vs open stand (zelfde hoek 55°)', font=FB, fill=(30, 30, 30))
for i, pose in enumerate(('W_breed', 'C_open')):
    F3.POSES3['_cur'] = F3.POSES3[pose]
    keep = F3.POSES3['W_breed']; F3.POSES3['W_breed'] = F3.POSES3['_cur']
    F4.HEAD_YAW = 10; m = F4.fase3_r4('Y'); F3.POSES3['W_breed'] = keep
    und, S = H.sil64(m, 55)
    lab = 'nu (C)' if i == 0 else 'C open stand'
    im.paste(und, (12 + 266 * i, 44)); d.text((16 + 266 * i, 304), lab, font=F, fill=(60, 60, 60))
    s = np.full((64, 64, 3), 255, np.uint8); s[S] = (40, 30, 30); s = Image.fromarray(s)
    im.paste(s.resize((256, 256), Image.NEAREST), (12 + 266 * i, 330)); im.paste(s, (12 + 266 * i + 190, 330 + 190))
    ys, xs = np.nonzero(S); d.text((16 + 266 * i, 592), f'{int(S.sum())} px, box {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}', font=F, fill=(60, 60, 60))
im.save(os.path.join(HERE, 'vel_open_stand.png'))
