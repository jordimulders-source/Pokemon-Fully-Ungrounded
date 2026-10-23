"""Metingen ronde 7: keuring-ronde5-metrics + eigen omlijningsmeting (puur zwart aan de buitenrand)."""
import sys
sys.path.insert(0, 'docs/concept/sprites/keuring_ronde5/scripts')
from metrics import metrics
from PIL import Image

S = 'docs/concept/sprites/'
G = 'graphics/pokemon/'


def blackedge(path):
    im = Image.open(path).convert('RGBA').crop((0, 0, 64, 64))
    W, H = im.size
    a = lambda x, y: 0 <= x < W and 0 <= y < H and im.getpixel((x, y))[3] > 0
    edge = black = light = 0
    for y in range(H):
        for x in range(W):
            if not a(x, y):
                continue
            if any(not a(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                r, g, b, _ = im.getpixel((x, y))
                l = 0.299 * r + 0.587 * g + 0.114 * b
                edge += 1
                black += l < 40
                light += l > 150
    return round(black / edge, 2), round(light / edge, 2)


rows = [('alpaca r6', S + 'alpaca/ronde6/anim_front.png'), ('alpaca r7', S + 'alpaca/ronde7/anim_front.png'),
        ('olinguito r6', S + 'olinguito/ronde6/anim_front.png'), ('olinguito r7', S + 'olinguito/ronde7/anim_front.png')]
rows += [(n, G + n + '/anim_front_gba.png') for n in
         ['mareep', 'growlithe', 'makuhita', 'hitmonchan', 'teddiursa', 'sentret', 'zigzagoon', 'aipom', 'pikachu', 'eevee']]
print('%-14s %5s %8s %6s %5s %10s %10s' % ('naam', 'opp', 'donker', 'detail', 'sat', 'puurzwart', 'lichtrand'))
for n, p in rows:
    m = metrics(p)
    b, l = blackedge(p)
    print('%-14s %5d %8.2f %6.2f %5.2f %10.2f %10.2f' % (n, m['area'], m['darkedge'], m['detail'], m['sat'], b, l))
