"""Stand A (Jordi): render, silhouet direct verkleind, vel met rode omtrek. python3 A/maak.py '<json kwargs>' naam"""
import sys, json, subprocess, numpy as np
from PIL import Image
kw = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
naam = sys.argv[2] if len(sys.argv) > 2 else 'A'
subprocess.run(['python3.11', '-c', f"import sys; sys.path.insert(0,'.'); import kolibrie_pre as K; K.render('A/model_{naam}.png', lijf=25, kop=10, kantel=8, een_oog=True, **{kw!r})"], capture_output=True)
r = Image.open(f'A/model_{naam}.png').convert('RGBA'); a = np.array(r)[..., 3] > 127
m = np.array(Image.fromarray((a * 255).astype(np.uint8)).resize((64, 64), Image.BOX)) >= 128
open(f'A/silhouet_{naam}.txt', 'w').write('\n'.join(''.join('#' if v else '.' for v in row) for row in m) + '\n')
v = Image.new('RGB', r.size, (236, 234, 228)); v.paste(r, (0, 0), r); A = np.array(v)
M = np.kron(m, np.ones((8, 8), bool)); E = M ^ np.roll(M, 1, 0) | M ^ np.roll(M, 1, 1); A[E] = (230, 0, 0)
ys, xs = np.nonzero(m); x0, x1, y0, y1 = (xs.min() - 2) * 8, (xs.max() + 3) * 8, (ys.min() - 2) * 8, (ys.max() + 3) * 8
ov = Image.fromarray(A).crop((x0, y0, x1, y1)); mod = v.crop((x0, y0, x1, y1))
sil = Image.fromarray(np.where(m, 40, 236).astype(np.uint8)).convert('RGB')
W = ov.width; V = Image.new('RGB', (W * 2 + 40 + 160, ov.height + 20), 'white')
V.paste(mod, (10, 10)); V.paste(ov, (W + 30, 10)); V.paste(sil.resize((128, 128), Image.NEAREST), (2 * W + 50, 10)); V.paste(sil, (2 * W + 50, 150))
V.save(f'A/vel_{naam}.png'); print(naam, m.sum())
