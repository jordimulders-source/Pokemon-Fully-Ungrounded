"""Great potoo ronde 7: 2D-vectortekening. Kop + snavel + muil = nauwkeurige overtrek van de leidraad (linkerhelft van
jordi_great_potoo_bek_open_duo.webp, Jordi: "leidraad voor het hoofd"); lijf, vleugel en staart = overtrek van
jordi_great_potoo_illustratie_LICHAAMSVORM.png (Jordi: "dit is de vorm van het lichaam"), iets voller (Pokémon-stap).
De kop staat ±30° frontaler dan het lijf (zoals bij Pokémon-sprites) en sluit zonder nek op de schouders aan.
Bovensnavel = één vorm (basis tussen de veren, rug, haak als einde), naar de illustratie/close-up, in de hoek van de leidraad.
Geen fotopixels: alleen eigen gladde vormen, op 4× getekend en verkleind. Alles gespiegeld: de vogel kijkt naar links.
Draaien vanuit de repo-root: python3 docs/concept/sprites/potoo/poppetje/pop2d_potoo_r7.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop2d_potoo as R6
from pop2d_potoo import catmull, hexc, C, erode

REF = R6.REF
SS = 4

# ------------------------------------------------------------------ leidraad (fotopixels, vogel kijkt naar rechts)
L_EYE, L_ER = R6.L_EYE, R6.L_ER
L_GAPE, L_NEAR, L_FAR, L_HEAD = R6.L_GAPE, R6.L_NEAR, R6.L_FAR, R6.L_HEAD
# buitenkant van de nabije kaak (bevederde kin), net buiten de mondrand (leidraad: veren links van de muil)
L_JAWOUT = [(322, 288), (314, 300), (312, 318), (316, 338), (322, 357), (330, 376), (340, 394), (352, 411), (366, 427),
            (382, 442), (398, 455), (410, 464), (418, 466)]
# bovensnavel: één vorm, haak als einde; komt tussen de veren uit het gezicht boven de gaplijn
L_BILL = [(458, 246), (470, 241), (483, 238), (495, 238), (506, 242), (514, 249), (519, 259), (520, 271), (517, 284),
          (512, 295), (506, 303), (503, 297), (505, 287), (506, 276), (504, 266), (499, 259), (490, 255), (478, 254),
          (466, 255), (457, 256)]
L_BILL_BASE, L_BILL_TIP = (460, 250), (506, 302)
# Pokémon-stap: snavel 1,15x om de basis, zodat hij op 64 px leest
L_BILL = [(460 + (x - 460) * 1.15, 248 + (y - 248) * 1.15) for x, y in L_BILL]
L_BILL_TIP = (460 + (506 - 460) * 1.15, 248 + (302 - 248) * 1.15)
L_SLITS = [((388, 311), (5.5, 17)), ((394, 357), (4.5, 15))]
L_BRUSH = [((430, 236), (466, 248)), ((436, 224), (470, 240)), ((445, 213), (476, 232)), ((426, 247), (458, 254)),
           ((452, 204), (482, 226))]

# ------------------------------------------------------------------ plaatsing van de kop op het lijf (illustratiepixels)
KS = 0.60                     # kopschaal (Pokémon-stap: kop ±33% van de totale hoogte)
K_OFF = (108, 20)             # achterhoofd en kruin van de leidraadkop op die van de illustratie
L_ORIG = (290, 107)
BODY_K = 1.25                 # lijf iets voller (breedte om de middellijn)
BODY_CX = 187


def head_tf(p):
    return (K_OFF[0] + (p[0] - L_ORIG[0]) * KS, K_OFF[1] + (p[1] - L_ORIG[1]) * KS)


def body_tf(p):
    return (BODY_CX + (p[0] - BODY_CX) * BODY_K, p[1])


class Canvas:
    def __init__(self, size, tf):
        """tf: bronpunt -> tekenpunt (in tekenpixels, al supersampled en gespiegeld)."""
        self.size, self.tf = size, tf
        self.im = Image.new('RGBA', size, (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [self.tf(p) for p in pts]

    def mask(self, pts, smooth=True):
        m = Image.new('L', self.size, 0)
        ImageDraw.Draw(m).polygon(self.P(catmull(pts) if smooth else pts), fill=255)
        return m

    def fill(self, m, col):
        self.im.paste(Image.new('RGBA', self.size, hexc(col) + (255,)), (0, 0), m)

    def shade(self, m, col, d):
        self.fill(ImageChops.subtract(m, ImageChops.offset(m, -int(d * 0.5), -int(d))), col)

    def line(self, pts, w, closed=True, col='line'):
        q = self.P(catmull(pts, closed))
        if closed:
            q = q + [q[0]]
        self.d.line(q, fill=hexc(C[col]), width=max(1, int(w)), joint='curve')
        r = w / 2
        for p in (q[0], q[-1]):
            self.d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=hexc(C[col]))

    def ellipse(self, c, rx, ry, col, outline=None, w=0):
        cx, cy = self.tf(c)
        self.d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=hexc(C[col]) if col else None,
                       outline=hexc(C[outline]) if outline else None, width=int(w))


def draw_head(cv, px):
    """Kop + muil + snavel in leidraadcoördinaten; px = tekenpixels per fotopixel (voor lijndikte en maten)."""
    head = cv.mask(L_HEAD + L_FAR[::-1][1:] + L_JAWOUT[::-1][1:-1])
    mouth_pts = L_GAPE[:-1] + [(504, 252), (510, 256)] + L_FAR[::-1][1:] + L_NEAR[::-1][1:-1]
    mouth = cv.mask(mouth_pts)
    jaw = ImageChops.subtract(cv.mask(L_JAWOUT + L_FAR[::-1][1:-1] + [(510, 256)] + L_GAPE[::-1][1:-1]), mouth)
    sil = ImageChops.lighter(head, mouth)
    cv.fill(sil, C['fur']); cv.shade(sil, C['shade'], 16 * px)
    cv.fill(jaw, C['jawfur'])
    # muil: lippen (licht, smal), kom licht bij de rand en donkerder naar de keel achterin, twee spleetjes
    cv.fill(mouth, C['lip'])
    inner = erode(mouth, 3.5 * px)
    cv.fill(inner, C['m0'])
    for k, (col, cx, cy, rx, ry) in enumerate(((C['m1'], 410, 330, 95, 80), (C['m2'], 405, 312, 70, 45), (C['m3'], 400, 300, 45, 22))):
        e = cv.mask([(cx + math.cos(a) * rx, cy + math.sin(a) * ry) for a in np.linspace(0, 2 * math.pi, 40)])
        cv.fill(ImageChops.multiply(e, erode(inner, (3 + 3 * k) * px)), col)
    # vage tong / middenrichel onderin (lichter)
    tng = cv.mask([(398, 380), (410, 378), (416, 420), (408, 445), (398, 420)])
    cv.fill(ImageChops.multiply(tng, erode(inner, 4 * px)), C['m0'])
    for (x, y), (rx, ry) in L_SLITS:
        cv.fill(cv.mask([(x + math.cos(a) * rx, y + math.sin(a) * ry) for a in np.linspace(0, 2 * math.pi, 24)]), C['slit'])
    # kaakpunt: de kaakrand zelf wordt donkerder naar de punt
    tip = L_NEAR[-1]
    rim = ImageChops.subtract(ImageChops.lighter(mouth, jaw), inner)
    for col, r in ((C['b1'], 30), (C['jt'], 14)):
        cm = cv.mask([(tip[0] + math.cos(a) * r, tip[1] + 4 + math.sin(a) * r) for a in np.linspace(0, 2 * math.pi, 24)])
        cv.fill(ImageChops.multiply(cm, rim), col)
    # bovensnavel: één vorm met kleurverloop van de basis (lichtgrijs) naar de haak (donker)
    bill = cv.mask(L_BILL)
    A, B = np.array(L_BILL_BASE, float), np.array(L_BILL_TIP, float)
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
    # borstelveertjes voor/tussen de ogen, naar de snavel, deels over de snavelbasis
    for a, b in L_BRUSH:
        A_, B_ = np.array(cv.tf(a)), np.array(cv.tf(b))
        vv = B_ - A_; n = np.array((vv[1], -vv[0])) / np.linalg.norm(vv)
        cv.d.polygon([tuple(A_ + n * 2.2 * px), tuple(B_), tuple(A_ - n * 2.2 * px)], fill=hexc(C['brush']))
    # oog: puur zwart, iets groter dan op de foto, alleen de donkere lijn
    r = L_ER * 1.08 * px
    cv.ellipse(L_EYE, r, r, 'eye', 'line', 3.2 * px)
    # lijnen
    cv.line(L_JAWOUT, 4.5 * px, closed=False)
    cv.line(mouth_pts, 3.8 * px)
    cv.line(L_BILL[1:-1], 3.6 * px, closed=False)
    return ImageChops.lighter(ImageChops.lighter(sil, jaw), bill)


def draw_full():
    """Volledig poppetje in illustratiecoördinaten (480 x 640), gespiegeld naar links."""
    W0, H0 = 480, 640
    size = (W0 * SS, H0 * SS)
    mir = lambda p: ((W0 - p[0]) * SS, p[1] * SS)
    cvb = Canvas(size, lambda p: mir(body_tf(p)))
    body_pts = [(150, 100), (200, 100)] + R6.BODY_RIGHT[2:] + R6.BODY_LEFT[:-6] + [(112, 105)]
    body = cvb.mask(body_pts)
    cvb.fill(body, C['fur']); cvb.shade(body, C['shade'], 12 * SS)
    tail = ImageChops.multiply(body, cvb.mask([(140, 400), (205, 360), (202, 450), (198, 520), (189, 575), (182, 585), (172, 560), (160, 500), (148, 440)]))
    cvb.fill(tail, C['tail'])
    wing = cvb.mask(R6.WING)
    cvb.fill(wing, C['wing']); cvb.shade(wing, C['wshade'], 8 * SS)
    cvb.line(R6.WING, 2.6 * SS)
    for wt in R6.WINGTIPS:
        cvb.line(wt, 1.6 * SS, closed=False)
    for a, b in R6.STREAKS:
        A, B = np.array(cvb.tf(a)), np.array(cvb.tf(b))
        v = B - A; n = np.array((v[1], -v[0])) / np.linalg.norm(v)
        cvb.d.polygon([tuple(A), tuple((A + B) / 2 + n * 2.6 * SS), tuple(B), tuple((A + B) / 2 - n * 2.6 * SS)], fill=hexc(C['bark']))
    # kop in leidraadcoördinaten -> illustratie -> gespiegeld
    cvh = Canvas(size, lambda p: mir(head_tf(p)))
    hsil = draw_head(cvh, KS * SS)
    im = cvb.im
    im.paste(cvh.im, (0, 0), cvh.im)
    full = ImageChops.lighter(body, hsil)
    edge = ImageChops.subtract(full, erode(full, 3.2 * SS))
    im.paste(Image.new('RGBA', size, hexc(C['line']) + (255,)), (0, 0), edge)
    im.putalpha(full)
    return im


def head_on_photo():
    """(b) de 2D-kop over de gespiegelde leidraad (zelfde schaal), half doorzichtig, met de overtreklijnen."""
    box = (270, 90, 545, 480)
    k = 1.2
    W, H = int((box[2] - box[0]) * k), int((box[3] - box[1]) * k)
    foto = Image.open(R6.LEID).convert('RGB').crop(box).transpose(Image.FLIP_LEFT_RIGHT).resize((W, H), Image.LANCZOS)
    tf = lambda p: ((box[2] - p[0]) * k * SS, (p[1] - box[1]) * k * SS)
    cv = Canvas((W * SS, H * SS), tf)
    sil = draw_head(cv, k * SS)
    hd = cv.im.resize((W, H), Image.LANCZOS)
    out = foto.copy()
    out.paste(hd.convert('RGB'), (0, 0), hd.split()[3].point(lambda v: int(v * 0.55)))
    d = ImageDraw.Draw(out)
    t2 = lambda p: ((box[2] - p[0]) * k, (p[1] - box[1]) * k)
    for pts, col, cl in ((L_HEAD, (230, 30, 30), False), (L_GAPE, (255, 140, 0), False), (L_NEAR, (255, 140, 0), False),
                         (L_FAR, (255, 140, 0), False), (L_BILL, (30, 120, 255), True)):
        q = [t2(p) for p in catmull(pts, cl)]
        if cl:
            q.append(q[0])
        d.line(q, fill=col, width=2)
    return out


def traced_photo():
    box = (270, 90, 545, 480)
    k = 1.2
    W, H = int((box[2] - box[0]) * k), int((box[3] - box[1]) * k)
    foto = Image.open(R6.LEID).convert('RGB').crop(box).transpose(Image.FLIP_LEFT_RIGHT).resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(foto)
    t2 = lambda p: ((box[2] - p[0]) * k, (p[1] - box[1]) * k)
    for pts, col, cl in ((L_HEAD, (230, 30, 30), False), (L_JAWOUT, (230, 30, 30), False), (L_GAPE, (255, 140, 0), False),
                         (L_NEAR, (255, 140, 0), False), (L_FAR, (255, 140, 0), False), (L_BILL, (30, 120, 255), True)):
        q = [t2(p) for p in catmull(pts, cl)]
        if cl:
            q.append(q[0])
        d.line(q, fill=col, width=2)
    ex, ey = t2(L_EYE); r = L_ER * k
    d.ellipse((ex - r, ey - r, ex + r, ey + r), outline=(230, 30, 30), width=2)
    return foto


def vel():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    W, H = 1360, 1000
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    lab = lambda x, y, t: d.text((x, y), t, font=F, fill=(60, 60, 60))
    d.text((12, 8), 'Great potoo ronde 7: kop/muil/snavel uit de leidraad, lijf uit de illustratie (2D, met de hand overgetrokken)', font=FB, fill=(30, 30, 30))
    a = traced_photo(); im.paste(a, (10, 36)); lab(14, 36 + a.height + 4, '(a) leidraad + overtrek')
    b = head_on_photo(); im.paste(b, (10 + a.width + 10, 36)); lab(20 + a.width, 36 + b.height + 4, '(b) 2D-kop over de foto')
    pop = draw_full()
    big = R6.fit(pop, 520)
    x0 = 30 + a.width + b.width
    im.paste(big, (x0, 30)); lab(x0 + 4, 552, '(c) poppetje, spritehoek (naar links)')
    s64 = R6.fit(pop, 64, pad=0.02)
    im.paste(s64, (30, 560)); im.paste(s64.resize((192, 192), Image.NEAREST), (110, 560)); lab(30, 756, '(d) 64 px: 1x en 3x')
    # (e) lijf: overtrek over de illustratie
    ill = Image.open(R6.ILL).convert('RGB')
    e = ill.resize((300, 400), Image.LANCZOS)
    R6.lines_over(e, [(R6.BACK + R6.CROWN_TO_BILL[1:] + [(216, 72), (216, 86), (214, 92), (218, 98)] + R6.BODY_RIGHT + R6.BODY_LEFT, (230, 30, 30), True),
                      (R6.WING, (30, 120, 255), True)], 300 / 480)
    im.paste(e, (330, 560)); lab(334, 964, '(e) lijf: overtrek illustratie')
    try:
        r6 = Image.open(os.path.join(HERE, 'ronde6_spritehoek.png')).resize((200, 200), Image.LANCZOS)
        im.paste(r6, (660, 600)); lab(664, 804, '(f) ronde 6')
    except FileNotFoundError:
        pass
    cu = Image.open(R6.CLOSE).convert('RGB').crop((80, 200, 900, 1200)).resize((250, 305), Image.LANCZOS)
    im.paste(cu, (900, 600)); lab(904, 908, 'close-up (ter vergelijking)')
    im.save(os.path.join(HERE, 'vel_ronde7.png'))
    big.save(os.path.join(HERE, 'ronde7_spritehoek.png'))


if __name__ == '__main__':
    vel()
