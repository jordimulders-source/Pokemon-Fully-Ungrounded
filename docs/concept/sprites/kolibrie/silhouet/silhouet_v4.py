"""Kolibrie silhouet v4 (Jordi, 24 okt): pose van Talonflame blijft (kop linksonder, vleugels als V,
staart naar rechts), maar kop, lijf en vleugelaanzet naar de leidraadfoto
(`referenties/jordi_leidraad_kop_vleugels.webp`) en Jordi's correctie op v3
(`referenties/jordi_silhouet_v3_correctie.png`):
- kop minder rond: een 'bovenhoofd' dat doorloopt in de nek; snavel uit de voorpunt van de kop;
- vleugels zitten met een brede, rechte aanzet op de rug (geen gat), iets kleiner t.o.v. het lijf;
- lijf gladder: één gestroomlijnde torpedo van borst naar staartwortel."""
import os, math
import numpy as np
from PIL import Image, ImageDraw
from silhouet import load, catmull, hi, tube, down, SS, HERE

yy, xx = np.mgrid[0:64, 0:64]


def poly(d, pts, smooth=True):
    c = catmull(pts + pts[:3], 12)[:-1] if smooth else pts
    d.polygon([(x * SS, y * SS) for x, y in c], fill=255)


def scaled(mask, cx, cy, k):
    """Masker schalen rond (cx, cy) met factor k (via 8x opschalen, dan weer omlaag)."""
    big = Image.fromarray((mask * 255).astype(np.uint8)).resize((64 * SS, 64 * SS), Image.NEAREST)
    a = 1 / k
    big = big.transform(big.size, Image.AFFINE, (a, 0, cx * SS * (1 - a), 0, a, cy * SS * (1 - a)), Image.NEAREST)
    return big


def build():
    tf = load('talonflame')
    m = tf[:, :, 3] > 0
    # vleugels uit Talonflame knippen
    cut = Image.new('L', (64, 64), 0)
    ImageDraw.Draw(cut).polygon([(0, 0), (30, 0), (24, 30), (4, 17), (0, 14)], fill=255)
    near = m & (np.array(cut) > 0)
    far = m & (xx >= 28) & (yy <= 27)
    add, d = hi()
    # verre vleugel: 85%, rond de aanzet op de rug
    add.paste(255, mask=scaled(far, 36, 28, 0.85))
    # rechte achterrand van de verre vleugel tot op het achterlijf (Jordi's lijn), geen gat
    poly(d, [(31, 26), (47, 24), (41, 37), (33, 34)], smooth=False)
    # nabije vleugel: 85%, rond de schouder; brede rechte aanzet op de schouder
    add.paste(255, mask=scaled(near, 22, 30, 0.85))
    poly(d, [(15, 23), (22, 25), (27, 31), (19, 33)], smooth=False)
    # rechte onderrand van de nabije vleugel tot op de schouder (Jordi's lijn), geen gat erboven
    poly(d, [(3, 15.5), (22.5, 32), (27, 30), (22, 16), (8, 10)], smooth=False)
    # lijf: gestroomlijnd, borst linksonder, rug omhoog naar de staartwortel rechts
    poly(d, [(18, 31), (26, 28.5), (35, 29), (42, 32), (46, 35), (45, 38.5), (39, 41.5),
             (30, 44.5), (22, 44.5), (16, 42.5), (14, 38)])
    # kop: 'bovenhoofd', schedel loopt over in de nek; voorpunt waar de snavel begint
    poly(d, [(19, 31), (15, 30), (11.5, 31.5), (9, 34.5), (7.8, 38), (9.5, 40.5), (13, 41.5), (17, 41)])
    # snavel uit de voorpunt van de kop, lang en dun naar linksonder
    tube(d, [(8.5, 38.5), (6, 44.5), (3.5, 51), (1.5, 58)], 2.2, 1.1)
    # jeguaka: klein waaiertje van drie veertjes op de kruin, naar achteren
    for tip in ((11, 26.5), (14.5, 25.5), (18, 27)):
        tube(d, [(13.5, 31.5), ((13.5 + tip[0]) / 2, (31.5 + tip[1]) / 2 - 0.4), tip], 2.6, 1.5)
    # staart: franje uit de staartwortel + drie slierten met Articuno-krul en racketpunt
    for a in (-15, 10, 35):
        r = math.radians(a)
        tube(d, [(43, 36), (43 + math.cos(r) * 8, 36 + math.sin(r) * 8)], 3.0, 1.8)
    ribbons = [[(45, 35), (53, 32), (60, 34), (62, 40), (58, 44)],
               [(45, 37), (54, 39), (60, 45), (59, 51), (54, 53)],
               [(44, 39), (49, 45), (52, 51), (50, 57)]]
    for rb in ribbons:
        tube(d, rb, 1.8, 1.3)
        (px, py), (x, y) = rb[-2], rb[-1]
        a = math.atan2(y - py, x - px)
        tube(d, [(x, y), (x + math.cos(a) * 3.5, y + math.sin(a) * 3.5)], 1.6, 4.4)
    m = down(add)
    # losse snippers (restjes van het knippen) weg: alleen het geheel dat aan het lijf vastzit houden
    keep = np.zeros_like(m); stack = [(38, 30)]
    while stack:
        y, x = stack.pop()
        if 0 <= y < 64 and 0 <= x < 64 and m[y, x] and not keep[y, x]:
            keep[y, x] = True
            stack += [(y + dy, x + dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
    return tf, keep


if __name__ == '__main__':
    tf, m = build()
    col = (40, 30, 60, 255)
    sil = np.zeros((64, 64, 4), np.uint8); sil[m] = col
    S = Image.fromarray(sil)
    W = Image.new('RGB', (64 * 4 * 3 + 64 + 50, 64 * 4 + 24), (236, 236, 230))
    v3 = Image.open(os.path.join(HERE, 'silhouet_v3_1x.png')).resize((256, 256), Image.NEAREST)
    W.paste(v3, (0, 0), v3)
    ghost = tf.copy(); ghost[:, :, 3] = (ghost[:, :, 3] * 0.35).astype(np.uint8)
    G = Image.fromarray(ghost).resize((256, 256), Image.NEAREST)
    W.paste(G, (266, 0), G)
    s2 = sil.copy(); s2[m, 3] = 170
    S2 = Image.fromarray(s2).resize((256, 256), Image.NEAREST)
    W.paste(S2, (266, 0), S2)
    S4 = S.resize((256, 256), Image.NEAREST)
    W.paste(S4, (532, 0), S4)
    W.paste(S, (800, 20), S)
    dr = ImageDraw.Draw(W)
    for x, t in ((0, 'v3 (vorige)'), (266, 'v4 over skelet'), (532, 'v4 4x'), (800, '1x')):
        dr.text((x + 2, 260), t, fill='black')
    W.save(os.path.join(HERE, 'silhouet_v4.png'))
    S.save(os.path.join(HERE, 'silhouet_v4_1x.png'))
