"""ASCII <-> geïndexeerde sprite, om sprites met de hand pixel voor pixel bij te werken.

  python3 ascii_sprite.py dump in.png uit.txt      # frames als tekstraster
  python3 ascii_sprite.py load in.txt pal.pal uit.png

Tekens: '.' = 0 (transparant), 1-9 = index 1-9, a-f = 10-15. Frames gescheiden door
een regel '== frame N'. Regels die met '#' beginnen zijn commentaar."""
import sys
import numpy as np
from PIL import Image

CH = '.123456789abcdef'


def dump(src, dst):
    a = np.array(Image.open(src))
    with open(dst, 'w') as f:
        for k in range(a.shape[0] // 64):
            f.write('== frame %d\n' % (k + 1))
            for row in a[k * 64:(k + 1) * 64]:
                f.write(''.join(CH[v] for v in row) + '\n')


def parse(txt):
    frames, cur = [], None
    for line in open(txt).read().split('\n'):
        if line.startswith('== '):
            cur = []; frames.append(cur); continue
        if line.startswith('#') or cur is None or not line.strip():
            continue
        row = [CH.index(ch) for ch in line.rstrip('\n')[:64].ljust(64, '.')]
        cur.append(row)
    return [np.array(f[:64] + [[0] * 64] * (64 - len(f)), np.uint8) for f in frames]


def load(txt, pal, dst):
    sys.path.insert(0, __file__.rsplit('/', 1)[0])
    import spritelib as L
    from shapelib import save_indexed
    save_indexed(dst, parse(txt), L.read_pal(pal))


if __name__ == '__main__':
    if sys.argv[1] == 'dump':
        dump(sys.argv[2], sys.argv[3])
    else:
        load(sys.argv[2], sys.argv[3], sys.argv[4])
