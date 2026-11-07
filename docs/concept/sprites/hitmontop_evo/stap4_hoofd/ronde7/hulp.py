"""Hulpfuncties ronde 6: rasters als tekst (Hitmontops palet-indices) <-> png, 8x-weergave met coordinaten."""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../../..'))
SRC = Image.open(os.path.join(ROOT, 'graphics/pokemon/hitmontop/anim_front.png'))
PAL = SRC.getpalette()[:48]
COL = {i: tuple(PAL[3*i:3*i+3]) for i in range(16)}
CH = '0123456789abcdef'

def top_idx():
    px = SRC.load()
    return {(x, y): px[x, y] for y in range(64) for x in range(64) if px[x, y]}

def naar_tekst(d):
    xs = [p[0] for p in d]; ys = [p[1] for p in d]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    return x0, y0, '\n'.join(''.join(CH[d[(x, y)]] if (x, y) in d else '.' for x in range(x0, x1+1)) for y in range(y0, y1+1))

def uit_tekst(t, x0=0, y0=0):
    d = {}
    for j, r in enumerate(t.strip('\n').split('\n')):
        for i, c in enumerate(r):
            if c != '.' and c != ' ':
                d[(x0+i, y0+j)] = CH.index(c.lower())
    return d

def beeld(d, w=64, h=64, bg=None):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0) if bg is None else bg + (255,))
    for (x, y), i in d.items():
        if 0 <= x < w and 0 <= y < h:
            im.putpixel((x, y), COL[i] + (255,))
    return im

def raster8(d, pad, titel='', Z=8):
    """8x met rasterlijnen en coordinaten (voor het eigen werk)."""
    xs = [p[0] for p in d]; ys = [p[1] for p in d]
    x0, y0 = min(xs)-1, min(ys)-1; w = max(xs)-x0+2; h = max(ys)-y0+2
    im = Image.new('RGB', (w*Z+30, h*Z+30), (235, 235, 240)); dr = ImageDraw.Draw(im)
    for (x, y), i in d.items():
        dr.rectangle([30+(x-x0)*Z, 30+(y-y0)*Z, 30+(x-x0)*Z+Z-1, 30+(y-y0)*Z+Z-1], fill=COL[i])
    for k in range(w+1):
        dr.line([30+k*Z, 30, 30+k*Z, 30+h*Z], fill=(200, 200, 210))
        if (x0+k) % 2 == 0 and k < w: dr.text((30+k*Z, 2 + 10*((x0+k)//2 % 2)), str(x0+k), fill=(0, 0, 0))
    for k in range(h+1):
        dr.line([30, 30+k*Z, 30+w*Z, 30+k*Z], fill=(200, 200, 210))
        if k < h: dr.text((2, 30+k*Z), str(y0+k), fill=(0, 0, 0))
    im.save(pad)
