"""Kijkvel ronde 4 (alleen deze ronde). Rij 1: lama.png op 4x (licht en donker) naast het model. Rij 2: oog A/B/C als kop op 8x.
Rij 3: 1x en 3x naast Mareep, Flaaffy, Girafarig, Ponyta en de alpaca (fase 1).
Draaien: python3 docs/concept/sprites/lama/fase2/kleur/ronde4/bron/vel.py"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(OUT, '../../../../../../..'))
BG = (152, 208, 160)

def rgba(path, frame=0, pal=None):
    im = Image.open(path)
    if pal:
        p = [tuple(int(v) for v in x.split()) for x in open(pal).read().split('\n')[3:19]]
        im = im.crop((0, frame * 64, 64, frame * 64 + 64)); px = im.load()
        out = Image.new('RGBA', (64, 64))
        for y in range(64):
            for x in range(64):
                if px[x, y]: out.putpixel((x, y), p[px[x, y]] + (255,))
        return out
    im = im.convert('RGBA').crop((0, 0, 64, 64))
    im.putdata([(0, 0, 0, 0) if p[:3] == BG else p for p in im.getdata()])
    return im

def op(im, bg, z):
    c = Image.new('RGBA', im.size, bg); c.alpha_composite(im)
    return c.resize((im.size[0] * z, im.size[1] * z), Image.NEAREST)

def gp(n): return rgba(f'{REPO}/graphics/pokemon/{n}/anim_front.png', 0, f'{REPO}/graphics/pokemon/{n}/normal.pal')

lama = rgba(os.path.join(OUT, 'lama.png'))
ogen = {v: rgba(os.path.join(OUT, f'oog_{v}.png')) for v in 'ABC'}
model = Image.open(os.path.join(OUT, '../../silhouet_r5/onderlaag_256.png')).convert('RGBA')
alpaca = rgba(f'{REPO}/docs/concept/sprites/alpaca/ronde17/variant_kop/anim_front.png')
refs = [('lama r4', lama), ('Mareep', gp('mareep')), ('Flaaffy', gp('flaaffy')), ('Girafarig', gp('girafarig')),
        ('Ponyta', gp('ponyta')), ('alpaca f1', alpaca)]
W, H = 1180, 1010
c = Image.new('RGBA', (W, H), (250, 250, 250, 255)); d = ImageDraw.Draw(c)
d.text((10, 6), 'Lama fase 2, kleur ronde 4 (silhouet ronde 6, met de hand; oog B in lama.png)', fill=(0, 0, 0))
y = 24
c.paste(op(lama, (255, 255, 255, 255), 4), (10, y)); c.paste(op(lama, (40, 40, 48, 255), 4), (280, y)); c.paste(model, (550, y))
d.text((10, y + 258), '4x licht', fill=(0, 0, 0)); d.text((280, y + 258), '4x donker', fill=(0, 0, 0)); d.text((550, y + 258), 'model (poppetje, onderlaag_256)', fill=(0, 0, 0))
y = 300
for i, v in enumerate('ABC'):
    k = op(ogen[v], (255, 255, 255, 255), 1).crop((8, 0, 30, 22)).resize((22 * 8, 22 * 8), Image.NEAREST)
    c.paste(k, (10 + i * 200, y))
lab = ['A: Numel-basis, vlak zwaar lid, warm lichtje', 'B: lid zakt achteraan + zachte wal (gekozen)', 'C: recept A, grijsbruine iris, creme lichtje']
for i, t in enumerate(lab): d.text((10 + i * 200, y + 180), t[:34], fill=(0, 0, 0)); d.text((10 + i * 200, y + 192), t[34:], fill=(0, 0, 0))
y = 520
for i, (n, im) in enumerate(refs):
    c.paste(op(im, (255, 255, 255, 255), 3), (10 + i * 196, y)); d.text((10 + i * 196, y + 194), n + ' 3x', fill=(0, 0, 0))
y = 740
for i, (n, im) in enumerate(refs):
    c.paste(op(im, (255, 255, 255, 255), 1), (10 + i * 80, y)); c.paste(op(im, (40, 40, 48, 255), 1), (10 + i * 80, y + 70))
d.text((10, y + 140), '1x op licht en donker: lama r4, Mareep, Flaaffy, Girafarig, Ponyta, alpaca', fill=(0, 0, 0))
c = c.crop((0, 0, W, y + 160))
c.save(os.path.join(OUT, 'vel.png')); print('vel.png', c.size)
