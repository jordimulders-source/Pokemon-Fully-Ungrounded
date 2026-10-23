"""Silhouetten (zwart) op 2x en 1x: kandidaten boven, echte sprites onder."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from sheet import *
O = sys.argv[1]
top = [S + 'alpaca/ronde5/anim_front.png', S + 'olinguito/ronde5/anim_front.png', S + 'nachtaap/ronde5/anim_front.png',
       S + 'cuyby/ronde1/anim_front.png', S + 'dj_rotom/ronde1/anim_front.png']
labels_top = ['alpaca r5', 'olinguito r5', 'nachtaap r5', 'cuyby A', 'DJ Rotom']
bot = [G + n + '/anim_front_gba.png' for n in ['mareep', 'zigzagoon', 'aipom', 'skitty', 'torchic']] + [G + 'rotom/wash/anim_front.png']
labels_bot = ['Mareep', 'Zigzagoon', 'Aipom', 'Skitty', 'Torchic', 'Rotom-Wash']
sc = 2
cw = 64 * sc + 70
W = 6 * cw + 10
img = Image.new('RGB', (W, 2 * (64 * sc + 20) + 10), (255, 255, 255))
d = ImageDraw.Draw(img)
for r, (paths, labs) in enumerate([(top, labels_top), (bot, labels_bot)]):
    for c, (p, l) in enumerate(zip(paths, labs)):
        sp = load(p, 0)
        a = sp.split()[3]
        sil = Image.new('RGBA', (64, 64), (20, 20, 20, 255))
        sil.putalpha(a)
        x = 5 + c * cw
        y = 5 + r * (64 * sc + 20)
        big = sil.resize((64 * sc, 64 * sc), Image.NEAREST)
        img.paste(big, (x, y + 14), big)
        img.paste(sil, (x + 64 * sc + 4, y + 14 + 64 * sc - 64), sil)
        d.text((x, y), l, fill=(0, 0, 0))
img.save(O)
print(O)
