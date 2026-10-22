"""Segmentraster: een sprite met de hand pixel voor pixel, zonder puntjes te tellen.

Bestand: per regel 'y: x tekst | x tekst | ...'; tekens zoals ascii_sprite.py
('.' = transparant, 1-9 = index, a-f = 10-15, '_' = laat staan). '== frame N' begint
een frame; '# ...' is commentaar. Een frame kan ook starten vanaf een basis-PNG:
'== frame N base=pad.png' (frame N uit die PNG), of 'base=prev' (kopie van het vorige
frame).

  python3 segraster.py in.seg normal.pal uit.png
"""
import sys, os
import numpy as np
from PIL import Image

CH = '.123456789abcdef'


def parse(path):
    frames = []
    cur = None
    for line in open(path).read().split('\n'):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('=='):
            parts = s.split()
            n = int(parts[2])
            base = [p[5:] for p in parts if p.startswith('base=')]
            if base and base[0] == 'prev':
                cur = frames[-1].copy()
            elif base:
                bp = base[0] if os.path.isabs(base[0]) else os.path.join(os.path.dirname(path), base[0])
                cur = np.array(Image.open(bp))[(n - 1) * 64:n * 64].copy()
            else:
                cur = np.zeros((64, 64), np.uint8)
            frames.append(cur)
            continue
        y, rest = s.split(':', 1)
        y = int(y)
        for seg in rest.split('|'):
            seg = seg.strip()
            if not seg:
                continue
            x, txt = seg.split(None, 1) if ' ' in seg else (seg, '')
            x = int(x)
            for i, ch in enumerate(txt.strip()):
                if ch == '_':
                    continue
                cur[y, x + i] = CH.index(ch)
    return frames


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import spritelib as L
    from shapelib import save_indexed
    save_indexed(sys.argv[3], parse(sys.argv[1]), L.read_pal(sys.argv[2]))
    print(sys.argv[3])
