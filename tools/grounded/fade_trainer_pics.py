#!/usr/bin/env python3
"""Project Grounded: trainerfoto's die onderaan hard zijn afgekapt (benen eraf) laten wegvloeien met hetzelfde
Bayer-dither als de DS-foto's (fade_bottom in plasma_sprites.py). Werkt op de geïndexeerde PNG (index 0 =
transparant) en is idempotent: het masker hangt alleen van (x, y) af. Jordi, v0.9.60: Mustard.
Gebruik: python3 tools/grounded/fade_trainer_pics.py"""
from PIL import Image

PICS = ['mustard', 'colress']
ROWS = 8
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

for name in PICS:
    path = 'graphics/trainers/front_pics/%s.png' % name
    im = Image.open(path)
    assert im.mode == 'P'
    for i in range(ROWS):
        y = im.height - 1 - i
        t = (ROWS - i) / (ROWS + 1)
        for x in range(im.width):
            if BAYER[y % 4][x % 4] < t * 16:
                im.putpixel((x, y), 0)
    im.save(path)
    print(path)
