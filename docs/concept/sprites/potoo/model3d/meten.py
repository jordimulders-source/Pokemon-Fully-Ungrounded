"""Verhoudingen van de kop meten: foto (handmatig gemeten punten) tegen het poppetje (automatisch uit de render).
Jordi (5 nov): "doe eens wat calculaties met lijnen", "en stop met het giswerk".
Alle maten t.o.v. kophoogte Hh (kruin -> onderkant onderkaak) en kopbreedte Wh (achterkant -> voorkant op ooghoogte)."""
import os, sys, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from potoo3d import *

# 3/4-foto: referenties/jordi_great_potoo_bek_open_drieluik.webp (bovenste foto), punten in fotopixels
FOTO = dict(kruin=(240, 27), achter=(170, 107), voor=(345, 110), oog=(271.7, 111.3), oog_b=35, oog_h=31,
            mond_l=237, mond_r=333, mond_top=132, kaaktip=(300, 207))


def ratios(p):
    Hh = p['kaaktip'][1] - p['kruin'][1]; Wh = p['voor'][0] - p['achter'][0]
    return {
        'kop breedte/hoogte': Wh / Hh,
        'oog hoogte vanaf kruin': (p['oog'][1] - p['kruin'][1]) / Hh,
        'oog vanaf achterkant': (p['oog'][0] - p['achter'][0]) / Wh,
        'oog breedte': p['oog_b'] / Wh,
        'mond bovenrand vanaf kruin': (p['mond_top'] - p['kruin'][1]) / Hh,
        'mond breedte': (p['mond_r'] - p['mond_l']) / Wh,
        'mond diepte': (p['kaaktip'][1] - p['mond_top']) / Hh,
        'mond links vanaf achterkant': (p['mond_l'] - p['achter'][0]) / Wh,
        'oog vorm (h/b, onbedekt)': p['oog_h'] / p['oog_b'],
    }


def meet_model(m, yaw, flip=True):
    """Meet dezelfde punten in de render; flip: de foto kijkt naar rechts, het model naar links."""
    x0, x1, y0, y1 = bbox(m, yaw, 8)
    scale = R * (232 / 256) / max(x1 - x0, y1 - y0); ctr = ((x0 + x1) / 2, (y0 + y1) / 2)
    _, gid, _, groups = render(m, yaw, 8, scale, ctr)
    kop = copy.copy(m); kop.parts = m.parts[m.n0:]
    _, gk, _, _ = render(kop, yaw, 8, scale, ctr)
    if flip:
        gid = gid[:, ::-1]; gk = gk[:, ::-1]
    head = gk >= 0
    ys, xs = np.nonzero(head)
    kruin_y = ys.min(); bodem = ys.max()
    eye = gid == groups.index('eye')
    # nabij oog = grootste samenhangende groep: neem de oogpixels links van de voorkant (na spiegelen: rechts = voor)
    ey, ex = np.nonzero(eye)
    voor = xs.max(); achter = xs.min()
    near = ex < voor - (voor - achter) * 0.15
    ey, ex = ey[near], ex[near]
    oog = (ex.mean(), ey.mean())
    row = int(oog[1]); hx = np.nonzero(head[row])[0]
    mo = np.isin(gid, [groups.index('mouth'), groups.index('throat')])
    my, mx = np.nonzero(mo)
    return {'kruin': (0, kruin_y), 'achter': (hx.min(), 0), 'voor': (hx.max(), 0), 'oog': oog,
            'oog_b': ex.max() - ex.min() + 1, 'oog_h': ey.max() - ey.min() + 1,
            'mond_l': mx.min(), 'mond_r': mx.max(), 'mond_top': my.min(), 'kaaktip': (0, bodem)}


def tabel(m, yaw):
    f, mm = ratios(FOTO), ratios(meet_model(m, yaw))
    rows = [(k, f[k], mm[k], mm[k] - f[k]) for k in f]
    return rows


if __name__ == '__main__':
    yaw = float(sys.argv[1]) if len(sys.argv) > 1 else 45
    for k, a, b, d in tabel(potoo(0), yaw):
        print(f'{k:30s} foto {a:5.2f}  model {b:5.2f}  verschil {d:+5.2f}')
