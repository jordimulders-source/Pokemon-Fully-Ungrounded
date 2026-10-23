"""Vergelijkingsvel ronde 7 (alpaca en olinguito). Vanuit de repo-root:
    python3 docs/concept/sprites/alpaca/ronde7/bron/compare.py alpaca
    python3 docs/concept/sprites/alpaca/ronde7/bron/compare.py olinguito
Rij 1: modeltekening, ronde 6, ronde 7 (frame 1 en 2) en echte Gen 3-sprites op 3x.
Rij 2: dezelfde sprites op 1x. Rij 3: de ogen op 6x naast echte Gen 3-ogen (pixelniveau)."""
import sys
from PIL import Image, ImageDraw

S = 'docs/concept/sprites/'
G = 'graphics/pokemon/'
CFG = {
    'alpaca': dict(model=('docs/concept/ontwerp/alpaca/concept_A.png', (30, 40, 245, 280)),
                   refs=['mareep', 'growlithe', 'makuhita', 'hitmonchan', 'eevee'], eye=(13, 24)),
    'olinguito': dict(model=('docs/concept/ontwerp/olinguito/concept_B.png', (40, 30, 245, 280)),
                      refs=['teddiursa', 'sentret', 'zigzagoon', 'aipom', 'pikachu'], eye=(14, 21)),
}
EYES = [('eevee', (12, 21)), ('pikachu', (15, 18)), ('teddiursa', (18, 23)), ('zigzagoon', (10, 19)),
        ('growlithe', (10, 22)), ('mareep', (12, 20))]
BG = (152, 208, 136)


def frame(path, n=0):
    im = Image.open(path).convert('RGBA').crop((0, 64 * n, 64, 64 * n + 64))
    out = Image.new('RGB', (64, 64), BG)
    out.paste(im, (0, 0), im)
    return out


name = sys.argv[1]
c = CFG[name]
items = [('ronde 6', frame(S + name + '/ronde6/anim_front.png')),
         ('ronde 7 f1', frame(S + name + '/ronde7/anim_front.png')),
         ('ronde 7 f2', frame(S + name + '/ronde7/anim_front.png', 1))]
items += [(r + ' (G3)', frame(G + r + '/anim_front_gba.png')) for r in c['refs']]
model = Image.open(c['model'][0]).convert('RGB').crop(c['model'][1])
model.thumbnail((192, 192))
EW, EH, EZ = 18, 11, 6
W = 200 + len(items) * 200
sheet = Image.new('RGB', (W, 20 + 210 + 90 + 30 + EH * EZ + 30), (236, 236, 240))
d = ImageDraw.Draw(sheet)
d.text((8, 4), '%s ronde 7: modeltekening, ronde 6, ronde 7 en echte Gen 3-sprites (3x, 1x, ogen 6x)' % name, fill=(20, 20, 20))
sheet.paste(model, (4, 24))
d.text((4, 220), 'modeltekening', fill=(60, 60, 60))
for i, (t, im) in enumerate(items):
    x = 200 + i * 200
    sheet.paste(im.resize((192, 192), Image.NEAREST), (x, 24))
    d.text((x, 220), t, fill=(20, 20, 20))
    sheet.paste(im, (x + 64, 240))
y0 = 330
d.text((8, y0), 'ogen 6x:', fill=(20, 20, 20))
eyes = [(name + ' r7', frame(S + name + '/ronde7/anim_front.png'), c['eye'])]
eyes += [(n, frame(G + n + '/anim_front_gba.png'), p) for n, p in EYES]
for i, (t, im, (ex, ey)) in enumerate(eyes):
    x = 80 + i * (EW * EZ + 16)
    sheet.paste(im.crop((ex, ey, ex + EW, ey + EH)).resize((EW * EZ, EH * EZ), Image.NEAREST), (x, y0 + 14))
    d.text((x, y0 + 16 + EH * EZ), t, fill=(20, 20, 20))
sheet.save(S + name + '/ronde7/compare.png')
