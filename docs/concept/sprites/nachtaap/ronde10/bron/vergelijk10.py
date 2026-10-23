"""vergelijk10.py <nachtaapmap>: compare.png met ronde 9 en ronde 10, beide frames, 1x (licht en donker) en 3x."""
import sys, os
from PIL import Image, ImageDraw
d = sys.argv[1]
BG, DK = (232, 232, 224), (40, 40, 56)


def frame(pad, i, bg):
    src = Image.open(pad)
    f = src.crop((0, 64 * i, 64, 64 * i + 64))
    m = Image.new('L', (64, 64))
    m.putdata([0 if p == 0 else 255 for p in f.getdata()])
    out = Image.new('RGB', (64, 64), bg)
    out.paste(f.convert('RGB'), (0, 0), m)
    return out


rondes = [('ronde 9', os.path.join(d, 'ronde9/anim_front.png')), ('ronde 10', os.path.join(d, 'ronde10/anim_front.png'))]
CW = 192 + 12
cv = Image.new('RGB', (CW * 4, 20 + 192 + 10 + 64 + 8), BG)
dr = ImageDraw.Draw(cv)
k = 0
for naam, pad in rondes:
    for i in range(2):
        x0 = k * CW
        dr.text((x0 + 6, 4), '%s, frame %d' % (naam, i + 1), fill=(40, 40, 40))
        cv.paste(frame(pad, i, BG).resize((192, 192), Image.NEAREST), (x0 + 6, 20))
        cv.paste(frame(pad, i, BG), (x0 + 30, 20 + 192 + 10))
        cv.paste(frame(pad, i, DK), (x0 + 110, 20 + 192 + 10))
        k += 1
cv.save(os.path.join(d, 'ronde10/compare.png'))
