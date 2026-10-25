"""Hulp: getaperde buis als masker op 64x64 (8x supersampling)."""
import math
import numpy as np
from PIL import Image, ImageDraw
SS, BOX = 8, 64


def tube_mask(pts, w0, w1):
    im = Image.new('L', (BOX * SS, BOX * SS), 0); d = ImageDraw.Draw(im)
    (ax, ay), (bx, by) = pts[0], pts[-1]
    n = max(2, int(math.hypot(bx - ax, by - ay) / 0.2))
    for i in range(n + 1):
        t = i / n; x, y = ax + (bx - ax) * t, ay + (by - ay) * t; r = (w0 + (w1 - w0) * t) / 2 * SS
        d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], fill=255)
    return np.array(im.resize((BOX, BOX), Image.BOX)) > 110
