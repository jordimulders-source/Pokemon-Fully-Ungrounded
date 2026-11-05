#!/usr/bin/env python3
"""Keurvel voor sprites (SPRITE_WERKWIJZE, Checklist): eigen werk naast de bronnen, elk op 8× en 1×, op licht en donker,
plus optionele close-ups. Schrijft ook een keuringssjabloon <uit>.keuring.md als dat nog niet bestaat
(het keurslot in .claude/hooks/ eist dat bestand vóór een afbeelding naar Jordi gaat).

Gebruik (vanuit de repo-root):
  python3 tools/grounded/keurvel.py -o uit.png --werk eigen.png --bron graphics/pokemon/drowzee/anim_front.png ref.png \
      [--zoom x0,y0,x1,y1 ...]   # close-up-vakken in 64-px-coördinaten van het eigen werk (8× → 16×)
Afbeeldingen groter dan 64×64 (foto's, renders) worden passend verkleind; anim_front-sheets: alleen frame 1."""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('-o', required=True)
ap.add_argument('--werk', required=True)
ap.add_argument('--bron', nargs='+', default=[])
ap.add_argument('--zoom', nargs='*', default=[])
a = ap.parse_args()
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)


def laad(p):
    im = Image.open(p)
    if im.mode == 'P':
        idx = np.array(im); rgba = np.array(im.convert('RGBA')); rgba[idx == 0, 3] = 0
        im = Image.fromarray(rgba)
    else:
        im = im.convert('RGBA')
    if im.size[0] == 64 and im.size[1] in (128, 64):
        return im.crop((0, 0, 64, 64)), True
    im.thumbnail((256, 256))
    return im, False


def tegel(im, pix, schaal, bg):
    w, h = im.size
    big = im.resize((w * schaal, h * schaal), Image.NEAREST) if pix else im.resize((w * schaal // 4 if w > 64 else w * schaal, h * schaal // 4 if w > 64 else h * schaal))
    t = Image.new('RGB', big.size, bg); t.paste(big, (0, 0), big); return t


rijen = []
for naam, p in [('WERK: ' + os.path.basename(a.werk), a.werk)] + [(os.path.basename(b), b) for b in a.bron]:
    im, pix = laad(p)
    groot = tegel(im, pix, 8 if pix else 2, (255, 255, 255))
    een_l = tegel(im, pix, 1, (255, 255, 255)) if pix else im.resize((64, 64)).convert('RGB')
    een_d = tegel(im, pix, 1, (40, 36, 48)) if pix else een_l
    rijen.append((naam, groot, een_l, een_d))
zooms = []
if a.zoom:
    w, _ = laad(a.werk)
    for z in a.zoom:
        x0, y0, x1, y1 = map(int, z.split(','))
        c = w.crop((x0, y0, x1, y1)); zooms.append(tegel(c, True, 16, (255, 255, 255)))
W = 20 + sum(r[1].size[0] + 10 for r in rijen) + 90
W = max(W, 20 + sum(z.size[0] + 10 for z in zooms))
H = 30 + max(r[1].size[1] for r in rijen) + 100 + (max([z.size[1] for z in zooms] + [0]) + 20)
vel = Image.new('RGB', (W, H), (236, 236, 240)); d = ImageDraw.Draw(vel)
x = 10
for naam, groot, l, dk in rijen:
    d.text((x, 8), naam + ' (8×)', fill=(0, 0, 0), font=F)
    vel.paste(groot, (x, 28)); y = 34 + groot.size[1]
    vel.paste(l, (x, y)); vel.paste(dk, (x + 70, y)); d.text((x + 140, y + 4), '1× licht/donker', fill=(60, 60, 60), font=F)
    x += max(groot.size[0], 260) + 10
y = 34 + max(r[1].size[1] for r in rijen) + 80
x = 10
for i, z in enumerate(zooms):
    d.text((x, y - 16), f'close-up {a.zoom[i]} (16×)', fill=(0, 0, 0), font=F); vel.paste(z, (x, y)); x += z.size[0] + 10
vel.save(a.o)
k = a.o + '.keuring.md'
if not os.path.exists(k):
    open(k, 'w', encoding='utf-8').write(
        '# Keuring\n- Bron: ' + ', '.join(a.bron) + '\n- Bekeken op 8× en 1× (licht/donker)' + (' + close-ups' if a.zoom else '') +
        '\n- Per onderdeel (lijkt op <bron> / wijkt af in <x>):\n  - \n- Oordeel: FAIL  (alleen PASS als er geen enkele afwijking of twijfel is)\n')
print('vel:', a.o, '\nkeuring:', k)
