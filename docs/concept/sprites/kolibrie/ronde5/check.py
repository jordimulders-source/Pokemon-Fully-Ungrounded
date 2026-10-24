"""Bewijs ronde 5: alpha (silhouet) identiek aan eind/kolibrie.png, telling van omgekleurde pixels, palet."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
a = Image.open(os.path.join(HERE, '../eind/kolibrie.png')); b = Image.open(os.path.join(HERE, 'kolibrie.png'))
assert b.size == (64, 64) and b.mode == 'P' and b.info.get('transparency') == 0
pa, pb = a.load(), b.load()
ra, rb = a.convert('RGBA').load(), b.convert('RGBA').load()
alpha = [(x, y) for y in range(64) for x in range(64) if (pa[x, y] == 0) != (pb[x, y] == 0)]
kleur = [(x, y) for y in range(64) for x in range(64) if pa[x, y] and ra[x, y] != rb[x, y]]
used = sorted({pb[x, y] for y in range(64) for x in range(64)})
print('alpha-verschillen:', len(alpha))
print('ondoorzichtige pixels:', sum(1 for y in range(64) for x in range(64) if pb[x, y]))
print('omgekleurde pixels:', len(kleur))
print('gebruikte indices:', used, '(', len(used), 'incl. 0 )')
# open randen: nieuw gekleurde pixel naast transparant
rand = [(x, y) for (x, y) in kleur if any(0 <= x + dx < 64 and 0 <= y + dy < 64 and pb[x + dx, y + dy] == 0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
print('omgekleurde pixels naast transparant:', rand)
