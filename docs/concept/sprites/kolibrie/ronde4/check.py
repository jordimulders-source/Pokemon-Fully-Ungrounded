"""Ronde 4: bewijs dat kop, kuif, lijf en vleugels bevroren zijn (diff 0 buiten de staartzone),
telt de gewijzigde staartpixels en zoekt open randen (basis/hooglicht naast transparant)."""
import sys, os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../ronde3'))
from teken import PAL
inv = {v[0]: k for k, v in PAL.items()}
a = np.array(Image.open(os.path.join(HERE, '../ronde3/kolibrie_variant_sleep.png')))
b = np.array(Image.open(os.path.join(HERE, 'kolibrie.png')))
def staartzone(x, y):
    return (y >= 26 and x >= 42) or (y >= 41 and x >= 36)
d = np.argwhere(a != b)
buiten = [(int(x), int(y)) for y, x in d if not staartzone(x, y)]
print('gewijzigd totaal:', len(d), '| buiten staartzone (bevroren):', len(buiten), buiten)
print('erbij:', int(((b > 0) & (a == 0)).sum()), 'eraf:', int(((b == 0) & (a > 0)).sum()), 'omgekleurd:', int(((a > 0) & (b > 0) & (a != b)).sum()))
print('px:', int((b > 0).sum()), 'kleuren:', len(set(b.flatten())))
open_ = {}
for y in range(64):
    for x in range(64):
        c = inv[b[y, x]]
        if c in 'VLTUWhw' or (c in 'pP' and x > 30):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                X, Y = x + dx, y + dy
                if 0 <= X < 64 and 0 <= Y < 64 and b[Y, X] == 0:
                    open_.setdefault(c, []).append((x, y, 'staart' if staartzone(x, y) else 'bevroren'))
                    break
print('open randen:', open_)
