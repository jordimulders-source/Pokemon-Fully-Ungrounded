#!/usr/bin/env python3
"""Project Grounded: Mustard (Kubfu-dojo). Overworld uit Jordi's sheet (graphics/mustard.png, RMXP 4x4, 2x vergroot,
frames 16x24) -> Gen 3-overworld 9 frames 16x32 met eigen palet; trainerfoto = graphics/grounded/trainers/mustard/
mustard_front.png (met de hand afgewerkte Gen 3-versie van graphics/mustard2.jpg, zie CHANGELOG v0.8.126)."""
import os
from collections import deque
from PIL import Image
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BG = (115, 197, 164)

def gba(c): return tuple((v >> 3) << 3 for v in c[:3])

def frames():
    im = Image.open(os.path.join(ROOT, 'graphics/mustard.png')).convert('RGB')
    im = im.resize((im.width // 2, im.height // 2), Image.NEAREST)          # 64x96
    cells = {}
    for r, d in enumerate(('down', 'left', 'right', 'up')):
        for c in range(4):
            cell = im.crop((c * 16, r * 24, c * 16 + 16, r * 24 + 24))
            px = cell.load(); seen = set(); q = deque()
            for x in range(16): q.extend([(x, 0), (x, 23)])
            for y in range(24): q.extend([(0, y), (15, y)])
            while q:   # witte achtergrond vanaf de rand weghalen (wit haar/broek binnenin blijft)
                x, y = q.popleft()
                if (x, y) in seen or not (0 <= x < 16 and 0 <= y < 24) or min(px[x, y]) < 245: continue
                seen.add((x, y)); q.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
            out = Image.new('RGBA', (16, 32), (0, 0, 0, 0))
            for y in range(24):
                for x in range(16):
                    if (x, y) not in seen: out.putpixel((x, y + 8), px[x, y] + (255,))
            cells[(d, c)] = out
    # Gen 3-volgorde: 0 onder, 1 boven, 2 links, 3/4 onder lopen, 5/6 boven lopen, 7/8 links lopen
    order = [('down', 0), ('up', 0), ('left', 0), ('down', 1), ('down', 3), ('up', 1), ('up', 3), ('left', 1), ('left', 3)]
    return [cells[k] for k in order]

def reduce_palette(imgs, n=15):
    cols = {}
    for im in imgs:
        for p in im.getdata():
            if p[3]: cols[gba(p)] = cols.get(gba(p), 0) + 1
    m = {c: c for c in cols}
    while len(set(m.values())) > n:   # twee dichtste kleuren samenvoegen (de meest gebruikte blijft)
        live = sorted(set(m.values()))
        best = None
        for i, a in enumerate(live):
            for b in live[i + 1:]:
                d = sum(w * (x - y) ** 2 for w, x, y in zip((3, 6, 1), a, b))
                if best is None or d < best[0]: best = (d, a, b)
        _, a, b = best
        cnt = lambda c: sum(v for k, v in cols.items() if m[k] == c)
        keep, drop = (a, b) if cnt(a) >= cnt(b) else (b, a)
        for k in m:
            if m[k] == drop: m[k] = keep
    return m

def main():
    fr = frames()
    m = reduce_palette(fr)
    pal = sorted(set(m.values()), key=sum)
    sheet = Image.new('P', (16 * 9, 32), 0)
    for i, f in enumerate(fr):
        for y in range(32):
            for x in range(16):
                p = f.getpixel((x, y))
                if p[3]: sheet.putpixel((i * 16 + x, y), pal.index(m[gba(p)]) + 1)
    flat = list(BG)
    for c in pal: flat += c
    flat += [0] * (768 - len(flat))
    sheet.putpalette(flat)
    sheet.save(os.path.join(ROOT, 'graphics/object_events/pics/people/mustard.png'))
    with open(os.path.join(ROOT, 'graphics/object_events/palettes/mustard.pal'), 'w') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for i in range(16):
            c = flat[i * 3:i * 3 + 3]; f.write(f'{c[0]} {c[1]} {c[2]}\n')
    print('mustard overworld:', len(pal), 'kleuren')

if __name__ == '__main__':
    main()
