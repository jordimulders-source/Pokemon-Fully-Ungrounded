"""Kleur ronde 8 van de wasbeer (S1a), met de hand in tekstrijen op ronde 7.
Jordi over ronde 7 (3 nov): staartpunt slordig, pixelwerk rond de ogen + ogen niet Pokemon-achtig,
oren niet netjes, lijf links tussen arm en hoofd (rechte lijn, sluit niet aan), neus is een streep,
willekeurige vlekken -> Pokemon-shading.

Elke regel hieronder is (x, y, tekst): de tekst vervangt ronde 7 vanaf (x, y), een teken per
paletindex (zie ronde7.pal); een spatie = ronde 7 houden.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde8.py
-> ronde8.txt, ronde8.png, ronde8.pal + controles (alpha-diff, open randen, losse pixels, bevroren zones)."""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PAL_TXT = open(os.path.join(HERE, 'ronde7.pal')).read()
PALET = [tuple(int(v) for v in l.split()) for l in PAL_TXT.split('\n')[3:19]]

# --- Kop (x 10-35, y 0-20) + borst/schouder links (x 10-22, y 21-30) -------------------------
# oren: crème rand (a/9), donkere binnenkant (5, kern 4) die onderaan in de schedellijn opgaat;
# oog: zwart lid (1) met ooghoeken, iris e boven met glans a in het midden, f onder, lichter
#      onderlid 4 tussen oog en masker; verre oog (13,11-12) ongewijzigd, alleen lid 1 en onderlid 4;
# neus: rond 3x2 + punt, donker 2 met glans 6, crème snuit eromheen (los van het masker);
# kaak/hals: geen rechte 4-lijn meer, schaduw 5 onder de kaak die taps in het lijf overgaat;
# borst: hooglicht 7/3 als bolling midden langs de lichte rand, 6 basis, 5 naar de arm.
KOP = (10, 0, [
    ".....4441.................",
    "....4aaa91.....441........",
    "...4a95591.....4a91.......",
    "..4a9544591...4a9591......",
    "..49955554441.495491......",
    "..4433333777744455991.....",
    "..4333337777666644591.....",
    "..477776666aaa6655551.....",
    "..12aa6666aaaaa66651......",
    ".12222666a2222aa9651......",
    ".1212244221111266651......",
    "122e222221eae1266651......",
    "122f222222fff2266551......",
    "1224222aa24442666551......",
    ".12222aaaa22226666551.....",
    ".1999aaaaa2226666555541bb1",
    ".262aaaaaaa9976655556651bd",
    "12229aaa9977766655556655bd",
    ".19999777766666555566555bd",
    ".11777777666666655555555b1",
    "...1455566666666665555555b",
    ".....4556677              ",
    ".....4677776              ",
    ".....4733776              ",
    ".....4737766              ",
    ".....4777766              ",
    ".....4777666              ",
    ".....4776665              ",
    "....46666665              ",
    "....46666655              ",
    "....144566 5              ",
])

RIJEN = [
    # --- Staartpunt (haak): donkere koepel met licht linksboven, de punt hangt links omlaag
    #     (lichte kant 5/4 loopt door van de koepel langs de punt), spleet 1 schuin van (53,22)
    #     naar (51,27); ring op de schacht rechts in de bocht, boven- en onderrand als boog.
    (50, 19, "1445421"),
    (49, 20, "14554221"),
    (49, 21, "15542221"),
    (49, 22, "154212221"),
    (48, 23, "1542129921"),
    (48, 24, "15421a9981"),
    (48, 25, "1541999881"),
    (48, 26, "1441992281"),
    (48, 27, "1441222221"),
    (49, 28, "114222211"),
    (49, 29, "142222221"),
    # --- Nabije dij: los 7-vlak midden op de dij weg; hooglicht als sikkel linksboven
    #     (onder de buik, langs de overlaplijn), schaduwgrens 5 gebogen in plaats van recht.
    (29, 36, "777776665555"),
    (29, 37, "777666665555"),
    (25, 38, "66677766666655555"),
    (23, 39, "6666777666666665555"),
    (26, 40, "77766666666655555"),
    (27, 41, "776666666655555"),
    (28, 42, "66666666555555"),
    (29, 43, "6666665555555"),
    (30, 44, "66666555555"),
]


def lees(p):
    return np.array([[0 if c == '.' else int(c, 16) for c in l.rstrip('\n')] for l in open(p).read().split('\n')[:64]])


def bouw():
    g = [list(l) for l in open(os.path.join(HERE, 'ronde7.txt')).read().split('\n')[:64]]
    x0, y0, rows = KOP
    for dy, r in enumerate(rows):
        for dx, c in enumerate(r):
            if c != ' ':
                g[y0 + dy][x0 + dx] = c
    for x, y, s in RIJEN:
        for i, c in enumerate(s):
            if c != ' ':
                g[y][x + i] = c
    return np.array([[0 if c == '.' else int(c, 16) for c in r] for r in g])


N4 = ((0, 1), (0, -1), (1, 0), (-1, 0))


def binnen_los(g):
    """Pixels die niet aan transparant grenzen en geen enkele 4-buur met dezelfde index hebben."""
    H, W = g.shape
    out = []
    for y in range(H):
        for x in range(W):
            v = g[y, x]
            if v == 0:
                continue
            nb = [g[y + dy, x + dx] if 0 <= y + dy < H and 0 <= x + dx < W else 0 for dy, dx in N4]
            if 0 in nb:
                continue
            if v not in nb:
                out.append((x, y, format(int(v), 'x')))
    return out


def echte(n):
    im = Image.open(os.path.join(HERE, '../../../../../graphics/pokemon', n, 'anim_front.png'))
    return np.array(im)[:64, :64]


def main():
    g = bouw()
    r7 = lees(os.path.join(HERE, 'ronde7.txt'))
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    lab = [l for l in open(os.path.join(HERE, '../silhouet_v2/labels_s1a.txt')).read().split('\n')[1:65]]
    print('alpha-diff:', int(((g > 0) != sil).sum()), '| gewijzigd t.o.v. ronde7:', int((g != r7).sum()), 'px')
    # bevroren: buidel (Z), klauwen/handen (K/k), buideltinten b/c/d, verre oog, crème van buik/handen
    ger = [(x, y) for y in range(64) for x in range(64) if g[y, x] != r7[y, x]]
    bev = [(x, y) for x, y in ger if lab[y][x] in 'ZKk' or r7[y, x] in (11, 12, 13) or g[y, x] in (11, 12, 13)
           or (x, y) in ((13, 11), (13, 12)) or (y >= 22 and x < 46 and (r7[y, x] in (8, 9, 10) or g[y, x] in (8, 9, 10)))]
    print('bevroren zones geraakt:', bev)
    rand = [(int(x), int(y)) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in N4)
            and g[y, x] not in (1, 2, 4, 11, 12)]
    print('open randen (randpixel niet 1/2/4/b/c):', rand)
    l8, l7 = binnen_los(g), binnen_los(r7)
    print('losse binnenpixels: ronde7', len(l7), '| ronde8', len(l8))
    for n in ('zigzagoon', 'mightyena', 'linoone'):
        e = echte(n)
        print(f'  {n}: {len(binnen_los(e))} op {int((e > 0).sum())} px')
    print('  ronde8 lijst:', l8)
    open(os.path.join(HERE, 'ronde8.txt'), 'w').write(
        '\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64))
    im.putpalette(sum(PALET, ()))
    im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, 'ronde8.png'), transparency=0)
    open(os.path.join(HERE, 'ronde8.pal'), 'w').write(PAL_TXT)


if __name__ == '__main__':
    main()
