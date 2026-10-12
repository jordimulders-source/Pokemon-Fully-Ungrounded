#!/usr/bin/env python3
"""Project Grounded: overworld van de Shy Guy (Yoshi's Island-stijl, 32x32, 9 frames).
Bron: 'shy guy.png' in de repo-root (custom Shy Guy-sprites door DarkSB24, sheet met dank aan Cheeseman; zie CREDITS.md).
- voor: rij 1 frame 1, achter: rij 1 frame 8, opzij (3/4, kijkt naar links): de loopcyclus uit rij 2.
- loopframes voor/achter: lijf 1 px omhoog, één schoen blijft op de grond.
Kleuren: 15 + transparant. De groene/roze/zwarte varianten zijn paletwissels; de kleuren komen per index uit de
trainerfoto-bronnen (graphics/grounded/trainers/guests/shyguy_*_bron.png, zelfde vorm als de rode).
Uitvoer: graphics/object_events/pics/people/shy_guy.png + palettes/shy_guy_{red,green,pink,black}.pal.
Gebruik: python3 tools/grounded/shyguy_overworld.py [voorbeeld.png]"""
import os, sys
from collections import Counter
from PIL import Image
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BG = (255, 255, 255)

R1 = [(9, 26), (36, 57), (66, 85), (96, 113), (125, 142), (152, 173), (184, 201), (212, 229), (239, 260)]
R2 = [(8, 25), (28, 45), (49, 66), (69, 87), (91, 108), (112, 129), (133, 150), (154, 171), (175, 192), (195, 213), (216, 234), (237, 255)]
SIDE_FRAMES = (1, 3, 9)  # stilstaan, stap 1, stap 2 (rij 2)

# Rood palet (index 0 = transparant)
PAL_RED = [(115, 197, 164),
           (0, 0, 0), (255, 255, 255), (231, 231, 231), (190, 190, 190), (128, 128, 128),  # 1-5 omlijning + masker
           (255, 0, 0), (185, 0, 0), (128, 0, 0), (72, 0, 0),                              # 6-9 mantel (rood)
           (102, 23, 0), (145, 69, 26), (173, 107, 45),                                    # a-c riem/rugzak (bruin)
           (0, 0, 255), (81, 81, 255),                                                     # d-e schoenen
           (238, 194, 37)]                                                                 # f gesp
MERGE = {(2, 2, 2): (0, 0, 0), (206, 0, 0): (185, 0, 0), (64, 21, 0): (72, 0, 0), (105, 53, 18): (102, 23, 0),
         (176, 176, 255): (81, 81, 255), (176, 144, 33): (238, 194, 37), (255, 245, 62): (238, 194, 37)}


# Met de hand: de roze bron (Fly Guy met vleugel) heeft een andere vorm, dus geen pixel-op-pixel-kleuren
OVERRIDE = {
    'pink': {1: (0, 0, 0), 2: (255, 255, 255), 3: (231, 231, 231), 4: (190, 190, 190), 5: (128, 128, 128),
             6: (255, 140, 198), 7: (255, 102, 179), 8: (255, 32, 143), 9: (230, 0, 115),
             0xa: (150, 100, 70), 0xb: (193, 148, 106), 0xc: (209, 176, 146), 0xd: (58, 58, 58), 0xe: (100, 100, 100)},
    'black': {0xa: (41, 41, 41), 0xb: (60, 60, 60), 0xc: (87, 87, 87), 0xf: (143, 143, 143)},
}


def grab(sheet, seg, y0, y1):
    a, b = seg
    im = sheet.crop((a, y0, b + 1, y1 + 1))
    w, h = im.size
    px = im.load()
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    o = out.load()
    outside = set()
    stack = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    while stack:  # wit buiten de omlijning = transparant (wit binnen = masker)
        x, y = stack.pop()
        if (x, y) in outside or not (0 <= x < w and 0 <= y < h) or px[x, y] != BG:
            continue
        outside.add((x, y))
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for y in range(h):
        for x in range(w):
            if (x, y) not in outside:
                o[x, y] = px[x, y] + (255,)
    return out.crop(out.getbbox())


def place(spr):
    f = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    w, h = spr.size
    f.alpha_composite(spr, ((32 - w) // 2, 32 - h))
    return f


def step(spr, side):
    w, h = spr.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.alpha_composite(spr.crop((0, 1, w, h)), (0, 0))  # lijf 1 px omhoog
    for x in range(w):
        if (x < w // 2) == (side == 0):  # deze schoen blijft staan
            for y in range(h - 3, h):
                out.putpixel((x, y), spr.getpixel((x, y)))
    return out


def recolor(name):
    """Kleur per index uit de trainerfoto-bron van deze kleur (zelfde pixels als de rode bron)."""
    gdir = os.path.join(ROOT, 'graphics/grounded/trainers/guests')
    red = Image.open(os.path.join(gdir, 'shyguy_red_bron.png')).convert('RGBA')
    oth = Image.open(os.path.join(gdir, f'shyguy_{name}_bron.png')).convert('RGBA')
    votes = {}
    for y in range(min(red.height, oth.height)):
        for x in range(min(red.width, oth.width)):
            r, o = red.getpixel((x, y)), oth.getpixel((x, y))
            if r[3] == 0 or o[3] == 0:
                continue
            rc = MERGE.get(r[:3], r[:3])
            if rc in PAL_RED:
                votes.setdefault(PAL_RED.index(rc), Counter())[o[:3]] += 1
    pal = list(PAL_RED)
    for i, c in votes.items():
        if i <= 9 or i in (0xd, 0xe):  # riem, rugzak en gesp blijven zoals bij de rode
            pal[i] = c.most_common(1)[0][0]
    for i, c in OVERRIDE.get(name, {}).items():
        pal[i] = c
    return pal


def main():
    sheet = Image.open(os.path.join(ROOT, 'shy guy.png')).convert('RGB')
    front = grab(sheet, R1[0], 4, 31)
    back = grab(sheet, R1[7], 4, 31)
    side = [grab(sheet, R2[i], 35, 63) for i in SIDE_FRAMES]
    frames = [place(front), place(back), place(side[0]),
              place(step(front, 0)), place(step(front, 1)),
              place(step(back, 0)), place(step(back, 1)),
              place(side[1]), place(side[2])]
    im = Image.new('P', (32 * 9, 32), 0)
    px = im.load()
    for i, f in enumerate(frames):
        for y in range(32):
            for x in range(32):
                c = f.getpixel((x, y))
                if c[3] == 0:
                    continue
                rgb = MERGE.get(c[:3], c[:3])
                px[32 * i + x, y] = PAL_RED.index(rgb)
    im.putpalette([v for c in PAL_RED for v in c] + [0] * (768 - 48))
    im.save(os.path.join(ROOT, 'graphics/object_events/pics/people/shy_guy.png'))
    for name in ('red', 'green', 'pink', 'black'):
        pal = PAL_RED if name == 'red' else recolor(name)
        with open(os.path.join(ROOT, f'graphics/object_events/palettes/shy_guy_{name}.pal'), 'w') as fh:
            fh.write('JASC-PAL\n0100\n16\n')
            for c in pal:
                fh.write(f'{c[0]} {c[1]} {c[2]}\n')
    if len(sys.argv) > 1:
        rows = []
        for name in ('red', 'green', 'pink', 'black'):
            pal = PAL_RED if name == 'red' else recolor(name)
            v = im.copy()
            v.putpalette([q for c in pal for q in c] + [0] * (768 - 48))
            rows.append(v.convert('RGB'))
        out = Image.new('RGB', (im.width, 32 * 4))
        for i, r in enumerate(rows):
            out.paste(r, (0, 32 * i))
        out.resize((out.width * 4, out.height * 4), Image.NEAREST).save(sys.argv[1])
    print('shy guy overworld klaar')


if __name__ == '__main__':
    main()
