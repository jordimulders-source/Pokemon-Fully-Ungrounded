#!/usr/bin/env python3
"""Project Grounded: titelbanner "UNGROUNDED" in de stijl van "EMERALD VERSION" (graphics/title_screen/emerald_version.png).
Zelfde 16-kleuren grijspalet (het groen komt uit emerald_version.gbapal): witte letters die naar onder grijzer worden, een
binnenrand, een dikke zwarte omlijning en een donkere 3D-rand rechtsonder; licht gekanteld zoals het origineel.
  python3 tools/grounded/title_banner.py [--preview uit.png]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = R + '/graphics/title_screen/emerald_version.png'
FONT = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
TEXT = 'UNGROUNDED'
W, H = 128, 32
S = 8                       # oversampling
ANGLE = 4.0                 # graden, stijgt naar rechts zoals EMERALD
BOX = (3, 5, 124, 25)       # doelvak van de letters (x0, y0, x1, y1), omlijning valt erbuiten
TRACK = -0.02               # letterafstand (fractie van de letterhoogte)

def render():
    font = ImageFont.truetype(FONT, 40 * S)
    # letters één voor één, met kleinere tussenruimte
    widths = [font.getbbox(c)[2] - font.getbbox(c)[0] for c in TEXT]
    asc = font.getbbox('H')
    h = asc[3] - asc[1]
    gap = int(TRACK * h)
    tw = sum(widths) + gap * (len(TEXT) - 1)
    big = Image.new('L', (tw + 40 * S, h + 40 * S), 0)
    d = ImageDraw.Draw(big)
    x = 20 * S
    for c, w in zip(TEXT, widths):
        bb = font.getbbox(c)
        d.text((x - bb[0], 20 * S - asc[1]), c, font=font, fill=255)
        x += w + gap
    big = big.rotate(ANGLE, resample=Image.BICUBIC, expand=True)
    bb = big.getbbox()
    big = big.crop(bb)
    bw, bh = BOX[2] - BOX[0], BOX[3] - BOX[1]
    small = big.resize((bw, bh), Image.LANCZOS)
    a = np.zeros((H, W), float)
    a[BOX[1]:BOX[3], BOX[0]:BOX[2]] = np.asarray(small, float) / 255
    return a

def dilate(m, r):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r + 1:
                out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out

def build():
    a = render()
    fill = a >= 0.45
    edge = (a > 0.12) & ~fill                     # AA-rand: wordt binnenrand
    outline = dilate(fill | edge, 2) & ~fill & ~edge
    depth = (np.roll(np.roll(outline | fill | edge, 1, 0), 1, 1) | np.roll(outline | fill | edge, 2, 0)) & ~(outline | fill | edge)
    idx = np.zeros((H, W), np.uint8)              # 0 = transparant (magenta)
    # verticale verloop per kolom: bovenkant van de letter wit, naar onder grijzer
    ys = np.arange(H)[:, None].repeat(W, 1)
    top = np.where(fill.any(0), fill.argmax(0), 0)[None, :]
    bot = np.where(fill.any(0), H - 1 - fill[::-1].argmax(0), 0)[None, :]
    t = np.clip((ys - top) / np.maximum(bot - top, 1), 0, 1)
    # grijswaarden van licht naar donker (indices in het palet van het origineel)
    ramp = [15, 15, 15, 15, 6, 6, 3, 12, 10]          # vooral wit, onderaan grijzer (ff ee de cd bd)
    lvl = np.minimum((t * len(ramp)).astype(int), len(ramp) - 1)
    for i, c in enumerate(ramp):
        idx[fill & (lvl == i)] = c
    # binnenrand: lichte schaduw rechtsonder in de letter, AA-rand in middengrijs
    inner = fill & ~np.roll(np.roll(fill, -1, 0), -1, 1)
    idx[inner] = 11                                   # 8b
    idx[edge] = np.where(a[edge] > 0.3, 1, 9)         # 9c / 6a
    idx[outline] = 4                                  # zwart
    idx[depth] = 14                                   # donkere 3D-rand
    return idx

def main():
    src = Image.open(SRC)
    idx = build()
    out = Image.fromarray(idx, 'P')
    out.putpalette(src.getpalette())
    if '--preview' in sys.argv:
        p = sys.argv[sys.argv.index('--preview') + 1]
        pal = open(R + '/graphics/title_screen/emerald_version.gbapal', 'rb').read()
        cols = []
        for i in range(16):
            v = pal[2 * i] | pal[2 * i + 1] << 8
            cols += [(v & 31) * 8, (v >> 5 & 31) * 8, (v >> 10 & 31) * 8]
        g = out.copy(); g.putpalette(cols + [0] * (768 - len(cols)))
        o = Image.fromarray(np.asarray(src), 'P'); o.putpalette(cols + [0] * (768 - len(cols)))
        sheet = Image.new('RGB', (W * 6, H * 12 + 12), (40, 40, 60))
        sheet.paste(o.convert('RGB').resize((W * 6, H * 6), Image.NEAREST), (0, 0))
        sheet.paste(g.convert('RGB').resize((W * 6, H * 6), Image.NEAREST), (0, H * 6 + 12))
        sheet.save(p)
    else:
        out.save(SRC)
        print('geschreven:', SRC)

main()
