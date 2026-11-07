"""Ronde 2: stand C2 (= stand C van ronde 1: lijf 40, kop +20, voorover 10, kantel 8) op 8x en 1x, rondom-vel
en standen_r2.png (Picapau af, Raichu Gen 1, ronde-1-C, C2; 1x en 4x). Draaien: python3.11 maak_r2.py [C2] [rond] [vel]"""
import os, sys
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
import picapau_evo_r2 as m
from PIL import Image, ImageDraw
C2 = dict(lijf=40, kop_draai=20, voorover=10, kantel=8)

def bbox1x(pad):
    return Image.open(pad).resize((64, 64), Image.BOX).split()[3].point(lambda a: 255 if a >= 128 else 0).getbbox()

def c2():
    proef = os.path.join(HIER, '_proef.png'); s0 = 0.7
    m.render(proef, schaal=s0, **C2); x0, y0, x1, y1 = bbox1x(proef); os.remove(proef)
    assert x0 > 0 and y0 > 0 and x1 < 64 and y1 < 64
    w, h = (x1 - x0) / s0, (y1 - y0) / s0; s = min(61.0 / w, 61.0 / h)
    cx, cy = ((x0 + x1) / 2 - 32) / s0, ((y0 + y1) / 2 - 32) / s0
    p8 = os.path.join(HIER, 'C2_8x.png'); m.render(p8, schaal=s, schuif=(-cx * s, cy * s), **C2)
    sm = Image.open(p8).convert('RGBA').resize((64, 64), Image.BOX)
    sm.putalpha(sm.split()[3].point(lambda a: 255 if a >= 128 else 0)); sm.save(os.path.join(HIER, 'C2_1x.png'))
    print(f'C2: schaal {s:.3f}, omtrek {sm.getbbox()}, {sum(1 for a in sm.split()[3].get_flattened_data() if a)} px')

def rond():
    U = os.path.join(HIER, 'rond'); os.makedirs(U, exist_ok=True); H = [0, 45, 90, 180, 270, 315]
    for h in H: m.render(os.path.join(U, f'rond_{h:03d}.png'), lijf=h, kop_draai=20, voorover=10, schaal=0.72)
    v = Image.new('RGBA', (384 * 3, 400 * 2), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
    for i, h in enumerate(H):
        x, y = (i % 3) * 384, (i // 3) * 400
        v.alpha_composite(Image.open(os.path.join(U, f'rond_{h:03d}.png')).resize((384, 384), Image.LANCZOS), (x, y + 14))
        d.text((x + 4, y + 2), f'lijf {h} (kop +20, voorover 10)', fill=(0, 0, 0, 255))
    v.convert('RGB').save(os.path.join(U, 'vel.png'))

def vel():
    items = [('Picapau (af)', Image.open(os.path.join(HIER, '../../../picapau/af/picapau.png')).convert('RGBA')),
             ('Raichu Gen 1', Image.open(os.path.join(HIER, '../../referenties/jordi_inspiratie_raichu_gen1.png')).convert('RGBA').resize((64, 64), Image.NEAREST)),
             ('ronde 1: C', Image.open(os.path.join(HIER, '../standen/C_1x.png')).convert('RGBA')),
             ('ronde 2: C2', Image.open(os.path.join(HIER, 'C2_1x.png')).convert('RGBA'))]
    W = 64 * 4 + 8; v = Image.new('RGBA', (W * len(items), 14 + 72 + 256 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
    for i, (t, im) in enumerate(items):
        x = i * W + 4; d.text((x, 2), t, fill=(0, 0, 0, 255))
        v.alpha_composite(im, (x, 16)); v.alpha_composite(im.resize((256, 256), Image.NEAREST), (x, 88))
    v.convert('RGB').save(os.path.join(HIER, 'standen_r2.png'))

if __name__ == '__main__':
    wat = sys.argv[1:] or ['C2', 'rond', 'vel']
    if 'C2' in wat: c2()
    if 'rond' in wat: rond()
    if 'vel' in wat: vel()
