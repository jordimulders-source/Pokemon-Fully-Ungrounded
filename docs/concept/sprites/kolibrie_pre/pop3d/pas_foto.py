"""Poppetje passend maken op foto 1 zelf (omtrek punt voor punt uit ../silhouet/silhouet.py, echte maten,
zonder snavel), daarna pas cute maken in 3D (kop groter, lijf korter). Coathief-volgorde: foto -> poppetje -> silhouet."""
import sys, json, math, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '../silhouet')
import silhouet as S1
import pas, pop3d_kuiken as K
K.set_palet('fluweel (als eindvorm)')
STAART = [(600, 585), (640, 592), (668, 605), (695, 640), (714, 695), (668, 690), (640, 640), (600, 610)]
def doel():
    im = Image.new('L', (S1.W, S1.H), 0); d = ImageDraw.Draw(im)
    for p in [S1.lijf, S1.kop, STAART]: d.polygon(p, fill=255)
    for p in [[(483, 540), (478, 590), (495, 590), (500, 545)], [(570, 575), (568, 615), (585, 615), (588, 580)]]: d.polygon(p, fill=255)
    a = np.asarray(im) > 0; ys, xs = np.nonzero(a)
    cr = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    return cr
D = doel()
def vergelijk(m, yaw, pitch, uit=None, H=60):
    img, a = K.view(m, yaw, pitch)
    A = Image.fromarray((a * 255).astype(np.uint8)); A = A.crop(A.getbbox())
    t = np.asarray(D.resize((round(D.width * H / D.height), H), Image.LANCZOS)) >= 128
    w = round(A.width * H / A.height); pm = np.asarray(A.resize((w, H), Image.LANCZOS)) >= 128
    W = max(w, t.shape[1]) + 2
    T = np.zeros((H, W), bool); T[:, :t.shape[1]] = t
    Pm = np.zeros((H, W), bool); Pm[:, :w] = pm      # beide links uitgelijnd (kop/borst links)
    iou = (T & Pm).sum() / (T | Pm).sum()
    if uit:
        rgb = np.full((H, W, 3), 255, np.uint8)
        rgb[T & Pm] = (90, 170, 90); rgb[T & ~Pm] = (220, 60, 60); rgb[Pm & ~T] = (60, 90, 220)
        Image.fromarray(rgb).resize((W * 4, H * 4), Image.NEAREST).save(uit)
    return iou
def model_zonder_bek(p):
    m = pas.model(p, ogen=False)
    m.parts = [x for x in m.parts if x[3] not in ('beak', 'gape', 'mouth')]
    return m
if __name__ == '__main__':
    p = dict(pas.START); p.update(tl=20, ty=-40, tt=-60)
    sc = lambda q: vergelijk(model_zonder_bek(q), 15, 4)
    best = sc(p); print('start', round(best, 3))
    steps = {k: (6 if k.endswith('t') else 4) for k in p}
    for rnd in range(3):
        for k in p:
            for s in (steps[k], -steps[k]):
                while True:
                    q = dict(p); q[k] += s; v = sc(q)
                    if v > best + 1e-4: p, best = q, v
                    else: break
        steps = {k: v / 2 for k, v in steps.items()}; print('ronde', rnd, round(best, 3))
    json.dump(p, open('pas_foto_params.json', 'w'), indent=1)
    vergelijk(model_zonder_bek(p), 15, 4, 'overlay_foto.png')
