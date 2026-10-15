#!/usr/bin/env python3
"""Kleurgroepen ("ramps") per sprite: welke paletindexen samen één onderdeel vormen
(lijf, buik, vlam, ogen, ...), herkend uit tint en uit welke kleuren in de sprite naast
elkaar liggen. Gebruik: python3 ramps.py <map> [uit.png]  -> tabel + indexkaart."""
import colorsys
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from variants import ROOT, read_pal  # noqa: E402


def load(folder, picname='anim_front.png'):
    im = Image.open(os.path.join(folder, picname))
    return im, list(im.get_flattened_data()) if hasattr(im, "get_flattened_data") else list(im.getdata()), im.size


def stats(folder):
    """Pixeltelling per index en buurparen (front + back)."""
    count = [0] * 16
    adj = {}
    for pic in ('anim_front.png', 'back.png'):
        p = os.path.join(folder, pic)
        if not os.path.exists(p):
            continue
        im, data, (w, h) = load(folder, pic)
        for y in range(h):
            for x in range(w):
                a = data[y * w + x] & 15
                count[a] += 1
                for dx, dy in ((1, 0), (0, 1)):
                    if x + dx < w and y + dy < h:
                        b = data[(y + dy) * w + x + dx] & 15
                        if a != b:
                            k = (min(a, b), max(a, b))
                            adj[k] = adj.get(k, 0) + 1
    return count, adj


def hls(c):
    return colorsys.rgb_to_hls(*(v / 255 for v in c))


def describe(folder):
    pal = read_pal(os.path.join(folder, 'normal.pal'))[:16]
    count, adj = stats(folder)
    rows = []
    for i in range(1, 16):
        if not count[i]:
            continue
        h, l, s = hls(pal[i])
        nb = sorted(((n, (k[0] if k[1] == i else k[1])) for k, n in adj.items() if i in k), reverse=True)[:4]
        rows.append((i, pal[i], count[i], round(h * 360), round(l, 2), round(s, 2), nb))
    return pal, rows


def index_map(folder, out):
    """Sprite 4x, met per pixel het indexnummer erop (alleen voor kijken)."""
    im, data, (w, h) = load(folder)
    pal = read_pal(os.path.join(folder, 'normal.pal'))[:16]
    S = 12
    img = Image.new('RGB', (64 * S + 260, 64 * S), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for y in range(64):
        for x in range(64):
            i = data[y * w + x] & 15
            if i == 0:
                continue
            c = pal[i]
            d.rectangle([x * S, y * S, x * S + S - 1, y * S + S - 1], fill=c)
            l = hls(c)[1]
            d.text((x * S + 2, y * S), '%x' % i, fill=(255, 255, 255) if l < 0.5 else (0, 0, 0))
    for i in range(16):
        d.rectangle([64 * S + 10, i * 40 + 5, 64 * S + 50, i * 40 + 35], fill=pal[i], outline=(0, 0, 0))
        d.text((64 * S + 60, i * 40 + 12), '%x  %s' % (i, pal[i]), fill=(0, 0, 0))
    img.save(out)


if __name__ == '__main__':
    folder = os.path.join(ROOT, 'graphics/pokemon', sys.argv[1])
    pal, rows = describe(folder)
    for r in rows:
        print('%2d %-15s n=%4d h=%3d l=%.2f s=%.2f buren=%s' % r[:6] + (r[6],) if False else
              '%2d %-15s n=%4d h=%3d l=%.2f s=%.2f buren=%s' % (r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
    if len(sys.argv) > 2:
        index_map(folder, sys.argv[2])
