"""grid.py uit.png zoom cols titel :: groep1naam: sp sp sp :: groep2naam: ...
sp mag naam=pad.png (frame 1) zijn. GBA-sprite als die bestaat, anders nieuwe."""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import spritelib as L
from PIL import Image, ImageDraw
out, z, cols, title = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
groups = []
for g in ' '.join(sys.argv[5:]).split('::'):
    if ':' not in g: continue
    n, s = g.split(':', 1); groups.append((n.strip(), s.split()))
S = 64 * z; LH = 12
def img(sp):
    if '=' in sp:
        n, p = sp.split('=', 1); a, pal = L.load_png(p); return n, L.rgb_img(a[:64], pal)
    for w in ('gba', 'new'):
        try:
            fr, pal = L.load_front(sp, w); return sp, L.rgb_img(fr[0], pal)
        except Exception: pass
    return sp, None
rows = sum((len(s) + cols - 1) // cols for _, s in groups)
H = 18 + len(groups) * 14 + rows * (S + LH + 2)
sheet = Image.new('RGB', (cols * (S + 2) + 4, H), (236, 234, 226)); d = ImageDraw.Draw(sheet)
d.text((4, 4), title, fill=(0, 0, 0)); y = 18
for gn, sps in groups:
    d.text((4, y), gn, fill=(120, 20, 20)); y += 14
    for i, sp in enumerate(sps):
        if i and i % cols == 0: y += S + LH + 2
        x = 2 + (i % cols) * (S + 2)
        n, im = img(sp)
        bg = Image.new('RGBA', (S, S), (250, 249, 244, 255))
        if im is not None:
            if gn.startswith('Silhouet'):
                import numpy as np
                a=np.array(im); a[a[...,3]>0,:3]=(30,30,30); im=Image.fromarray(a)
            bg.alpha_composite(L.scaled(im, z))
        sheet.paste(bg.convert('RGB'), (x, y + LH)); d.text((x + 2, y), n[:14], fill=(0, 0, 0))
    y += S + LH + 2
sheet.save(out); print(out, sheet.size)
