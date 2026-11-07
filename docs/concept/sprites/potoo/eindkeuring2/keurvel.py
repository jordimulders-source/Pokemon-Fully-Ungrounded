"""Eindkeuring 2 potoo: keurvel (8x naast Gen 3-referenties) + metingen.
Gebruik: python3 keurvel.py (vanuit de repo-root)."""
import colorsys, os
from collections import Counter
from PIL import Image, ImageDraw
R = 'graphics/pokemon/'
KAND = 'docs/concept/sprites/potoo/eind_r1/potoo.png'
UIT = 'docs/concept/sprites/potoo/eindkeuring2/'
REFS = ['noctowl', 'xatu', 'swellow', 'drifloon', 'swablu', 'dusclops']

def laad(p):
    im = Image.open(p)
    im = im.crop((0, 0, 64, 64))
    return im

def pad(n):
    for f in ('anim_front_gba.png', 'anim_front.png', 'front.png'):
        if os.path.exists(R + n + '/' + f):
            return R + n + '/' + f

def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

def info(im, naam):
    pal = im.getpalette()
    cnt = Counter(im.getdata())
    regels = []
    for i in sorted(cnt):
        if i == 0:
            continue
        c = pal[3 * i:3 * i + 3]
        h, l, s = colorsys.rgb_to_hls(*[v / 255 for v in c])
        regels.append((lum(c), i, tuple(c), h * 360, s, cnt[i]))
    regels.sort()
    tot = sum(r[5] for r in regels)
    donker = sum(r[5] for r in regels if r[0] < 40) / tot
    out = [f'## {naam}: {len(regels)} kleuren, {tot} px, aandeel L<40 = {donker:.2f}']
    for L, i, c, h, s, n in regels:
        out.append(f'  idx{i:2d} {c} L={L:5.1f} H={h:5.0f} S={s:.2f} n={n}')
    return '\n'.join(out)

def rgba(im, bg):
    rgb = im.convert('RGB')
    out = Image.new('RGB', (64, 64), bg)
    m = Image.new('L', (64, 64), 0)
    for y in range(64):
        for x in range(64):
            if im.getpixel((x, y)) != 0:
                m.putpixel((x, y), 255)
    out.paste(rgb, (0, 0), m)
    return out

def vel():
    namen = ['potoo (eind_r1)'] + REFS
    ims = [laad(KAND)] + [laad(pad(n)) for n in REFS]
    S = 8
    W = len(ims) * (64 * S + 8) + 8
    H = 64 * S + 16 + 2 * 64 + 48 + 72
    v = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(v)
    for k, (im, nm) in enumerate(zip(ims, namen)):
        x0 = 8 + k * (64 * S + 8)
        g = rgba(im, (200, 208, 216)).resize((64 * S, 64 * S), Image.NEAREST)
        v.paste(g, (x0, 16))
        d.text((x0, 2), nm, fill=(0, 0, 0))
        # 1x op wit en op lichte grasgroene battle-achtergrond, 2x
        v.paste(rgba(im, (248, 248, 248)).resize((128, 128), Image.NEAREST), (x0, 64 * S + 24))
        v.paste(rgba(im, (232, 240, 208)), (x0 + 140, 64 * S + 24))
        v.paste(rgba(im, (248, 248, 248)), (x0 + 210, 64 * S + 24))
        v.paste(rgba(im, (40, 40, 48)), (x0 + 140, 64 * S + 100))
        v.paste(rgba(im, (24, 32, 56)), (x0 + 210, 64 * S + 100))
    # rooster op kandidaat
    for i in range(0, 65, 8):
        d.line([(8 + i * S, 16), (8 + i * S, 16 + 64 * S)], fill=(150, 150, 150))
        d.line([(8, 16 + i * S), (8 + 64 * S, 16 + i * S)], fill=(150, 150, 150))
    v.save(UIT + 'keurvel.png')

def clusters(im, minimum=3):
    W, Hh = im.size
    gezien = set(); klein = []
    for y in range(Hh):
        for x in range(W):
            i = im.getpixel((x, y))
            if i == 0 or (x, y) in gezien:
                continue
            st = [(x, y)]; gezien.add((x, y)); comp = []
            while st:
                a, b = st.pop(); comp.append((a, b))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    p = (a + dx, b + dy)
                    if 0 <= p[0] < W and 0 <= p[1] < Hh and p not in gezien and im.getpixel(p) == i:
                        gezien.add(p); st.append(p)
            if len(comp) < minimum:
                klein.append((i, comp))
    return klein

if __name__ == '__main__':
    vel()
    rap = [info(laad(KAND), 'potoo')]
    for n in REFS:
        rap.append(info(laad(pad(n)), n + ' (' + pad(n).split('/')[-1] + ')'))
    k = laad(KAND)
    kl = clusters(k)
    rap.append(f'## potoo: tintvlakjes < 3 px (4-buren): {len(kl)}')
    for i, c in kl:
        rap.append(f'  idx{i}: {c}')
    for n in ('swellow', 'noctowl', 'xatu'):
        rap.append(f'## {n}: tintvlakjes < 3 px: {len(clusters(laad(pad(n))))}')
    open(UIT + 'metingen.txt', 'w').write('\n'.join(rap) + '\n')
    print('\n'.join(rap))
