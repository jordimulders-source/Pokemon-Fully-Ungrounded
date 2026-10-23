"""compare_sheet.py uit.png --own naam=pad.png[,naam=pad.png] --ref soort[:gba|new],...

Vergelijkingsvel: eigen sprites (f1 en f2) en referentiesprites (f1, f2) op 3x,
daaronder alles op 1x (zoals in de game). Referenties: ':gba' = originele GBA-sprite
(Gen 1-3), ':new' = wat de game nu toont (DPPt-stijl), standaard gba als die er is.
Ook gebruikt door dj_rotom/ronde1."""
import sys, os
from PIL import Image, ImageDraw
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(W, 'tools', 'concept', 'sprites'))
import spritelib as L

a = sys.argv[1:]
out = a.pop(0)
own, ref, z = [], [], 3
while a:
    k = a.pop(0)
    if k == '--own':
        own = [s.split('=', 1) for s in a.pop(0).split(',')]
    elif k == '--ref':
        ref = a.pop(0).split(',')
    elif k == '--zoom':
        z = int(a.pop(0))

cells = []   # (label, [f1, f2])
for name, path in own:
    arr, pal = L.load_png(path)
    fr = [arr[k * 64:(k + 1) * 64] for k in range(arr.shape[0] // 64)]
    cells.append((name, [L.rgb_img(f, pal) for f in fr[:2]]))
for r in ref:
    sp, _, which = r.partition(':')
    which = which or ('gba' if L.front_path(sp, 'gba') else 'new')
    fr, pal = L.load_front(sp, which)
    lab = sp.replace('/', '-') + (' (GBA)' if which == 'gba' else '')
    cells.append((lab, [L.rgb_img(f, pal) for f in fr[:2]]))

S = 64 * z
cw = 2 * S + 6
cols = 4
rows = (len(cells) + cols - 1) // cols
H = rows * (S + 18) + 64 + 40
sheet = Image.new('RGB', (cols * (cw + 8), H), 'white')
dr = ImageDraw.Draw(sheet)


def tile(im, zz):
    bg = L.checker_bg(64 * zz, 64 * zz, 4 * zz)
    if im is not None:
        bg.alpha_composite(L.scaled(im, zz))
    return bg


for i, (lab, frs) in enumerate(cells):
    x0 = (i % cols) * (cw + 8); y0 = (i // cols) * (S + 18)
    dr.text((x0 + 2, y0), lab + '  (f1 | f2)', fill='black')
    for j, im in enumerate(frs):
        sheet.paste(tile(im, z), (x0 + j * (S + 6), y0 + 12))
y = rows * (S + 18) + 22
dr.text((2, y - 14), '1x (echte grootte), frame 1:', fill='black')
x = 2
for lab, frs in cells:
    sheet.paste(tile(frs[0], 1), (x, y)); x += 68
sheet.save(out)
print(out)
