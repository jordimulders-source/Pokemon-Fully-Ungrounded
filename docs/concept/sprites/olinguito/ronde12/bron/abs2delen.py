"""abs2delen.py <map>: zet bron/delen_abs.txt om naar bron/delen.txt (formaat van bouw9.py).
delen_abs.txt: per deel '## naam [dy2] [dx2]' (achterste deel eerst), daarna regels 'y x pixels'
in doekcoordinaten van frame 1 ('.' = niets). Zo schrijf je elke rij met de hand met een absolute
x-positie en hoef je niet in lange rijen te tellen. Daarna: python3 bron/bouw9.py <map>.
"""
import sys, os
B = os.path.join(sys.argv[1], 'bron')
delen = []
for r in open(os.path.join(B, 'delen_abs.txt'), encoding='utf-8'):
    r = r.rstrip('\n')
    if r.startswith('## '):
        p = r[3:].split()
        delen.append([p[0], p[1:], {}])
        continue
    r = r.split('#')[0].strip()
    if not r:
        continue
    y, x, px = r.split()
    y, x = int(y), int(x)
    for i, c in enumerate(px):
        if c != '.':
            delen[-1][2][(x + i, y)] = c
out = ['# gegenereerd uit delen_abs.txt door abs2delen.py; niet met de hand bewerken']
for naam, extra, px in delen:
    xs = [k[0] for k in px]
    ys = [k[1] for k in px]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    dy2 = extra[0] if extra else '0'
    dx2 = extra[1] if len(extra) > 1 else '0'
    out.append('## %s %d %d %s %s' % (naam, x0, y0, dy2, dx2))
    for y in range(y0, y1 + 1):
        out.append(''.join(px.get((x, y), '.') for x in range(x0, x1 + 1)))
open(os.path.join(B, 'delen.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
