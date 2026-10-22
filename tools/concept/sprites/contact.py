"""Contactvel van sprites, op schaal, op een lichte achtergrond.

  python3 tools/concept/sprites/contact.py uit.png [opties] soort1 soort2 ...
  opties: --zoom N (standaard 3), --cols 'gf1,gf2,gb,nf1,nf2,nb'
          kolommen: gf1/gf2 = GBA front frame 1/2, gb = GBA back,
                    nf1/nf2/nb = idem van de huidige (DPPt/HGSS-)sprites,
                    gi/ni = icoon (frame 1), en een pad naar een eigen PNG
                    (64x64 of 64x128) via soort=pad/naar/bestand.png
          --grid  : 8x8-raster (tegels) eroverheen
Een rij per soort; een soort 'x=pad.png' laadt een eigen sprite (fakemon in
wording) zodat je hem naast echte Hoenn-sprites op dezelfde schaal ziet.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import spritelib as L


def cell(sp, col):
    if '=' in sp:
        name, path = sp.split('=', 1)
        a, pal = L.load_png(path)
        fr = [a[k * 64:(k + 1) * 64] for k in range(a.shape[0] // 64)]
        if col.endswith('f1'): return L.rgb_img(fr[0], pal)
        if col.endswith('f2'): return L.rgb_img(fr[min(1, len(fr) - 1)], pal)
        return None
    which = 'gba' if col[0] == 'g' else 'new'
    try:
        if col[1:] in ('f1', 'f2'):
            fr, pal = L.load_front(sp, which)
            k = 0 if col[1:] == 'f1' else min(1, len(fr) - 1)
            return L.rgb_img(fr[k], pal)
        if col[1:] == 'b':
            a, pal = L.load_back(sp, which)
            return L.rgb_img(a, pal)
        if col[1:] == 'i':
            a, _ = L.load_icon(sp, which)
            im = Image.fromarray(a[:32], 'RGBA')
            c = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); c.paste(im, (16, 32))
            return c
    except Exception:
        return None


def main():
    args = sys.argv[1:]
    out = args.pop(0)
    zoom, cols, grid = 3, 'gf1,gf2,gb,nf1,nf2,nb'.split(','), False
    sp = []
    while args:
        a = args.pop(0)
        if a == '--zoom': zoom = int(args.pop(0))
        elif a == '--cols': cols = args.pop(0).split(',')
        elif a == '--grid': grid = True
        else: sp.append(a)
    S = 64 * zoom; lab = 70
    sheet = Image.new('RGBA', (lab + len(cols) * (S + 4), 14 + len(sp) * (S + 4)), (255, 255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for j, c in enumerate(cols):
        d.text((lab + j * (S + 4) + 2, 2), c, fill=(0, 0, 0))
    for i, s in enumerate(sp):
        y = 14 + i * (S + 4)
        d.text((2, y + 2), s.split('=')[0][:11], fill=(0, 0, 0))
        for j, c in enumerate(cols):
            x = lab + j * (S + 4)
            bg = L.checker_bg(S, S, 4 * zoom)
            im = cell(s, c)
            if im is not None:
                bg.alpha_composite(L.scaled(im, zoom))
            if grid:
                g = ImageDraw.Draw(bg)
                for k in range(0, S, 8 * zoom):
                    g.line([(k, 0), (k, S)], fill=(150, 150, 255, 255))
                    g.line([(0, k), (S, k)], fill=(150, 150, 255, 255))
            sheet.paste(bg, (x, y))
    sheet.convert('RGB').save(out)
    print(out, sheet.size)


if __name__ == '__main__':
    main()
