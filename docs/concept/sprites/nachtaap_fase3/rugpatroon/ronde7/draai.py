"""Rugpatroon ronde 7 (Claude, 5 nov): Jordi "de strepen mogen een klein beetje counterclockwise draaien, probeer
verschillende standen en laat mij keuren". Ronde-6-band (zelfde vorm, plek, shading), per rij verschoven zodat de band
tegen de klok in draait om zijn midden (boven naar links, onder naar rechts). Standen 0 (ronde 6), 8, 15, 22 graden (30 gaf trappetjes, geschrapt)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../../kleur/ronde7c/nachtaap_fase3.png')); A0 = np.array(src); pal = src.getpalette()
FUR = np.isin(A0, [3, 4, 5])
BANDEN = [(23, 32), (29, 31), (35, 30)]
VORM = [(0, 2), (1, 2), (1, 3), (2, 3), (2, 3), (2, 3), (2, 3), (1, 3), (1, 2), (0, 2), (0, 1)]
def maak(graden):
    a = A0.copy(); t = np.tan(np.radians(graden)); mid = (len(VORM) - 1) / 2
    for x0, y0 in BANDEN:
        for i, (dx, w) in enumerate(VORM):
            y = y0 + i; f = i / (len(VORM) - 1); sx = int(round(t * (i - mid)))
            for j in range(w):
                x = x0 + dx + j + sx
                if not FUR[y, x]: continue
                u = A0[y, x]
                if w >= 2 and j == w - 1: c = 14
                elif j == 0 and w == 3 and f < 0.6 and u != 3: c = 15
                else: c = 14 if f > 0.85 else 13
                a[y, x] = c
    return a
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
def rgb(arr, bgc=(255, 255, 255, 255)):
    i = Image.fromarray(arr, 'P'); i.putpalette(pal); r = np.array(i.convert('RGBA')); r[arr == 0, 3] = 0
    bb = Image.new('RGBA', (64, 64), bgc); bb.alpha_composite(Image.fromarray(r)); return bb.convert('RGB')
STANDEN = [('A', 0), ('B', 8), ('C', 15), ('D', 22)]
v = Image.new('RGB', (4 * 210 + 10, 470), 'white'); d = ImageDraw.Draw(v)
for k, (n, g) in enumerate(STANDEN):
    a = maak(g); im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(os.path.join(H, f'stand_{n}.png'), transparency=0)
    X = 10 + k * 210; t = rgb(a)
    d.text((X, 4), f'{n}: {g} graden' + (' (ronde 6)' if g == 0 else ''), font=F, fill='black')
    v.paste(t.resize((192, 192), Image.NEAREST), (X, 22))
    v.paste(t.crop((18, 26, 46, 46)).resize((196, 140), Image.NEAREST), (X, 220))
    v.paste(t, (X, 370)); v.paste(rgb(a, (36, 36, 48, 255)), (X + 70, 370))
v.save(os.path.join(H, 'vel.png'))
