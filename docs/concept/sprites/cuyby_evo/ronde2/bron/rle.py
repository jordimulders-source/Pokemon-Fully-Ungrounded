"""Cuyby-evolutie ronde 2: zet de met de hand geschreven run-length-rijen (delen_rle.txt) om naar delen.txt
voor bouw9.py (overgenomen uit olinguito ronde 9). Er wordt niets berekend: elk stuk is een rij pixels die met de
hand is gekozen, op een absolute x.

delen_rle.txt:
  '## naam [dy2] [dx2]'          begin van een deel (achterste deel eerst); dy2/dx2 = verschuiving in frame 2
  'y: x: tokens  x: tokens ...'   tokens = [aantal]teken, bv. '3h 12s K'; latere stukken overschrijven eerdere
  '#' = commentaar
Vanuit de repo-root:
  python3 docs/concept/sprites/cuyby_evo/ronde2/bron/rle.py
  python3 docs/concept/sprites/cuyby_evo/ronde2/bron/bouw9.py docs/concept/sprites/cuyby_evo/ronde2 [preview.png]
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
# Knippen (zoals in een tekenprogramma een kolom/rij wegknippen): na het tekenen bleek de figuur te groot
# (1487 px). Deze kolommen en rij gaan uit elk deel; wat rechts ligt schuift naar links, wat boven ligt naar onder.
KNIP_X = [33, 41]
KNIP_Y = [30]


def expand(tokens):
    out = ''
    for t in tokens.split():
        m = re.fullmatch(r'(\d*)(.)', t)
        assert m, t
        out += m.group(2) * int(m.group(1) or 1)
    return out


def main():
    parts = []
    for line in open(os.path.join(HERE, 'delen_rle.txt'), encoding='utf-8'):
        line = line.split('#', 1)[0].rstrip() if not line.startswith('##') else line.rstrip()
        if not line.strip():
            continue
        if line.startswith('## '):
            p = line[3:].split()
            parts.append([p[0], p[1:] , {}])
            continue
        y, rest = line.split(':', 1)
        y = int(y)
        row = parts[-1][2].setdefault(y, {})
        for x, toks in re.findall(r'(\d+):([^:]*?)(?=\s+\d+:|$)', rest.strip()):
            for i, ch in enumerate(expand(toks)):
                row[int(x) + i] = ch
    with open(os.path.join(HERE, 'delen.txt'), 'w', encoding='utf-8') as fh:
        fh.write('# gegenereerd door rle.py uit delen_rle.txt; niet met de hand bewerken\n')
        for naam, extra, rows in parts:
            new = {}
            for y, r in rows.items():
                if y in KNIP_Y:
                    continue
                ny = y + sum(1 for k in KNIP_Y if y < k)
                new[ny] = {x - sum(1 for k in KNIP_X if x > k): c for x, c in r.items() if x not in KNIP_X}
            y0, y1 = min(new), max(new)
            fh.write('## %s 0 %d %s\n' % (naam, y0, ' '.join(extra)))
            for y in range(y0, y1 + 1):
                r = new.get(y, {})
                fh.write(''.join(r.get(x, '.') for x in range(64)) + '\n')


if __name__ == '__main__':
    main()
