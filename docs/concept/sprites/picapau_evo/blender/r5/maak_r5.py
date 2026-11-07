"""Ronde 5: render van het r5-model in de stand van r4 V2 (lijf 35, kop +5, oog_az 65), passend in 61 px, plus vel en
close-up. Uitvoer: R5_8x.png, R5_1x.png, vel_r5.png, closeup_r5.png. Draaien: python3.11 maak_r5.py [render] [vel]"""
import os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(HIER, '../r3'))
import maak_r3
STAND = dict(lijf=35, kop_draai=5, oog_az=65, voorover=0, kantel=8)
G = os.path.join(HIER, '../../../../../../graphics/pokemon')

def render():
    m5 = maak_r3.laad(os.path.join(HIER, 'picapau_evo_r5.py'), 'r5')
    proef = os.path.join(HIER, '_proef.png'); s0 = 0.6
    m5.render(proef, schaal=s0, **STAND); x0, y0, x1, y1 = maak_r3.bbox1x(proef); os.remove(proef)
    cx, cy = ((x0 + x1) / 2 - 32) / s0, ((y0 + y1) / 2 - 32) / s0
    s = 61.0 / (max(x1 - x0, y1 - y0) / s0)
    p8 = os.path.join(HIER, 'R5_8x.png'); m5.render(p8, schaal=s, schuif=(-cx * s, cy * s), **STAND)
    sm = Image.open(p8).convert('RGBA').resize((64, 64), Image.BOX)
    sm.putalpha(sm.split()[3].point(lambda a: 255 if a >= 128 else 0)); sm.save(os.path.join(HIER, 'R5_1x.png'))
    print('R5 schaal', round(s, 3), 'omtrek', sm.getbbox(), sum(1 for a in sm.split()[3].get_flattened_data() if a), 'px')

def front(naam):
    im = Image.open(os.path.join(G, naam, 'anim_front.png')).convert('RGBA').crop((0, 0, 64, 64)); px = im.load(); bg = px[0, 0]
    for y in range(64):
        for x in range(64):
            if px[x, y] == bg: px[x, y] = (0, 0, 0, 0)
    return im

def vel():
    items = [('r5 (1x-verkleining)', Image.open(os.path.join(HIER, 'R5_1x.png')).convert('RGBA')),
             ('r4 V2', Image.open(os.path.join(HIER, '../r4/V2_1x.png')).convert('RGBA')),
             ('Staraptor', front('staraptor')), ('Braviary', front('braviary')), ('Talonflame', front('talonflame')),
             ('Raichu Gen 1', Image.open(os.path.join(HIER, '../../referenties/jordi_inspiratie_raichu_gen1.png')).convert('RGBA').resize((64, 64), Image.NEAREST))]
    R = 512; W = 256 + 8
    v = Image.new('RGBA', (R + 16 + W * len(items), 16 + R + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
    d.text((8, 2), 'r5: render 8x', fill=(0, 0, 0, 255)); v.alpha_composite(Image.open(os.path.join(HIER, 'R5_8x.png')).convert('RGBA'), (8, 16))
    for i, (t, im) in enumerate(items):
        x = R + 16 + i * W; d.text((x, 2), t, fill=(0, 0, 0, 255))
        v.alpha_composite(im, (x, 16)); v.alpha_composite(im.resize((256, 256), Image.NEAREST), (x, 88))
    v.convert('RGB').save(os.path.join(HIER, 'vel_r5.png')); print('vel_r5.png', v.size)

def closeup():
    """kop, snavel en oren op 8x: render, 1x-verkleining op 8x, en Raichu Gen 1 / Gen 3 oren ter vergelijking"""
    r8 = Image.open(os.path.join(HIER, 'R5_8x.png')).convert('RGBA'); r1 = Image.open(os.path.join(HIER, 'R5_1x.png')).convert('RGBA')
    a = r1.split()[3].getbbox(); bb = r1.getbbox()
    # kopgebied: bovenste 24 px, linker 36 px van de omtrek
    x0, y0 = bb[0], bb[1]; box = (x0, y0, x0 + 36, y0 + 26)
    k8 = r8.crop(tuple(c * 8 for c in box)); k1 = r1.crop(box).resize((36 * 8, 26 * 8), Image.NEAREST)
    g1 = Image.open(os.path.join(HIER, '../../referenties/jordi_inspiratie_raichu_gen1.png')).convert('RGBA').crop((40 * 16, 0, 64 * 16, 28 * 16)).resize((24 * 8, 28 * 8), Image.NEAREST)
    g3 = Image.open(os.path.join(HIER, '../../referenties/raichu_gen3_8x.png')).convert('RGBA').crop((200, 0, 512, 260))
    items = [('r5 render', k8), ('r5 1x (op 8x)', k1), ('Raichu Gen 1 oor', g1), ('Raichu Gen 3 oor', g3)]
    W = sum(im.size[0] + 12 for _, im in items) + 8; H = max(im.size[1] for _, im in items) + 24
    v = Image.new('RGBA', (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(v); x = 8
    for t, im in items:
        d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16)); x += im.size[0] + 12
    v.convert('RGB').save(os.path.join(HIER, 'closeup_r5.png')); print('closeup_r5.png', v.size)

if __name__ == '__main__':
    wat = sys.argv[1:] or ['render', 'vel', 'closeup']
    if 'render' in wat: render()
    if 'vel' in wat: vel()
    if 'closeup' in wat: closeup()
