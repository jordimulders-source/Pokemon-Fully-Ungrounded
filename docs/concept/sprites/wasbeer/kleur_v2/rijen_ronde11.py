"""Kleur ronde 11 van de wasbeer = allerlaatste afwerking op ronde10b (Jordi: "10b met pupil, laat de eindkeurder deze
keuren, voor de allerlaatste afwerking"). Exact de 8 reparaties uit EINDKEURING_ronde10b.md + de optionele klauwlijn
buiten budget; de oogglans blijft waar hij is. Als (x, y): (oud, nieuw).
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde11.py -> ronde11.txt/.png/.pal + controles."""
import os
import numpy as np
from PIL import Image
from rijen_ronde8 import binnen_los, N4, lees

HERE = os.path.dirname(os.path.abspath(__file__))
PAL_TXT = open(os.path.join(HERE, 'ronde10.pal')).read()
PALET = [tuple(int(v) for v in l.split()) for l in PAL_TXT.split('\n')[3:19]]
R = {
    'R1 verre oorvoet sluit': {(29, 6): ('5', '4')},
    'R2-4 staartrand naast poot = crème ring': {(43, 41): ('1', '9'), (43, 42): ('1', '9'), (43, 43): ('1', '9')},
    'R5-8 staartrand naast poot = donkere ring': {(42, 44): ('1', '2'), (42, 45): ('1', '2'), (42, 46): ('1', '2'), (42, 47): ('1', '2')},
    'opt. zachter begin klauwlijn': {(23, 25): ('4', '5')},
}
# Niet uitgevoerd: opt. kinschaduw (14,19),(15,19) 7->5 maakt (13,19) 7 een nieuwe losse pixel (eis: geen nieuwe losse pixels).
# Rechtzetten kan alleen met een extra pixel (13,19) 7->5, en dat valt buiten de opdracht.


def main():
    r10b = lees(os.path.join(HERE, 'ronde10b.txt'))
    g = r10b.copy()
    for n, d in R.items():
        for (x, y), (o, c) in d.items():
            assert g[y, x] == int(o, 16), (n, x, y)
            g[y, x] = int(c, 16)
    assert all(r10b[y, x] == 1 for x, y in ((42, 41), (42, 42), (42, 43), (41, 44), (41, 45), (41, 46), (41, 47)))  # pootrand blijft zwart
    rand = [(int(x), int(y)) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in N4)
            and g[y, x] not in (1, 2, 4, 11, 12)]
    l0, l1 = set(binnen_los(r10b)), set(binnen_los(g))
    print('alpha-diff t.o.v. ronde10b:', int(((g > 0) != (r10b > 0)).sum()), '| gewijzigd:', int((g != r10b).sum()), 'px',
          '| open randen:', rand, '| losse binnenpixels', len(l0), '->', len(l1), '| nieuw los:', sorted(l1 - l0), '| weg:', sorted(l0 - l1))
    open(os.path.join(HERE, 'ronde11.txt'), 'w').write(
        '\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64)); im.putpalette(sum(PALET, ())); im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, 'ronde11.png'), transparency=0)
    open(os.path.join(HERE, 'ronde11.pal'), 'w').write(PAL_TXT)


if __name__ == '__main__':
    main()
