"""Kolibrie (Ghost/Flying), eindvorm: eerste schets naar Jordi's pose (24 okt).
Duikt schuin naar linksonder (drinkt), vleugels als V omhoog, franjestaart naar rechtsonder."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *

C = dict(line='#1a1226', head='#2a2238', crown='#c46bff', body='#6a3fc8', body2='#8f63e6',
         wing='#2e2840', wing2='#4a3f6e', teal='#2fc7b8', orange='#f08a3c', beak='#1e1a26',
         soul='#efe6ff', soul2='#b9a6f2', eye='#ffffff', iris='#1a1226')


def draw():
    cv = Canvas(line=C['line'], lw=2.6)
    def wing(base, ang0, ang1, lens, wid, col, col2):
        # bladvormige vleugel (Jordi's schets) met een paar slagpennen aan de achterrand
        n = len(lens)
        m = None
        for i in range(n):
            a = math.radians(ang0 + (ang1 - ang0) * i / (n - 1))
            L = lens[i]
            tip = (base[0] + math.cos(a) * L, base[1] + math.sin(a) * L)
            mid = (base[0] + math.cos(a) * L * 0.5, base[1] + math.sin(a) * L * 0.5)
            f = cv.m_tube(catmull([base, mid, tip], closed=False), wid, wid * 0.45)
            m = f if m is None else m | f
        cv.fill(m, col)
        for i in range(1, n):
            a = math.radians(ang0 + (ang1 - ang0) * (i - 0.5) / (n - 1))
            L = (lens[i] + lens[i - 1]) / 2
            cv.stroke([(base[0] + math.cos(a) * L * 0.55, base[1] + math.sin(a) * L * 0.55),
                       (base[0] + math.cos(a) * L * 0.97, base[1] + math.sin(a) * L * 0.97)], 2.0)
        a = math.radians(ang1)
        cv.fill(cv.m_ellipse(base[0] + math.cos(a) * 30, base[1] + math.sin(a) * 30, 30, 14, rot=ang1), col2, line=False, clip=m)
    # ---- verre vleugel (achter, kleiner, hoger) ----
    wing((152, 112), -62, -84, [70, 86, 98, 100], 22, C['wing'], C['wing2'])
    # ---- staart: korte waaier (franje) + twee lange slierten met zielvlammen ----
    tails = [([(178, 114), (214, 112), (236, 150), (238, 200), (226, 232)], 5.5, 2.2),
             ([(176, 120), (200, 130), (206, 170), (196, 214)], 5.5, 2.2)]
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
    wing((134, 122), -108, -136, [84, 102, 114, 116], 26, C['wing'], C['wing2'])
    cv.fill(cv.m_ellipse(124, 102, 5, 4, rot=-60), C['orange'], line=False)
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
    cv.fill(cv.m_ellipse(72, 174, 7.5, 8), C['soul'], lw=1.6)
    cv.dot(71, 175, 5.2, C['iris'])
    cv.dot(73, 172, 1.8, C['eye'])
    return cv


if __name__ == '__main__':
    out = sys.argv[1]
    cv = draw()
    big = cv.image()
    s = sprite_scale(cv, 64, 0.9)
    sil = silhouette(s)
    W = Image.new('RGB', (256 + 64 * 3 + 64 + 40, 280), 'white')
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
    W.save(os.path.join(out, 'schets_v1.png'))
