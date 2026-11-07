"""Vel voor Jordi: onderlaag | silhouet 4x | silhouet over de onderlaag | 1x, naast echte Gen 3-silhouetten.
Draaien: python3 docs/concept/sprites/coathief/silhouet/vel.py <silhouet.txt|direct> <uit.png> [fill]"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
REFS = ("linoone", "mightyena", "liepard", "furret", "houndoom")
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
INK = (40, 32, 44, 255)


def gen3(p):
    for f in ('anim_front_gba.png', 'anim_front.png', 'front.png'):
        fp = os.path.join(ROOT, 'graphics/pokemon', p, f)
        if os.path.exists(fp):
            im = Image.open(fp)
            a = np.array(im)[:64] != 0
            return a
    raise FileNotFoundError(p)


def img(mask, big=1):
    a = np.zeros(mask.shape + (4,), np.uint8); a[mask] = INK
    return Image.fromarray(a).resize((64 * big, 64 * big), Image.NEAREST)


def load_txt(fp):
    return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(fp) if l.strip()])


def sheet(sil, under, out, title):
    W = Image.new("RGBA", (6 * 200 + 10, 300 + 190), (236, 236, 230, 255)); d = ImageDraw.Draw(W)
    d.text((8, 4), title, fill='black', font=F)
    W.paste(under, (5, 22))
    W.alpha_composite(img(sil, 4), (271, 22))
    ov = under.convert('RGBA').copy(); s = img(sil, 4); s.putalpha(Image.fromarray((np.array(s)[..., 3] * 0.55).astype(np.uint8)))
    ov.alpha_composite(s); W.paste(ov, (537, 22))
    W.alpha_composite(img(sil), (803 + 20, 22)); W.alpha_composite(img(sil), (803 + 100, 22))
    for x, t in ((5, 'onderlaag: B1, kop C'), (271, 'silhouet 4x'), (537, 'silhouet over de onderlaag'), (823, '1x  (%d px)' % sil.sum())):
        d.text((x, 282), t, fill='black', font=F)
    for i, p in enumerate(REFS):
        a = gen3(p); x = 5 + 200 * i
        W.alpha_composite(img(a, 2), (x, 300)); W.alpha_composite(img(a), (x + 130, 300 + 64))
        d.text((x, 300 + 130), '%s (%d px)' % (p, a.sum()), fill='black', font=F)
    W.alpha_composite(img(sil, 2), (5 + 200 * 5, 300)); d.text((5 + 1000, 430), 'Coathief', fill='black', font=F)
    W.convert('RGB').save(out)


if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    import silhouet_direct as S
    fill = float(sys.argv[3]) if len(sys.argv) > 3 else 0.98
    d, under = S.direct(fill)
    sil = d if src == 'direct' else load_txt(src)
    sheet(sil, under, out, 'Coathief silhouet (%s)' % os.path.basename(src))
