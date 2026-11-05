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
BACK = [(300, 236), (282, 244), (258, 254), (232, 266), (206, 282), (182, 302), (161, 328), (144, 360), (133, 396),
        (127, 435), (126, 472), (129, 510), (136, 548), (146, 585), (158, 622), (171, 658), (183, 692), (192, 722)]
# staart: lang, smal, licht naar achteren hangend (voorover zittende vogel)
TAIL_L = [(192, 722), (198, 790), (202, 860), (205, 930), (207, 980)]
TAIL_TIP = [(212, 1000), (232, 1012), (256, 1010), (272, 996)]
TAIL_R = [(277, 950), (286, 890), (298, 832), (314, 784), (336, 752)]
# borst/buik: van de staartbasis omhoog tot achter de kaak; recht en taps (illustratie), geen eibuik
BELLY = [(354, 738), (374, 714), (392, 682), (406, 640), (416, 592), (421, 540), (422, 488), (424, 440)]
# verre vleugel: smalle reep langs de verre borstrand onder de kaak (verre schouder net zichtbaar)
FAR_WING = [(426, 452), (424, 500), (420, 550), (412, 600), (400, 646), (384, 688), (380, 676), (392, 636), (402, 590),
            (408, 540), (410, 492), (412, 456)]
BODY = BACK + TAIL_L[1:] + TAIL_TIP + TAIL_R + BELLY + [(420, 340), (340, 262)]

# vleugel: dekveren (bovenrand = de rug, geen dubbele lijn) met de boeg vóór onder de kaak; daaronder getrapte pennen
COV_EDGE = [(133, 396), (140, 430), (166, 452), (212, 468), (252, 480), (292, 488), (328, 488), (354, 478), (364, 458),
            (360, 424), (350, 384), (336, 344), (320, 302), (306, 268), (298, 246)]
COVERTS = BACK[:9] + COV_EDGE[1:]
# pennen (wortel, punt, breedte): handpennen voor en het langst, armpennen korter naar achteren
FEATHERS = [((338, 470), (262, 940), 60),
            ((304, 462), (244, 880), 64),
            ((268, 456), (224, 806), 66),
            ((228, 450), (200, 730), 66),
            ((184, 440), (176, 650), 64)]
STREAKS = [((404, 482), (407, 504)), ((422, 520), (424, 542)), ((392, 540), (395, 562)), ((414, 580), (416, 602)),
           ((396, 622), (398, 642)), ((376, 662), (378, 680)),
           ((200, 330), (206, 352)), ((236, 300), (242, 322)), ((272, 296), (276, 318)), ((300, 330), (304, 352)),
           ((214, 380), (218, 402)), ((256, 360), (260, 382)), ((290, 390), (294, 412)), ((184, 400), (188, 420)),
           ((240, 420), (244, 440))]


def tf(p, k=1.0):
    return ((MIRX - p[0]) * SS * k, (p[1] - Y0) * SS * k)


def feather_pts(root, tip, w):
    """Lange pen: volle breedte, afgeronde punt (eigen gladde vorm)."""
    A, B = np.array(root, float), np.array(tip, float)
    v = B - A; L = np.linalg.norm(v); u = v / L; n = np.array((-u[1], u[0]))
    prof = [(0.0, 0.5), (0.25, 0.5), (0.6, 0.45), (0.82, 0.36), (0.93, 0.25), (0.985, 0.11)]
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
    cv.fill(tm.point(lambda v: int(v * 0.35)), C['m0'])
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
    # bevederde snavelrug: kleine schubveertjes (ronde punt naar de snavel), dakpansgewijs tussen oog en snavel
    for (x, y) in ((418, 206), (430, 214), (442, 222), (454, 231), (466, 239),
                   (420, 224), (433, 231), (446, 238), (458, 245),
                   (428, 196), (440, 204), (452, 212)):
        cv.line([(x - 5, y - 7), (x + 2, y - 3), (x + 4, y + 1), (x - 1, y + 6)], 1.7 * px, closed=False, col='brush')
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
    fw = ImageChops.multiply(cv.mask(FAR_WING + [(440, 700), (450, 440)][:0]), body)
    cv.fill(fw, C['wing'])
    cv.line(FAR_WING[6:] + FAR_WING[:1], 2.6 * px, closed=False, col='jt')
    # borst: schorsstreepjes
    for a, b in STREAKS[:6]:
        streak(cv, a, b, 2.4 * px, 'bark')
    # vleugel: pennen (langste eerst), dan dekveren met de boeg
    wing = Image.new('L', size, 0)
    for i, (root, tip, w) in enumerate(FEATHERS):
        pts = feather_pts(root, tip, w)
        m = cv.mask(pts, smooth=False)
        cv.fill(m, C['wing']); cv.shade(m, C['wshade'], 11 * px)
        # lijn alleen waar de pen over de volgende valt: achterrand (onderste deel) + punt; de voorste pen ook vóór
        cv.line(pts[1:9], 2.6 * px, closed=False, col='jt')                  # achterrand + punt (binnenlijn, lila)
        cv.line(pts[5:12], 2.6 * px, closed=False, col='jt')                 # punt + voorrand waar hij over de vorige valt
        if i == 0:
            cv.line(pts[8:13], 3.0 * px, closed=False)                       # voorrand van de vleugel over de borst
        A, B = np.array(root, float), np.array(tip, float)
        for t in (0.42, 0.6, 0.78):          # schorsvlekjes op de pen
            p = A + (B - A) * t
            streak(cv, tuple(p + (4, -11)), tuple(p + (2, 11)), 2.0 * px, 'bark')
        wing = ImageChops.lighter(wing, m)
    cov = cv.mask(COVERTS)
    cv.fill(cov, C['wing']); cv.shade(cov, C['wshade'], 7 * px)
    for a, b in STREAKS[6:]:
        streak(cv, a, b, 2.4 * px, 'bark')
    cv.line(COV_EDGE, 3.2 * px, closed=False)
    # rijtje dekveertjes (boogjes) langs de onderrand van de dekveren
    for dy, xs in ((-16, (172, 204, 236, 268, 300, 330)), (-62, (166, 198, 230, 262, 294, 322)), (-108, (190, 222, 254, 286, 312))):
        for x in xs:
            y = float(np.interp(x, [166, 212, 252, 292, 328, 354], [452, 468, 480, 488, 488, 478])) + dy
            cv.line([(x - 13, y - 9), (x, y + 2), (x + 13, y - 7)], 2.0 * px, closed=False, col='fline')
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


NACHT = os.path.join(R6.REF, 'jordi_great_potoo_nacht_stam_volledig.webp')


def hfit(im, h):
    return im.resize((max(1, int(im.width * h / im.height)), h), Image.LANCZOS)


def vel():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    W, H = 1500, 1250
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    lab = lambda x, y, t: d.text((x, y), t, font=F, fill=(60, 60, 60))
    d.text((12, 8), 'Great potoo ronde 8: nieuw lijf (illustratie, meegedraaid naar 3/4) onder de vaste kop van ronde 7', font=FB, fill=(30, 30, 30))
    RED, BLU, ORA = (230, 30, 30), (30, 120, 255), (255, 140, 0)
    groups = [(BODY, RED, True), (COVERTS, BLU, True)] + [(feather_pts(r, t, w), BLU, True) for r, t, w in FEATHERS]
    # (a1) lijf over de illustratie: schouder (y 236 -> 100) en staartpunt (1012 -> 583) gelijk, rug op rug
    ill = Image.open(R6.ILL).convert('RGB')
    s_ = (583 - 100) / (1012 - 236); ox = 111 - 146 * s_; oy = 100 - 236 * s_
    k = 1.0
    a1 = ill.copy()
    outline_over(a1, groups, lambda p: ((p[0] * s_ + ox) * k, (p[1] * s_ + oy) * k))
    a1 = a1.crop((60, 0, 330, 620))
    im.paste(a1, (10, 36)); lab(14, 660, '(a) lijf over de illustratie')
    lab(14, 676, '    (schouder + staartpunt gelijk; breder = 3/4-draai)')
    # (a2) hele omtrek over de leidraad (bovenlijf en kop zijn daar zichtbaar)
    ld = Image.open(R6.LEID).convert('RGB').crop((60, 80, 600, 720))
    kl = 0.97
    ld = ld.resize((int(ld.width * kl), int(ld.height * kl)), Image.LANCZOS)
    outline_over(ld, groups + [(R7.L_HEAD + R7.L_FAR[::-1][1:] + R7.L_JAWOUT[::-1][1:-1], ORA, True)],
                 lambda p: ((p[0] - 60) * kl, (p[1] - 80) * kl))
    im.paste(ld, (290, 36)); lab(294, 660, '(a) lijf + kop over de leidraad (foto loopt tot de tak)')
    pop = draw_full()
    big = R6.fit(pop, 640)
    im.paste(big, (830, 30)); lab(834, 660, '(b) poppetje, spritehoek (naar links)')
    # (c) gelijke hoogte
    y0, hh = 700, 380
    crop = pop.crop(pop.split()[3].getbbox())
    bg = Image.new('RGB', crop.size, 'white'); bg.paste(crop, (0, 0), crop)
    items = [(hfit(bg, hh), 'poppetje'),
             (hfit(Image.open(R6.LEID).convert('RGB').crop((80, 95, 540, 640)).transpose(Image.FLIP_LEFT_RIGHT), hh), 'leidraad (gespiegeld)'),
             (hfit(ill.crop((100, 15, 280, 590)).transpose(Image.FLIP_LEFT_RIGHT), hh), 'illustratie'),
             (hfit(Image.open(NACHT).convert('RGB').crop((330, 210, 660, 1010)), hh), 'nachtfoto')]
    x = 10
    for it, t in items:
        im.paste(it, (x, y0)); lab(x, y0 + hh + 4, t); x += it.width + 14
    lab(10, y0 + hh + 22, '(c) naast elkaar op gelijke hoogte')
    # (d) 64 px
    s64 = R6.fit(pop, 64, pad=0.03)
    xd = x + 20
    im.paste(s64, (xd, y0)); im.paste(s64.resize((192, 192), Image.NEAREST), (xd + 74, y0)); lab(xd, y0 + 196, '(d) 64 px: 1x en 3x')
    # (e) ronde 7
    r7 = Image.open(os.path.join(HERE, 'ronde7_spritehoek.png')).resize((180, 180), Image.LANCZOS)
    im.paste(r7, (xd + 290, y0)); lab(xd + 294, y0 + 184, '(e) ronde 7')
    im.save(os.path.join(HERE, 'vel_ronde8.png'))
    big.save(os.path.join(HERE, 'ronde8_spritehoek.png'))


if __name__ == '__main__':
    vel()
