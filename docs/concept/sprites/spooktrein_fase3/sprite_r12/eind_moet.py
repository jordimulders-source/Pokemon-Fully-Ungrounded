"""Eindkeuring r12 (16 nov): past de MOET-punten toe op sprite.png -> eind_voorstel.png (+ _8x).
Alleen niet-groene pixels; asserts: groen (idx 2,3,4,5,6,13) ongewijzigd, palet gelijk."""
from pathlib import Path
from PIL import Image
D = Path(__file__).parent
GROEN = {2, 3, 4, 5, 6, 13}
# (x, y, oud, nieuw)
MOET = [
    # A. overgang kop/lijf rechtsonder: zwart in vlak + dambord
    (22, 43, 1, 9), (24, 45, 1, 12), (24, 47, 1, 12), (25, 47, 12, 1),
    # B. onderrand onderste lijfplaat: dubbele zwarte lijn y42 -> schaduwtint
    (32, 42, 1, 12), (33, 42, 1, 12), (34, 42, 11, 12), (35, 42, 1, 12), (36, 42, 12, 9), (37, 42, 1, 9),
    # C. losse zwarte pixels in grijze plaatvlakken
    (31, 31, 1, 12), (35, 31, 1, 12),
    # D. koeienvanger: buil in de linkerrand weg (roest blijft als streep), lichte bovenrand, naad dicht
    (0, 52, 9, 0), (0, 53, 9, 0), (1, 52, 8, 9), (1, 53, 8, 9), (2, 51, 7, 8), (2, 52, 7, 8), (2, 53, 7, 8),
    (8, 47, 11, 9), (15, 53, 12, 1),
]
im = Image.open(D / 'sprite.png')
assert im.mode == 'P' and im.size == (64, 64)
uit = im.copy(); p = uit.load()
for x, y, a, b in MOET:
    assert p[x, y] == a, (x, y, p[x, y], a)
    assert a not in GROEN and b not in GROEN
    p[x, y] = b
o = im.load()
for y in range(64):
    for x in range(64):
        if o[x, y] in GROEN or p[x, y] in GROEN:
            assert o[x, y] == p[x, y], ('groen gewijzigd', x, y)
assert uit.getpalette() == im.getpalette()
n = sum(o[x, y] != p[x, y] for y in range(64) for x in range(64))
assert n == len(MOET)
uit.save(D / 'eind_voorstel.png', transparency=0)
uit.resize((512, 512), Image.NEAREST).save(D / 'eind_voorstel_8x.png', transparency=0)
print(n, 'pixels gewijzigd, groen 0')
