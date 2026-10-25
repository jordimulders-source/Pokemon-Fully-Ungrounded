"""Leest de zwarte omlijning van de onderlaag (256 = 4x) af in de voorpootzone en legt die verkleind over de sprite
(20x), als controle. Ook een lijst per spriterij: x-posities van de omlijning (in spritepixels)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '../../../silhouet')
u = np.array(Image.open(os.path.join(S, 'onderlaag_b1c_256.png')).convert('RGB')).astype(int)
lum = u[..., 0] * .3 + u[..., 1] * .59 + u[..., 2] * .11
X0, Y0, X1, Y1 = 17, 44, 36, 61   # zone in spritepixels
lijn = (lum < 30)
sprite = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, '../coathief.png')
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(H, '../onderlaaglijn_over_6e.png')
Z = 20
im = Image.open(sprite).convert('RGBA').crop((X0, Y0, X1, Y1)).resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.NEAREST)
bg = Image.new('RGBA', im.size, (236, 236, 230, 255)); bg.alpha_composite(im); d = ImageDraw.Draw(bg)
for py in range(Y0 * 4, Y1 * 4):
    for px in range(X0 * 4, X1 * 4):
        if lijn[py, px]:
            sx = (px + .5) / 4 - X0; sy = (py + .5) / 4 - Y0
            d.ellipse([sx * Z - 2, sy * Z - 2, sx * Z + 2, sy * Z + 2], fill=(0, 200, 255, 255))
for x in range(X1 - X0 + 1): d.line([(x * Z, 0), (x * Z, bg.height)], fill=(255, 255, 255, 60))
for y in range(Y1 - Y0 + 1): d.line([(0, y * Z), (bg.width, y * Z)], fill=(255, 255, 255, 60))
bg.save(out)
