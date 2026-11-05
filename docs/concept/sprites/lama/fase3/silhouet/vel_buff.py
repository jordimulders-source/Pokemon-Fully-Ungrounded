"""Poppetje ronde 6 (5 nov): fase 3 buffer. Jordi: "Is deze sprite wel duidelijk massiever en buffer dan fase 2? Dat moet de
bedoeling zijn, echt een buff worstelende lama" + "dan is jouw suggestie voor kortere dikkere hals misschien slim, perspectief creëren".
Zelfde ontwerp Y, pose C2 (yaw 45, kop +18); varianten: hals korter/dikker, kop relatief kleiner, poten dikker, lage camera.
Draaien vanuit deze map: python3 vel_buff.py"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../ontwerp'))
import pop3d_lama as L, fase3_r4 as F4
P = L.P
VARS = [('nu (ronde 1)', {}, 8), ('V1: hals korter', dict(neck=34, kopk=.85, nr=3, hb_hoog=True), 8),
        ('V2: + dikker', dict(neck=28, kopk=.78, nr=5, legk=1.7, hb_hoog=True), 8),
        ('V3: zwaarst', dict(neck=22, kopk=.72, nr=6, legk=1.8, hb_hoog=True), 8),
        ('B: perspectief (mislukt)', dict(neck=32, kopk=.85, nr=5, legk=1.6, persp=.2, schouder=1.0, hb_hoog=True), 8)]
def sil64(m, yaw, pitch, fill=0.99):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = L.R * fill / max(x1 - x0, y1 - y0)
    c = ((x0 + x1) / 2, (y0 + y1) / 2 + (1 - fill) * L.R / scale * 0.5)
    und, a = L.shade(*L.render(m, yaw, pitch, scale, c), out=256)
    a = np.asarray(a, float); k = a.shape[0] // 64
    return und, a.reshape(64, k, 64, k).mean((1, 3)) >= 0.5
if __name__ == '__main__':
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    L.set_vacht('bont (foto 4)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#C9A982'; F4.HEAD_YAW = 18
    cell = 262; n = len(VARS) + 1
    im = Image.new('RGB', (12 + cell * n, 44 + 290 + 290 + 100), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Lama fase 3: buffer (kortere dikkere hals, kop relatief kleiner, dikkere poten, lage camera) naast fase 2', font=FB, fill=(30, 30, 30))
    f2 = np.array(Image.open(os.path.join(HERE, '../../fase2/af/lama.png')).convert('RGBA'))
    bg = Image.new('RGBA', (64, 64), 'white'); bg.alpha_composite(Image.fromarray(f2))
    A2 = f2[..., 3] > 0
    im.paste(bg.convert('RGB').resize((256, 256), Image.NEAREST), (12, 44)); d.text((16, 304), 'fase 2 (af)', font=F, fill=(60, 60, 60))
    def silimg(S):
        s = np.full((64, 64, 3), 255, np.uint8); s[S] = (40, 30, 30); return Image.fromarray(s)
    im.paste(silimg(A2).resize((256, 256), Image.NEAREST), (12, 334)); d.text((16, 594), f'{int(A2.sum())} px', font=F, fill=(60, 60, 60))
    im.paste(silimg(A2), (12, 624))
    for i, (lab, kw, pitch) in enumerate(VARS):
        x = 12 + cell * (i + 1)
        m = F4.fase3_r4('Y', **kw); und, S = sil64(m, 45, pitch)
        im.paste(und, (x, 44)); d.text((x + 4, 304), f'{lab}, kop {L.kopaandeel(m, 45, pitch):.0%}', font=F, fill=(60, 60, 60))
        ys, xs = np.nonzero(S)
        im.paste(silimg(S).resize((256, 256), Image.NEAREST), (x, 334))
        d.text((x + 4, 594), f'{int(S.sum())} px ({S.sum() / A2.sum():.2f}x fase 2), box {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}', font=F, fill=(60, 60, 60))
        im.paste(silimg(S), (x, 624))
    d.text((12, 700), '1x onderaan; Gen 3-zwaargewichten: Camerupt 2039, Tauros 1931, Donphan 2096, Rhyhorn 1702 px', font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, 'vel_buff.png'))
