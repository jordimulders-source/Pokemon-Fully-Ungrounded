#!/usr/bin/env python3
"""Welk deel van het hoge gras op een kaart is te voet bereikbaar (zonder Surf), vanaf een rand?

Gebruik: python3 tools/grounded/balance/reach.py Route115 down
(richting = de kant waar je binnenkomt: up/down/left/right). Negeert objecten (bomen om te knippen,
rotsen, trainers) en warps; richels (jump-tiles) zijn eenrichtingsverkeer."""
import json, os, struct, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
GRASS = {0x02, 0x03, 0x07, 0x06, 0x24}  # tall/long grass, deep sand (woestijn), ash grass
WATER = set(range(0x10, 0x16)) | {0x17}
JUMP = {0x38: (1, 0), 0x39: (-1, 0), 0x3A: (0, -1), 0x3B: (0, 1)}


def tsdir(sym):
    import re
    hdr = open(os.path.join(ROOT, 'src/data/tilesets/headers.h')).read()
    body = re.search(r'const struct Tileset ' + sym + r' =\s*\{(.*?)\};', hdr, re.S).group(1)
    attr = re.search(r'\.metatileAttributes = (\w+)', body).group(1)
    g = open(os.path.join(ROOT, 'src/data/tilesets/metatiles.h')).read()
    return re.search(attr + r'\[\] = INCBIN_U16\("([^"]+)"', g).group(1)


def load(mapname):
    d = json.load(open(os.path.join(ROOT, 'data/maps', mapname, 'map.json')))
    L = [l for l in json.load(open(os.path.join(ROOT, 'data/layouts/layouts.json')))['layouts'] if l.get('id') == d['layout']][0]
    w, h = L['width'], L['height']
    blocks = struct.unpack('<%dH' % (w * h), open(os.path.join(ROOT, L['blockdata_filepath']), 'rb').read())
    pa = open(os.path.join(ROOT, tsdir(L['primary_tileset'])), 'rb').read()
    sa = open(os.path.join(ROOT, tsdir(L['secondary_tileset'])), 'rb').read()
    pa = struct.unpack('<%dH' % (len(pa) // 2), pa)
    sa = struct.unpack('<%dH' % (len(sa) // 2), sa)

    def beh(b):
        mid = b & 0x3FF
        a = pa[mid] if mid < 512 else (sa[mid - 512] if mid - 512 < len(sa) else 0)
        return a & 0xFF
    return w, h, blocks, beh


def reach(mapname, side):
    w, h, blocks, beh = load(mapname)
    coll = lambda x, y: (blocks[y * w + x] >> 10) & 3
    start = []
    for i in range(max(w, h)):
        x, y = {'down': (i, h - 1), 'up': (i, 0), 'left': (0, i), 'right': (w - 1, i)}[side]
        if 0 <= x < w and 0 <= y < h and coll(x, y) == 0 and beh(blocks[y * w + x]) not in WATER:
            start.append((x, y))
    seen = set(start)
    todo = list(start)
    while todo:
        x, y = todo.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            b = beh(blocks[ny * w + nx])
            if b in JUMP:
                if JUMP[b] == (dx, dy):
                    nx, ny = nx + dx, ny + dy
                    if (nx, ny) not in seen and 0 <= nx < w and 0 <= ny < h:
                        seen.add((nx, ny))
                        todo.append((nx, ny))
                continue
            if coll(nx, ny) != 0 or b in WATER or (nx, ny) in seen:
                continue
            seen.add((nx, ny))
            todo.append((nx, ny))
    grass = [(x, y) for y in range(h) for x in range(w) if beh(blocks[y * w + x]) in GRASS]
    ok = [g for g in grass if g in seen]
    return len(ok), len(grass), ok


if __name__ == '__main__':
    n, tot, ok = reach(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'down')
    print('%s: %d van %d grastiles te voet bereikbaar' % (sys.argv[1], n, tot))
    if ok:
        ys = [y for x, y in ok]
        print('  bereikbaar gras tussen y=%d en y=%d' % (min(ys), max(ys)))
