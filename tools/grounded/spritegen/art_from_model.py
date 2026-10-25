"""2D-tekening uit een 3D-poppetje (zoals een Sugimori-tekening: vlakke kleuren, lijnen, cel-schaduw), plus de exacte
maskers die de pixel-over-motor nodig heeft (figuur, lijnen, materialen, helderheid).
Gebruik in code: art, fig, line, mat, tone, names, info = model_art(model, spec, size=512)"""
import numpy as np
from model3d import camera, bbox, render


def model_art(model, spec, size=512, line_px=None):
    Rc = camera(spec['yaw'], spec['pitch'], spec.get('stretch_x', 1.0))
    x0, x1, y0, y1 = bbox(model, Rc)
    sc = size * 0.92 / max(x1 - x0, y1 - y0)
    origin = (x0 - (size / sc - (x1 - x0)) / 2, y1 + (size / sc - (y1 - y0)) / 2)
    R = render(model, Rc, size, sc, origin)
    fig = R['mat'] >= 0
    L = np.array(spec.get('light', (-0.6, 0.7, 0.35)), float); L /= np.linalg.norm(L)
    tone = np.clip((R['n'] @ L + 1) / 2, 0, 1)
    # lijnen: waar een deel duidelijk vóór een ander ligt (dieptesprong), plus lijnen op gemarkeerde materiaalgrenzen
    z, part, mat = R['z'], R['part'], R['mat']
    jump = spec.get('art_dz', 6.0)
    line = np.zeros(fig.shape, bool)
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        z2 = np.roll(np.roll(z, -dy, 0), -dx, 1)
        p2 = np.roll(np.roll(part, -dy, 0), -dx, 1)
        f2 = np.roll(np.roll(fig, -dy, 0), -dx, 1)
        e = fig & f2 & (p2 != part) & (np.abs(z - z2) > jump)
        # lijn op de voorste kant
        front = e & (z > z2)
        back = e & (z2 > z)
        line |= front
        line |= np.roll(np.roll(back, dy, 0), dx, 1)
    lined = [R['mats'].index(n) for n in spec.get('lined_mats', []) if n in R['mats']]
    for i in lined:
        sel = mat == i
        for dy, dx in ((0, 1), (1, 0)):
            line |= sel & ~np.roll(np.roll(sel, -dy, 0), -dx, 1) & np.roll(np.roll(fig, -dy, 0), -dx, 1)
    w = line_px or max(1, size // 128)
    for _ in range(w - 1):
        line = line | np.roll(line, 1, 0) | np.roll(line, 1, 1)
    line &= fig
    # tekening voor het oog
    pal = spec['palette']
    art = np.full(fig.shape + (3,), 255, np.uint8)
    for i, n in enumerate(R['mats']):
        sel = mat == i
        b = np.array(pal.get(n + 'b', (200, 0, 200))); s = np.array(pal.get(n + 's', b))
        art[sel] = np.where((tone[sel] > 0.5)[:, None], b, s)
    art[line] = (40, 26, 20)
    return art, fig, line, mat, tone, {i: n for i, n in enumerate(R['mats'])}, dict(R=R, Rc=Rc, scale=sc, origin=origin)
