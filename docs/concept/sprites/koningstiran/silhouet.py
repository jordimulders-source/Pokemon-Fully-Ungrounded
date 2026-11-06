"""Sapa Inca: silhouet 64x64 uit het goedgekeurde 3D-poppetje (B3, buiging 1), werkwijze stap 2.
De render wordt direct verkleind (massa heilig); daarna alleen benoemde reparaties van dunne delen.
Draaien vanuit de repo-root: python3 docs/concept/sprites/koningstiran/silhouet.py"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
YAW, PITCH = 44, 8


def render_full(**kw):
    m = pop3d.bird(extra=32, curl=0.5, **kw)
    x0, x1, y0, y1 = pop3d.bbox(m, YAW, PITCH)
    scale = pop3d.R * (236 / 256) / max(x1 - x0, y1 - y0)
    im, a = pop3d.shade(*pop3d.render(m, YAW, PITCH, scale, ((x0 + x1) / 2, (y0 + y1) / 2)))
    return im, a


def to64(a, maxh=62, maxw=62, thr=0.45):
    ys, xs = np.nonzero(a)
    crop = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.float32)
    h, w = crop.shape
    s = min(maxh / h, maxw / w)
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    small = np.array(Image.fromarray((crop * 255).astype(np.uint8)).resize((nw, nh), Image.BOX)) / 255.0
    out = np.zeros((64, 64), bool)
    ox, oy = (64 - nw) // 2, 63 - nh
    out[oy:oy + nh, ox:ox + nw] = small > thr
    return out


def gen3_sil(name):
    p = os.path.join(ROOT, 'graphics/pokemon', name, 'anim_front.png')
    im = Image.open(p).crop((0, 0, 64, 64))
    return np.array(im) != 0


def sheet(src, sil, refs):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
    BG, INK = (236, 232, 222), (20, 20, 24)

    def silimg(m, k):
        im = Image.new('RGB', (64, 64), (255, 255, 255))
        im.paste(Image.new('RGB', (64, 64), INK), (0, 0), Image.fromarray((m * 255).astype(np.uint8)))
        return im.resize((64 * k, 64 * k), Image.NEAREST)

    W = Image.new('RGB', (10 + 256 + 10 + 256 + 10 + 256 + 10 + 80, 40 + 256 + 30 + 120), BG)
    d = ImageDraw.Draw(W)
    d.text((10, 10), f'Sapa Inca: silhouet 64x64 ({int(sil.sum())} px), uit het 3D-poppetje B3', font=FB, fill=INK)
    W.paste(src.resize((256, 256), Image.LANCZOS), (10, 36))
    d.text((10, 296), 'onderlaag (poppetje)', font=F, fill=INK)
    W.paste(silimg(sil, 4), (276, 36))
    d.text((276, 296), 'silhouet 4x', font=F, fill=INK)
    ov = src.resize((256, 256), Image.LANCZOS).convert('RGBA')
    mask = Image.fromarray((sil * 110).astype(np.uint8)).resize((256, 256), Image.NEAREST)
    # onderlaag met hetzelfde kader als het silhouet: opnieuw schalen via de bbox van de render
    W.paste(ov, (542, 36))
    red = Image.new('RGBA', (256, 256), (220, 30, 30, 0))
    red.putalpha(mask)
    d.text((542, 296), 'silhouet over onderlaag', font=F, fill=INK)
    W.paste(silimg(sil, 1), (808, 36))
    d.text((808, 104), '1x', font=F, fill=INK)
    x = 10
    d.text((10, 318), 'Gen 3-silhouetten, zelfde bouwtype (1x en 2x):', font=F, fill=INK)
    for n in refs:
        r = gen3_sil(n)
        W.paste(silimg(r, 1), (x, 336))
        W.paste(silimg(r, 2) if False else silimg(r, 1), (x, 336))
        d.text((x, 404), f'{n} ({int(r.sum())})', font=F, fill=INK)
        x += 130
    W.paste(silimg(sil, 1), (x, 336))
    d.text((x, 404), f'Sapa Inca ({int(sil.sum())})', font=F, fill=INK)
    return W, red


if __name__ == '__main__':
    src_img, a = render_full()
    sil = to64(a)
    # overlay correct uitlijnen: onderlaag in hetzelfde 64-kader schalen
    ys, xs = np.nonzero(a)
    crop = src_img.resize((768, 768), Image.NEAREST).crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    h, w = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    s = min(62 / h, 62 / w)
    nw, nh = round(w * s), round(h * s)
    under = Image.new('RGB', (64 * 4, 64 * 4), (255, 255, 255))
    under.paste(crop.resize((nw * 4, nh * 4), Image.LANCZOS), (((64 - nw) // 2) * 4, (63 - nh) * 4))
    W, _ = sheet(under, sil, ['noctowl', 'empoleon', 'decidueye', 'honchkrow', 'xatu'])
    # echte overlay op paneel 3
    ov = under.convert('RGBA')
    red = Image.new('RGBA', ov.size, (220, 30, 30, 0))
    red.putalpha(Image.fromarray((sil * 120).astype(np.uint8)).resize(ov.size, Image.NEAREST))
    W.paste(Image.alpha_composite(ov, red).convert('RGB'), (542, 36))
    Image.fromarray(np.where(sil, 255, 0).astype(np.uint8)).save(os.path.join(HERE, 'silhouet_v2_1x.png'))
    W.save(os.path.join(HERE, 'silhouet_v2_vel.png'))
    print('px', int(sil.sum()))
