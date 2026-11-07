"""Ronde 3: C3 = C2 met nieuwe kuif (Raichu-oren) en staart (koord + grote bliksem). Zelfde kader als C2 (schaal en
schuif uit de proefrender van het r2-model), zodat alleen kuif en staart verschillen.
Uitvoer: C3_8x.png, C3_1x.png, standen_r3.png, closeup_r3.png. Draaien: python3.11 maak_r3.py"""
import os, sys, importlib.util
HIER = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageDraw
C = dict(lijf=40, kop_draai=20, voorover=10, kantel=8)
REF = os.path.join(HIER, '../../referenties')

def laad(pad, naam):
    spec = importlib.util.spec_from_file_location(naam, pad); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def bbox1x(pad):
    return Image.open(pad).resize((64, 64), Image.BOX).split()[3].point(lambda a: 255 if a >= 128 else 0).getbbox()

def kader_c2():
    m2 = laad(os.path.join(HIER, '../r2/picapau_evo_r2.py'), 'r2')
    proef = os.path.join(HIER, '_proef.png'); s0 = 0.7
    m2.render(proef, schaal=s0, **C); x0, y0, x1, y1 = bbox1x(proef); os.remove(proef)
    w, h = (x1 - x0) / s0, (y1 - y0) / s0; s = min(61.0 / w, 61.0 / h)
    cx, cy = ((x0 + x1) / 2 - 32) / s0, ((y0 + y1) / 2 - 32) / s0
    return s, (-cx * s, cy * s)

def c3():
    s, sch = kader_c2()
    m3 = laad(os.path.join(HIER, 'picapau_evo_r3.py'), 'r3')
    p8 = os.path.join(HIER, 'C3_8x.png'); m3.render(p8, schaal=s, schuif=sch, **C)
    sm = Image.open(p8).convert('RGBA').resize((64, 64), Image.BOX)
    sm.putalpha(sm.split()[3].point(lambda a: 255 if a >= 128 else 0)); sm.save(os.path.join(HIER, 'C3_1x.png'))
    print(f'C3: schaal {s:.3f} (= C2), omtrek {sm.getbbox()}, {sum(1 for a in sm.split()[3].get_flattened_data() if a)} px')

def gen1(): return Image.open(os.path.join(REF, 'jordi_inspiratie_raichu_gen1.png')).convert('RGBA')
def gen3(): return Image.open(os.path.join(REF, 'raichu_gen3_8x.png')).convert('RGBA')

def vel():
    items = [('Raichu Gen 1 (hoofdbron)', gen1().resize((64, 64), Image.NEAREST)),
             ('Raichu Gen 3', gen3().resize((64, 64), Image.NEAREST)),
             ('ronde 2: C2', Image.open(os.path.join(HIER, '../r2/C2_1x.png')).convert('RGBA')),
             ('ronde 3: C3', Image.open(os.path.join(HIER, 'C3_1x.png')).convert('RGBA')),
             ('Picapau (af)', Image.open(os.path.join(HIER, '../../../picapau/af/picapau.png')).convert('RGBA'))]
    W = 64 * 4 + 8; v = Image.new('RGBA', (W * len(items), 14 + 72 + 256 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
    for i, (t, im) in enumerate(items):
        x = i * W + 4; d.text((x, 2), t, fill=(0, 0, 0, 255))
        v.alpha_composite(im, (x, 16)); v.alpha_composite(im.resize((256, 256), Image.NEAREST), (x, 88))
    v.convert('RGB').save(os.path.join(HIER, 'standen_r3.png'))

def closeup():
    """8x: kuif (rij 1) en staart (rij 2) van Gen 1, Gen 3 en C3 (render 8x en 1x op 8x)"""
    g1 = gen1().resize((512, 512), Image.NEAREST); g3 = gen3()
    c8 = Image.open(os.path.join(HIER, 'C3_8x.png')).convert('RGBA')
    c1 = Image.open(os.path.join(HIER, 'C3_1x.png')).convert('RGBA').resize((512, 512), Image.NEAREST)
    k = lambda x0, y0, x1, y1: (x0 * 8, y0 * 8, x1 * 8, y1 * 8)
    rijen = [('kuif / oren', [('Gen 1', g1.crop(k(24, 0, 64, 28))), ('Gen 3', g3.crop(k(24, 2, 64, 30))),
                              ("C3 render", c8.crop(k(4, 0, 44, 28))), ("C3 1x", c1.crop(k(4, 0, 44, 28)))]),
             ('staart', [('Gen 1', g1.crop(k(0, 26, 64, 64))), ('Gen 3', g3.crop(k(0, 8, 64, 46))),
                         ('C3 render', c8.crop(k(0, 26, 64, 64))), ('C3 1x', c1.crop(k(0, 26, 64, 64)))])]
    W = 512 + 8
    v = Image.new('RGBA', (W * 4, 2 * (16 + 304 + 8)), (255, 255, 255, 255)); d = ImageDraw.Draw(v); y = 0
    for titel, cel in rijen:
        for i, (t, im) in enumerate(cel):
            d.text((i * W + 4, y + 2), f'{titel}: {t}', fill=(0, 0, 0, 255)); v.alpha_composite(im, (i * W + 4, y + 16))
        y += 16 + 304 + 8
    v.convert('RGB').save(os.path.join(HIER, 'closeup_r3.png'))

if __name__ == '__main__':
    wat = sys.argv[1:] or ['C3', 'vel', 'closeup']
    if 'C3' in wat: c3()
    if 'vel' in wat: vel()
    if 'closeup' in wat: closeup()
