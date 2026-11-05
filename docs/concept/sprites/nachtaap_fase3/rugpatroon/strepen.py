"""Rugpatroon optie D (Jordi: "kunnen we niet voor horizontale strepen gaan en dan meerdere? Zoals bij de vorige lijn?
Genoeg pokemon die dat hebben"): meerdere dwarsstrepen over de rug, taps van de ruggengraat de flank in (fase 2-stijl),
licht met een schaduwrand; 4 en 6 strepen als varianten. Ruw, om te kiezen; de maker tekent het netjes."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(H, '../../../../..')
exec(open(os.path.join(H, 'opties.py')).read().split('opts = {}')[0])  # src, idx0, pal, L, S, rug, zet
D = 3
def rand(idx, pts):
    ps = set(pts)
    for x, y in pts:
        for dx, dy in ((0, 1), (1, 0), (1, 1)):
            q = (x + dx, y + dy)
            if q not in ps: zet(idx, [q], D)
def binnen(idx, x, y): return 0 <= x < 64 and 0 <= y < 64 and idx[y, x] not in (0, 1, 2, 7)
def streep(idx, x0, y0, lengte):
    """brede dwarsstreep: 3 px aan de ruggengraat, taps naar 1 px, licht schuin met de ronding mee; stopt aan de lijfrand"""
    pts = []
    for k in range(lengte):
        w = 3 if k < lengte * 0.45 else (2 if k < lengte * 0.8 else 1)
        x = x0 - k // 4
        row = [(x + i, y0 + k) for i in range(w) if binnen(idx, x + i, y0 + k)]
        if not row: break
        pts += row
    return pts
var = {}
for naam, xs in (('D5: 5 brede strepen', (21, 26, 40, 45, 30)), ('D7: 7 brede strepen', (21, 24, 28, 39, 42, 45, 30))):
    a = idx0.copy(); r = rug(a); allp = []
    for x0 in xs:
        if x0 == 30:  # streep vlak voor het opgeheven been
            pass
        x0 = min(r, key=lambda x: abs(x - x0)); allp += streep(a, x0, r[x0], 12)
    rand(a, allp); zet(a, allp, L)
    var[naam] = a
def rgb(arr):
    im = Image.fromarray(arr.astype(np.uint8), 'P'); im.putpalette(pal)
    a_ = np.array(im.convert('RGBA')); a_[arr == 0, 3] = 0
    bg = Image.new('RGBA', (64, 64), 'white'); bg.alpha_composite(Image.fromarray(a_)); return bg.convert('RGB')
def gba(n):
    a = Image.open(os.path.join(ROOT, f'graphics/pokemon/{n}/anim_front_gba.png')); idx = np.array(a)[:64]
    rgba = np.array(a.convert('RGBA'))[:64]; rgba[idx == 0, 3] = 0
    bg = Image.new('RGBA', (64, 64), 'white'); bg.alpha_composite(Image.fromarray(rgba)); return bg.convert('RGB')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
vel = Image.new('RGB', (3 * 214 + 10, 470), 'white'); d = ImageDraw.Draw(vel)
for i, (lab, arr) in enumerate([('zonder (v7)', idx0)] + list(var.items())):
    t = rgb(arr); x = 10 + i * 214
    vel.paste(t.resize((192, 192), Image.NEAREST), (x, 26)); vel.paste(t, (x, 226))
    vel.paste(t.crop((14, 22, 50, 50)).resize((108, 84), Image.NEAREST), (x + 76, 226)); d.text((x, 6), lab, font=F, fill='black')
d.text((10, 322), 'Referenties (Gen 3, 2x): strepen over de rug', font=F, fill='black')
fase2 = Image.open(os.path.join(H, '../../nachtaap_evo/af/nachtaap_evo.png')).convert('RGBA'); b2 = Image.new('RGBA', (64, 64), 'white'); b2.alpha_composite(fase2)
for i, (n, t) in enumerate([('fase 2', b2.convert('RGB'))] + [(n, gba(n)) for n in ('raikou', 'linoone', 'zigzagoon', 'furret')]):
    x = 10 + i * 130; vel.paste(t.resize((128, 128), Image.NEAREST), (x, 340)); d.text((x, 455), n, font=f, fill='black')
vel.save(os.path.join(H, 'vel_strepen.png'))
