"""Cuyby-evolutie ronde 3: zet de met de hand geschreven rijen (delen_rle.txt) om naar delen.txt voor bouw9.py.
Er wordt niets berekend: elk stuk is een rij pixels die met de hand is gekozen, op een absolute x.

delen_rle.txt:
  '## naam [dy2] [dx2]'          begin van een deel (achterste deel eerst); dy2/dx2 = verschuiving in frame 2
  'y: x: tokens  x: tokens ...'   token = [aantal]teken ('3h') of letterlijke pixels ('rhhs'); '.' = laat staan
                                 latere stukken (en latere delen) overschrijven eerdere
  '#' = commentaar
Vanuit de repo-root:
  python3 docs/concept/sprites/cuyby_evo/ronde3/bron/rle3.py
  python3 docs/concept/sprites/cuyby_evo/ronde3/bron/bouw9.py docs/concept/sprites/cuyby_evo/ronde3 [preview.png]
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
# Knippen (zoals in een tekenprogramma een kolom/rij wegknippen, les ronde 2): de figuur werd te groot.
# Deze kolommen en rijen gaan uit elk deel; wat rechts ligt schuift naar links, wat boven ligt naar onder.
# De coordinaten in delen_rle.txt zijn dus van voor het knippen; de rasters tonen het eindresultaat.
KNIP_X = [37, 46]
KNIP_Y = [23, 44]


def expand(tokens):
    out = ''
    for t in tokens.split():
        m = re.fullmatch(r'(\d+)(.)', t)
        out += m.group(2) * int(m.group(1)) if m else t
    return out


def main():
    parts = []
    for line in open(os.path.join(HERE, 'delen_rle.txt'), encoding='utf-8'):
        line = line.rstrip() if line.startswith('##') else line.split('#', 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith('## '):
            p = line[3:].split()
            parts.append([p[0], p[1:], {}])
            continue
        y, rest = line.split(':', 1)
        row = parts[-1][2].setdefault(int(y), {})
        for x, toks in re.findall(r'(\d+):([^:]*?)(?=\s+\d+:|$)', rest.strip()):
            for i, ch in enumerate(expand(toks)):
                if ch != '.':
                    row[int(x) + i] = ch
    with open(os.path.join(HERE, 'delen.txt'), 'w', encoding='utf-8') as fh:
        fh.write('# gegenereerd door rle3.py uit delen_rle.txt; niet met de hand bewerken\n')
        for naam, extra, rows in parts:
            rows = {y + sum(1 for k in KNIP_Y if y < k):
                    {x - sum(1 for k in KNIP_X if x > k): c for x, c in r.items() if x not in KNIP_X}
                    for y, r in rows.items() if y not in KNIP_Y}
            if not rows:
                continue
            y0, y1 = min(rows), max(rows)
            fh.write('## %s 0 %d %s\n' % (naam, y0, ' '.join(extra)))
            for y in range(y0, y1 + 1):
                r = rows.get(y, {})
                fh.write(''.join(r.get(x, '.') for x in range(64)) + '\n')


if __name__ == '__main__':
    main()
