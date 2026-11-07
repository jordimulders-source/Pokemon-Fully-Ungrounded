"""Pose-proef r6pose: 3 varianten (lijfdraai naar de kijker, achterover, kopdraai, oog bij de snavelbasis), snel (STAP=0.5),
elk passend in 61 px; vel_pose.png met Taillow, Staraptor, Swellow en Raichu Gen 1 op dezelfde schaal (1x en 4x).
Draaien: STAP=0.5 python3.11 maak_pose.py [P1 P2 P3] [vel]"""
import os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(HIER, '../r3'))
import maak_r3
# voorover < 0 = achterover (romp kantelt om de heup naar achteren); kop_kantel houdt de kop rechtop
VAR = {'P1': dict(lijf=45, kop_draai=10, voorover=-15, kop_kantel=-12, oog_az=48, kantel=8),
       'P2': dict(lijf=50, kop_draai=8, voorover=-22, kop_kantel=-18, oog_az=45, kantel=8),
       'P3': dict(lijf=55, kop_draai=5, voorover=-30, kop_kantel=-24, oog_az=42, kantel=8)}
# eerste proef lijf 60 + kop 10 (70 graden totaal) gaf een kop recht van voren met een verkorte snavel: te ver
G = os.path.join(HIER, '../../../../../../graphics/pokemon')

def maak(naam):
    m = maak_r3.laad(os.path.join(HIER, 'picapau_evo_r6pose.py'), 'r6pose')
    kw = VAR[naam]; proef = os.path.join(HIER, '_proef.png'); s0 = 0.55
    m.render(proef, schaal=s0, res=256, **kw); x0, y0, x1, y1 = maak_r3.bbox1x(proef); os.remove(proef)
    cx, cy = ((x0 + x1) / 2 - 32) / s0, ((y0 + y1) / 2 - 32) / s0; s = 61.0 / (max(x1 - x0, y1 - y0) / s0)
    p8 = os.path.join(HIER, f'{naam}_8x.png'); m.render(p8, schaal=s, schuif=(-cx * s, cy * s), **kw)
    sm = Image.open(p8).convert('RGBA').resize((64, 64), Image.BOX)
    sm.putalpha(sm.split()[3].point(lambda a: 255 if a >= 128 else 0)); sm.save(os.path.join(HIER, f'{naam}_1x.png'))
    print(naam, kw, 'schaal', round(s, 3), 'omtrek', sm.getbbox())

def front(naam):
    im = Image.open(os.path.join(G, naam, 'anim_front.png')).convert('RGBA').crop((0, 0, 64, 64)); px = im.load(); bg = px[0, 0]
    for y in range(64):
        for x in range(64):
            if px[x, y] == bg: px[x, y] = (0, 0, 0, 0)
    return im

def vel():
    items = [(f'{n}: lijf {v["lijf"]}, kop +{v["kop_draai"]}, achterover {-v["voorover"]}', Image.open(os.path.join(HIER, f'{n}_1x.png')).convert('RGBA'),
              Image.open(os.path.join(HIER, f'{n}_8x.png')).convert('RGBA').resize((256, 256), Image.LANCZOS)) for n, v in VAR.items()]
    for n in ('taillow', 'staraptor', 'swellow'): items.append((n.capitalize(), front(n), None))
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
