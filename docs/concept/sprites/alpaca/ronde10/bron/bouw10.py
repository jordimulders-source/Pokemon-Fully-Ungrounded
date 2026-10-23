"""Ronde 10: bouwt de alpaca uit met de hand geschreven run-length-rijen (geen automatische
schaduw of omlijning) en controleert hem.
Gebruik: python3 bouw10.py <map> [preview.png]   (map bevat bron/palet.txt en bron/delen.txt)
delen.txt: '## naam [dy2] [dx2]' en dan per rij 'y x0 runs', met runs als '3V 2W 1. 5w'
           ('.' = overslaan). Achterste deel eerst. dy2/dx2 = verschuiving in frame 2.
Schrijft anim_front.png, normal.pal, bron/raster_f1.txt, bron/raster_f2.txt en drukt een dump af.
"""
import sys, os, re
from PIL import Image, ImageDraw

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
        r = r.split('#', 1)[0] if not r.startswith('##') else r
        r = r.strip()
        if r.startswith('## '):
            p = r[3:].split()
            dy2 = int(p[1]) if len(p) > 1 else 0
            dx2 = int(p[2]) if len(p) > 2 else 0
            delen.append([p[0], dy2, dx2, []])
        elif r:
            p = r.split()
            y, x = int(p[0]), int(p[1])
            px = []
            for tok in p[2:]:
                m = re.fullmatch(r'(\d+)(.)', tok)
                if not m:
                    print('FOUT token', tok, 'in', delen[-1][0], 'rij', y); continue
                px.append((int(m.group(1)), m.group(2)))
            delen[-1][3].append((y, x, px))
    return delen


def samen(delen, f2):
    g = [['.'] * 64 for _ in range(64)]
    for naam, dy2, dx2, rijen in delen:
        for y, x, px in rijen:
            if f2:
                y += dy2; x += dx2
            for n, c in px:
                for _ in range(n):
                    if c != '.':
                        if c not in IDX:
                            print('ONBEKEND', c, naam)
                        elif 0 <= x < 64 and 0 <= y < 64:
                            g[y][x] = c
                        else:
                            print('BUITEN', naam, x, y)
                    x += 1
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
    lang = []
    for y in range(64):
        for kant, dy in (('boven', -1), ('onder', 1)):
            run = 0
            for x in range(65):
                ok = x < 64 and g[y][x] != '.' and (not 0 <= y + dy < 64 or g[y + dy][x] == '.')
                if ok:
                    run += 1
                else:
                    if run > 4: lang.append((kant, y, x - run, run))
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
        print('  open rand (randpixel zonder omlijningskleur):', lek[:40])
    if lang:
        print('  rechte randstukken >4 px:', lang)


f1, f2 = samen(lees(), 0), samen(lees(), 1)
check(f1, 'frame 1'); check(f2, 'frame 2')
print('   ' + ''.join(str(x % 10) for x in range(64)))
for y in range(64):
    if any(c != '.' for c in f1[y]):
        print('%2d ' % y + ''.join(f1[y]))
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
    wit = (255, 255, 255)
    def rgb(g):
        im = beeld(g).convert('RGB'); px = im.load()
        for y in range(64):
            for x in range(64):
                if g[y][x] == '.': px[x, y] = wit
        return im
    pv = Image.new('RGB', (512 * 2 + 8 + 64 + 8 + 128, 512), wit)
    pv.paste(rgb(f1).resize((512, 512), Image.NEAREST), (0, 0))
    pv.paste(rgb(f2).resize((512, 512), Image.NEAREST), (520, 0))
    pv.paste(rgb(f1), (1040, 0))
    pv.paste(rgb(f1).resize((128, 128), Image.NEAREST), (1040, 72))
    d = ImageDraw.Draw(pv)
    for o in (0, 520):
        for k in range(0, 65, 4):
            col = (60, 60, 200) if k % 8 == 0 else (200, 200, 235)
            d.line([(o + k * 8, 0), (o + k * 8, 511)], fill=col)
            d.line([(o, k * 8), (o + 511, k * 8)], fill=col)
    pv.save(sys.argv[2])
