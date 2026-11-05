"""Rugpatroon, ruwe opties (Jordi 5 nov: "denk gelijk na over het rugpatroon"), op kleur/ronde1f/v7 (been +7).
Alleen om te kiezen: de maker tekent het gekozen patroon later netjes (met schaduwkant, meebuigend)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../kleur/ronde1f/v7/nachtaap_fase3.png'))
idx0 = np.array(src); pal = src.getpalette()
L, S = 13, 14   # maanzilver licht / schaduw (zoals de lichte wiggen van fase 2)
def rug(idx):
    """ruggengraat: eerste binnenpixel (onder de omlijning) per kolom op de romp, buiten het opgeheven been"""
    r = {}
    for x in list(range(21, 31)) + list(range(39, 46)):
        col = idx[26:48, x]; ys = np.nonzero(col)[0]
        if len(ys): r[x] = 26 + ys[0] + 1
    return r
def zet(idx, pts, c):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64 and idx[y, x] not in (0, 1, 2): idx[y, x] = c
opts = {}
D = 3  # vachtschaduw als rand onder/naast de tekening (contrast op de belichte rug)
def rand(idx, pts):
    ps = set(pts)
    for x, y in pts:
        for dx, dy in ((0, 1), (1, 0), (1, 1)):
            q = (x + dx, y + dy)
            if q not in ps: zet(idx, [q], D)
# A: getrapte wiggen vanaf de ruggengraat (fase 2-wiggen + Andes-trede): 4 -> 3 -> 2 -> 1 px
a = idx0.copy(); r = rug(a)
for x0 in (21, 26, 40):
    y0 = r[x0]; pts = []
    for k, w in enumerate((4, 3, 2, 1)):
        pts += [(x0 + i, y0 + k) for i in range(w)]
    rand(a, pts); zet(a, pts, L); zet(a, [(x0 + 3 - k, y0 + k) for k in range(4) if 3 - k >= 1], S)
opts['A_getrapte_wiggen'] = a
# B: trapband (chakana-fries) langs de rug: band van 2 px die traps op en neer gaat
b = idx0.copy(); r = rug(b); pts = []
for x, y in r.items():
    off = 1 + (1 if (x // 2) % 2 else 0)
    pts += [(x, y + off), (x, y + off + 1)]
rand(b, pts); zet(b, pts, L)
opts['B_trapband'] = b
# C: weefruit (rombo van de kallawaya-tas): gevulde getrapte ruit midden op de rug + kleine na het been
c = idx0.copy()
def ruit(cx, cy, rr):
    return [(cx + dx, cy + dy) for dy in range(-rr, rr + 1) for dx in range(-(rr - abs(dy)), rr - abs(dy) + 1)]
p1 = ruit(25, 36, 3); p2 = ruit(42, 40, 2)
rand(c, p1); rand(c, p2); zet(c, p1, L); zet(c, p2, L); zet(c, [(25, 36), (42, 40)], D)
opts['C_weefruit'] = c
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
vel = Image.new('RGB', (4 * 214 + 10, 330), 'white'); d = ImageDraw.Draw(vel)
items = [('zonder (v7)', idx0)] + [(k.replace('_', ' '), v) for k, v in opts.items()]
for i, (lab, arr) in enumerate(items):
    im = Image.fromarray(arr.astype(np.uint8), 'P'); im.putpalette(pal)
    rgba = im.convert('RGBA'); a_ = np.array(rgba); a_[arr == 0, 3] = 0; rgba = Image.fromarray(a_)
    bg = Image.new('RGBA', (64, 64), 'white'); bg.alpha_composite(rgba); bg = bg.convert('RGB')
    x = 10 + i * 214
    vel.paste(bg.resize((192, 192), Image.NEAREST), (x, 26)); vel.paste(bg, (x, 226))
    vel.paste(bg.crop((14, 22, 50, 50)).resize((108, 84), Image.NEAREST), (x + 76, 226))
    d.text((x, 6), lab, font=F, fill='black')
    if lab != 'zonder (v7)': im.save(os.path.join(H, lab.split()[0] + '.png'))
vel.save(os.path.join(H, 'vel_opties.png'))
