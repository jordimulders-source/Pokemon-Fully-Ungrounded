"""Kolibrie (Ghost/Flying), eindvorm: schets naar Jordi's pose (24 okt).
Duikt schuin naar linksonder (drinkt), vleugels als V omhoog uit de rug, staart waaiert naar rechtsonder.
v7: opnieuw opgebouwd. Volgorde achter -> voor: verre vleugel, staart, lijf, nabije vleugel, dekveren
(versmolten met het lijf), lijfdetails, kuif, snavel, kop, oog."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *

C = dict(line='#1a1226', head='#2a2238', crown='#c46bff', body='#6a3fc8', body2='#8f63e6',
         wing='#4e4670', wing2='#6a5f92', teal='#2fc7b8', beak='#1e1a26',
         soul='#f4eeff', soul2='#b9a6f2', iris='#120c1c')
BG = '#c9d6c0'  # zacht bosgroen, alleen om de doorzichtige vleugels te tonen

BODY = [(188, 108), (164, 112), (134, 124), (108, 138), (90, 152), (84, 170), (96, 188),
        (124, 186), (152, 166), (174, 134)]


def wing(cv, base, ang, L, W, n=9):
    """Kolibrievleugel naar Jordi's close-up: lange driehoek, breedst aan de schouder, rechte voorrand
    naar een scherpe punt, rechte achterrand met kleine zaagtandjes (penpunten, strak parallel).
    Vanaf het midden naar buiten geleidelijk doorzichtiger. Geeft het vleugelmasker terug."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux  # positieve v = achterrand

    def P(u, v):
        return (base[0] + ux * u * L + nx * v * W, base[1] + uy * u * L + ny * v * W)
    tip, root = (0.97, 0.14), (0.12, 0.85)
    pts = [P(-0.1, -0.1), P(0.5, -0.10), P(0.82, -0.06), P(0.95, -0.01), P(1.0, 0.05), P(*tip)]
    dv = (root[0] - tip[0], root[1] - tip[1])
    dl = math.hypot(dv[0] * L, dv[1] * W)
    on, ov = (dv[1] * W / dl) / W, (-dv[0] * L / dl) / L
    pens = []
    for k in range(1, n + 1):
        f0, f1 = (k - 0.55) / n, k / n
        q0 = (tip[0] + dv[0] * f0, tip[1] + dv[1] * f0)
        q1 = (tip[0] + dv[0] * f1, tip[1] + dv[1] * f1)
        pts.append(P(q0[0] - on * 4, q0[1] - ov * 4))
        pts.append(P(*q1))
        pens.append(q0)
    pts += [P(-0.1, 0.8)]
    m = cv.m_poly(pts)
    under = cv.img.copy()
    # glasvleugel: alleen de vulling wordt doorzichtig (vanaf het midden tot ±90% aan de punt);
    # omlijning en pennen blijven goed zichtbaar, zodat je er echt doorheen kijkt
    cv.fill(m, C['wing'])
    lines = cv.m_stroke([P(0.05, 0.02), P(0.9, -0.03)], 1.2, smooth=False)
    for (pu, pv) in pens:
        lines |= cv.m_stroke([P(pu, pv), P(pu - 0.42, pv - 0.22)], 1.1, smooth=False)
    lines &= m
    yy, xx = np.nonzero(m & ~lines)
    u = ((xx / SS - base[0]) * ux + (yy / SS - base[1]) * uy) / L
    t = np.clip((u - 0.45) / 0.5, 0, 1) * 0.9
    cv.img[yy, xx] = (cv.img[yy, xx] * (1 - t[:, None]) + under[yy, xx] * t[:, None]).astype(np.uint8)
    cv.img[lines] = hexc(C['wing2'])
    return P


def draw():
    cv = Canvas(line=C['line'], lw=2.4)
    cv.img[:] = hexc(BG)
    bg = Image.fromarray(cv.img)
    dr = ImageDraw.Draw(bg)
    for (x, y, r, c) in ((70, 40, 46, '#e8dca0'), (170, 30, 38, '#9fbf8a'), (130, 80, 30, '#f0e4b8'),
                         (210, 70, 34, '#a9c79a'), (40, 110, 28, '#b5cfa4')):
        dr.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=c)
    cv.img[:] = np.array(bg)
    body = cv.m_blob(BODY)

    # ---- verre vleugel (wortel verdwijnt achter het lijf) ----
    wing(cv, (150, 120), -76, 104, 44)

    # ---- staart: wig uit het achterlijf, franje, drie slierten met zielvlammetjes ----
    shafts = [[(186, 112), (214, 104), (234, 124), (240, 160), (234, 194)],
              [(186, 114), (208, 118), (220, 148), (216, 186), (206, 210)],
              [(184, 116), (198, 130), (200, 162), (190, 192)]]
    for pts in shafts:
        cv.fill(cv.m_tube(catmull(pts, closed=False), 5, 3.4), C['head'], lw=2.0)
    for pts in shafts:
        (px, py), (x, y) = pts[-2], pts[-1]
        a = math.atan2(y - py, x - px)
        end = (x + math.cos(a) * 18, y + math.sin(a) * 18)
        cv.fill(cv.m_tube([(x - math.cos(a) * 2, y - math.sin(a) * 2), end], 3.4, 14), C['soul2'], lw=2.0)
        cv.dot(end[0] - math.cos(a) * 2, end[1] - math.sin(a) * 2, 3.6, C['soul'])
    for i, ang in enumerate((-18, 2, 22, 42)):
        r = math.radians(ang)
        tip = (180 + math.cos(r) * 26, 116 + math.sin(r) * 26)
        cv.fill(cv.m_tube([(176, 118), tip], 10, 4.5), C['body2'] if i % 2 else C['body'], lw=2.0)
        cv.dot(tip[0], tip[1], 2.2, C['soul2'])

    # ---- lijf ----
    cv.fill(body, C['body'])

    # ---- nabije vleugel uit de rug ----
    P = wing(cv, (124, 130), -110, 122, 50)
    # dekveren: geschubde rand die met het lijf versmelt (één omlijning om lijf + schubben)
    cov = cv.m_poly([P(-0.1, -0.1), P(0.08, -0.12), P(0.07, 0.72), P(-0.1, 0.8)])
    for k in range(4):
        cov |= cv.m_ellipse(*P(0.085, 0.0 + 0.2 * k), 6, 5.5)
    cv.fill(cov | body, C['body'])

    # ---- lijfdetails ----
    cv.fill(cv.m_ellipse(114, 146, 14, 8, rot=-30), C['teal'], line=False, clip=body & ~cov)
    for (x, y) in ((104, 170), (116, 176), (112, 162), (128, 170), (124, 158), (140, 162)):
        cv.fill(cv.m_ellipse(x, y, 5, 3.5), C['body2'], line=False, clip=body)

    # ---- kuif: jeguaka (drie veertjes met bleke punt), wortels achter de kop ----
    for p in ([(76, 162), (80, 144), (90, 132)], [(80, 164), (94, 150), (106, 147)], [(72, 162), (68, 146), (72, 133)]):
        cv.fill(cv.m_tube(catmull(p, closed=False), 6, 2.6), C['crown'], lw=1.8)
        cv.dot(p[-1][0], p[-1][1], 2.2, C['soul'])

    # ---- snavel: lang, dun, licht gebogen, wortel onder de kop ----
    cv.fill(cv.m_tube(catmull([(62, 182), (44, 202), (30, 222), (22, 242)], closed=False), 5.5, 1.4), C['beak'], lw=2.0)

    # ---- kop: rond, zit direct op de borst (kolibries hebben nauwelijks nek) ----
    head = cv.m_ellipse(74, 174, 21, 19, rot=-20) | cv.m_ellipse(88, 166, 10, 10)
    cv.fill(head, C['head'])
    cv.fill(cv.m_ellipse(78, 160, 12, 5, rot=-15), C['crown'], line=False, clip=head)

    # ---- oog: klein, midden in de kop, bleke gloeiring ----
    cv.dot(70, 172, 4.4, C['soul'])
    cv.dot(70, 172, 3.2, C['iris'])
    cv.dot(71.2, 170.8, 1.0, '#ffffff')
    return cv


if __name__ == '__main__':
    out = sys.argv[1]
    cv = draw()
    big = cv.image()
    s = sprite_scale(cv, 64, 0.9)
    sil = silhouette(s)
    W = Image.new('RGB', (256 + 64 * 3 + 64 + 40, 280), BG)
    W.paste(big, (0, 0))
    W.paste(s.resize((192, 192), Image.NEAREST), (266, 20), s.resize((192, 192), Image.NEAREST))
    W.paste(s, (470, 20), s)
    W.paste(sil, (470, 100), sil)
    d = ImageDraw.Draw(W)
    f = font(11)
    d.text((4, 262), 'modeltekening', fill='black', font=f)
    d.text((266, 216), 'sprite-formaat 3x', fill='black', font=f)
    d.text((470, 86), '1x', fill='black', font=f)
    d.text((470, 166), 'silhouet 1x', fill='black', font=f)
    W.save(os.path.join(out, 'schets_v7.png'))
