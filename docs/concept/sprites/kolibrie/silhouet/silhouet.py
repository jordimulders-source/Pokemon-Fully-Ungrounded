"""Kolibrie, stap 2: silhouet op een echt skelet (Jordi, 24 okt).
Skelet: Talonflame (pose + vleugels: kop linksonder, vleugels als V, staart naar rechts).
Aanpassingen: haviksnavel -> lange dunne kolibriesnavel; jeguaka-kuif; poten weg;
staart -> franje + drie slierten met Articuno-achtige zwier en een racketpunt (zielvlammetje)."""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../..'))
SS = 8


def load(n):
    im = Image.open(os.path.join(ROOT, 'graphics/pokemon', n, 'anim_front.png'))
    L = open(os.path.join(ROOT, 'graphics/pokemon', n, 'normal.pal')).read().split('\n')[3:19]
    flat = []
    for l in L:
        flat += [int(v) for v in l.split()]
    im.putpalette(flat)
    fr = im.crop((0, 0, 64, 64))
    rgba = np.array(fr.convert('RGBA'))
    rgba[np.array(fr) == 0, 3] = 0
    return rgba


def catmull(pts, steps=16):
    out = []
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        for k in range(steps):
            t = k / steps
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def hi():
    im = Image.new('L', (64 * SS, 64 * SS), 0)
    return im, ImageDraw.Draw(im)


def tube(d, pts, w0, w1):
    c = catmull(pts)
    for i, (x, y) in enumerate(c):
        r = (w0 + (w1 - w0) * i / (len(c) - 1)) / 2 * SS
        d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], fill=255)


def down(im):
    return np.array(im.resize((64, 64), Image.BOX)) > 100


def build():
    tf = load('talonflame')
    m = tf[:, :, 3] > 0
    yy, xx = np.mgrid[0:64, 0:64]
    # poten weg
    m[yy >= 47] = False
    # Talonflame-staart weg (zwart/gele waaier rechts)
    tail = Image.new('L', (64, 64), 0)
    ImageDraw.Draw(tail).polygon([(40, 28), (50, 25), (60, 25), (61, 31), (56, 37), (52, 43), (44, 47), (40, 45)], fill=255)
    m &= ~(np.array(tail) > 0)
    # haviksnavel weg
    m[(xx < 9) & (yy >= 33) & (yy <= 42)] = False

    add, d = hi()
    # v2: lijf slanker (diepte/lengte 0,8 -> ±0,5 zoals op de foto's): buik afsnijden langs een
    # schuine lijn van de keel naar de staartwortel, dan een ronde onderkant terug
    cut = Image.new('L', (64, 64), 0)
    ImageDraw.Draw(cut).polygon([(14, 41), (26, 43), (40, 42), (44, 46), (44, 64), (10, 64)], fill=255)
    m &= ~(np.array(cut) > 0)
    d.ellipse([17 * SS, 33 * SS, 42 * SS, 45 * SS], fill=255)
    # kop iets ronder naar voren
    d.ellipse([7 * SS, 31 * SS, 19 * SS, 43 * SS], fill=255)
    # kolibriesnavel: lang en dun, schuin naar linksonder
    tube(d, [(9.5, 39), (6, 46), (3, 53), (1.5, 59)], 2.4, 1.2)
    # jeguaka: drie veertjes op de kruin, naar achteren/boven
    # (valt in het silhouet binnen de nabije vleugel; leest pas in kleur)
    tube(d, [(13, 32), (14, 28), (16.5, 25.5)], 2.0, 1.3)
    tube(d, [(15, 32.5), (18, 29.5), (21, 28.5)], 2.0, 1.3)
    tube(d, [(11, 32), (10.5, 28), (11.5, 25)], 2.0, 1.3)
    # staart: franje (korte waaier) uit het achterlijf
    for a in (-10, 15, 40):
        r = math.radians(a)
        tube(d, [(40, 40), (40 + math.cos(r) * 8, 40 + math.sin(r) * 8)], 3.0, 1.8)
    # drie slierten met Articuno-achtige zwier (S-boog), eindigend in een racket
    ribbons = [[(42, 38), (52, 33), (60, 35), (62, 41), (58, 45)],
               [(42, 41), (53, 41), (60, 46), (59, 52), (54, 54)],
               [(41, 43), (48, 48), (51, 54), (49, 59)]]
    for rb in ribbons:
        tube(d, rb, 1.8, 1.3)
        (px, py), (x, y) = rb[-2], rb[-1]
        a = math.atan2(y - py, x - px)
        tube(d, [(x, y), (x + math.cos(a) * 3.5, y + math.sin(a) * 3.5)], 1.6, 4.4)
    m |= down(add)
    return tf, m


if __name__ == '__main__':
    tf, m = build()
    col = (40, 30, 60, 255)
    sil = np.zeros((64, 64, 4), np.uint8); sil[m] = col
    S = Image.fromarray(sil)
    # vel: skelet | silhouet over vaag skelet | silhouet 4x | 1x
    W = Image.new('RGB', (64 * 4 * 3 + 64 + 50, 64 * 4 + 24), (236, 236, 230))
    T = Image.fromarray(tf)
    W.paste(T.resize((256, 256), Image.NEAREST), (0, 0), T.resize((256, 256), Image.NEAREST))
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
    for x, t in ((0, 'skelet: Talonflame'), (266, 'silhouet over skelet'), (532, 'silhouet 4x'), (800, '1x')):
        dr.text((x + 2, 260), t, fill='black')
    W.save(os.path.join(HERE, 'silhouet_v2.png'))
    S.save(os.path.join(HERE, 'silhouet_v2_1x.png'))
