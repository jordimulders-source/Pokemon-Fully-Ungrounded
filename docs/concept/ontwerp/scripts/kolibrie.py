"""Kolibrie (Ghost/Flying), eindvorm: eerste schets naar Jordi's pose (24 okt).
Duikt schuin naar linksonder (drinkt), vleugels als V omhoog, franjestaart naar rechtsonder."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *

C = dict(line='#1a1226', head='#2a2238', crown='#c46bff', body='#6a3fc8', body2='#8f63e6',
         wing='#3e3656', wing2='#5e5486', teal='#2fc7b8', orange='#f08a3c', beak='#1e1a26',
         soul='#efe6ff', soul2='#b9a6f2', eye='#ffffff', iris='#1a1226')


BG = '#c9d6c0'  # zacht bosgroen, alleen om de doorzichtige vleugels te tonen


def draw():
    cv = Canvas(line=C['line'], lw=2.6)
    cv.img[:] = hexc(BG)
    def wing(base, ang, L, W, col, col2, bend=0.12):
        # kolibrievleugel: lang, smal, sikkelvormig; rechte voorrand, bolle achterrand, scherpe punt.
        # Vanaf het midden naar buiten steeds doorzichtiger (geblend met wat erachter zit).
        a = math.radians(ang)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux  # positieve v = achterrand (naar rechts/achteren)
        # profiel naar de foto's: breed bij de schouder, lange smalle punt; rechte voorrand,
        # holle achterrand, licht gebogen naar achteren; pennen lopen in de lengte
        prof = [(0, -0.45), (0.35, -0.45), (0.7, -0.32), (0.9, -0.16), (1.0, 0.0),
                (0.85, 0.10), (0.62, 0.28), (0.38, 0.52), (0.16, 0.70), (0, 0.58)]
        def P(u, v):
            v = v * W + bend * L * u * u
            return (base[0] + ux * u * L + nx * v, base[1] + uy * u * L + ny * v)
        m = cv.m_blob([P(u, v) for u, v in prof])
        under = cv.img.copy()
        cv.fill(m, col)
        # dekveren aan de basis (iets lichter), dan slagpennen in de lengte
        cv.fill(cv.m_blob([P(u, v) for u, v in [(0, -0.45), (0.22, -0.45), (0.27, 0.0), (0.2, 0.55), (0, 0.58)]]),
                col2, line=False, clip=m)
        for v0 in (-0.15, 0.12, 0.38):
            cv.stroke([P(0.27, v0), P(0.6, v0 * 0.5), P(0.92, 0.0)], 1.2, col2)
        # transparantie: dekkend tot het midden, daarna geleidelijk doorzichtiger tot ±90% aan de punt
        ring = cv.dilate(m, (cv.lw * SS) / 2 + 0.5)
        yy, xx = np.nonzero(ring)
        u = ((xx / SS - base[0]) * ux + (yy / SS - base[1]) * uy) / L
        t = np.clip((u - 0.5) / 0.5, 0, 1) * 0.9
        cv.img[yy, xx] = (cv.img[yy, xx] * (1 - t[:, None]) + under[yy, xx] * t[:, None]).astype(np.uint8)


    # ---- verre vleugel (achter, kleiner, hoger) ----
    wing((152, 114), -78, 112, 34, C['wing'], C['wing2'], bend=0.10)
    # ---- staart: korte waaier (franje) + twee lange slierten met zielvlammen ----
    tails = [([(178, 114), (214, 112), (240, 146), (248, 186), (246, 214)], 5.5, 2.2),
             ([(177, 117), (206, 122), (220, 160), (218, 204), (214, 234)], 5.5, 2.2),
             ([(176, 120), (196, 134), (198, 170), (184, 206)], 5.5, 2.2)]
    for pts, w0, w1 in tails:
        cv.fill(cv.m_tube(catmull(pts, closed=False), w0, w1), C['head'], lw=2.0)
    for i, a in enumerate((-6, 10, 26, 42, 58)):
        r = math.radians(a)
        L = 42 - abs(a - 26) * 0.35
        tip = (176 + math.cos(r) * L, 118 + math.sin(r) * L)
        cv.fill(cv.m_tube([(172, 118), tip], 12, 5), C['body'] if i % 2 else C['body2'], lw=2.0)
        cv.fill(cv.m_ellipse(tip[0], tip[1], 4, 4), C['soul2'], line=False)
    for pts, _, _ in tails:
        x, y = pts[-1]
        px, py = pts[-2]
        a = math.atan2(y - py, x - px)
        cx, cy = x + math.cos(a) * 9, y + math.sin(a) * 9
        nx, ny = -math.sin(a), math.cos(a)
        flame = cv.m_blob([(x, y), (cx + nx * 9, cy + ny * 9), (x + math.cos(a) * 26, y + math.sin(a) * 26),
                           (cx - nx * 9, cy - ny * 9)])
        cv.fill(flame, C['soul2'], lw=2.0)
        cv.fill(cv.m_ellipse(cx + math.cos(a) * 2, cy + math.sin(a) * 2, 4, 4), C['soul'], line=False)
    # ---- lijf: volle borst, violet fluweel met schubbenglans ----
    body = cv.m_ellipse(136, 140, 48, 31, rot=-28)
    cv.fill(body, C['body'])
    for (x, y) in ((116, 158), (128, 154), (122, 168), (140, 150), (134, 164), (148, 160), (110, 170)):
        cv.fill(cv.m_ellipse(x, y, 5, 3.5), C['body2'], line=False, clip=body)
    cv.fill(cv.m_ellipse(126, 122, 18, 9, rot=-28), C['teal'], line=False, clip=body)
    # ---- nabije vleugel (voor, groter, naar links gekanteld) ----
    wing((132, 124), -114, 130, 40, C['wing'], C['wing2'], bend=0.12)
    cv.fill(cv.m_ellipse(124, 108, 5, 4, rot=-60), C['orange'], line=False)
    # ---- nek + kop ----
    cv.fill(cv.m_tube([(106, 160), (88, 170)], 22, 20), C['head'])
    # snavel: lang, dun, iets gebogen naar linksonder
    cv.fill(cv.m_tube(catmull([(66, 186), (48, 206), (34, 230), (28, 246)], closed=False), 5, 1.2), C['beak'], lw=2.0)
    head = cv.m_ellipse(76, 176, 23, 20, rot=-20)
    # kuif: drie korte veren met bleke punt (jeguaka, de Guaraní-verentooi)
    for p in ([(80, 162), (82, 144), (90, 134)], [(84, 164), (94, 148), (104, 144)], [(76, 162), (70, 146), (74, 134)]):
        cv.fill(cv.m_tube(catmull(p, closed=False), 6, 2.5), C['crown'], lw=1.8)
        cv.dot(p[-1][0], p[-1][1], 2.2, C['soul'])
    cv.fill(head, C['head'])
    cv.fill(cv.m_ellipse(78, 162, 12, 5, rot=-15), C['crown'], line=False, clip=head)
    # oog: groot, rond, vriendelijk; bleke ring = gloed
    cv.dot(72, 174, 4.6, C['soul'])
    cv.dot(72, 174, 3.4, C['iris'])
    cv.dot(73.2, 172.8, 1.1, C['eye'])
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
    W.save(os.path.join(out, 'schets_v3.png'))
