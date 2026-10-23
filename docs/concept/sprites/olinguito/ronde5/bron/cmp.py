"""Vergelijkingsvel ronde 5: ronde 4 en 5 naast Gen 3-sprites (GBA-originelen).
Rij 1: 3x; rij 2: 1x; rij 3: silhouet 2x; rij 4: silhouet 1x.
python3 cmp.py <ronde5/anim_front.png> <ronde4/anim_front.png> <uit.png>"""
import sys
sys.path.insert(0, '/home/user/projectgrounded/.claude/worktrees/agent-af3d51a344c743349/tools/concept/sprites')
import numpy as np
from PIL import Image, ImageDraw
import spritelib as L

r5, r4, out = sys.argv[1:4]


def own(path, k):
    a, pal = L.load_png(path)
    return L.rgb_img(a[64 * k:64 * (k + 1)], pal)


def mon(sp):
    fr, pal = L.load_front(sp, 'gba')
    return L.rgb_img(fr[0], pal)


cols = [('ronde 4', own(r4, 0)), ('ronde 5 f1', own(r5, 0)), ('ronde 5 f2', own(r5, 1))]
for sp in ['treecko', 'torchic', 'mudkip', 'cyndaquil', 'totodile', 'teddiursa', 'zigzagoon', 'poochyena', 'sneasel', 'meowth']:
    cols.append((sp, mon(sp)))


def sil(im):
    a = np.array(im); a[a[..., 3] > 0, :3] = (24, 24, 24); return Image.fromarray(a)


z = 3; S = 64 * z; G = 6
W = len(cols) * (S + G) + G
H = 14 + S + 14 + 64 + 14 + 128 + 14 + 64 + 20
sheet = Image.new('RGB', (W, H), (244, 242, 236)); d = ImageDraw.Draw(sheet)
y = 2
for i, (n, im) in enumerate(cols):
    x = G + i * (S + G)
    d.text((x, y), n, fill=(150, 20, 20) if n.startswith('ronde 5') else (0, 0, 0))
    bg = L.checker_bg(S, S, 4 * z); bg.alpha_composite(L.scaled(im, z)); sheet.paste(bg.convert('RGB'), (x, y + 12))
y += 12 + S + 4
d.text((G, y), 'op 1x (zoals in de game)', fill=(0, 0, 0)); y += 12
for i, (n, im) in enumerate(cols):
    b = Image.new('RGBA', (64, 64), (248, 248, 248, 255)); b.alpha_composite(im)
    sheet.paste(b.convert('RGB'), (G + i * 70, y))
y += 64 + 4
d.text((G, y), 'silhouettest (2x en 1x)', fill=(0, 0, 0)); y += 12
for i, (n, im) in enumerate(cols):
    b = Image.new('RGBA', (64, 64), (248, 248, 248, 255)); b.alpha_composite(sil(im))
    sheet.paste(b.convert('RGB').resize((128, 128), Image.NEAREST), (G + i * 134, y))
y += 128 + 4
for i, (n, im) in enumerate(cols):
    b = Image.new('RGBA', (64, 64), (248, 248, 248, 255)); b.alpha_composite(sil(im))
    sheet.paste(b.convert('RGB'), (G + i * 70, y))
sheet.save(out); print(out, sheet.size)
