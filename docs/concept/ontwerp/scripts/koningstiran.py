"""Koningstiran-lijn (Inca-rangen), eerste conceptschetsen (5 nov). Geen ontwerp, alleen richting.
Rij 1: kiskadie (hatun runa) -> tiran met gouden oorschijf en gele franje (awki/orejon) -> koningstiran met
open waaier en rode franje (Sapa Inca). Rij 2: alternatieven: vorkstaarttiran als chaski (begin),
zonneral als willaq umu (splitsing eindvorm).
Gebruik: python3 koningstiran.py <uitmap>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *

LINE = '#2a1d16'
BRANCH = '#7a5a3a'


def branch(cv):
    cv.fill(cv.m_stroke([(40, 212), (130, 208), (230, 214)], 9, 7), BRANCH)


def legs(cv, xs=(126, 140), y0=192, y1=208):
    for x in xs:
        cv.stroke([(x, y0), (x - 2, y1)], 3.2, '#3a2a20')


def eye(cv, x, y, r=5.5, ring=None):
    if ring:
        cv.dot(x, y, r + 2.2, ring)
    cv.dot(x, y, r, '#140e0a')
    cv.dot(x - 1.6, y - 1.8, 1.6, '#ffffff')


def ray_fan(cv, cx, cy, a0, a1, n, L, w, col, tip, lw=1.6):
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * k / (n - 1))
        ex, ey = cx + math.cos(a) * L, cy + math.sin(a) * L
        mx, my = cx + math.cos(a) * L * 0.5, cy + math.sin(a) * L * 0.5
        cv.fill(cv.m_tube(catmull([(cx, cy), (mx, my), (ex, ey)], closed=False), w * 0.5, w), col, lw=lw)
        cv.dot(ex, ey, w * 0.42, tip)


def fringe(cv, x0, x1, y, L, col, n=7):
    """Mascaypacha: franje van draadjes die van een band over het voorhoofd hangt."""
    for k in range(n):
        x = x0 + (x1 - x0) * k / (n - 1)
        cv.fill(cv.m_stroke([(x, y), (x - 1, y + L * 0.6), (x - 2, y + L)], 3.4, 2.2), col, lw=1.2)


def tocapu(cv, clip, x0, y0, cell, nx, ny, cols):
    for i in range(nx):
        for j in range(ny):
            c = cols[(i + j) % len(cols)]
            m = cv.m_poly([(x0 + i * cell, y0 + j * cell), (x0 + (i + 1) * cell - 1, y0 + j * cell),
                           (x0 + (i + 1) * cell - 1, y0 + (j + 1) * cell - 1), (x0 + i * cell, y0 + (j + 1) * cell - 1)])
            cv.fill(m, c, line=False, clip=clip)


# ---------------------------------------------------------------- fase 1
def kiskadie():
    """Grote kiskadie als hatun runa: bruine rug, gele buik, zwart masker; de witte wenkbrauwstreep van de echte
    vogel is hier de gevlochten hoofdband (llawt'u). Gedrongen, groot hoofd, klein: een basisvorm."""
    cv = Canvas(LINE, 2.6)
    branch(cv)
    cv.fill(cv.m_blob([(150, 170), (170, 214), (160, 222), (138, 182)]), '#6e5232')  # staart
    legs(cv, (120, 134), 186, 208)
    body = cv.m_ellipse(128, 160, 34, 36, rot=15)
    cv.fill(body, '#f0cc3a')
    cv.fill(cv.m_ellipse(146, 150, 26, 32, rot=20), '#8a6a44', line='inner', clip=body)  # vleugel/rug
    for k in range(3):
        cv.stroke([(140 + k * 6, 160 + k * 4), (160 + k * 4, 176 + k * 3)], 1.2, '#5a4228')
    head = cv.m_ellipse(108, 112, 32, 30)
    cv.fill(head, '#1e1a1a')
    cv.fill(cv.m_ellipse(104, 132, 22, 9), '#f6f2e6', line=False, clip=head)  # witte keel
    band = cv.m_tube(catmull([(78, 104), (104, 98), (136, 106)], closed=False), 9)
    cv.fill(band, '#f6f2e6', lw=1.6, clip=head)
    for k in range(7):  # vlechtpatroon
        x = 82 + k * 8
        cv.stroke([(x, 99 + abs(k - 3) * 0.6), (x + 4, 107 + abs(k - 3) * 0.6)], 1.3, '#c23a2a')
    cv.fill(cv.m_ellipse(110, 86, 9, 3), '#f2d03a', lw=1.4)  # verborgen gele kroon, nog een spleetje
    cv.fill(cv.m_poly([(80, 112), (54, 118), (80, 122)]), '#2a2220', lw=1.8)  # brede tirannensnavel
    eye(cv, 92, 112, 5)
    return cv


# ---------------------------------------------------------------- fase 2
def awki():
    """Koningstiran met dichte kuif (hamerkop-silhouet), gouden oorschijf (orejon) en gele franje (awki, kroonprins).
    Bruin met okergele borst zoals de echte vogel."""
    cv = Canvas(LINE, 2.6)
    branch(cv)
    cv.fill(cv.m_blob([(152, 176), (184, 226), (174, 234), (142, 188)]), '#c9733a')  # rossige staart
    legs(cv, (124, 138), 190, 208)
    body = cv.m_ellipse(134, 150, 30, 44, rot=18)
    cv.fill(body, '#e9b868')
    cv.fill(cv.m_ellipse(150, 144, 22, 40, rot=22), '#7a5a3c', line='inner', clip=body)
    for k in range(4):
        cv.dot(148 + k * 5, 140 + k * 9, 2, '#e9c890')  # vleugelstippen
    # dichte kuif naar achteren: geeft de kop een hamervorm
    cv.fill(cv.m_blob([(104, 76), (150, 66), (176, 74), (150, 86), (112, 92)]), '#8a4a2a', lw=2.2)
    cv.fill(cv.m_blob([(150, 70), (174, 74), (152, 80)]), '#f2c840', line=False)  # geel schemert al door
    head = cv.m_ellipse(110, 98, 25, 23)
    cv.fill(head, '#7a5a3c')
    cv.fill(cv.m_ellipse(104, 116, 16, 8), '#f2e2b8', line=False, clip=head)
    # hoofdband + gele franje over het voorhoofd
    cv.fill(cv.m_tube(catmull([(86, 86), (106, 80), (128, 86)], closed=False), 6), '#c23a2a', lw=1.4)
    fringe(cv, 84, 100, 88, 12, '#f2d03a', 5)
    # gouden oorschijf
    cv.fill(cv.m_ellipse(122, 102, 9, 9), '#f0c040', lw=1.8)
    cv.dot(122, 102, 4, '#c8901c')
    cv.fill(cv.m_poly([(88, 100), (52, 106), (88, 110)]), '#3a2a22', lw=1.8)  # lange platte snavel
    eye(cv, 98, 98, 4.6)
    return cv


# ---------------------------------------------------------------- fase 3
def sapa():
    """Sapa Inca: de waaier staat altijd open (rood met staalblauwe puntjes, zoals de echte vogel), rode franje van
    de mascaypacha, gouden oorschijf, borst met een tocapu-vak, lange staart als de scepter-veer."""
    cv = Canvas(LINE, 2.6)
    branch(cv)
    cv.fill(cv.m_blob([(150, 172), (196, 236), (184, 246), (140, 186)]), '#c9733a')
    cv.fill(cv.m_blob([(176, 224), (196, 236), (184, 246), (170, 232)]), '#3a3a4a', line=False)
    legs(cv, (124, 138), 192, 208)
    body = cv.m_ellipse(136, 146, 34, 50, rot=16)
    cv.fill(body, '#e9b868')
    cv.fill(cv.m_ellipse(154, 140, 24, 46, rot=20), '#7a5a3c', line='inner', clip=body)
    bib = cv.m_poly([(108, 124), (132, 120), (136, 158), (120, 176), (106, 150)]) & body
    cv.fill(bib, '#c23a2a', line=False)
    tocapu(cv, bib, 108, 124, 8, 4, 7, ['#c23a2a', '#f0c040', '#1e1a1a', '#f6f2e6'])
    # open waaier: halve cirkel van veren dwars op de kop
    ray_fan(cv, 112, 82, 175, 365, 11, 58, 13, '#d8321e', '#2e4a8c', 1.8)
    for k in range(11):
        a = math.radians(175 + 190 * k / 10)
        cv.dot(112 + math.cos(a) * 42, 82 + math.sin(a) * 42, 3.0, '#1a1a2a')  # zwarte band voor de punt
    head = cv.m_ellipse(112, 94, 25, 23)
    cv.fill(head, '#7a5a3c')
    cv.fill(cv.m_ellipse(104, 112, 16, 8), '#f2e2b8', line=False, clip=head)
    cv.fill(cv.m_tube(catmull([(88, 82), (108, 76), (130, 82)], closed=False), 6.5), '#f0c040', lw=1.4)
    fringe(cv, 84, 104, 84, 15, '#c23a2a', 6)
    cv.fill(cv.m_ellipse(124, 98, 10, 10), '#f0c040', lw=1.8)
    for k in range(8):  # zonnestraaltjes op de oorschijf
        a = k * math.pi / 4
        cv.stroke([(124 + math.cos(a) * 4, 98 + math.sin(a) * 4), (124 + math.cos(a) * 8, 98 + math.sin(a) * 8)], 1.1, '#c8901c')
    cv.fill(cv.m_poly([(90, 96), (50, 102), (90, 106)]), '#3a2a22', lw=1.8)
    eye(cv, 100, 94, 4.6)
    return cv


# ---------------------------------------------------------------- alternatief: chaski
def chaski():
    """Vorkstaarttiran als chaski (renbode): grijze rug, witte buik, zwarte kap met de hoofdband; de extreem lange
    gevorkte staart wappert als de linten van een loper. Klein schelptoetertje (pututu) als halsband."""
    cv = Canvas(LINE, 2.6)
    branch(cv)
    cv.fill(cv.m_tube(catmull([(150, 180), (176, 214), (196, 250), (204, 256)], closed=False), 7, 3), '#1e1e24', lw=2)
    cv.fill(cv.m_tube(catmull([(146, 182), (160, 220), (164, 256)], closed=False), 7, 3), '#1e1e24', lw=2)
    legs(cv, (120, 134), 186, 208)
    body = cv.m_ellipse(128, 156, 28, 36, rot=15)
    cv.fill(body, '#f6f4ee')
    cv.fill(cv.m_ellipse(144, 150, 20, 32, rot=20), '#8a8e96', line='inner', clip=body)
    head = cv.m_ellipse(108, 112, 24, 23)
    cv.fill(head, '#1e1e24')
    cv.fill(cv.m_ellipse(104, 128, 18, 8), '#f6f4ee', line=False, clip=head)
    cv.fill(cv.m_tube(catmull([(86, 102), (106, 96), (128, 102)], closed=False), 7), '#e0a030', lw=1.4, clip=head)
    for k in range(6):
        cv.stroke([(88 + k * 7, 98), (91 + k * 7, 105)], 1.2, '#2a6a4a')
    # pututu (schelp) aan een koordje
    cv.stroke([(96, 132), (110, 142), (124, 134)], 1.3, '#c23a2a')
    cv.fill(cv.m_spiral(110, 148, 2, 7, 1.6, 6, 3), '#f2e6d0', lw=1.4)
    cv.fill(cv.m_poly([(86, 110), (62, 115), (86, 119)]), '#2a2220', lw=1.8)
    eye(cv, 96, 108, 4.4)
    return cv


# ---------------------------------------------------------------- alternatief: willaq umu
def willaq():
    """Zonneral als willaq umu (zonnepriester), splitsing in fase 3: lange hals, vleugels gespreid tot een zon
    (de echte oogvlekken van de zonneral worden zonneschijven), gouden kap met een kleine waaier."""
    cv = Canvas(LINE, 2.6)
    branch(cv)
    for side, cx in ((-1, 84), (1, 176)):
        w = cv.m_ellipse(cx, 120, 52, 40, rot=side * -20)
        cv.fill(w, '#8a6a44')
        cv.fill(cv.m_ellipse(cx + side * 4, 118, 30, 24, rot=side * -20), '#f08a1e', line=False, clip=w)
        cv.fill(cv.m_ellipse(cx + side * 4, 118, 20, 15, rot=side * -20), '#1e1a1a', line=False, clip=w)
        cv.fill(cv.m_ellipse(cx + side * 4, 118, 11, 8, rot=side * -20), '#f0c040', line=False, clip=w)
        for k in range(5):
            cv.stroke([(cx + side * (20 + k * 6), 150 - k * 4), (cx + side * (30 + k * 6), 156 - k * 6)], 1.3, '#4a3624')
    cv.fill(cv.m_blob([(124, 176), (136, 176), (142, 214), (118, 214)]), '#6e5232')
    legs(cv, (124, 136), 190, 208)
    body = cv.m_ellipse(130, 160, 24, 32)
    cv.fill(body, '#c9a878')
    for k in range(4):
        cv.stroke([(114, 148 + k * 8), (146, 148 + k * 8)], 1.3, '#7a5a3c')
    cv.fill(cv.m_tube(catmull([(130, 136), (124, 110), (118, 84)], closed=False), 14, 11), '#c9a878', lw=2.2)
    ray_fan(cv, 118, 62, 200, 340, 7, 26, 8, '#d8321e', '#2e4a8c', 1.4)
    head = cv.m_ellipse(116, 70, 15, 13)
    cv.fill(head, '#1e1a1a')
    cv.fill(cv.m_tube(catmull([(102, 64), (116, 60), (130, 64)], closed=False), 4.5), '#f0c040', lw=1.2, clip=head)
    cv.stroke([(104, 74), (126, 78)], 2.2, '#f6f2e6')
    cv.fill(cv.m_poly([(103, 70), (74, 76), (103, 78)]), '#f08a1e', lw=1.6)
    eye(cv, 110, 68, 3.4, ring='#c23a2a')
    return cv


PANELS = [
    (kiskadie, 'Fase 1: "hatun runa"', 'grote kiskadie', 'gewone stadsvogel; witte streep =\ngevlochten hoofdband, kroon nog dicht'),
    (awki, 'Fase 2: "awki" / orejón', 'koningstiran, kuif dicht', 'kroonprins: gele franje,\ngouden oorschijf'),
    (sapa, 'Fase 3: "Sapa Inca"', 'koningstiran, kuif open', 'rode franje (mascaypacha), waaier\naltijd open, tocapu-borst'),
    (chaski, 'Alt. begin: "chaski"', 'vorkstaarttiran', 'renbode met schelptoeter;\nstaart als wapperende linten'),
    (willaq, 'Alt. fase 3: "willaq umu"', 'zonneral', 'zonnepriester: de oogvlekken\nop de vleugels worden zonnen'),
]

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    BG = (238, 232, 218)
    PW, PH = 256, 256 + 118
    W = Image.new('RGB', (PW * 3 + 40, PH * 2 + 70), BG)
    d = ImageDraw.Draw(W)
    d.text((12, 10), 'Koningstiran-lijn (Inca-rangen) — conceptschetsen, geen sprites', fill='black', font=font(16, True))
    d.text((12, 32), 'Rij 1: voorkeurslijn (afkomst + geel→rood). Rij 2: alternatieven. Rechtsonder elk paneel: 1x sprite-formaat.',
           fill='#333', font=font(11))
    pos = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)]
    for (fn, title, bird, note), (cx, cy) in zip(PANELS, pos):
        cv = fn()
        x, y = 10 + cx * (PW + 10), 56 + cy * (PH + 6)
        W.paste(cv.image(), (x, y))
        s = sprite_scale(cv, 64, 0.92)
        W.paste(s, (x + PW - 66, y + PW - 66), s)
        d.text((x + 4, y + 262), title, fill='black', font=font(13, True))
        d.text((x + 4, y + 281), bird, fill='#7a2a1a', font=font(12, True))
        d.multiline_text((x + 4, y + 300), note, fill='#333', font=font(11), spacing=3)
    # rechtsonder: legenda
    x, y = 10 + 2 * (PW + 10), 56 + PH + 6
    d.multiline_text((x + 4, y + 20),
                     'Vogels:\n• grote kiskadie (Great kiskadee)\n• koningstiran (Tropical royal\n  flycatcher)\n'
                     '• vorkstaarttiran (Fork-tailed\n  flycatcher)\n• zonneral (Sunbittern)\n\n'
                     'Inca-attributen:\n• llawt\'u: gevlochten hoofdband\n• franje: geel = kroonprins,\n  rood = Sapa Inca\n'
                     '• gouden oorschijf = adel (orejón)\n• tocapu: geometrische vakjes\n• pututu: schelptoeter',
                     fill='#222', font=font(11), spacing=4)
    W.save(os.path.join(out, 'schets_v1.png'))
