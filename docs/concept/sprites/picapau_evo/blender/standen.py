"""Driekwart-standen A/B/C van het evo-model (+ tong-variant) en het vergelijkingsvel standen.png.
Per stand: eerst een kleine proefrender om het model passend in het 64x64-frame te zetten (1 px marge),
dan de render op 8x (512 px) en direct verkleind naar 1x (box-filter, alpha >= 128).
Draaien: python3.11 standen.py [A B C T]   (T = tong-variant van de beste stand)"""
import os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import picapau_evo as m
from PIL import Image

# lijf = lijfdraai naar de kijker, kop_draai komt daar bovenop (kop totaal = lijf + kop_draai), voorover = romp kantelt naar voren
STANDEN = {
    'A': dict(lijf=30, kop_draai=20, voorover=15, kantel=8),    # kop totaal 50
    'B': dict(lijf=20, kop_draai=25, voorover=22, kantel=12),   # kop totaal 45, dieper voorover (uitval)
    'C': dict(lijf=40, kop_draai=20, voorover=10, kantel=8),    # kop totaal 60, meer naar de kijker
}
BESTE = 'A'

def verklein(pad8, pad1):
    im = Image.open(pad8).convert('RGBA'); sm = im.resize((64, 64), Image.BOX)
    sm.putalpha(sm.split()[3].point(lambda a: 255 if a >= 128 else 0)); sm.save(pad1)
    return sm

def passend(stand, **extra):
    """proefrender 512 px -> schaal en schuif zodat de omtrek binnen ±60 px valt, gecentreerd"""
    proef = os.path.join(HIER, 'standen', '_proef.png')
    m.render(proef, **stand, **extra)
    x0, y0, x1, y1 = Image.open(proef).resize((64, 64), Image.BOX).split()[3].point(lambda a: 255 if a >= 128 else 0).getbbox()
    os.remove(proef)
    w, h = x1 - x0, y1 - y0
    s = min(60.0 / w, 60.0 / h)
    cx, cy = (x0 + x1) / 2 - 32, (y0 + y1) / 2 - 32          # midden van de omtrek t.o.v. het frame (px)
    return s, (-cx * s, cy * s)                              # Blender X = x - 32, Z = 32 - y

def maak(naam, stand, **extra):
    os.makedirs(os.path.join(HIER, 'standen'), exist_ok=True)
    s, sch = passend(stand, **extra)
    pad8 = os.path.join(HIER, 'standen', f'{naam}_8x.png')
    m.render(pad8, schaal=s, schuif=sch, **stand, **extra)
    sm = verklein(pad8, os.path.join(HIER, 'standen', f'{naam}_1x.png'))
    n = sum(1 for a in sm.split()[3].get_flattened_data() if a)
    print(f'{naam}: schaal {s:.3f}, schuif {sch[0]:.1f},{sch[1]:.1f}, omtrek {sm.getbbox()}, {n} px')

def vel():
    """1x en 4x naast elkaar: Picapau (af), Raichu Gen 1, A, B, C (en tong-variant als die er is)"""
    S = os.path.join(HIER, 'standen')
    items = [('Picapau (af)', Image.open(os.path.join(HIER, '../../picapau/af/picapau.png')).convert('RGBA')),
             ('Raichu Gen 1', Image.open(os.path.join(HIER, '../referenties/jordi_inspiratie_raichu_gen1.png')).convert('RGBA').resize((64, 64), Image.NEAREST))]
    for n in ['A', 'B', 'C', f'{BESTE}_tong']:
        p = os.path.join(S, f'{n}_1x.png')
        if os.path.exists(p): items.append((n, Image.open(p).convert('RGBA')))
    from PIL import ImageDraw
    W = 64 * 4 + 8
    v = Image.new('RGBA', (W * len(items), 14 + 72 + 64 * 4 + 8), (255, 255, 255, 255))
    d = ImageDraw.Draw(v)
    for i, (t, im) in enumerate(items):
        x = i * W + 4
        d.text((x, 2), t, fill=(0, 0, 0, 255))
        v.alpha_composite(im, (x, 16))
        v.alpha_composite(im.resize((256, 256), Image.NEAREST), (x, 16 + 72))
    v.convert('RGB').save(os.path.join(S, 'standen.png'))

if __name__ == '__main__':
    wat = sys.argv[1:] or ['A', 'B', 'C', 'T']
    for w in wat:
        if w == 'T': maak(f'{BESTE}_tong', STANDEN[BESTE], tong=True)
        else: maak(w, STANDEN[w])
    vel()
