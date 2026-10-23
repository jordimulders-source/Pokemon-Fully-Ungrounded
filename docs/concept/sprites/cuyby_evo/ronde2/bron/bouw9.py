"""Ronde 9: bouwt een sprite uit met de hand getekende delen (alleen samenvoegen, geen automatische
schaduw of omlijning) en controleert hem.
Gebruik: python3 bouw9.py <map>   (map bevat bron/palet.txt en bron/delen.txt)
palet.txt: per regel  'teken r g b [omlijning]'  (eerste regel = transparant; 'omlijning' markeert
           kleuren die als buitenrand mogen dienen; 'zwart' markeert de zwarte omlijning)
delen.txt: '## naam x y [dy2] [dx2]' gevolgd door rijen tekens ('.' = niets); achterste deel eerst.
           dy2/dx2 = verschuiving van dat deel in frame 2.
Schrijft anim_front.png, normal.pal, bron/raster_f1.txt, bron/raster_f2.txt en een 8x-preview.
"""
import sys, os
from PIL import Image

D = sys.argv[1]
B = os.path.join(D, 'bron')
PAL, RAND, ZWART = [], set(), set()
for r in open(os.path.join(B, 'palet.txt'), encoding='utf-8'):
    p = r.split('#')[0].split()
    if not p:
        continue
    PAL.append((p[0], (int(p[1]), int(p[2]), int(p[3]))))
    if 'omlijning' in p[4:]:
        RAND.add(p[0])
    if 'zwart' in p[4:]:
        ZWART.add(p[0]); RAND.add(p[0])
IDX = {c: i for i, (c, _) in enumerate(PAL)}
assert len(PAL) <= 16


def lees():
    delen = []
    for r in open(os.path.join(B, 'delen.txt'), encoding='utf-8'):
        r = r.rstrip('\n')
        if r.startswith('## '):
            p = r[3:].split()
            dy2 = int(p[3]) if len(p) > 3 else 0
            dx2 = int(p[4]) if len(p) > 4 else 0
            delen.append([p[0], int(p[1]), int(p[2]), dy2, dx2, []])
        elif r.startswith('#') or not r.strip():
            continue
        else:
            delen[-1][5].append(r)
    return delen


def samen(delen, f2):
    g = [['.'] * 64 for _ in range(64)]
    for naam, x0, y0, dy2, dx2, rijen in delen:
        if f2:
            x0 += dx2; y0 += dy2
        for dy, rij in enumerate(rijen):
            for dx, c in enumerate(rij):
                if c == '.':
                    continue
                if c not in IDX:
                    print('ONBEKEND teken', repr(c), 'in', naam); continue
                X, Y = x0 + dx, y0 + dy
                if 0 <= X < 64 and 0 <= Y < 64:
                    g[Y][X] = c
                else:
                    print('BUITEN doek:', naam, X, Y)
    return g


def beeld(g):
    im = Image.new('P', (64, 64))
    flat = []
    for _, rgb in PAL:
        flat += list(rgb)
    im.putpalette(flat + [0] * (48 - len(flat)))
    im.putdata([IDX[c] for r in g for c in r])
    return im


def check(g, label):
    opp = sum(c != '.' for r in g for c in r)
    rand = zw = 0
    lek = []
    for y in range(64):
        for x in range(64):
            if g[y][x] == '.':
                continue
            if any(not (0 <= u < 64 and 0 <= v < 64) or g[v][u] == '.'
                   for u, v in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                rand += 1
                zw += g[y][x] in ZWART
                if g[y][x] not in RAND:
                    lek.append((x, y, g[y][x]))
    # rechte stukken in de buitenrand (horizontaal/verticaal) langer dan 4
    lang = []
    for y in range(64):
        run = 0
        for x in range(65):
            ok = x < 64 and g[y][x] != '.' and (y == 0 or g[y - 1][x] == '.')
            if ok:
                run += 1
            else:
                if run > 4: lang.append(('boven', y, x - run, run))
                run = 0
        run = 0
        for x in range(65):
            ok = x < 64 and g[y][x] != '.' and (y == 63 or g[y + 1][x] == '.')
            if ok:
                run += 1
            else:
                if run > 4: lang.append(('onder', y, x - run, run))
                run = 0
    for x in range(64):
        for kant, dx in (('links', -1), ('rechts', 1)):
            run = 0
            for y in range(65):
                ok = y < 64 and g[y][x] != '.' and (not 0 <= x + dx < 64 or g[y][x + dx] == '.')
                if ok:
                    run += 1
                else:
                    if run > 4: lang.append((kant, x, y - run, run))
                    run = 0
    print('%s: oppervlak %d, zwart-aandeel rand %.2f' % (label, opp, zw / max(rand, 1)))
    if lek:
        print('  randpixels zonder omlijningskleur (open rand?):', lek[:40])
    if lang:
        print('  rechte randstukken >4 px (kant, rij/kolom, start, lengte):', lang)


f1, f2 = samen(lees(), 0), samen(lees(), 1)
check(f1, 'frame 1'); check(f2, 'frame 2')
for naam, g in (('raster_f1.txt', f1), ('raster_f2.txt', f2)):
    with open(os.path.join(B, naam), 'w') as fh:
        fh.write('\n'.join(''.join(r) for r in g) + '\n')
im = Image.new('P', (64, 128))
im.putpalette(beeld(f1).getpalette())
im.paste(beeld(f1), (0, 0)); im.paste(beeld(f2), (0, 64))
im.save(os.path.join(D, 'anim_front.png'), transparency=0)
with open(os.path.join(D, 'normal.pal'), 'w', newline='\r\n') as fh:
    fh.write('JASC-PAL\n0100\n16\n')
    for i in range(16):
        r, gg, b = PAL[i][1] if i < len(PAL) else (0, 0, 0)
        fh.write('%d %d %d\n' % (r, gg, b))
if len(sys.argv) > 2:
    pv = Image.new('RGB', (64 * 8 * 2 + 8 + 64 + 8, 64 * 8), (255, 255, 255))
    pv.paste(beeld(f1).convert('RGB').resize((512, 512), Image.NEAREST), (0, 0))
    pv.paste(beeld(f2).convert('RGB').resize((512, 512), Image.NEAREST), (520, 0))
    pv.paste(beeld(f1).convert('RGB'), (1040, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(pv)
    for o in (0, 520):
        for k in range(0, 65, 4):
            col = (60, 60, 200) if k % 8 == 0 else (190, 190, 230)
            d.line([(o + k * 8, 0), (o + k * 8, 511)], fill=col)
            d.line([(o, k * 8), (o + 511, k * 8)], fill=col)
    pv.save(sys.argv[2])
