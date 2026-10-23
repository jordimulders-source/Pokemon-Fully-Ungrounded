"""Vergelijkend vel ronde 5: ronde 4 en ronde 5 (f1, f2) naast Gen 3-sprites, op 3x en 1x.
python3 compare5.py <ronde5 anim_front.png> <ronde4 anim_front.png> <graphics/pokemon> uit.png"""
import sys
from PIL import Image, ImageDraw

r5, r4, G, out = sys.argv[1:5]
REFS = ['torchic', 'mudkip', 'treecko', 'ponyta', 'mareep', 'growlithe', 'vulpix']
items = [('ronde 4', r4, 0), ('ronde 5 f1', r5, 0), ('ronde 5 f2', r5, 1)]
items += [(n.capitalize(), '%s/%s/anim_front_gba.png' % (G, n), 0) for n in REFS]
z, pad = 3, 8
cw = 64 * z + pad
W, H = len(items) * cw + pad, 64 * z + 64 + 2 * 64 + 60
sheet = Image.new('RGB', (W, H), (248, 248, 248))
d = ImageDraw.Draw(sheet)


def checker(w, h, s):
    im = Image.new('RGB', (w, h))
    dd = ImageDraw.Draw(im)
    for y in range(0, h, s):
        for x in range(0, w, s):
            dd.rectangle([x, y, x + s - 1, y + s - 1], fill=(232, 232, 232) if (x // s + y // s) % 2 else (216, 216, 216))
    return im


for i, (name, path, fr) in enumerate(items):
    im = Image.open(path).convert('RGBA').crop((0, fr * 64, 64, fr * 64 + 64))
    x0 = pad + i * cw
    bg = checker(64 * z, 64 * z, 4 * z)
    big = im.resize((64 * z, 64 * z), Image.NEAREST)
    bg.paste(big, (0, 0), big)
    sheet.paste(bg, (x0, 22))
    d.text((x0, 6), name, fill=(40, 40, 40))
    # 1x op wit en op een GBA-achtig gevechtsveld
    y1 = 22 + 64 * z + 10
    sheet.paste(im, (x0 + 64 * z // 2 - 32, y1), im)
    field = Image.new('RGB', (64, 64), (200, 224, 176))
    field.paste(im, (0, 0), im)
    sheet.paste(field, (x0 + 64 * z // 2 - 32, y1 + 70))
    # silhouet
    sil = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    a = im.split()[3]
    sil.paste((30, 30, 30, 255), (0, 0), a)
    sheet.paste(sil, (x0 + 64 * z // 2 - 32, y1 + 140), sil)
sheet.save(out)
