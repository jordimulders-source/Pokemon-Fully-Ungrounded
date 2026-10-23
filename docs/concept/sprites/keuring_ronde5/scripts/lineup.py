"""Blinde rij: kandidaten tussen echte Gen 3-sprites op 2x, zonder namen (oplossing in de bestandsnaam-legenda)."""
import sys, random
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from sheet import *
O = sys.argv[1]
c = [S + 'alpaca/ronde5/anim_front.png', S + 'olinguito/ronde5/anim_front.png', S + 'nachtaap/ronde5/anim_front.png',
     S + 'cuyby/ronde1/anim_front.png']
names = ['treecko', 'torchic', 'mudkip', 'mareep', 'zigzagoon', 'aipom', 'skitty', 'teddiursa', 'poochyena', 'sentret', 'whismur', 'electrike']
items = [(p, 'K') for p in c] + [(G + n + '/anim_front_gba.png', n) for n in names]
random.seed(5)
random.shuffle(items)
sc = 2
img = Image.new('RGB', (8 * 64 * sc + 20, 2 * 64 * sc + 30), (152, 208, 136))
d = ImageDraw.Draw(img)
legend = []
for i, (p, n) in enumerate(items):
    sp = load(p, 0).resize((64 * sc, 64 * sc), Image.NEAREST)
    x = 10 + (i % 8) * 64 * sc
    y = 10 + (i // 8) * (64 * sc + 10)
    img.paste(sp, (x, y), sp)
    d.text((x + 2, y + 2), str(i + 1), fill=(0, 0, 0))
    legend.append('%d=%s' % (i + 1, 'KANDIDAAT ' + p.split('/sprites/')[1].split('/')[0] if n == 'K' else n))
img.save(O)
print(O)
print(', '.join(legend))
