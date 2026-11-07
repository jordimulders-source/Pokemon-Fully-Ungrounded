"""Poppetje op de ontwerphoek: 3D-lijf (potoo3d.py) + kop uit de overgetrokken lijnen van de 3/4-foto
(referenties/jordi_great_potoo_bek_open_drieluik.webp, fotopixels). In 3D lukte de snavel niet zonder te gokken;
hier komt elke lijn van de foto (Jordi: "stop met het giswerk", "meet ook de snavel af", "de puntige uiteinden",
"de golvende vorm naar de punt toe"). Ontwerpkleuren: lichte vacht, pikzwarte ogen (Drifloon), geestpaarse mond."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from potoo3d import *
import potoo3d as P3

HERE = os.path.dirname(os.path.abspath(__file__))
# kopomtrek (zonder de mond): van de wang links via de kruin naar de voorkant en het haakje
KOP = [(186, 160), (176, 135), (173, 110), (180, 85), (192, 60), (210, 40), (233, 28), (257, 27), (280, 30), (303, 37), (323, 47),
       (335, 63), (342, 83), (345, 107), (343, 127), (340, 143), (333, 160), (322, 184), (309, 201), (296, 206),
       (286, 212), (265, 214), (240, 200), (215, 180)]
OOG = ((271.7, 111.3), 17.5, 15.5)            # midden, halve breedte, halve hoogte
VER_OOG = ((340.5, 117), 6, 12.5)              # aan de voorrand, half verscholen
MOND = P3.BOVENRAND + P3.VERRE_RAND[1:] + P3.NABIJE_RAND[::-1][1:]   # rondom: mondhoek -> voor -> punt -> terug
HAAK = [(329, 139.5), (334, 140.5), (338.5, 143), (340.5, 149), (340.2, 157.5), (338.6, 157), (337.2, 150), (334.8, 146),
        (330.5, 144.5)]                        # spits, krult omlaag
KAAKPUNT = [(289, 201), (296.4, 205.7), (300.5, 209.5), (297, 211.5), (291, 206)]
RAND = 3.5                                     # lichte mondrand, fotopixels (±0,013 x kopbreedte)


def glad(pts, vast=(), n=3, dicht=True):
    """Chaikin-afronding; punten in 'vast' (indices) blijven scherp (de spitse uiteinden)."""
    pts = [(tuple(p), i in vast) for i, p in enumerate(pts)]
    for _ in range(n):
        out = []
        N = len(pts)
        for i in range(N if dicht else N - 1):
            (p, vp), (q, vq) = pts[i], pts[(i + 1) % N]
            if vp: out.append((p, True))
            else: out.append(((0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]), False))
            out.append(((0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1]), False) if not vq else (q, True))
        if not dicht: out.append(pts[-1])
        pts = out
    return [p for p, _ in pts]


def render_lijf(yaw=45):
    m = potoo(0)
    lijf = Model(); lijf.parts = m.parts[:m.n0]
    x0, x1, y0, y1 = bbox(m, yaw, 8)
    scale = R * (232 / 256) / max(x1 - x0, y1 - y0)
    z, gid, nrm, groups = render(lijf, yaw, 8, scale, ((x0 + x1) / 2, (y0 + y1) / 2))
    return z, gid, nrm, groups


def maak(yaw=45, kop_breed=0.92, out='samengesteld.png'):
    z, gid, nrm, groups = render_lijf(yaw)
    a = gid >= 0
    ys, xs = np.nonzero(a)
    top = ys.min()
    # breedte van het lijf op schouderhoogte (15% onder de bovenkant van het lijf)
    lijf_b = xs.max() - xs.min()                 # grootste breedte van het lijf
    foto_b = 345 - 173                           # kopbreedte op de foto
    k = kop_breed * lijf_b / foto_b              # voorfoto: kop ±0,9 x zo breed als het lijf
    # spiegelen (foto kijkt naar rechts); kopmidden iets naar de kijkrichting, kruin boven het lijf
    cx = (xs.min() + xs.max()) / 2 - 0.12 * lijf_b
    T = lambda p: (cx - (p[0] - 244) * k, top - 0.10 * lijf_b + (p[1] - 27) * k)
    im = shade(z, gid, nrm, groups).resize((R, R), Image.LANCZOS).convert('RGB')
    d = ImageDraw.Draw(im)
    lw = max(2, int(R / 256 * 1.6))
    kop = glad(KOP)
    d.polygon([T(p) for p in kop], fill=COL['fur'])
    boven = glad(KOP[1:16], n=3, dicht=False)                       # omlijning alleen langs de bovenkant (onder gaat de kop in het lijf over)
    d.line([T(p) for p in boven], fill=tuple(LINE), width=lw, joint='curve')
    tip = len(P3.BOVENRAND) + len(P3.VERRE_RAND) - 2                # index van de onderkaakpunt in MOND
    mond = glad(MOND, vast=(0, tip))
    d.polygon([T(p) for p in mond], fill=COL['mouth'])
    d.line([T(p) for p in mond] + [T(mond[0])], fill=COL['rim'], width=max(2, int(RAND * k)), joint='curve')
    d.line([T(p) for p in mond] + [T(mond[0])], fill=tuple(LINE), width=1)
    for (c, rx, ry) in (OOG, VER_OOG):
        x, y = T(c); d.ellipse((x - rx * k, y - ry * k, x + rx * k, y + ry * k), fill=COL['eye'], outline=tuple(LINE), width=lw)
    d.polygon([T(p) for p in glad(HAAK, vast=(4,), n=2)], fill=COL['beak'], outline=tuple(LINE))
    d.polygon([T(p) for p in glad(KAAKPUNT, vast=(2,), n=2)], fill=COL['beak'], outline=tuple(LINE))
    g = np.array(im.convert('L')) < 250
    yy, xx = np.nonzero(g); pad = 12
    im = im.crop((xx.min() - pad, yy.min() - pad, xx.max() + pad, yy.max() + pad))
    im.thumbnail((360, 360), Image.LANCZOS)
    im.save(os.path.join(HERE, out))
    return im


if __name__ == '__main__':
    maak()
