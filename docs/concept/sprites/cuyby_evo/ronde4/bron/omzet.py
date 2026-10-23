"""Eenmalig: zet ronde3/bron/delen.txt (per deel, al geknipt) om naar ronde4/bron/delen_rle.txt in EIND-coordinaten.
Zo zijn de coordinaten in de bron van ronde 4 gelijk aan die in het raster en in de keuring (geen knip meer).
Niet opnieuw draaien: dat overschrijft het handwerk van ronde 4 in delen_rle.txt.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '../../ronde3/bron/delen.txt')
OUD = os.path.join(HERE, '../../ronde3/bron/delen_rle.txt')

# commentaar per deel uit ronde 3 meenemen
comm, cur = {}, None
for line in open(OUD, encoding='utf-8'):
    if line.startswith('## '):
        cur = line[3:].split()[0]
        comm[cur] = []
    elif cur and line.startswith('#'):
        comm[cur].append(line.rstrip())


def tokens(seg):
    out, i = [], 0
    while i < len(seg):
        j = i
        while j < len(seg) and seg[j] == seg[i]:
            j += 1
        n = j - i
        out.append('%d%s' % (n, seg[i]) if n >= 3 else seg[i] * n)
        i = j
    # losse letters samenvoegen tot letterlijke tokens
    merged = []
    for t in out:
        if merged and not t[0].isdigit() and not merged[-1][0].isdigit():
            merged[-1] += t
        else:
            merged.append(t)
    return ' '.join(merged)


lines = ['# Cuyby-evolutie ronde 4 - bron in EIND-coordinaten (= raster, geen knip). Omgezet uit ronde 3 met omzet.py;',
         '# daarna met de hand bijgewerkt (zie NOTITIES.md). Formaat: zie rle4.py.',
         '# Tekens: K zwart, h/s/d/q stro (hooglicht/basis/schaduw/roest), r stro-omlijning, a/b/c wit,',
         '# e wit-omlijning, g/G zwart vlak, p/P roze, n weerkaatsing in het oog.', '']
for line in open(SRC, encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('## '):
        p = line[3:].split()
        naam, y = p[0], int(p[2])
        extra = ' '.join(p[3:])
        lines += ['', ('## %s %s' % (naam, extra)).rstrip()] + comm.get(naam, [])
        continue
    if line.startswith('#'):
        continue
    segs = [(m.start(), m.group()) for m in re.finditer(r'[^.]+', line)]
    if segs:
        lines.append('%d: ' % y + '   '.join('%d: %s' % (x, tokens(s)) for x, s in segs))
    y += 1
open(os.path.join(HERE, 'delen_rle.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('ok')
