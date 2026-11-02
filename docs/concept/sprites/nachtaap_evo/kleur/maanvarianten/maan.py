"""Maanvarianten op de kop van ronde 3 (alleen de maan; ogen, snoet, omtrek blijven). Voor Jordi's keuze."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(HERE, '..', 'ronde3', 'nachtaap.png'))
pal = src.getpalette(); A0 = np.array(src)
EYE = {1, 9, 10, 11}

def variant(oc, orad, ic, irad, ymax=60):
    a = A0.copy()
    yy, xx = np.mgrid[0:64, 0:64]
    head = np.zeros((64, 64), bool); head[36:54, 3:25] = True
    # oude maan weg: wit/zilverlila op de kop -> vacht
    old = head & np.isin(a, [7, 8])
    a[old] = 4
    o = (xx + .5 - oc[0]) ** 2 + (yy + .5 - oc[1]) ** 2 < orad ** 2
    i = (xx + .5 - ic[0]) ** 2 + (yy + .5 - ic[1]) ** 2 < irad ** 2
    moon = head & o & ~i & np.isin(a, [4, 5, 3, 6]) & (yy <= ymax)
    a[moon] = 8
    # schaduwkant (rechts/onder) van de maan in zilverlila
    sh = moon & ~np.roll(moon, -1, 1) | moon & ~np.roll(moon, -1, 0)
    a[sh & (xx > 13)] = 7
    return a

# Jordi 2 nov: referentie-sikkel (referenties/jordi_maan_referentie): dik midden, tapse scherpe punten,
# binnencirkel ±0,8R en ±0,38R verschoven -> hier omlaag (punten omlaag).
def sikkel(cy, R, k_off=0.38, k_r=0.80):
    return variant((13.5, cy), R, (13.5, cy + k_off * R), k_r * R)
V = {
 'D1: sikkel rond de ogen': sikkel(46.6, 9.0),
 'D2: sikkel iets hoger': sikkel(45.6, 8.8),
 'D3: sikkel groter, punten bij de kaak': sikkel(46.8, 9.8, 0.36, 0.80),
}
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
def img(a):
    im = Image.fromarray(a.astype(np.uint8), 'P'); im.putpalette(pal)
    rgba = im.convert('RGBA'); px = rgba.load()
    for y in range(64):
        for x in range(64):
            if a[y, x] == 0: px[x, y] = (0, 0, 0, 0)
    return rgba
o = Image.new('RGB', (4 * 330, 380), (235, 235, 240)); d = ImageDraw.Draw(o)
items = [('ronde 3 (nu)', A0)] + list(V.items())
for k, (n, a) in enumerate(items):
    im = img(a); bg = Image.new('RGBA', (64, 64), (235, 235, 240, 255)); bg.alpha_composite(im)
    o.paste(bg.crop((0, 30, 30, 58)).resize((300, 280), Image.NEAREST), (10 + 330 * k, 10))
    o.paste(bg.convert('RGB'), (10 + 330 * k, 300)); o.paste(bg.convert('RGB').resize((128, 128), Image.NEAREST).crop((0, 50, 128, 128)), (90 + 330 * k, 300))
    d.text((10 + 330 * k, 292 - 2), n, font=F, fill=(30, 30, 30))
    if k: im.save(os.path.join(HERE, 'variant_%s.png' % ['D1','D2','D3'][k - 1]))
o.save(os.path.join(HERE, 'maanvarianten.png'))
