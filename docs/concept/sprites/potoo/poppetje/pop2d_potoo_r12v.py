"""Great potoo ronde 12, diagnosevarianten (basis ronde 11, één ding per stap):
v1 = snavel als twee delen (lichte onderkaakrand langs de hele onderrand van de muil, klein hoornstuk vast aan de bovenrand
dat in de haak eindigt) + oog naar voren boven de achterste helft van de bovenrand (afstand oog-rand ±0,55 oogstraal);
v2 = v1 + roze muil; v3 = v1 + sterker grijsbruin schorspatroon; v4 = v1 + roze muil + sterker patroon.
Ronde 11 (basis ronde 10; blinde test r10: "paars vlak als vizier/masker, glas", "grijze rand als kromme
snavelpunt"): geen grijze snijrand meer langs de muil (gezichtsveren lopen door tot de dunne lip); snavel = alleen het korte
hoornstukje vóóraan dat in de haak eindigt; muil mat in vlakke zachte tonen (lip, middentoon, indigo diep onder het
gehemelte), bevederde wang valt over de nabije mondrand; voorhoofd bolt iets verder naar voren; mantel lager zodat hij de
koepel niet afsnijdt.
Ronde 10 (basis ronde 9; blinde test r9: "haakje met driehoekige zak", "kop als losse bol op de vleugel",
"lijf glad buis/kegel"): muil als brede U (onderkaak bolt uit, stompe punt; nooit smaller dan de leidraad), kleinere korte
haak, mantel/schouderveren hoog achter en naast de kop (gebocheld, geen nek) met één doorlopende ruige omtrek, veerpunten
langs rug, flank en borst, dons onder de kin, vleugel met eigen rand.
Ronde 9 (basis ronde 8, blinde test r8 "parkiet"): snijrand van de bovensnavel als hard deel langs de hele
bovenrand van de muil (haak = voorhoek van de open bek), licht ruige bevederde kopomtrek die in de schouders overloopt,
zachte spleten in de muil, bredere stompe staart en voller lijf, schorsachtige streepjes en vegen over kop, borst en vleugel.
Ronde 8:
- Kop + snavel + muil: ongewijzigd uit ronde 7 (overtrek van de leidraad, linkerhelft van jordi_great_potoo_bek_open_duo.webp).
  Alleen de binnenkant van de muil is vloeiend (geen ringen) en de borstelveertjes zijn fijne veertjes langs de snavelrug.
- Lijf: met de hand overgetrokken naar jordi_great_potoo_illustratie_LICHAAMSVORM.png (Jordi: "kijk dit is de vorm van het
  lichaam"): rechtop, brede schouders direct onder de kop met de vleugelboeg, gevouwen vleugel langs de flank met getrapte
  pennen ver naar beneden, smal taps lijf, lange staart. Meegedraaid naar de kijker (3/4) zoals het lijf op de leidraad zelf
  (schouder/vleugel achter de kop, borst onder de kaak); breedte ±1,35x de kop (nachtfoto: ±1,5x van voren).
- Alles in leidraadpixels (vogel kijkt naar rechts) en bij het tekenen gespiegeld (spritehoek naar links).
Geen fotopixels: alleen eigen gladde vormen, op 4x getekend en verkleind.
Draaien vanuit de repo-root: python3 docs/concept/sprites/potoo/poppetje/pop2d_potoo_r12v.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop2d_potoo as R6
import pop2d_potoo_r7 as R7
from pop2d_potoo import catmull, hexc, erode

# muil als brede U: beide kaakhelften bollen naar buiten (meest halverwege), de punt wordt stomper; haak korter
def _u(p, A=16.0, ramp=False):
    x, y = p
    f = max(0.0, math.sin(math.pi * min(1.0, max(0.0, (y - 288) / (472 - 288))))) ** 0.8
    if ramp:                                    # voorhoek (onder de haak) blijft op de leidraad, daarna vloeiend uitbollen
        r = min(1.0, max(0.0, (y - 300) / 90)); f *= r * r * (3 - 2 * r)
    x = x + (A * f if x > 416 else -A * f)
    if y > 425:
        y = y - (y - 425) * 0.35
    return (x, y)


if not getattr(R7, '_U_DONE', False):
    R7.L_NEAR = [_u(p) for p in R7.L_NEAR]
    R7.L_FAR = [R7.L_FAR[0]] + [_u(p, ramp=True) for p in R7.L_FAR[1:]]
    R7.L_FAR[0] = R7.L_NEAR[-1]
    R7.L_JAWOUT = [_u(p, 18.0) for p in R7.L_JAWOUT]
    HK = 0.92                                   # haak: 1,15 -> ±0,97x de foto (kort snaveltje)
    R7.L_BILL = [(460 + (x - 460) * HK, 248 + (y - 248) * HK) for x, y in R7.L_BILL]
    R7.L_BILL_TIP = (460 + (R7.L_BILL_TIP[0] - 460) * HK, 248 + (R7.L_BILL_TIP[1] - 248) * HK)
    # voorhoofd bolt verder naar voren over de muil (koepel), meest rond y 205, niet bij de snavelbasis/mondhoek
    R7.L_HEAD = [(x + 9 * max(0.0, math.sin(math.pi * (y - 140) / (250 - 140))) if (x > 440 and 140 < y < 250) else x, y)
                 for x, y in R7.L_HEAD]
    R7._U_DONE = True

PINK, STRONG = False, False
PURPLE = dict(mlight='#B6A6E6', mmid='#8F7ED6', mdeep2='#4B3D98', slit2='#2C2270', lip='#E6D4E8')
ROZE = dict(mlight='#F1B9C1', mmid='#DE8E9B', mdeep2='#8E3E57', slit2='#5E1F38', lip='#F3DADB')
# oog: naar voren tot boven de achterste helft van de bovenrand; afstand oog-rand ±0,55 oogstraal
EYE_R = R7.L_ER * 1.08
_ex = R7.L_EYE[0] + 24
_gy = float(np.interp(_ex, [p[0] for p in R7.L_GAPE], [p[1] for p in R7.L_GAPE]))
EYE = (_ex, _gy - 0.55 * EYE_R - EYE_R)
C = R6.C                                    # zelfde dict als ronde 6/7 (Canvas.line leest hieruit)
C.update(jawrim='#F4EEF6', sb1='#8C7F78', sb2='#A69890', sb3='#6E625E', mlight='#B6A6E6', mmid='#8F7ED6', mdeep1='#6D5CC0', mdeep2='#4B3D98', lip='#E6D4E8', slit2='#2C2270', breast='#E9E6F0', feather='#DCD7E7', fline='#8F86A6', bark2='#BDB4CB')

SS = 4
X0, X1, Y0, Y1 = 60, 600, 80, 1080            # tekenvak in leidraadpixels
MIRX = X1

# ------------------------------------------------------------------ lijf (leidraadpixels, vogel kijkt naar rechts)
# rug: komt achter het achterhoofd vandaan (geen nek), brede schouder, smal taps naar de staart
BACK = [(304, 188), (290, 196), (272, 202), (252, 209), (231, 220), (210, 236), (191, 256), (174, 282), (158, 314),
        (144, 350), (131, 386), (121, 420), (116, 452), (118, 484), (128, 516), (140, 552), (152, 588), (162, 622),
        (170, 656), (176, 690), (180, 720)]
# staart: lang, smal, licht naar achteren hangend (voorover zittende vogel)
TAIL_L = [(180, 720), (182, 780), (184, 840), (186, 900), (188, 944)]
TAIL_TIP = [(192, 962), (214, 970), (242, 972), (270, 968), (290, 958)]
TAIL_R = [(296, 938), (302, 884), (312, 830), (326, 784), (348, 748)]
# borst/buik: van de staartbasis omhoog tot achter de kaak; recht en taps (illustratie), geen eibuik
BELLY = [(366, 734), (388, 708), (406, 674), (420, 634), (430, 588), (435, 538), (436, 488), (432, 440)]
# verre vleugel: smalle reep langs de verre borstrand onder de kaak (verre schouder net zichtbaar)
FAR_WING = [(434, 452), (436, 500), (432, 550), (424, 600), (412, 646), (396, 686), (392, 674), (404, 636), (414, 590),
            (420, 540), (422, 492), (420, 456)]
BODY = BACK + TAIL_L[1:] + TAIL_TIP + TAIL_R + BELLY + [(420, 340), (340, 262)]

# vleugel: dekveren (bovenrand = de rug, geen dubbele lijn) met de boeg vóór onder de kaak; daaronder getrapte pennen
COV_EDGE = [(122, 402), (130, 432), (158, 452), (212, 468), (252, 480), (292, 488), (328, 488), (354, 478), (364, 458),
            (360, 424), (350, 384), (336, 344), (320, 302), (306, 268), (298, 246)]
COVERTS = [p for p in BACK if p[1] <= 402] + COV_EDGE[1:]
# pennen (wortel, punt, breedte): handpennen voor en het langst, armpennen korter naar achteren
FEATHERS = [((344, 470), (272, 905), 64),
            ((308, 462), (250, 850), 68),
            ((270, 456), (226, 784), 70),
            ((228, 450), (196, 716), 74),
            ((178, 440), (160, 650), 76)]
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
    """Matte muil: vlakke tonen met zachte randen (geen glans, geen ringen): middentoon paars, daaronder een halve maan
    indigo diep achterin onder het gehemelte (langs de bovenrand), met een smalle tussentoon."""
    cv.fill(inner, C['mmid'])
    # holte: één donkere vlek diep achterin (bovenmidden, rond de keel en de spleten), zachte rand, geen banden
    deep = [(352, 282), (380, 276), (410, 270), (440, 264), (468, 262), (480, 276), (478, 306), (466, 340), (448, 372),
            (424, 392), (402, 392), (384, 372), (368, 340), (356, 308)]
    z = cv.mask(deep).filter(ImageFilter.GaussianBlur(9 * px))
    cv.fill(ImageChops.multiply(z, inner), C['mdeep2'])
    # lichte kom naar de kaakpunt (lager, buiten de holte), zacht
    lowz = cv.mask([(372, 420), (400, 412), (432, 414), (452, 430), (440, 452), (414, 458), (388, 448)]).filter(ImageFilter.GaussianBlur(8 * px))
    cv.fill(ImageChops.multiply(lowz.point(lambda v: v // 2), inner), C['mlight'])


def ferode(m, r, q=4):
    """Snelle erosie: op 1/q rekenen, glad terugschalen en afkappen."""
    sm = m.resize((m.width // q, m.height // q), Image.BOX).filter(ImageFilter.MinFilter(2 * max(1, round(r / q)) + 1))
    return sm.resize(m.size, Image.BILINEAR).point(lambda v: 255 if v >= 128 else 0)


def draw_head(cv, px):
    """Kop + muil + snavel van ronde 7 (zelfde vormen en lijnen); alleen muilbinnenkant en borstelveertjes nieuw."""
    head = cv.mask(R7.L_HEAD + R7.L_FAR[::-1][1:] + R7.L_JAWOUT[::-1][1:-1])
    mouth_pts = R7.L_GAPE[:-1] + [(504, 252), (510, 256)] + R7.L_FAR[::-1][1:] + R7.L_NEAR[::-1][1:-1]
    mouth = cv.mask(mouth_pts)
    jaw = ImageChops.subtract(cv.mask(R7.L_JAWOUT + R7.L_FAR[::-1][1:-1] + [(510, 256)] + R7.L_GAPE[::-1][1:-1]), mouth)
    sil = ImageChops.lighter(head, mouth)
    hc = np.array((400.0, 235.0))
    curve = catmull(R7.L_HEAD[1:15], closed=False, n=6)
    tufts = Image.new('L', cv.size, 0); td = ImageDraw.Draw(tufts)
    acc, last = 0.0, np.array(curve[0])
    for p in curve[1:]:
        p = np.array(p); acc += np.linalg.norm(p - last); last = p
        if acc < 25:
            continue
        acc = 0.0
        out = (p - hc) / np.linalg.norm(p - hc)
        back = np.array((-out[1], out[0]))            # langs de omtrek, naar achteren/onder (vogel kijkt naar rechts)
        if back[0] > 0:
            back = -back
        q = [tuple(p - back * 11 - out * 2), tuple(p - back * 4 + out * 2.5), tuple(p + back * 3 + out * 4),
             tuple(p + back * 8 + out * 3.2), tuple(p + back * 7 - out * 2)]
        td.polygon(cv.P(catmull(q, closed=True, n=6)), fill=255)
    sil = ImageChops.lighter(sil, tufts)
    cv.fill(sil, C['fur']); cv.shade(sil, C['shade'], 16 * px)
    cv.fill(jaw, C['jawfur'])
    cv.fill(mouth, C['lip'])
    inner = erode(mouth, 3.5 * px)
    head_inner_mouth(cv, mouth, inner, px)
    for (x, y), (rx, ry) in R7.L_SLITS:                 # zachte langgerekte spleten (leidraad), niet zwart
        ry2 = ry * 1.6
        lens = [(x + math.sin(a) * rx * 0.8 * abs(math.sin(a)) ** 0.3, y - math.cos(a) * ry2) for a in np.linspace(0, 2 * math.pi, 40)]
        sm = ImageChops.multiply(cv.mask(lens), inner).filter(ImageFilter.GaussianBlur(1.2 * px))
        cv.fill(sm, C['slit2'])
    # onderkaak als eigen deel: lichte kaakrand langs de hele onderrand van de muil (mondhoek -> punt -> voorhoek)
    gtop = [(x, y + 15) for x, y in catmull(R7.L_GAPE, closed=False)]
    topzone = cv.mask([(300, 150), (540, 150), (540, gtop[-1][1])] + gtop[::-1], smooth=False)
    e1, e2 = ferode(mouth, 7 * px), ferode(mouth, 9 * px)
    band = ImageChops.subtract(ImageChops.subtract(mouth, e1), topzone)
    bline = ImageChops.subtract(ImageChops.subtract(e1, e2), topzone)
    cv.fill(bline, C['jt'])
    cv.fill(band, C['jawrim'])
    tip = R7.L_NEAR[-1]
    rim = ImageChops.subtract(ImageChops.lighter(mouth, jaw), inner)
    for col, r in ((C['b1'], 30), (C['jt'], 14)):
        cm = cv.mask([(tip[0] + math.cos(a) * r, tip[1] + 4 + math.sin(a) * r) for a in np.linspace(0, 2 * math.pi, 24)])
        cv.fill(ImageChops.multiply(cm, rim), col)
    # bovensnavel = alleen het korte hoornstukje vóóraan: komt uit de gezichtsveren en eindigt in de haak (één vorm)
    gg = [p for p in catmull(R7.L_GAPE, closed=False) if 428 <= p[0] <= 476]
    sliver = [(x, y - 7 * (x - 428) / 48) for x, y in gg] + [(x, y + 2) for x, y in gg[::-1]]
    bill = ImageChops.lighter(cv.mask(R7.L_BILL), cv.mask(sliver, smooth=False))
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
    for (x, y) in ((442, 210), (454, 218), (466, 227), (476, 236),
                   (446, 228), (458, 236), (469, 243),
                   (450, 198), (462, 207)):
        cv.line([(x - 5, y - 7), (x + 2, y - 3), (x + 4, y + 1), (x - 1, y + 6)], 1.7 * px, closed=False, col='brush')
    r = EYE_R * px
    cv.ellipse(EYE, r, r, 'eye', 'line', 3.2 * px)
    cv.line(R7.L_JAWOUT, 4.5 * px, closed=False)
    cv.line(mouth_pts, 3.8 * px)
    cv.im.paste(grad, (0, 0), bill)                     # hoornstuk óver de mondlijn: vast aan de bovenrand, haak vóór
    cv.line([sliver[0]] + sliver[len(gg) // 2:len(gg)] + R7.L_BILL[2:-1], 3.6 * px, closed=False)
    # bevederde wang van de nabije kant valt over de mondrand (muil = holte in de kop, geen paneel ervoor)
    near = [p for p in catmull(R7.L_NEAR, closed=False) if p[1] <= 380]
    inner_edge = [(x + 11 * math.sin(math.pi * (y - 288) / 92) ** 0.6 + 2.5 * math.sin(y / 7.0), y) for x, y in near]
    cheek = cv.mask([(x - 8, y) for x, y in near] + inner_edge[::-1], smooth=False)
    cv.fill(cheek, C['jawfur'])
    cv.line(inner_edge[::2], 3.0 * px, closed=False)
    # achterhoofd over de mantel: zachte binnenlijn (vorm over vorm, donkere tint van het vlak)
    cv.line([(296, 168), (291, 190), (293, 215), (300, 240)], 2.4 * px, closed=False, col='fline')
    return ImageChops.lighter(ImageChops.lighter(sil, jaw), bill), mouth, bill


def streak(cv, a, b, w, col):
    A, B = np.array(cv.tf(a)), np.array(cv.tf(b))
    v = B - A; n = np.array((v[1], -v[0])) / np.linalg.norm(v)
    cv.d.polygon([tuple(A), tuple((A + B) / 2 + n * w), tuple(B), tuple((A + B) / 2 - n * w)], fill=hexc(C[col]))


def ruffle(cv, pts, hint, every=24, size=1.0, start=0.0):
    """Afgeronde veerpuntjes langs een omtrek (bronpunten), naar buiten (hint) en met de punt omlaag/naar achteren."""
    curve = [np.array(p) for p in catmull(pts, closed=False, n=8)]
    m = Image.new('L', cv.size, 0); td = ImageDraw.Draw(m)
    acc = start
    hint = np.array(hint, float)
    for i in range(1, len(curve) - 1):
        acc += np.linalg.norm(curve[i] - curve[i - 1])
        if acc < every:
            continue
        acc = 0.0
        p = curve[i]; t = curve[i + 1] - curve[i - 1]; t = t / np.linalg.norm(t)
        out = np.array((t[1], -t[0]))
        if out @ hint < 0:
            out = -out
        back = t if t[1] > 0 else -t
        k = size
        q = [p - back * 11 * k - out * 2, p - back * 4 * k + out * 2.5 * k, p + back * 3 * k + out * 4 * k,
             p + back * 8 * k + out * 3.2 * k, p + back * 7 * k - out * 2]
        td.polygon(cv.P(catmull([tuple(v) for v in q], closed=True, n=6)), fill=255)
    return m


def bark_pattern(cv, full, skip, px, seed=9):
    """Schorsachtige streepjes en vegen (Hisui-Zorua-idee, licht binnen C2): korte gerichte lila-grijze streepjes over kop,
    borst, vleugel en staart; nooit op lijnen, oog, snavel of in de muil."""
    rng = np.random.default_rng(seed)
    q = 4                                     # maskers op 1/4 (snel)
    sz = (cv.size[0] // q, cv.size[1] // q)
    small = cv.im.convert('RGB').resize(sz, Image.BOX)
    lum = np.asarray(small).astype(int).mean(axis=2)
    r = lambda v: 2 * max(1, int(round(v / q))) + 1
    dark = Image.fromarray(((lum < 165) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(r(5 * px)))
    fs = full.resize(sz, Image.BOX).point(lambda v: 255 if v > 200 else 0).filter(ImageFilter.MinFilter(r(9 * px)))
    sk = skip.resize(sz, Image.BOX).point(lambda v: 255 if v > 0 else 0).filter(ImageFilter.MaxFilter(r(5 * px)))
    okA = np.asarray(ImageChops.subtract(ImageChops.subtract(fs, sk), dark)) > 0
    pts = []
    for _ in range(9000):
        x, y = rng.uniform(X0, X1), rng.uniform(Y0, Y1)
        X, Y = cv.tf((x, y)); X, Y = X / q, Y / q
        if not (0 <= X < okA.shape[1] and 0 <= Y < okA.shape[0]) or not okA[int(Y), int(X)]:
            continue
        if any((x - a) ** 2 + (y - b) ** 2 < (24 if STRONG else 36) ** 2 for a, b in pts):
            continue
        pts.append((x, y))
    for x, y in pts:
        L = rng.uniform(16, 28); ang = math.radians(rng.uniform(-22, 22) + (25 if y < 300 else 8))
        a = (x - math.sin(ang) * L / 2, y - math.cos(ang) * L / 2); b = (x + math.sin(ang) * L / 2, y + math.cos(ang) * L / 2)
        if STRONG:                           # grijsbruin gemêleerd: drie tonen, vaker vegen
            col = ['sb1', 'sb2', 'sb3'][int(rng.choice(3, p=[0.45, 0.35, 0.2]))]
            streak(cv, a, b, rng.uniform(2.4, 3.4) * px, col)
            if rng.uniform() < 0.55:
                streak(cv, (a[0] + 7, a[1] + 4), (b[0] + 7, b[1] + 1), 2.0 * px, 'sb2')
            continue
        col = 'bark' if rng.uniform() < 0.6 else 'bark2'
        streak(cv, a, b, rng.uniform(2.0, 2.8) * px, col)
        if rng.uniform() < 0.3:              # veeg: tweede streepje ernaast
            streak(cv, (a[0] + 7, a[1] + 4), (b[0] + 7, b[1] + 1), 1.8 * px, 'bark2')


def draw_full(k=1.0):
    size = (int((X1 - X0) * SS * k), int((Y1 - Y0) * SS * k))
    px = SS * k
    T = lambda p: ((MIRX - p[0]) * px - (MIRX - X1) * px, (p[1] - Y0) * px)
    cv = R7.Canvas(size, T)
    body = cv.mask(BODY)
    body = ImageChops.lighter(body, ruffle(cv, [p for p in BACK if p[1] < 600], (-1, 0), 34, 1.1))
    body = ImageChops.lighter(body, ruffle(cv, BELLY[::-1], (1, 0), 38, 1.0, 10))
    cv.fill(body, C['fur']); cv.shade(body, C['shade'], 14 * px)
    tail = ImageChops.multiply(body, cv.mask(TAIL_L + TAIL_TIP + TAIL_R + [(300, 700), (240, 690)]))
    cv.fill(tail, C['tail']); cv.shade(tail, C['wshade'], 6 * px)
    # staartbanden (schors)
    fw = ImageChops.multiply(cv.mask(FAR_WING + [(440, 700), (450, 440)][:0]), body)
    cv.fill(fw, C['wing'])
    cv.line(FAR_WING[6:] + FAR_WING[:1], 2.6 * px, closed=False, col='jt')
    # dons onder de kin: zachte boogjes op de borst onder de kaak
    for (x, y) in ((404, 478), (420, 490), (392, 498), (410, 512), (426, 522), (398, 530)):
        cv.line([(x - 9, y - 6), (x, y + 2), (x + 9, y - 5)], 1.9 * px, closed=False, col='fline')
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
        wing = ImageChops.lighter(wing, m)
    cov = cv.mask(COVERTS)
    cv.fill(cov, C['wing']); cv.shade(cov, C['wshade'], 7 * px)
    cv.line(COV_EDGE, 3.2 * px, closed=False)
    # rijtje dekveertjes (boogjes) langs de onderrand van de dekveren
    for dy, xs in ((-16, (172, 204, 236, 268, 300, 330)), (-62, (166, 198, 230, 262, 294, 322)), (-108, (190, 222, 254, 286, 312))):
        for x in xs:
            y = float(np.interp(x, [166, 212, 252, 292, 328, 354], [452, 468, 480, 488, 488, 478])) + dy
            cv.line([(x - 13, y - 9), (x, y + 2), (x + 13, y - 7)], 2.0 * px, closed=False, col='fline')
    # kop
    hsil, mouth, bill = draw_head(cv, px)
    full = ImageChops.lighter(ImageChops.lighter(body, wing), ImageChops.lighter(cov, hsil))
    bark_pattern(cv, full, ImageChops.lighter(mouth, bill), px)
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
    W, H = 1500, 1360
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    lab = lambda x, y, t: d.text((x, y), t, font=F, fill=(60, 60, 60))
    d.text((12, 8), 'Great potoo ronde 11: geen snijrandstreep, kort hoornsnaveltje, matte muil, wang over de mondrand (basis ronde 10)', font=FB, fill=(30, 30, 30))
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
    r10 = Image.open(os.path.join(HERE, 'ronde10_spritehoek.png')).resize((180, 180), Image.LANCZOS)
    im.paste(r10, (xd + 290, y0)); lab(xd + 294, y0 + 184, '(e) ronde 10')
    # (f) kop naast de gespiegelde leidraad, zelfde uitsnede en grootte
    box = (270, 90, 545, 480); kf = 1.0
    hp = pop.crop((int((X1 - box[2]) * SS), int((box[1] - Y0) * SS), int((X1 - box[0]) * SS), int((box[3] - Y0) * SS)))
    hw, hh2 = int((box[2] - box[0]) * kf), int((box[3] - box[1]) * kf)
    hp = hp.resize((hw, hh2), Image.LANCZOS)
    hb = Image.new('RGB', hp.size, 'white'); hb.paste(hp, (0, 0), hp)
    lf = Image.open(R6.LEID).convert('RGB').crop(box).transpose(Image.FLIP_LEFT_RIGHT).resize((hw, hh2), Image.LANCZOS)
    yf = y0 + 230
    im.paste(hb, (xd, yf)); im.paste(lf, (xd + hw + 10, yf)); lab(xd, yf + hh2 + 4, '(f) kop naast de gespiegelde leidraad (zelfde uitsnede)')
    im.save(os.path.join(HERE, 'vel_ronde11.png'))
    big.save(os.path.join(HERE, 'ronde11_spritehoek.png'))


BT = '/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/279ed44b-aa1d-54e2-8396-02fa8e081036/scratchpad/bt'
VARIANTS = [('v1', False, False, 'v1: snavel twee delen + oog naar voren'), ('v2', True, False, 'v2: v1 + roze muil'),
            ('v3', False, True, 'v3: v1 + sterker schorspatroon'), ('v4', True, True, 'v4: v1 + roze muil + sterker patroon')]


def run():
    global PINK, STRONG
    os.makedirs(BT, exist_ok=True)
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    imgs = []
    for name, pink, strong, label in VARIANTS:
        PINK, STRONG = pink, strong
        C.update(ROZE if pink else PURPLE)
        big = R6.fit(draw_full(), 640)
        big.save(os.path.join(BT, name + '.png'))
        imgs.append((big.resize((360, 360), Image.LANCZOS), label))
    vel = Image.new('RGB', (4 * 370 + 10, 400), 'white'); d = ImageDraw.Draw(vel)
    for i, (im, label) in enumerate(imgs):
        vel.paste(im, (10 + i * 370, 10)); d.text((14 + i * 370, 374), label, font=F, fill=(50, 50, 50))
    vel.save(os.path.join(HERE, 'vel_ronde12_varianten.png'))


if __name__ == '__main__':
    run()
