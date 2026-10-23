"""Vergelijkingsvellen: kandidaten naast echte sprites op 1x en 3x."""
import sys, os
from PIL import Image, ImageDraw

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../..'))
S = REPO + '/docs/concept/sprites/'
G = REPO + '/graphics/pokemon/'
BG = (232, 236, 240)


def load(path, frame=0, pal=None):
    im = Image.open(path)
    pal_img = im
    if pal is None and os.path.exists(os.path.join(os.path.dirname(path), 'normal.pal')):
        pal = os.path.join(os.path.dirname(path), 'normal.pal')
    if path.endswith('_gba.png'):
        p2 = path.replace('anim_front_gba.png', 'normal_gba.pal')
        if os.path.exists(p2):
            pal = p2
    im = im.crop((0, frame * 64, 64, frame * 64 + 64))
    idx = list(im.getdata())
    if pal:
        lines = open(pal).read().split('\n')[3:]
        cols = [tuple(int(v) for v in l.split()) for l in lines if l.strip()]
    else:
        p = pal_img.getpalette()
        cols = [tuple(p[i*3:i*3+3]) for i in range(16)]
    out = Image.new('RGBA', (64, 64))
    out.putdata([(0, 0, 0, 0) if i == 0 else cols[i] + (255,) for i in idx])
    return out


def sheet(items, out, title_rows=None, scale=3):
    """items: list of rows; each row list of (label, path, frame)."""
    cw = 64 * scale + 64 + 12
    ch = 64 * scale + 18
    rows = len(items)
    cols = max(len(r) for r in items)
    W = cols * cw + 10
    H = rows * ch + 10
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    for r, row in enumerate(items):
        for c, it in enumerate(row):
            if it is None:
                continue
            label, path, frame = it
            sp = load(path, frame)
            x = 5 + c * cw
            y = 5 + r * ch
            big = sp.resize((64 * scale, 64 * scale), Image.NEAREST)
            img.paste(big, (x, y + 14), big)
            img.paste(sp, (x + 64 * scale + 4, y + 14 + 64 * scale - 64), sp)
            d.text((x, y + 1), label, fill=(20, 20, 20))
    img.save(out)
    print(out, img.size)


def bbox(path, frame=0):
    sp = load(path, frame)
    return sp.getbbox()


if __name__ == '__main__':
    pass
