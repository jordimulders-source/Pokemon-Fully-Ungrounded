"""Pose-proef r7pose: 3 varianten vanuit P3 (r6pose) met meer lijf- en kopdraai naar de kijker (kop meer dan lijf), beide
ogen, de verre vleugel opgetild en de snavel schuin naar links-onder (Ho-Oh). Snel (STAP=0.5), elk passend in 61 px.
vel_pose.png: varianten + P3 + Ho-Oh, Pidgeot, Fletchinder, Raichu Gen 1 (1x, 4x, render). Draaien: STAP=0.5 python3.11 maak_pose.py"""
import os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(HIER, '../r3'))
import maak_r3
P3 = dict(lijf=55, kop_draai=5, voorover=-30, kop_kantel=-24, oog_az=42, kantel=8)          # r6pose P3 (Jordi: "ik kies p3")
VAR = {'Q1': (dict(lijf=60, kop_draai=12, voorover=-30, kop_kantel=-24, oog_az=50, kantel=8), dict(snavel=-8, vleugel=(4.0, 0.0, 2.0))),
       'Q2': (dict(lijf=66, kop_draai=14, voorover=-30, kop_kantel=-24, oog_az=52, kantel=8), dict(snavel=-14, vleugel=(2.0, 0.0, 4.0))),
       'Q3': (dict(lijf=72, kop_draai=14, voorover=-28, kop_kantel=-22, oog_az=55, kantel=8), dict(snavel=-20, vleugel=(0.0, 0.0, 6.0)))}
G = os.path.join(HIER, '../../../../../../graphics/pokemon')

def maak(naam):
    m = maak_r3.laad(os.path.join(HIER, 'picapau_evo_r7pose.py'), 'r7pose')
    kw, mod = VAR[naam]
    m.TWEE_OGEN = True; m.SNAVEL_HOEK = mod['snavel']; m.VERRE_VLEUGEL = mod['vleugel']
    proef = os.path.join(HIER, '_proef.png'); s0 = 0.55
    m.render(proef, schaal=s0, res=256, **kw); x0, y0, x1, y1 = maak_r3.bbox1x(proef); os.remove(proef)
    cx, cy = ((x0 + x1) / 2 - 32) / s0, ((y0 + y1) / 2 - 32) / s0; s = 61.0 / (max(x1 - x0, y1 - y0) / s0)
    p8 = os.path.join(HIER, f'{naam}_8x.png'); m.render(p8, schaal=s, schuif=(-cx * s, cy * s), **kw)
    sm = Image.open(p8).convert('RGBA').resize((64, 64), Image.BOX)
    sm.putalpha(sm.split()[3].point(lambda a: 255 if a >= 128 else 0)); sm.save(os.path.join(HIER, f'{naam}_1x.png'))
    print(naam, kw, mod, 'schaal', round(s, 3), 'omtrek', sm.getbbox())

def front(naam):
    im = Image.open(os.path.join(G, naam, 'anim_front.png')).convert('RGBA').crop((0, 0, 64, 64)); px = im.load(); bg = px[0, 0]
    for y in range(64):
        for x in range(64):
            if px[x, y] == bg: px[x, y] = (0, 0, 0, 0)
    return im

def vel():
    items = []
    for n, (kw, mod) in VAR.items():
        items.append((f'{n}: lijf {kw["lijf"]} kop +{kw["kop_draai"]} snavel {mod["snavel"]}', Image.open(os.path.join(HIER, f'{n}_1x.png')).convert('RGBA'),
                      Image.open(os.path.join(HIER, f'{n}_8x.png')).convert('RGBA').resize((256, 256), Image.LANCZOS)))
    items.append(('P3 (r6pose)', Image.open(os.path.join(HIER, '../r6pose/P3_1x.png')).convert('RGBA'),
                  Image.open(os.path.join(HIER, '../r6pose/P3_8x.png')).convert('RGBA').resize((256, 256), Image.LANCZOS)))
    for n, t in (('ho_oh', 'Ho-Oh'), ('pidgeot', 'Pidgeot'), ('fletchinder', 'Fletchinder')): items.append((t, front(n), None))
    items.append(('Raichu Gen 1', Image.open(os.path.join(HIER, '../../referenties/jordi_inspiratie_raichu_gen1.png')).convert('RGBA').resize((64, 64), Image.NEAREST), None))
    W = 264; v = Image.new('RGBA', (W * len(items) + 8, 16 + 72 + 264 + 264), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
    for i, (t, im, r) in enumerate(items):
        x = 8 + i * W; d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16))
        v.alpha_composite(im.resize((256, 256), Image.NEAREST), (x, 88))
        if r: v.alpha_composite(r, (x, 88 + 264))
    v.convert('RGB').save(os.path.join(HIER, 'vel_pose.png')); print('vel_pose.png', v.size)

if __name__ == '__main__':
    wat = sys.argv[1:] or list(VAR) + ['vel']
    for w in wat:
        if w in VAR: maak(w)
    if 'vel' in wat: vel()
