"""Referentievel snavels (r7): de snavel van Fearow, Pidgeot, Staraptor, Spearow, Skarmory, Picapau en Picapau-evo r6/r7,
uitsnede op 8x (bovenrij: hele sprite op 1x). Draaien: python3.11 ref_snavels.py [zoom] [uit.png]
Wordt ook door kop_closeup.py gebruikt (uitsneden SNAVELS)."""
import sys
from PIL import Image, ImageDraw
G = '../../../../../../graphics/pokemon/'
def png(p):
    im = Image.open(p)
    if im.mode == 'P':
        im = im.convert('RGBA'); px = im.load(); bg = px[0, 0]
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                if px[x, y] == bg: px[x, y] = (0, 0, 0, 0)
    return im.convert('RGBA').crop((0, 0, 64, 64))
# (naam, bestand, uitsnede rond de snavel x0,y0,x1,y1)
SNAVELS = [('Fearow', G + 'fearow/anim_front.png', (2, 20, 26, 52)),
           ('Pidgeot', G + 'pidgeot/anim_front.png', (6, 14, 30, 34)),
           ('Staraptor', G + 'staraptor/anim_front.png', (10, 12, 30, 32)),
           ('Spearow', G + 'spearow/anim_front.png', (24, 14, 44, 34)),
           ('Skarmory', G + 'skarmory/anim_front.png', (0, 14, 24, 38)),
           ('Picapau', '../../../picapau/af/picapau.png', (10, 6, 30, 26)),
           ('evo r6', '../r6/picapau_evo.png', (6, 2, 32, 20)),
           ('evo r7', 'picapau_evo.png', (4, 2, 32, 20))]
def vel(items, Z, uit):
    W = max((c[2] - c[0]) * Z for _, _, c in items); H = max((c[3] - c[1]) * Z for _, _, c in items)
    v = Image.new('RGBA', (8 + len(items) * (max(W, 64) + 8), 16 + 72 + H + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
    for i, (t, f, c) in enumerate(items):
        im = png(f); x = 8 + i * (max(W, 64) + 8)
        d.text((x, 2), f'{t} {c}', fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16))
        k = im.crop(c); v.alpha_composite(k.resize((k.size[0] * Z, k.size[1] * Z), Image.NEAREST), (x, 88))
    v.convert('RGB').save(uit); print(uit, v.size)
if __name__ == '__main__':
    vel(SNAVELS, int(sys.argv[1]) if len(sys.argv) > 1 else 8, sys.argv[2] if len(sys.argv) > 2 else 'ref_snavels.png')
