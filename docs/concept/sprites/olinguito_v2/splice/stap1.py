import numpy as np, sys
from PIL import Image, ImageDraw
P = '/home/user/projectgrounded/graphics/pokemon/'
li = np.array(Image.open(P + 'linoone/anim_front.png'))[:64, :64]
# rol per Linoone-index: vacht licht/basis/schaduw, omlijning, zwart, poot, klauw, oog
ROLE = {1: 'L', 2: 'B', 3: 'B', 4: 'S', 5: 'H', 6: 'L', 7: 'K', 8: 'S', 9: 'E', 10: 'E', 11: 'C', 12: 'PS', 13: 'S'}
PAL = {'.': None, 'K': (16, 16, 16), 'L': (57, 24, 16), 'S': (98, 65, 49), 'B': (139, 90, 65), 'H': (164, 115, 74),
       'g': (184, 192, 192), 'G': (144, 152, 160), 'q': (104, 104, 128), 'Q': (80, 88, 88),
       'E': (104, 24, 40), 'e': (184, 40, 64), 'PB': (205, 140, 140), 'PS': (164, 98, 106), 'C': (230, 222, 205), 'W': (248, 248, 248)}
g = np.full((64, 64), '.', object)
for y in range(64):
    for x in range(64):
        v = li[y, x]
        if v: g[y, x] = ROLE[v]
g[:, 47:] = '.'
# lichte vacht: hooglicht binnen 3 px onder de bovenrand (licht van boven), anders basis; Linoone's schaduw blijft
for x in range(64):
    col = [y for y in range(64) if g[y, x] != '.']
    if not col: continue
    top = col[0]
    for y in col:
        if g[y, x] in ('H', 'B'): g[y, x] = 'H' if y - top <= 3 else 'B'   # pluimstaart weg (wordt een lange dunne olinguitostaart)
k = float(sys.argv[1]) if len(sys.argv) > 1 else 1 / 7
out = np.full((64, 64), '.', object)
for x in range(64):
    dy = int(round((47 - x) * k))
    for y in range(64):
        if g[y, x] != '.' and 0 <= y + dy < 64: out[y + dy, x] = g[y, x]
np.save('/tmp/claude-0/-home-user/85c98b1f-d9df-5017-bb41-e464ac2180c3/scratchpad/spl/stap1.npy', out)
def show(grid, path, z=8):
    im = Image.new('RGB', (64 * z, 64 * z), (152, 208, 160)); d = ImageDraw.Draw(im)
    for y in range(64):
        for x in range(64):
            c = PAL[grid[y, x]]
            if c: d.rectangle([x * z, y * z, x * z + z - 1, y * z + z - 1], fill=c)
    for i in range(0, 64, 8): d.line([(i * z, 0), (i * z, 64 * z)], fill=(120, 170, 130)); d.line([(0, i * z), (64 * z, i * z)], fill=(120, 170, 130))
    im.save(path)
show(out, '/tmp/claude-0/-home-user/85c98b1f-d9df-5017-bb41-e464ac2180c3/scratchpad/spl/stap1.png')
