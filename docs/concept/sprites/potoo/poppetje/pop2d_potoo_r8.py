"""Great potoo ronde 8: nieuw lijf onder de vaste kop van ronde 7.
- Kop + snavel + muil: ongewijzigd uit ronde 7 (overtrek van de leidraad, linkerhelft van jordi_great_potoo_bek_open_duo.webp).
  Alleen de binnenkant van de muil is vloeiend (geen ringen) en de borstelveertjes zijn fijne veertjes langs de snavelrug.
- Lijf: met de hand overgetrokken naar jordi_great_potoo_illustratie_LICHAAMSVORM.png (Jordi: "kijk dit is de vorm van het
  lichaam"): rechtop, brede schouders direct onder de kop met de vleugelboeg, gevouwen vleugel langs de flank met getrapte
  pennen ver naar beneden, smal taps lijf, lange staart. Meegedraaid naar de kijker (3/4) zoals het lijf op de leidraad zelf
  (schouder/vleugel achter de kop, borst onder de kaak); breedte ±1,35x de kop (nachtfoto: ±1,5x van voren).
- Alles in leidraadpixels (vogel kijkt naar rechts) en bij het tekenen gespiegeld (spritehoek naar links).
Geen fotopixels: alleen eigen gladde vormen, op 4x getekend en verkleind.
Draaien vanuit de repo-root: python3 docs/concept/sprites/potoo/poppetje/pop2d_potoo_r8.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop2d_potoo as R6
import pop2d_potoo_r7 as R7
from pop2d_potoo import catmull, hexc, erode

C = R6.C                                    # zelfde dict als ronde 6/7 (Canvas.line leest hieruit)
C.update(breast='#E9E6F0', feather='#DCD7E7', fline='#8F86A6', bark2='#BDB4CB')

SS = 4
X0, X1, Y0, Y1 = 60, 600, 80, 1080            # tekenvak in leidraadpixels
MIRX = X1

# ------------------------------------------------------------------ lijf (leidraadpixels, vogel kijkt naar rechts)
# rug: komt achter het achterhoofd vandaan (geen nek), brede schouder, smal taps naar de staart
BACK = [(300, 236), (284, 246), (264, 256), (242, 268), (220, 284), (198, 304), (178, 328), (162, 356), (150, 388),
        (143, 420), (141, 455), (144, 490), (151, 525), (162, 560), (176, 595), (192, 628), (208, 658), (222, 686), (232, 708)]
# staart: lang, smal, licht naar achteren hangend (voorover zittende vogel)
TAIL_L = [(232, 708), (228, 760), (224, 820), (220, 880), (216, 940), (213, 990), (214, 1022)]
TAIL_TIP = [(222, 1036), (236, 1040), (250, 1036), (259, 1024)]
TAIL_R = [(262, 990), (268, 940), (276, 880), (284, 820), (294, 770), (306, 735)]
# buik/borst: van de staartbasis omhoog tot achter de kaak (verre schouder piept net rechts onder de kaak)
BELLY = [(330, 724), (356, 708), (382, 684), (404, 654), (422, 618), (436, 578), (444, 536), (446, 494), (442, 458), (432, 428)]
BODY = BACK + TAIL_L[1:] + TAIL_TIP + TAIL_R + BELLY + [(400, 330), (340, 260)]

# vleugel: dekveren met de boeg bovenaan (schouder, net onder/achter de kop), daaronder getrapte pennen
COVERTS = [(250, 262), (276, 258), (300, 268), (318, 292), (330, 326), (336, 362), (336, 398), (330, 432), (316, 452),
           (296, 462), (272, 466), (246, 466), (222, 462), (200, 456), (180, 448), (164, 436), (156, 416), (158, 390),
           (166, 360), (180, 330), (198, 304), (222, 280)]
# pennen (as van wortel naar punt, breedte): de langste (handpennen) voor/onder, korter naar achteren/boven
FEATHERS = [((306, 420), (250, 930), 46),
            ((282, 420), (236, 870), 50),
            ((256, 420), (222, 800), 52),
            ((228, 420), (206, 720), 54),
            ((196, 420), (186, 640), 52)]
STREAKS = [((396, 520), (400, 548)), ((418, 590), (420, 612)), ((380, 600), (384, 626)), ((404, 470), (407, 494)),
           ((360, 660), (364, 684)), ((424, 540), (426, 560)),
           ((200, 330), (206, 352)), ((236, 300), (242, 322)), ((272, 296), (276, 318)), ((300, 330), (304, 352)),
           ((214, 380), (218, 402)), ((256, 360), (260, 382)), ((290, 390), (294, 412)), ((184, 400), (188, 420)),
           ((240, 420), (244, 440))]


def tf(p, k=1.0):
    return ((MIRX - p[0]) * SS * k, (p[1] - Y0) * SS * k)


def feather_pts(root, tip, w):
    """Lange pen: volle breedte, afgeronde punt (eigen gladde vorm)."""
    A, B = np.array(root, float), np.array(tip, float)
    v = B - A; L = np.linalg.norm(v); u = v / L; n = np.array((-u[1], u[0]))
    prof = [(0.0, 0.5), (0.25, 0.5), (0.6, 0.48), (0.82, 0.42), (0.93, 0.3), (0.985, 0.14)]
    left = [tuple(A + u * L * t + n * w * s) for t, s in prof]
    right = [tuple(A + u * L * t - n * w * s) for t, s in prof[::-1]]
    return left + [tuple(B)] + right


def head_inner_mouth(cv, mouth, inner, px):
    """Vloeiende muil: licht bij de rand, donker achterin onder de bovensnavel (geen ringen)."""
    W, H = cv.size
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # keel: achterin onder de bovensnavel (leidraad (420, 290))
    gx, gy = cv.tf((420, 292))
    rx, ry = 120 * px, 150 * px
    d = np.sqrt(((xx - gx) / rx) ** 2 + ((yy - gy) / ry) ** 2)
    t = np.clip(d, 0, 1)
    stops = [(0.0, C['m3']), (0.35, C['m2']), (0.7, C['m1']), (1.0, C['m0'])]
    out = np.zeros((H, W, 3), np.float32)
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        a, b = np.array(hexc(c0), np.float32), np.array(hexc(c1), np.float32)
        sel = (t >= t0) & (t <= t1)
        f = ((t - t0) / (t1 - t0))[..., None]
        out[sel] = (a + (b - a) * f)[sel]
    img = Image.fromarray(out.astype(np.uint8), 'RGB').convert('RGBA')
    cv.im.paste(img, (0, 0), inner)


def draw_head(cv, px):
    """Kop + muil + snavel van ronde 7 (zelfde vormen en lijnen); alleen muilbinnenkant en borstelveertjes nieuw."""
    head = cv.mask(R7.L_HEAD + R7.L_FAR[::-1][1:] + R7.L_JAWOUT[::-1][1:-1])
    mouth_pts = R7.L_GAPE[:-1] + [(504, 252), (510, 256)] + R7.L_FAR[::-1][1:] + R7.L_NEAR[::-1][1:-1]
    mouth = cv.mask(mouth_pts)
    jaw = ImageChops.subtract(cv.mask(R7.L_JAWOUT + R7.L_FAR[::-1][1:-1] + [(510, 256)] + R7.L_GAPE[::-1][1:-1]), mouth)
    sil = ImageChops.lighter(head, mouth)
    cv.fill(sil, C['fur']); cv.shade(sil, C['shade'], 16 * px)
    cv.fill(jaw, C['jawfur'])
    cv.fill(mouth, C['lip'])
    inner = erode(mouth, 3.5 * px)
    head_inner_mouth(cv, mouth, inner, px)
    tng = cv.mask([(398, 380), (410, 378), (416, 420), (408, 445), (398, 420)])
    tm = ImageChops.multiply(tng, erode(inner, 4 * px)).filter(ImageFilter.GaussianBlur(3 * px))
    cv.fill(tm.point(lambda v: int(v * 0.55)), C['m0'])
    for (x, y), (rx, ry) in R7.L_SLITS:
        cv.fill(cv.mask([(x + math.cos(a) * rx, y + math.sin(a) * ry) for a in np.linspace(0, 2 * math.pi, 24)]), C['slit'])
    tip = R7.L_NEAR[-1]
    rim = ImageChops.subtract(ImageChops.lighter(mouth, jaw), inner)
    for col, r in ((C['b1'], 30), (C['jt'], 14)):
        cm = cv.mask([(tip[0] + math.cos(a) * r, tip[1] + 4 + math.sin(a) * r) for a in np.linspace(0, 2 * math.pi, 24)])
        cv.fill(ImageChops.multiply(cm, rim), col)
    # bovensnavel (ronde 7)
    bill = cv.mask(R7.L_BILL)
    A, B = np.array(R7.L_BILL_BASE, float), np.array(R7.L_BILL_TIP, float)
    cols = [hexc(C[c]) for c in ('b0', 'b1', 'b2', 'b3')]
    grad = Image.new('RGBA', cv.size); gd = ImageDraw.Draw(grad)
    v = B - A; u = v / np.linalg.norm(v); nrm = np.array((-u[1], u[0]))
    for i in range(60):
        t0, t1 = i / 60, (i + 1) / 60
        t = (t0 + t1) / 2; k = min(int(t * 3), 2); f = t * 3 - k
        col = tuple(int(cols[k][j] + (cols[k + 1][j] - cols[k][j]) * f) for j in range(3)) + (255,)
        p0, p1 = A + v * (t0 * 1.3 - 0.15), A + v * (t1 * 1.3 - 0.15)
        gd.polygon(cv.P([tuple(p0 + nrm * 200), tuple(p1 + nrm * 200), tuple(p1 - nrm * 200), tuple(p0 - nrm * 200)]), fill=col)
    cv.im.paste(grad, (0, 0), bill)
    # bevederde snavelrug: kleine schubveertjes (boogjes) in rijen van voor het oog naar de snavelbasis
    rows = [[(424, 214), (438, 222), (452, 230), (466, 238)],
            [(420, 232), (434, 238), (448, 244), (461, 249)],
            [(432, 200), (446, 210), (460, 220), (473, 230)]]
    for row in rows:
        for (x, y) in row:
            arc = [(x - 7, y - 5), (x - 2, y + 1), (x + 5, y + 3)]
            cv.line(arc, 1.5 * px, closed=False, col='brush')
    r = R7.L_ER * 1.08 * px
    cv.ellipse(R7.L_EYE, r, r, 'eye', 'line', 3.2 * px)
    cv.line(R7.L_JAWOUT, 4.5 * px, closed=False)
    cv.line(mouth_pts, 3.8 * px)
    cv.line(R7.L_BILL[1:-1], 3.6 * px, closed=False)
    # achterhoofd over de schouder: binnenlijn (vorm over vorm)
    cv.line([(290, 205), (292, 228), (300, 250), (312, 270), (322, 288)], 3.4 * px, closed=False)
    return ImageChops.lighter(ImageChops.lighter(sil, jaw), bill)


def streak(cv, a, b, w, col):
    A, B = np.array(cv.tf(a)), np.array(cv.tf(b))
    v = B - A; n = np.array((v[1], -v[0])) / np.linalg.norm(v)
    cv.d.polygon([tuple(A), tuple((A + B) / 2 + n * w), tuple(B), tuple((A + B) / 2 - n * w)], fill=hexc(C[col]))


def draw_full(k=1.0):
    size = (int((X1 - X0) * SS * k), int((Y1 - Y0) * SS * k))
    px = SS * k
    T = lambda p: ((MIRX - p[0]) * px - (MIRX - X1) * px, (p[1] - Y0) * px)
    cv = R7.Canvas(size, T)
    body = cv.mask(BODY)
    cv.fill(body, C['fur']); cv.shade(body, C['shade'], 14 * px)
    tail = ImageChops.multiply(body, cv.mask(TAIL_L + TAIL_TIP + TAIL_R + [(300, 700), (240, 690)]))
    cv.fill(tail, C['tail']); cv.shade(tail, C['wshade'], 6 * px)
    # staartbanden (schors)
    for y in (800, 870, 940, 1000):
        streak(cv, (226 + (y - 760) * -0.05, y), (268 + (y - 760) * -0.11, y + 4), 2.2 * px, 'bark2')
    # borst: schorsstreepjes
    for a, b in STREAKS[:6]:
        streak(cv, a, b, 2.4 * px, 'bark')
    # vleugel: pennen (langste eerst), dan dekveren met de boeg
    wing = Image.new('L', size, 0)
    for root, tip, w in FEATHERS:
        m = cv.mask(feather_pts(root, tip, w), smooth=False)
        cv.fill(m, C['wing']); cv.shade(m, C['wshade'], 6 * px)
        cv.line(feather_pts(root, tip, w)[1:-1], 3.0 * px, closed=False)
        A, B = np.array(root, float), np.array(tip, float)
        for t in (0.55, 0.72):           # schorsvlekjes op de pen
            p = A + (B - A) * t
            streak(cv, tuple(p + (0, -10)), tuple(p + (-2, 12)), 2.0 * px, 'bark')
        wing = ImageChops.lighter(wing, m)
    cov = cv.mask(COVERTS)
    cv.fill(cov, C['wing']); cv.shade(cov, C['wshade'], 7 * px)
    for a, b in STREAKS[6:]:
        streak(cv, a, b, 2.4 * px, 'bark')
    cv.line(COVERTS, 3.2 * px)
    # rijtje dekveertjes (boogjes) langs de onderrand van de dekveren
    for x in (176, 204, 232, 260, 288, 314):
        y = 444 + 0.12 * (x - 176) if x < 300 else 456 - 0.4 * (x - 300)
        cv.line([(x - 13, y - 10), (x, y + 2), (x + 13, y - 8)], 2.0 * px, closed=False, col='fline')
    # kop
    hsil = draw_head(cv, px)
    full = ImageChops.lighter(ImageChops.lighter(body, wing), ImageChops.lighter(cov, hsil))
    edge = ImageChops.subtract(full, erode(full, 5.0 * px))
    cv.fill(edge, C['line'])
    cv.im.putalpha(full)
    return cv.im


def outline_over(img, groups, tfp, w=2):
    d = ImageDraw.Draw(img)
    for pts, col, closed in groups:
        q = [tfp(p) for p in catmull(pts, closed)]
        if closed:
            q.append(q[0])
        d.line(q, fill=col, width=w)
    return img


if __name__ == '__main__':
    pop = draw_full()
    R6.fit(pop, 600).save(os.path.join(HERE, 'ronde8_spritehoek.png'))
