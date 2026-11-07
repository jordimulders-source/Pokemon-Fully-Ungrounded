"""Rugpatroon optie E (Jordi: "kijk naar de tweede fase, naar furret, naar dusclops"): gelijke brede banden die als
boog om de ronde romp lopen (evenwijdig, gelijke afstand, strakke randen), van de ruggengraat de flank in en taps
aflopend zoals fase 2. Bogen: romp als cilinder met de kop-kant naar de kijker, dus het midden van elke band buigt
naar de staart toe ( ')' ). Getekend op 8x en per pixel op 50% dekking terug naar 64; alleen binnen de romp."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(H, '../../../../..')
src = Image.open(os.path.join(H, '../kleur/ronde1f/v7/nachtaap_fase3.png')); idx0 = np.array(src); pal = src.getpalette()
L, S = 13, 14; RAND = (0, 1, 2, 7)
def top(idx, x):
    if 31 <= x <= 38: return 35                      # onder de dijwortel van het opgeheven been
    zag = False
    for y in range(26, 48):
        if idx[y, x] in (1, 2, 7): zag = True
        elif idx[y, x] != 0 and zag: return y
    return None
def romp(idx):
    m = np.zeros((64, 64), bool)
    for x in range(21, 47):
        t = top(idx, x)
        if t is None: continue
        for y in range(t, 47):
            if idx[y, x] in RAND: break
            m[y, x] = True
    m[42:, :24] = False                               # healerarm
    return m
def banden(idx, xs, lengte=10, breedte=3.2, boog=1.6):
    K = 8; im = Image.new('L', (64 * K, 64 * K), 0); d = ImageDraw.Draw(im)
    for x0 in xs:
        t0 = top(idx, x0); L_ = lengte if x0 < 31 else lengte - 2
        left, right = [], []
        for t in np.linspace(0, 1, 30):
            cx = x0 + 0.5 + boog * math.sin(math.pi * t * 0.9) - 0.8 * t
            cy = t0 - 0.5 + L_ * t
            hw = breedte / 2 * (1 - 0.7 * t ** 1.5)
            left.append(((cx - hw) * K, cy * K)); right.append(((cx + hw) * K, cy * K))
        d.polygon(left + right[::-1], fill=255)
    a = np.asarray(im).reshape(64, K, 64, K).mean((1, 3)) / 255
    return a >= 0.5
def maak(xs):
    a = idx0.copy(); m = banden(a, xs) & romp(a)
    a[m] = L
    # schaduwkant: rechterrand van elke band 1 tint donkerder
    for y, x in zip(*np.nonzero(m)):
        if x + 1 < 64 and not m[y, x + 1]: a[y, x] = S
    return a
var = {'E4: 4 banden': maak((22, 28, 34, 41)), 'E5: 5 banden': maak((21, 26, 31, 36, 42))}
def rgb(arr):
    im = Image.fromarray(arr.astype(np.uint8), 'P'); im.putpalette(pal)
    a_ = np.array(im.convert('RGBA')); a_[arr == 0, 3] = 0
    bg = Image.new('RGBA', (64, 64), 'white'); bg.alpha_composite(Image.fromarray(a_)); return bg.convert('RGB')
def gba(n):
    a = Image.open(os.path.join(ROOT, f'graphics/pokemon/{n}/anim_front_gba.png')); idx = np.array(a)[:64]
    rgba = np.array(a.convert('RGBA'))[:64]; rgba[idx == 0, 3] = 0
    bg = Image.new('RGBA', (64, 64), 'white'); bg.alpha_composite(Image.fromarray(rgba)); return bg.convert('RGB')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14); f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
vel = Image.new('RGB', (3 * 214 + 10, 470), 'white'); d = ImageDraw.Draw(vel)
for i, (lab, arr) in enumerate([('zonder (v7)', idx0)] + list(var.items())):
    t = rgb(arr); x = 10 + i * 214
    vel.paste(t.resize((192, 192), Image.NEAREST), (x, 26)); vel.paste(t, (x, 226))
    vel.paste(t.crop((14, 22, 50, 50)).resize((108, 84), Image.NEAREST), (x + 76, 226)); d.text((x, 6), lab, font=F, fill='black')
d.text((10, 322), 'Referenties (2x): banden als boog om het lijf', font=F, fill='black')
f2 = Image.open(os.path.join(H, '../../nachtaap_evo/af/nachtaap_evo.png')).convert('RGBA'); b2 = Image.new('RGBA', (64, 64), 'white'); b2.alpha_composite(f2)
for i, (n, t) in enumerate([('fase 2', b2.convert('RGB'))] + [(n, gba(n)) for n in ('furret', 'dusclops', 'linoone')]):
    x = 10 + i * 130; vel.paste(t.resize((128, 128), Image.NEAREST), (x, 340)); d.text((x, 455), n, font=f, fill='black')
vel.save(os.path.join(H, 'vel_banden.png'))
