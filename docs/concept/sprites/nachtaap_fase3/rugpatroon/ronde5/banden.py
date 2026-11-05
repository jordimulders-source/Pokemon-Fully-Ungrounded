"""Rugpatroon ronde 5 (Claude, 5 nov) naar Jordi's krabbel (`referenties/jordi_krabbel_rugbanden.png`: drie gebogen banden
')' midden op de romp) + "wat dacht je van zoiets maar dan wat netter en met goede shading". Per band een gladde kromme door
de krabbel (2e-graads fit per rij), 3 px breed, ronde uiteinden; tint volgt de lichaamsshading (13 op licht/midden, 14 op
schaduw), schaduwrandje (14) aan de rechterkant. Alleen op de vacht, omtrek gelijk."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../../kleur/ronde7c/nachtaap_fase3.png')); A0 = np.array(src); pal = src.getpalette()
K = np.load(os.path.join(H, 'krabbel.npy'))
lab, n = nd.label(K, structure=np.ones((3, 3)))
banden = sorted([np.argwhere(lab == i + 1) for i in range(n)], key=lambda p: p[:, 1].mean())
banden = [b for b in banden if len(b) >= 10]
a = A0.copy(); Ks = 8
mask = Image.new('L', (64 * Ks, 64 * Ks), 0); dr = ImageDraw.Draw(mask)
for b in banden:
    ys = b[:, 0]; xs = b[:, 1]
    rows = np.arange(ys.min(), ys.max() + 1)
    cx = np.array([xs[ys == r].mean() if (ys == r).any() else np.nan for r in rows])
    ok = ~np.isnan(cx); c = np.polyfit(rows[ok], cx[ok], 2)
    t = np.linspace(rows.min(), rows.max(), 60)
    pts = [((np.polyval(c, y) + 0.5) * Ks, (y + 0.5) * Ks) for y in t]
    for i, (x, y) in enumerate(pts):
        f = i / (len(pts) - 1); w = 1.55 - 0.55 * abs(2 * f - 1) ** 2      # 3 px midden, smaller aan de uiteinden
        r = w * Ks; dr.ellipse([x - r, y - r, x + r, y + r], fill=255)
M = np.asarray(mask).reshape(64, Ks, 64, Ks).mean((1, 3)) >= 127
M &= np.isin(A0, [3, 4, 5])
for y, x in zip(*np.nonzero(M)):
    a[y, x] = 14 if A0[y, x] == 3 else 13
for y, x in zip(*np.nonzero(M)):                                         # schaduwrand rechts van elke band
    if x + 1 < 64 and not M[y, x + 1] and A0[y, x] != 3: a[y, x] = 14
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(os.path.join(H, 'nachtaap_fase3.png'), transparency=0)
print('banden', len(banden), 'px', int(M.sum()))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
def rgb(arr, bgc=(255, 255, 255, 255)):
    i = Image.fromarray(arr, 'P'); i.putpalette(pal); r = np.array(i.convert('RGBA')); r[arr == 0, 3] = 0
    bb = Image.new('RGBA', (64, 64), bgc); bb.alpha_composite(Image.fromarray(r)); return bb.convert('RGB')
v = Image.new('RGB', (1060, 330), 'white'); d = ImageDraw.Draw(v)
kr = Image.open(os.path.join(H, '../../referenties/jordi_krabbel_rugbanden.png')).convert('RGB')
v.paste(kr.resize((192, 229)), (10, 24)); d.text((10, 4), 'jouw krabbel', font=F, fill='black')
t = rgb(a); d.text((220, 4), 'netjes, 3x | 1x', font=F, fill='black')
v.paste(t.resize((192, 192), Image.NEAREST), (220, 24)); v.paste(t, (420, 24)); v.paste(rgb(a, (36, 36, 48, 255)), (420, 100))
d.text((500, 4), '8x romp', font=F, fill='black'); v.paste(t.crop((18, 26, 46, 46)).resize((224, 160), Image.NEAREST), (500, 24))
f2 = Image.open(os.path.join(H, '../../../nachtaap_evo/af/nachtaap_evo.png')).convert('RGBA'); b2 = Image.new('RGBA', (64, 64), 'white'); b2.alpha_composite(f2)
d.text((740, 4), 'fase 2', font=F, fill='black'); v.paste(b2.convert('RGB').resize((192, 192), Image.NEAREST), (740, 24))
v.save(os.path.join(H, 'vel.png'))
