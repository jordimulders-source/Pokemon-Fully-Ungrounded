import numpy as np, sys
from PIL import Image
sys.path.insert(0, sys.argv[1]); S = sys.argv[1]
from common import PAL, show
P = '/home/user/projectgrounded/graphics/pokemon/'
sil = np.array(Image.open(S + '/sil5.png').convert('RGBA'))[..., 3] > 0
zz = np.array(Image.open(P + 'zigzagoon/anim_front.png'))[:64, :64]
# Zigzagoon-index -> rol op de olinguitokop (warm grijsbruin, zwart masker, donkerrood oog)
ZR = {1: 'Q', 2: 'K', 3: 'g', 4: 'g', 5: 'G', 6: 'q', 7: 'Q', 8: 'K', 9: 'W', 10: 'Q', 11: 'E', 12: 'K', 13: 'g', 15: 'g'}
DX, DY = int(sys.argv[2]), int(sys.argv[3])
g = np.full((64, 64), '.', object)
HEAD = np.zeros((64, 64), bool)
for y in range(64):
    for x in range(64):
        if sil[y, x] and x <= 30 and y <= 41: HEAD[y, x] = True
for y in range(64):
    for x in range(64):
        if not HEAD[y, x]: continue
        sx, sy = x - DX, y - DY
        v = zz[sy, sx] if 0 <= sx < 64 and 0 <= sy < 64 and sx <= 31 else 0
        g[y, x] = ZR.get(v, 'G') if v else 'G'
# rest van het silhouet voorlopig vlak lijf
for y in range(64):
    for x in range(64):
        if sil[y, x] and not HEAD[y, x]: g[y, x] = 'B'
# omtrek: licht van linksboven -> omlijningsbasis, anders zwart
for y in range(64):
    for x in range(64):
        if not sil[y, x]: continue
        out = [(dx, dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if not (0 <= x + dx < 64 and 0 <= y + dy < 64) or not sil[y + dy, x + dx]]
        if out:
            lit = any(dx < 0 or dy < 0 for dx, dy in out)
            dark = any(dx > 0 or dy > 0 for dx, dy in out)
            head = HEAD[y, x]
            g[y, x] = ('Q' if head else 'L') if lit and not dark else 'K'
np.save(S + '/sp1.npy', g); show(g, S + '/sp1.png'); show(g, S + '/sp1_1x.png', 1)
