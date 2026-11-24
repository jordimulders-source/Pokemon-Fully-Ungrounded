# vergelijkvel studie Gen 1-3 lijn/kleur: r16 | Kangaskhan echte Gen 3 (anim_front_gba + normal_gba.pal) | Kangaskhan expansion-standaard (Gen 4/5-stijl)
# + paletladders (L = luminantie).  Draaien vanuit docs/concept/sprites/bibarel_evo: python3 stijl_gen123/studie.py
import numpy as np, colorsys
from PIL import Image, ImageDraw
R = '/home/user/Pokemon-Fully-Ungrounded/'
def jasc(p):
    L = open(p).read().split('\n'); n = int(L[2]); return np.array([[int(v) for v in L[3+i].split()] for i in range(n)], dtype='uint8')
def mon(n, gba):
    s = '_gba' if gba else ''
    return np.asarray(Image.open(R+f'graphics/pokemon/{n}/anim_front{s}.png'))[:64].astype(int), jasc(R+f'graphics/pokemon/{n}/normal{s}.pal')
im = Image.open('sprite_r16/sprite.png'); ons = (np.asarray(im).astype(int), np.array(im.getpalette()[:48]).reshape(16, 3).astype('uint8'))
def rgb(a, p):
    t = np.zeros((64, 64, 3), 'uint8'); t[:] = (152, 208, 160); m = a > 0; t[m] = p[a[m]]; return Image.fromarray(t).resize((512, 512), Image.NEAREST)
V = Image.new('RGB', (3*522+10, 22+512+200), 'white'); d = ImageDraw.Draw(V)
sets = [('ons r16', ons, {'bruin': 'fdcb', 'creme': 'CMSD'}), ('Kangaskhan Gen 3 (GBA)', mon('kangaskhan', 1), {'bruin': [12, 13, 14, 15], 'buik': [3, 4]}),
        ('Kangaskhan expansion-standaard (Gen 4/5-stijl, GEEN maatstaf)', mon('kangaskhan', 0), {})]
ch = '.KbcdfSCeLMogWwD'
for i, (t, (a, p), lad) in enumerate(sets):
    V.paste(rgb(a, p), (10+i*522, 22)); d.text((10+i*522, 6), t, fill='black')
    y = 22+512+10
    for naam, idx in lad.items():
        idx = [ch.index(c) for c in idx] if isinstance(idx, str) else idx
        d.text((10+i*522, y+12), naam, fill='black')
        for j, k in enumerate(idx):
            c = tuple(int(v) for v in p[k]); h, s, v = colorsys.rgb_to_hsv(*(x/255 for x in c)); L = int(.299*c[0]+.587*c[1]+.114*c[2])
            d.rectangle([60+i*522+j*110, y, 60+i*522+j*110+40, y+40], fill=c)
            d.text((60+i*522+j*110, y+44), f'h{int(h*360)} s{int(s*100)} L{L}', fill='black')
        y += 80
V.save('stijl_gen123/vergelijk.png')
