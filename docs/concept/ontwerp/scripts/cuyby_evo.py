"""Cuyby-evolutie (fase 2): de wandelende hooiberg (Stipa ichu). Modeltekening met drie silhouetvarianten.

A  Ichu-fontein: de vacht is een pol die vanaf een smalle voet omhoog en naar buiten waaiert; de buitenste plukken
   buigen over. Het gezicht kijkt laag uit de pol, onder een pony van sprieten.
B  Bol met kuif: Cuyby's bol, groter, met een kroon van rechtopstaande sprieten; de lokken hangen nog.
C  Hooiberg-koepel: een koepel van omlaag vallende plukken (rieten dak); alleen de oogjes zijn zichtbaar.

Vlakke kleuren, donkere omlijning, basisvormen (dit is de ontwerptekening, niet de sprite).
Draaien vanuit de repo-root:
python3 docs/concept/ontwerp/scripts/cuyby_evo.py docs/concept/ontwerp/cuyby_evo
"""
import sys
import os
import math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *
from PIL import Image, ImageDraw

C = dict(straw='#e9c45c', strawd='#c99a3e', rust='#e08a34', rustd='#b8641e', fur='#fbf6ea', dark='#2f2830',
         pink='#f4909e', line='#3a2a22', eye='#241a20')


def tuft(cv, root, mid, tip, w):
    """Pluk ichu-gras: brede voet, spits uiteinde, licht gebogen."""
    return cv.m_stroke([root, mid, tip], w, 0.4)


def feet(cv, xs, y, col, r=(11, 7)):
    for x in xs:
        cv.fill(cv.m_ellipse(x, y, r[0], r[1]), col)
        cv.stroke([(x - 3, y + 2), (x - 3, y + 6)], 1.3)
        cv.stroke([(x + 3, y + 2), (x + 3, y + 6)], 1.3)


def small_eyes(cv, eyes):
    for (ex, ey) in eyes:
        cv.fill(cv.m_ellipse(ex, ey, 5.5, 6.5), C['eye'], lw=1.4)
        cv.dot(ex - 1.6, ey - 2.4, 2.0, '#ffffff')
        cv.dot(ex + 2.0, ey + 2.8, 1.1, '#9c624a')


def fan(cv, layer, angles, r0, r1, w, cx=128, cy=180, droop=0.0):
    """Waaier van plukken vanuit het hart van de pol; hoe verder naar buiten, hoe meer de punt overhangt (fontein)."""
    for ang in angles:
        a = math.radians(ang)
        dx, dy = math.sin(a), -math.cos(a)
        d = max(0.0, abs(ang) - 12) / 40 * droop
        rr = r1 * (1 - 0.18 * d)
        root = (cx + dx * r0, cy + dy * r0)
        mid = (cx + dx * rr * 0.85, cy + dy * rr * 0.85)
        sgn = 1 if ang > 0 else -1
        tip = (cx + dx * rr + sgn * 22 * d, cy + dy * rr + 30 * d)
        k = 'rust' if ang > 18 else 'straw'
        cv.fill(tuft(cv, root, mid, tip, w), C[k + ('d' if layer == 'back' else '')])


def draw_A():
    c = C
    cv = Canvas(line=c['line'], lw=2.6)
    feet(cv, (98, 164), 204, '#d9707f', (9, 6))
    # achterste waaier (schaduwtint), tussen de voorste plukken in
    fan(cv, 'back', [-58, -40, -21, -3, 15, 33, 52], 60, 156, 30, droop=1.0)
    # de pol: breder naar boven, als een pol ichu
    body = cv.m_blob([(84, 200), (62, 170), (54, 130), (70, 90), (128, 70), (186, 90), (202, 130), (194, 170), (172, 200)])
    # zoom van lokken onderaan (zoals Cuyby), nu als hangende grasplukken
    hem = [((74, 172), (64, 192), (56, 208), 26), ((98, 186), (94, 204), (90, 216), 24),
           ((158, 186), (162, 204), (166, 216), 24), ((182, 172), (192, 192), (200, 208), 26)]
    coat = body.copy()
    for r, m, t, w in hem:
        coat |= tuft(cv, r, m, t, w)
    cv.fill(coat, c['straw'])
    cv.fill(cv.m_blob([(160, 74), (198, 104), (210, 160), (204, 212), (170, 206), (174, 150), (170, 110)]), c['rust'],
            line=False, clip=coat)
    # voorste waaier
    fan(cv, 'front', [-49, -30, -12, 6, 24, 43], 50, 140, 28, droop=1.0)
    # gezicht laag in de pol, half onder een korte pony
    face = cv.m_ellipse(128, 164, 30, 21)
    cv.fill(face, c['fur'])
    cv.fill(cv.m_ellipse(94, 140, 12, 8, rot=-30), c['dark'])
    cv.fill(cv.m_blob([(100, 146), (120, 148), (122, 166), (112, 180), (98, 174), (96, 156)]), c['dark'],
            line=False, clip=face)
    for r, m, t, w, k in [((108, 128), (112, 142), (104, 154), 15, 'straw'), ((128, 126), (130, 140), (126, 152), 15, 'straw'),
                          ((148, 128), (150, 142), (156, 152), 15, 'rust')]:
        cv.fill(tuft(cv, r, m, t, w), c[k], lw=1.8)
    small_eyes(cv, [(110, 162), (145, 161)])
    cv.fill(cv.m_ellipse(128, 172, 5, 3.5), c['pink'], lw=1.6)
    cv.stroke([(122, 178), (125, 181), (128, 178), (131, 181), (134, 178)], 1.4)
    feet(cv, (112, 146), 210, c['pink'])
    return cv


def draw_B():
    c = C
    cv = Canvas(line=c['line'], lw=2.6)
    feet(cv, (100, 160), 212, c['pink'])
    crown = [((90, 90), (70, 50), (52, 30), 24, 'straw'), ((110, 80), (104, 40), (96, 14), 24, 'straw'),
             ((132, 78), (134, 38), (136, 10), 24, 'straw'), ((154, 80), (166, 42), (178, 18), 24, 'rust'),
             ((172, 92), (194, 56), (212, 38), 24, 'rust')]
    for r, m, t, w, k in crown:
        cv.fill(tuft(cv, r, m, t, w), c[k])
    ball = cv.m_ellipse(128, 136, 74, 66)
    locks = [((70, 160), (50, 196), (42, 210), 34), ((100, 180), (94, 206), (88, 216), 30),
             ((156, 180), (162, 206), (168, 216), 30), ((186, 160), (206, 196), (214, 210), 34)]
    coat = ball.copy()
    for r, m, t, w in locks:
        coat |= tuft(cv, r, m, t, w)
    cv.fill(coat, c['straw'])
    cv.fill(cv.m_blob([(150, 70), (200, 90), (214, 140), (214, 212), (176, 200), (162, 140)]), c['rust'], line=False, clip=coat)
    face = cv.m_ellipse(128, 146, 40, 30)
    cv.fill(face, c['fur'])
    cv.fill(cv.m_blob([(92, 120), (120, 124), (122, 160), (100, 168), (88, 150)]), c['dark'], line=False, clip=face)
    cv.fill(cv.m_ellipse(66, 86, 13, 9, rot=-35), c['dark'])
    small_eyes(cv, [(106, 142), (150, 141)])
    cv.fill(cv.m_ellipse(128, 156, 5, 3.5), c['pink'], lw=1.6)
    cv.stroke([(121, 163), (125, 166), (128, 163), (131, 166), (135, 163)], 1.4)
    return cv


def draw_C():
    c = C
    cv = Canvas(line=c['line'], lw=2.6)
    feet(cv, (98, 162), 214, c['pink'])
    dome = cv.m_blob([(128, 24), (178, 40), (206, 96), (220, 170), (210, 206), (46, 206), (36, 170), (50, 96), (78, 40)])
    cv.fill(dome, c['straw'])
    cv.fill(cv.m_blob([(150, 28), (200, 60), (222, 150), (214, 206), (170, 206), (174, 120)]), c['rust'], line=False, clip=dome)
    # rieten dak: rijen plukken die omlaag vallen
    for row, y in enumerate((70, 116, 162)):
        for i in range(4 + row):
            x = 128 + (i - (3 + row) / 2) * (36 - row * 3)
            k = 'rust' if x > 150 else 'straw'
            cv.fill(tuft(cv, (x, y - 30), (x + (x - 128) * 0.12, y), (x + (x - 128) * 0.2, y + 30), 26), c[k], lw=1.8)
    cv.fill(cv.m_ellipse(92, 132, 14, 10), c['dark'], line=False)
    small_eyes(cv, [(94, 134), (144, 133)])
    cv.fill(cv.m_ellipse(120, 150, 5, 3.5), c['pink'], lw=1.6)
    return cv


def sheet(variants, out):
    W, H = 30 + 300 * 3, 620
    img = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((16, 10), 'Cuyby-evolutie (fase 2): wandelende hooiberg (Stipa ichu)  -  drie silhouetvarianten',
           fill=(20, 20, 20), font=font(15, True))
    G = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../graphics/pokemon/'))
    for i, (lab, cv) in enumerate(variants):
        x = 16 + i * 300
        img.paste(cv.image(256), (x, 40))
        d.rectangle([x - 1, 39, x + 257, 297], outline=(200, 200, 200))
        d.text((x, 302), lab, fill=(30, 30, 30), font=font(13, True))
        sp = sprite_scale(cv, 64, 0.80)
        img.paste(sp, (x, 330), sp)
        sp2 = sp.resize((128, 128), Image.NEAREST)
        img.paste(sp2, (x + 70, 330), sp2)
        s = silhouette(sp)
        img.paste(s, (x, 470), s)
        s2 = s.resize((128, 128), Image.NEAREST)
        img.paste(s2, (x + 70, 470), s2)
    d.text((16, 600), 'rij 2: spriteformaat 1x/2x; rij 3: silhouet 1x/2x', fill=(80, 80, 80), font=font(11))
    img.save(out)


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    a, b, cc = draw_A(), draw_B(), draw_C()
    sheet([('A  ichu-fontein', a), ('B  bol met kuif', b), ('C  hooiberg-koepel', cc)], os.path.join(out, 'varianten.png'))
    a.image(256).save(os.path.join(out, 'modeltekening_A.png'))
