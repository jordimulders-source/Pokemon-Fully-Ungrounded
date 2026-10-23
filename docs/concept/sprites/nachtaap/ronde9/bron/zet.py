"""zet.py <delen.txt> <patch.txt>: zet met de hand geschreven pixelrijen in een deel.
patch.txt: regels 'deel y x0 pixels' in doekcoördinaten (frame 1); '.' in pixels = laat staan,
'_' = maak leeg. Het deel groeit vanzelf als de rij erbuiten valt.
"""
import sys
pad, patch = sys.argv[1], sys.argv[2]
kop, delen = [], []
for r in open(pad, encoding='utf-8'):
    r = r.rstrip('\n')
    if r.startswith('## '):
        p = r[3:].split()
        delen.append([p[0], int(p[1]), int(p[2]), p[3:], []])
    elif not delen:
        kop.append(r)
    elif r.startswith('#') or not r.strip():
        continue
    else:
        delen[-1][4].append(list(r))
idx = {d[0]: d for d in delen}
for r in open(patch, encoding='utf-8'):
    p = r.split()
    if not p or p[0].startswith('#'):
        continue
    naam, y, x0, px = p[0], int(p[1]), int(p[2]), p[3]
    d = idx[naam]
    w = max(len(row) for row in d[4]) if d[4] else 0
    # groei naar links/boven
    while x0 < d[1]:
        d[1] -= 1; d[4] = [['.'] + row for row in d[4]]; w += 1
    while y < d[2]:
        d[2] -= 1; d[4].insert(0, ['.'] * w)
    while y >= d[2] + len(d[4]):
        d[4].append(['.'] * w)
    row = d[4][y - d[2]]
    for i, c in enumerate(px):
        x = x0 + i - d[1]
        while x >= len(row):
            row.append('.')
        if c == '.':
            continue
        row[x] = '.' if c == '_' else c
    w = max(len(row) for row in d[4])
    d[4] = [row + ['.'] * (w - len(row)) for row in d[4]]
with open(pad, 'w', encoding='utf-8') as f:
    f.write('\n'.join(kop) + '\n')
    for naam, x, y, rest, rows in delen:
        f.write('## %s %d %d%s\n' % (naam, x, y, ''.join(' ' + s for s in rest)))
        for row in rows:
            f.write(''.join(row) + '\n')
