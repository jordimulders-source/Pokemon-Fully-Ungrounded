"""Rugpatroon ronde 6 (Claude, 5 nov): Jordi's krabbel als richting, niet als overtrek ("mijn krabbel is dus niet perfect he,
het is een krabbel"). Drie gelijke ')'-banden, gelijke afstand, gelijke vorm; elke band begint net onder de rugomtrek en
buigt mee om de romp naar de buik; 2 px in het midden, 1 px aan de uiteinden. Tint volgt de lichaamsshading:
15 linksboven, 13 midden, 14 onderaan en op schaduw. Geen extra randlijnen."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../../kleur/ronde7c/nachtaap_fase3.png')); A0 = np.array(src); pal = src.getpalette()
FUR = np.isin(A0, [3, 4, 5])
BANDEN = [(23, 32), (29, 31), (35, 30)]   # (x, bovenste rij) uit de krabbel, gelijk verdeeld
a = A0.copy(); M = np.zeros_like(FUR)
# één vaste bandvorm (')', 11 rijen: (dx, breedte)), drie keer geplaatst op gelijke afstand -> gelijk en netjes
VORM = [(0, 2), (1, 2), (1, 3), (2, 3), (2, 3), (2, 3), (2, 3), (1, 3), (1, 2), (0, 2), (0, 1)]
for x0, y0 in BANDEN:
    for i, (dx, w) in enumerate(VORM):
        y = y0 + i; f = i / (len(VORM) - 1)
        for j in range(w):
            x = x0 + dx + j
            if not FUR[y, x]: continue
            M[y, x] = True; u = A0[y, x]
            if w >= 2 and j == w - 1: c = 14                                 # schaduwkant rechts
            elif j == 0 and w == 3 and f < 0.6 and u != 3: c = 15            # licht linksboven
            else: c = 14 if f > 0.85 else 13                                  # band loopt over de schaduwnaad heen
            a[y, x] = c
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(os.path.join(H, 'nachtaap_fase3.png'), transparency=0)
print('px', int(M.sum()))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
def rgb(arr, bgc=(255, 255, 255, 255)):
    i = Image.fromarray(arr, 'P'); i.putpalette(pal); r = np.array(i.convert('RGBA')); r[arr == 0, 3] = 0
    bb = Image.new('RGBA', (64, 64), bgc); bb.alpha_composite(Image.fromarray(r)); return bb.convert('RGB')
v = Image.new('RGB', (1060, 250), 'white'); d = ImageDraw.Draw(v)
kr = Image.open(os.path.join(H, '../../referenties/jordi_krabbel_rugbanden.png')).convert('RGB')
v.paste(kr.resize((192, 229)), (10, 18)); d.text((10, 2), 'jouw krabbel', font=F, fill='black')
t = rgb(a); d.text((220, 2), 'ronde 6, 3x | 1x', font=F, fill='black')
v.paste(t.resize((192, 192), Image.NEAREST), (220, 18)); v.paste(t, (420, 18)); v.paste(rgb(a, (36, 36, 48, 255)), (420, 94))
d.text((500, 2), '8x romp', font=F, fill='black'); v.paste(t.crop((18, 26, 46, 48)).resize((224, 176), Image.NEAREST), (500, 18))
f2 = Image.open(os.path.join(H, '../../../nachtaap_evo/af/nachtaap_evo.png')).convert('RGBA'); b2 = Image.new('RGBA', (64, 64), 'white'); b2.alpha_composite(f2)
d.text((740, 2), 'fase 2', font=F, fill='black'); v.paste(b2.convert('RGB').resize((192, 192), Image.NEAREST), (740, 18))
v.save(os.path.join(H, 'vel.png'))
