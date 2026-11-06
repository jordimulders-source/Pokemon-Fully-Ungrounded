"""Ronde 4: draai-varianten van het r4-model (oren, staart, vleugel nieuw). Zelfde schaal als C2/C3 (kader_c2), per
variant opnieuw gecentreerd (de draai verschuift de omtrek). Uitvoer per variant: <naam>_8x.png, <naam>_1x.png;
plus varianten_r4.png (1x en 4x naast C3). Draaien: python3.11 maak_r4.py [V0 V1 V2 V3] [vel]"""
import os, sys, importlib.util
HIER = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(HIER, '../r3'))
import maak_r3
BASIS = dict(voorover=10, kantel=8)
VAR = {'V0': dict(lijf=40, kop_draai=20, oog_az=75),    # stand van r3 (60 graden totaal), alleen nieuwe onderdelen
       'V1': dict(lijf=40, kop_draai=10, oog_az=70),    # kop 10 graden minder naar de kijker
       'V2': dict(lijf=35, kop_draai=5, oog_az=65),     # kop 20 graden minder, lijf 5 mee
       'V3': dict(lijf=30, kop_draai=0, oog_az=60)}     # kop 30 graden minder, lijf 10 mee
m4 = maak_r3.laad(os.path.join(HIER, 'picapau_evo_r4.py'), 'r4')

def bbox1x(pad): return maak_r3.bbox1x(pad)

def maak(naam, s):
    kw = dict(BASIS, **VAR[naam])
    proef = os.path.join(HIER, '_proef.png'); s0 = 0.7
    m4.render(proef, schaal=s0, **kw); x0, y0, x1, y1 = bbox1x(proef); os.remove(proef)
    cx, cy = ((x0 + x1) / 2 - 32) / s0, ((y0 + y1) / 2 - 32) / s0
    p8 = os.path.join(HIER, f'{naam}_8x.png'); m4.render(p8, schaal=s, schuif=(-cx * s, cy * s), **kw)
    sm = Image.open(p8).convert('RGBA').resize((64, 64), Image.BOX)
    sm.putalpha(sm.split()[3].point(lambda a: 255 if a >= 128 else 0)); sm.save(os.path.join(HIER, f'{naam}_1x.png'))
    print(naam, kw, 'schuif', (round(-cx * s, 2), round(cy * s, 2)), 'omtrek', sm.getbbox(),
          sum(1 for a in sm.split()[3].get_flattened_data() if a), 'px')

def vel():
    items = [('C3 (r3)', Image.open(os.path.join(HIER, '../r3/C3_1x.png')).convert('RGBA'))]
    items += [(f'{n}: lijf {v["lijf"]} kop +{v["kop_draai"]}', Image.open(os.path.join(HIER, f'{n}_1x.png')).convert('RGBA'))
              for n, v in VAR.items() if os.path.exists(os.path.join(HIER, f'{n}_1x.png'))]
    W = 64 * 4 + 8; v = Image.new('RGBA', (W * len(items), 14 + 72 + 256 + 8 + 256 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
    for i, (t, im) in enumerate(items):
        x = i * W + 4; d.text((x, 2), t, fill=(0, 0, 0, 255))
        v.alpha_composite(im, (x, 16)); v.alpha_composite(im.resize((256, 256), Image.NEAREST), (x, 88))
        p8 = os.path.join(HIER, f'{t.split(":")[0]}_8x.png') if i else os.path.join(HIER, '../r3/C3_8x.png')
        v.alpha_composite(Image.open(p8).convert('RGBA').resize((256, 256), Image.LANCZOS), (x, 88 + 264))
    v.convert('RGB').save(os.path.join(HIER, 'varianten_r4.png'))

if __name__ == '__main__':
    wat = sys.argv[1:] or list(VAR) + ['vel']
    s, _ = maak_r3.kader_c2() if any(w in VAR for w in wat) else (0.89, None)
    for w in wat:
        if w in VAR: maak(w, s)
    if 'vel' in wat: vel()
