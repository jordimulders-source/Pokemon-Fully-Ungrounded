"""Snelle proef (SPRITE_PLAN §5/§6): vacht albino en zwart, accent zilver; blijven de lijnen staan?
python3 varianttest.py <anim_front.png> <uit.png>"""
import sys
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from PIL import Image
from shapepaint import hexc, to_rgba
im = Image.open(sys.argv[1]); a = np.array(im)
p = im.getpalette()[:48]; base = [tuple(p[3 * i:3 * i + 3]) for i in range(16)]
V = {
    'normaal': {},
    'albino vacht': {1: '#FFFFF8', 2: '#E6DED6', 3: '#B4A8A4', 4: '#6E6260'},
    'zwarte vacht': {1: '#6A6470', 2: '#46404C', 3: '#302A36', 4: '#1E1A24'},
    'zilver accent': {9: '#FFFFFF', 10: '#C8D0DC', 11: '#7A8494', 12: '#B83A3A', 13: '#7A2228'},
}
z = 3; tiles = []
for n, ch in V.items():
    pal = [hexc(ch[i]) if i in ch else base[i] for i in range(16)]
    t = Image.new('RGB', (128 * z, 64 * z), (210, 222, 210))
    for k in range(2):
        t.paste(to_rgba(a[64 * k:64 * (k + 1)], pal, z, (210, 222, 210, 255)).convert('RGB'), (64 * z * k, 0))
    tiles.append(t)
out = Image.new('RGB', (128 * z, 64 * z * len(tiles)), 'white')
for i, t in enumerate(tiles):
    out.paste(t, (0, 64 * z * i))
out.save(sys.argv[2]); print(sys.argv[2])
