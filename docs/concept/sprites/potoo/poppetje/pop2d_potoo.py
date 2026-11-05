"""Great potoo ronde 6: het hele poppetje als 2D-vectortekening, met de hand overgetrokken (geen fotopixels,
geen segmentatie), gladde Catmull-Rom-curven, hoog getekend en met antialiasing verkleind.
- Lijf, vleugel, staart, kop en bovensnavel: van jordi_great_potoo_illustratie_LICHAAMSVORM.png (Jordi: "dit is de vorm
  van het lichaam"; kop op dezelfde plek op de schouders, geen nek, niet naar voren geschoven).
- Open muil (onderkaak als U naar een spitse punt, kom met twee spleetjes): naar de leidraad (linkerhelft van
  jordi_great_potoo_bek_open_duo.webp). Alleen de onderkaak klapt open om de mondhoek en hangt vóór de borst.
Alles staat in de coördinaten van de illustratie (vogel kijkt naar rechts) en wordt bij het tekenen gespiegeld (spritehoek
naar links). Kleur C2 (bijna wit met lila zweem), één schaduwtoon (licht linksboven), donkere lijn.
Draaien vanuit de repo-root: python3 docs/concept/sprites/potoo/poppetje/pop2d_potoo.py"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '../referenties')
ILL = os.path.join(REF, 'jordi_great_potoo_illustratie_LICHAAMSVORM.png')
LEID = os.path.join(REF, 'jordi_great_potoo_bek_open_duo.webp')
CLOSE = os.path.join(REF, 'jordi_great_potoo_kop_closeup_bek_open.webp')

# ------------------------------------------------------------------ overtrek van de illustratie (480 x 640 px)
# omtrek kop + lijf + staart, met de klok mee vanaf de kruin; bek dicht zoals op de illustratie (de kin wordt
# hieronder vervangen door de open muil)
CROWN_TO_BILL = [(165, 22), (180, 23), (192, 27), (201, 34), (209, 42), (215, 50), (218, 57)]      # voorhoofd -> snavelbasis
BACK = [(127, 42), (138, 32), (150, 25), (165, 22)]                                                 # achterhoofd -> kruin
BODY_RIGHT = [(222, 100), (228, 108), (236, 117), (246, 126), (254, 138), (259, 152), (261, 170), (262, 192), (262, 215),
              (261, 238), (259, 258), (255, 280), (249, 300), (241, 318), (230, 333), (216, 344), (206, 356), (202, 380),
              (201, 410), (200, 440), (199, 470), (198, 500), (196, 530), (193, 556), (189, 575), (184, 583)]
BODY_LEFT = [(178, 580), (172, 560), (167, 535), (161, 505), (156, 480), (150, 452), (144, 425), (139, 398), (134, 370),
             (130, 340), (126, 310), (122, 280), (118, 250), (115, 222), (113, 195), (112, 168), (112, 140), (112, 122),
             (111, 105), (112, 90), (114, 70), (119, 55), (127, 42)]
# gevouwen vleugel (nabij) met de vleugelboeg bij de schouder; de punten lopen ver langs de staart
WING = [(146, 128), (160, 120), (176, 116), (192, 116), (206, 121), (217, 132), (224, 150), (227, 175), (226, 205),
        (222, 238), (216, 272), (209, 305), (201, 340), (194, 380), (188, 420), (183, 460), (179, 495), (176, 520),
        (173, 538), (169, 545), (164, 530), (159, 500), (153, 465), (147, 430), (141, 395), (136, 360), (131, 325),
        (127, 290), (124, 255), (124, 220), (127, 190), (132, 162), (139, 140)]
WINGTIPS = [[(205, 330), (196, 380), (188, 430), (181, 480), (175, 525)],      # pennenranden (getrapte punten)
            [(214, 290), (206, 340), (199, 395), (193, 450)]]
EYE, ER = (190, 70), 10.0
# bovensnavel = één vorm: komt tussen de veren uit het gezicht (basis), rug naar voren, krult omlaag in de haak, en de
# snijrand loopt van de haak terug langs de onderkant; kleur van lichtgrijs (basis) naar donker (haak)
BILL = [(214, 77), (226, 74), (238, 73), (247, 74), (254, 78), (258, 83), (260, 89), (259, 94), (257, 96),
        (256, 91), (252, 88), (244, 86.5), (232, 86.5), (220, 87), (214, 84)]
BILL_BASE, BILL_TIP = (216, 80), (258, 95)
CORNER = (182, 90)                       # mondhoek, recht onder/achter het oog (illustratie)
GAPE = [(182, 90), (192, 89), (202, 88), (212, 87), (220, 86)]   # snijrand van het gezicht van de mondhoek tot de snavel
# onderkaak open (naar de leidraad: U naar een spitse punt, breed bij de mondhoeken; ±55° open, punt onder/achter de haak)
JAW_NEAR = [(182, 90), (182, 104), (185, 118), (190, 132), (197, 146), (205, 158), (214, 168), (222, 175), (228, 178)]
JAW_FAR = [(228, 178), (237, 170), (246, 158), (253, 144), (258, 130), (260, 116), (259, 104), (257, 97)]
JAW_OUT = [(177, 94), (176, 108), (178, 123), (183, 138), (190, 152), (199, 165), (209, 175), (219, 182), (228, 185),
           (235, 181)]
SLITS = [((226, 102), (1.6, 6.0)), ((229, 124), (1.4, 5.0))]         # twee donkere spleetjes (leidraad)
BRUSH = [((199, 60), (214, 66)), ((201, 52), (216, 60)), ((204, 68), (216, 72)), ((206, 45), (217, 54))]
STREAKS = [[(150, 160), (156, 195)], [(170, 150), (176, 190)], [(160, 220), (166, 262)], [(190, 200), (195, 240)],
           [(150, 300), (155, 340)], [(178, 290), (182, 330)], [(240, 180), (243, 215)], [(245, 240), (247, 270)],
           [(168, 400), (171, 440)]]

# ------------------------------------------------------------------ overtrek van de leidraad (1280 x 720 px), ter controle
L_EYE, L_ER = (379, 223), 30
L_GAPE = [(322, 288), (340, 282), (360, 277), (380, 272), (400, 266), (420, 260), (440, 256), (460, 253), (480, 250),
          (500, 250), (510, 255)]
L_NEAR = [(322, 288), (327, 300), (330, 312), (334, 326), (337, 340), (342, 355), (347, 370), (353, 382), (360, 393),
          (368, 405), (377, 417), (388, 429), (400, 440), (410, 450), (414, 457)]
L_FAR = [(414, 457), (422, 455), (430, 451), (440, 437), (447, 427), (453, 417), (460, 405), (467, 393), (471, 381),
         (475, 370), (479, 355), (483, 340), (488, 325), (493, 310), (502, 300), (510, 290), (513, 275), (512, 262), (510, 255)]
L_HEAD = [(322, 288), (312, 270), (300, 250), (292, 228), (290, 205), (293, 182), (300, 160), (312, 140), (328, 124),
          (346, 114), (365, 108), (385, 107), (405, 110), (425, 117), (443, 127), (460, 140), (475, 156), (488, 172),
          (499, 190), (507, 208), (513, 226), (517, 240), (514, 252), (510, 255)]

C = dict(fur='#F1EFF6', shade='#CEC8DA', wing='#E2DEEC', wshade='#BFB8CF', tail='#DAD5E5', line='#28223A',
         bark='#A99FB8', lip='#F2EADF', m0='#C9B8F0', m1='#A08CE6', m2='#7563CF', m3='#4C3E9C', slit='#231B52',
         jawfur='#E2DDEA', b0='#D4CDD6', b1='#B0A7B6', b2='#7E7489', b3='#4A4157', eye='#09080D', brush='#9A8FB0',
         jt='#6E6484')
SS = 4
W0, H0 = 480, 640
MIRROR = True


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def catmull(pts, closed=True, n=10):
    pts = [np.array(p, float) for p in pts]
    if closed and np.allclose(pts[0], pts[-1]):
        pts = pts[:-1]
    N = len(pts); out = []
    for i in (range(N) if closed else range(N - 1)):
        p0 = pts[(i - 1) % N] if closed else pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[(i + 1) % N]
        p3 = pts[(i + 2) % N] if closed else pts[min(i + 2, N - 1)]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    if not closed:
        out.append(pts[-1])
    return [tuple(p) for p in out]


class Canvas:
    def __init__(self, mirror=MIRROR):
        self.mirror = mirror
        self.size = (W0 * SS, H0 * SS)
        self.im = Image.new('RGBA', self.size, (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [(((W0 - x) if self.mirror else x) * SS, y * SS) for x, y in pts]

    def mask(self, pts, closed=True):
        m = Image.new('L', self.size, 0)
        ImageDraw.Draw(m).polygon(self.P(catmull(pts)) if closed else self.P(pts), fill=255)
        return m

    def fill(self, m, col):
        self.im.paste(Image.new('RGBA', self.size, hexc(col) + (255,)), (0, 0), m)

    def shade(self, m, col, d=10):
        """Eén schaduwtoon als sikkel aan de kant van rechtsonder (licht linksboven)."""
        s = ImageChops.subtract(m, ImageChops.offset(m, -d * SS // 2, -d * SS))
        self.fill(s, col)

    def line(self, pts, w=3.2, closed=True, col='line'):
        q = self.P(catmull(pts, closed))
        if closed:
            q = q + [q[0]]
        self.d.line(q, fill=hexc(C[col]), width=int(w * SS), joint='curve')
        r = w * SS / 2
        for p in (q[0], q[-1]):
            self.d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=hexc(C[col]))


def erode(m, px):
    return m.filter(ImageFilter.MinFilter(2 * int(px) + 1)) if px >= 1 else m


def draw(mirror=MIRROR):
    cv = Canvas(mirror)
    sil_pts = BACK + CROWN_TO_BILL[1:] + [(216, 72), (216, 86)] + [(214, 92), (218, 98)] + BODY_RIGHT + BODY_LEFT
    sil = cv.mask(sil_pts)
    jaw_out = cv.mask(JAW_OUT + JAW_FAR[::-1][:-1] + [(257, 97), (220, 86)] + [CORNER])
    sil = ImageChops.lighter(sil, jaw_out)
    # lijf + kop als één vacht, één schaduwtoon
    cv.fill(sil, C['fur']); cv.shade(sil, C['shade'], 12)
    # staart (onder de vleugelpunten) iets donkerder
    tail = ImageChops.multiply(sil, cv.mask([(140, 400), (205, 360), (202, 450), (198, 520), (189, 575), (182, 585), (172, 560), (160, 500), (148, 440)]))
    cv.fill(tail, C['tail'])
    # vleugel
    wing = cv.mask(WING)
    cv.fill(wing, C['wing']); cv.shade(wing, C['wshade'], 8)
    cv.line(WING, 2.6)
    for wt in WINGTIPS:
        cv.line(wt, 1.6, closed=False)
    # schorsvegen: korte gerichte streepjes op vleugel en flank
    for a, b in STREAKS:
        A, B = np.array(cv.P([a])[0]), np.array(cv.P([b])[0])
        v = B - A; n = np.array((v[1], -v[0])) / np.linalg.norm(v)
        cv.d.polygon([tuple(A), tuple((A + B) / 2 + n * 2.6 * SS), tuple(B), tuple((A + B) / 2 - n * 2.6 * SS)], fill=hexc(C['bark']))
    # onderkaak: bolle bevederde buitenkant (kin) vóór de borst
    cv.fill(jaw_out, C['jawfur'])
    # muil: binnenkant als kom (licht bij de rand, donkerder naar de keel achterin), lippen dun en licht
    mouth_pts = GAPE + [(232, 85), (244, 85), (252, 87), (256, 92), (257, 97)] + JAW_FAR[::-1][1:] + JAW_NEAR[::-1][1:-1]
    mouth = cv.mask(mouth_pts)
    cv.fill(mouth, C['lip'])
    inner = erode(mouth, 1.6 * SS)
    cv.fill(inner, C['m0'])
    # diepte: donker achterin onder de bovensnavel (bovenkant van de kom), lichter naar de kaakpunt
    for k, (col, cx, cy, rx, ry) in enumerate(((C['m1'], 222, 96, 40, 34), (C['m2'], 223, 92, 32, 20), (C['m3'], 224, 89, 22, 9))):
        e = cv.mask([(cx + math.cos(a) * rx, cy + math.sin(a) * ry) for a in np.linspace(0, 2 * math.pi, 40)])
        cv.fill(ImageChops.multiply(e, erode(inner, (1.5 + 1.2 * k) * SS)), col)
    for (x, y), (rx, ry) in SLITS:
        cv.fill(cv.mask([(x + math.cos(a) * rx, y + math.sin(a) * ry) for a in np.linspace(0, 2 * math.pi, 20)]), C['slit'])
    # kaakpunt: de kaak zelf wordt donkerder naar de punt
    tp = JAW_NEAR[-1]
    for col, r in ((C['b1'], 12), (C['jt'], 6)):
        cm = cv.mask([(tp[0] + math.cos(a) * r, tp[1] + 4 + math.sin(a) * r) for a in np.linspace(0, 2 * math.pi, 24)])
        cv.fill(ImageChops.multiply(cm, ImageChops.subtract(ImageChops.lighter(jaw_out, mouth), inner)), col)
    # bovensnavel: één vorm, kleurverloop van de basis naar de haak
    bill = cv.mask(BILL)
    A, B = np.array(BILL_BASE, float), np.array(BILL_TIP, float)
    cols = [hexc(C[c]) for c in ('b0', 'b1', 'b2', 'b3')]
    grad = Image.new('RGBA', cv.size)
    gd = ImageDraw.Draw(grad)
    v = B - A; L = np.linalg.norm(v); u = v / L; nrm = np.array((-u[1], u[0]))
    for i in range(60):
        t0, t1 = i / 60, (i + 1) / 60
        t = (t0 + t1) / 2
        k = min(int(t * 3), 2); f = t * 3 - k
        col = tuple(int(cols[k][j] + (cols[k + 1][j] - cols[k][j]) * f) for j in range(3)) + (255,)
        p0, p1 = A + v * (t0 - 0.3) * 1.6, A + v * (t1 - 0.3) * 1.6
        quad = [p0 + nrm * 60, p1 + nrm * 60, p1 - nrm * 60, p0 - nrm * 60]
        gd.polygon(cv.P([tuple(q) for q in quad]), fill=col)
    cv.im.paste(grad, (0, 0), bill)
    # borstelveertjes tussen/voor de ogen over de snavelbasis
    for a, b in BRUSH:
        A_, B_ = np.array(cv.P([a])[0]), np.array(cv.P([b])[0])
        vv = B_ - A_; n = np.array((vv[1], -vv[0])) / np.linalg.norm(vv)
        cv.d.polygon([tuple(A_ + n * 1.4 * SS), tuple(B_), tuple(A_ - n * 1.4 * SS)], fill=hexc(C['brush']))
    # oog: puur zwarte kraal, iets groter dan op de illustratie; geen glans, geen lichte rand
    r = ER * 1.25
    ex, ey = cv.P([EYE])[0]
    cv.d.ellipse((ex - r * SS, ey - r * SS, ex + r * SS, ey + r * SS), fill=hexc(C['eye']), outline=hexc(C['line']), width=int(2.4 * SS))
    # lijnen
    cv.line(JAW_OUT, 2.8, closed=False)
    cv.line(mouth_pts, 2.4)
    cv.line(BILL[1:-1], 2.4, closed=False)                            # geen lijn aan de basis: de snavel komt uit het gezicht
    cv.line(GAPE, 1.6, closed=False)
    # buitenomtrek als laatste (één doorlopende lijn om het hele poppetje)
    full = ImageChops.lighter(ImageChops.lighter(sil, jaw_out), ImageChops.lighter(bill, mouth))
    edge = ImageChops.subtract(full, erode(full, 3.2 * SS))
    cv.fill(edge, C['line'])
    cv.im.putalpha(full)
    return cv.im


def fit(im, size, pad=0.06):
    bb = im.split()[3].getbbox()
    im = im.crop(bb)
    k = size * (1 - 2 * pad) / max(im.size)
    im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    out = Image.new('RGB', (size, size), 'white')
    out.paste(im, ((size - im.width) // 2, (size - im.height) // 2), im)
    return out


def lines_over(img, groups, k, mirror_w=None, off=(0, 0), wdt=2):
    d = ImageDraw.Draw(img)
    for pts, col, closed in groups:
        q = catmull(pts, closed)
        q = [((((mirror_w - x) if mirror_w else x) - off[0]) * k, (y - off[1]) * k) for x, y in q]
        if closed:
            q.append(q[0])
        d.line(q, fill=col, width=wdt)
    return img


def vel():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    W, H = 1360, 1250
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    lab = lambda x, y, t: d.text((x, y), t, font=F, fill=(60, 60, 60))
    d.text((12, 8), 'Great potoo ronde 6: 2D-tekening, met de hand overgetrokken (lijf + kop + snavel van de illustratie, open muil naar de leidraad)', font=FB, fill=(30, 30, 30))
    RED, ORA, BLU = (230, 30, 30), (255, 140, 0), (30, 120, 255)
    # (a) overtrek over de illustratie (groot)
    ill = Image.open(ILL).convert('RGB')
    k = 1.25
    a = ill.resize((int(480 * k), int(640 * k)), Image.LANCZOS)
    sil = BACK + CROWN_TO_BILL[1:] + [(216, 72), (216, 86), (214, 92), (218, 98)] + BODY_RIGHT + BODY_LEFT
    lines_over(a, [(sil, RED, True), (WING, BLU, True), (BILL, ORA, True)] + [(wt, BLU, False) for wt in WINGTIPS], k)
    dd = ImageDraw.Draw(a)
    dd.ellipse(((EYE[0] - ER) * k, (EYE[1] - ER) * k, (EYE[0] + ER) * k, (EYE[1] + ER) * k), outline=RED, width=2)
    a = a.crop((80, 0, 400, 760))
    im.paste(a, (10, 36)); lab(14, 800, '(a) overtrek over de illustratie: rood omtrek, blauw vleugel, oranje snavel')
    # (b) leidraad met de overtrek van de open muil (gespiegeld niet nodig: alleen controle van de vorm)
    ld = Image.open(LEID).convert('RGB').crop((270, 90, 540, 470))
    kb = 1.2
    ld = ld.resize((int(270 * kb), int(380 * kb)), Image.LANCZOS)
    lines_over(ld, [(L_HEAD, RED, False), (L_GAPE, ORA, False), (L_NEAR, ORA, False), (L_FAR, ORA, False)], kb, off=(270, 90))
    dd = ImageDraw.Draw(ld)
    dd.ellipse(((L_EYE[0] - L_ER - 270) * kb, (L_EYE[1] - L_ER - 90) * kb, (L_EYE[0] + L_ER - 270) * kb, (L_EYE[1] + L_ER - 90) * kb), outline=RED, width=2)
    im.paste(ld, (340, 36)); lab(344, 500, '(b) leidraad: overtrek kop (rood) en muil (oranje)')
    # (c) het poppetje in de spritehoek (gespiegeld: kijkt naar links)
    pop = draw(True)
    big = fit(pop, 600)
    im.paste(big, (680, 30)); lab(684, 632, '(c) poppetje, spritehoek (naar links)')
    # (d) 64 px 1x en 3x
    s64 = fit(pop, 64, pad=0.02)
    im.paste(s64, (690, 660)); im.paste(s64.resize((192, 192), Image.NEAREST), (770, 660)); lab(690, 856, '(d) 64 px: 1x en 3x')
    # (e) ronde 5
    try:
        r5 = Image.open(os.path.join(HERE, 'vel_ronde5.png')).crop((10, 34, 410, 434)).resize((190, 190), Image.LANCZOS)
        im.paste(r5, (990, 660)); lab(994, 856, '(e) ronde 5')
    except FileNotFoundError:
        pass
    # (f) snavelpaneel: alleen de snavel, naast de illustratie-uitsnede en de close-up
    y = 880
    bill_only = draw(False).crop((205 * SS, 50 * SS, 268 * SS, 110 * SS)).resize((300, 286), Image.LANCZOS)
    bg = Image.new('RGB', bill_only.size, 'white'); bg.paste(bill_only, (0, 0), bill_only)
    ic = ill.crop((205, 50, 268, 110)).resize((300, 286), Image.LANCZOS)
    cu = Image.open(CLOSE).convert('RGB').crop((560, 520, 900, 900)).resize((300, 335), Image.LANCZOS)
    im.paste(ic, (340, y)); lab(344, y + 290, '(f) snavel op de illustratie')
    im.paste(bg, (660, y)); lab(664, y + 290, 'snavel van het poppetje (zelfde uitsnede)')
    im.paste(cu, (980, y)); lab(984, y + 338, 'close-up: snavel (foto)')
    im.save(os.path.join(HERE, 'vel_ronde6.png'))
    big.save(os.path.join(HERE, 'ronde6_spritehoek.png'))


if __name__ == '__main__':
    vel()
