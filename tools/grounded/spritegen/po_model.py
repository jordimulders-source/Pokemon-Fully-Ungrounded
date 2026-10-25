"""3D-poppetje -> 2D-tekening -> pixel-over (Dragonfly Cave-methode). Gebruik: po_model.py <model> <breedte> uitmap"""
import importlib, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'models'))
from art_from_model import model_art
from pixelover import pixelover

mod = importlib.import_module(sys.argv[1])
target = int(sys.argv[2]); outdir = sys.argv[3]
os.makedirs(outdir, exist_ok=True)
spec = mod.SPEC
m = mod.build()
art, fig, line, mat, tone, names, info = model_art(m, spec, 512)
Image.fromarray(art).save(os.path.join(outdir, f'{sys.argv[1]}_tekening.png'))
ys, xs = np.nonzero(fig)
crop = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
out, inf = pixelover(art[crop], fig[crop], line[crop], mat[crop], tone[crop], target, int(sys.argv[4]) if len(sys.argv) > 4 else 60, dict(materials=names, style=spec.get('po_style', {})))
h, w = out.shape
# details (sjablonen) op de juiste plek: punt -> tekening -> sprite
f = inf['f']
for t in spec.get('templates', []):
    name, rows, colors = t[:3]
    if name.startswith('klauw'):
        continue
    anchor = t[3] if len(t) > 3 else (len(rows[0]) / 2, len(rows) / 2)
    if name not in m.points:
        continue
    p = info['Rc'] @ np.array(m.points[name], float)
    ax = (p[0] - info['origin'][0]) * info['scale'] - xs.min()
    ay = (info['origin'][1] - p[1]) * info['scale'] - ys.min()
    X0, Y0 = int(round(ax / f - anchor[0])), int(round(ay / f - anchor[1]))
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != '.' and 0 <= Y0 + j < h and 0 <= X0 + i < w:
                out[Y0 + j, X0 + i] = colors[ch]
pal = spec['palette']
canvas = np.zeros((64, 64, 4), np.uint8)
oy, ox = 64 - h - spec.get('bottom', 2), (64 - w) // 2
for y in range(h):
    for x in range(w):
        if out[y, x] and 0 <= oy + y < 64:
            canvas[oy + y, ox + x, :3] = pal[out[y, x]]; canvas[oy + y, ox + x, 3] = 255
Image.fromarray(canvas, 'RGBA').save(os.path.join(outdir, f'{sys.argv[1]}_po.png'))
print('maat', w, h, 'pixels', int((canvas[..., 3] > 0).sum()), 'kleuren', len({tuple(pal[k]) for k in set(out.ravel()) if k}))
