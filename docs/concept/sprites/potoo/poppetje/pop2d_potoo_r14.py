"""Great potoo ronde 14 = ronde 13 met alleen een nieuwe muil/kaken (blinde tests r13: "paars schild/masker vóór op
kop en borst", "geen mondhoek die tot onder/achter het oog doorloopt", "kaken te dun", "binnenkant vlak, sticker",
"onderkaak sluit niet aan op kin/keel").
- Mondhoek als scharnier: dikke vlezige lip-lob in de hoek, plooi met schaduw die achter onder het oog de wang in loopt.
- Kaken dikker: lichte lip van wisselende dikte om de onderkaak (dik bij de mondhoek en onderin, dun naar de punt en de
  voorkant), dunne bovenlip onder de gezichtsveren; vóóraan het hoornstuk dat in de haak eindigt (ongewijzigd).
- Diepte: slagschaduw onder de bovenkaak, gehemelte met donkere V-spleet, donkere keel, lichtere kaakbodem met tong en
  groef, binnenwand van de verre kaak als eigen toon, donkere binnenrand langs de lip.
- Onderkaak sluit aan op de keel: bevederde onderkant van de kop (kin) die vanaf de punt terugloopt naar de keel onder
  de mondhoek, met schaduw aan de onderkant en een slagschaduw op de borst.
Alles buiten de muil/kin is bevroren: het schorspatroon wordt uit ronde 13 opgenomen en herhaald (zelfde streepjes),
en het eindbeeld is buiten de opdrachtzone pixel voor pixel ronde 13 (controle in __main__).
Draaien vanuit de repo-root: python3 docs/concept/sprites/potoo/poppetje/pop2d_potoo_r14.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop2d_potoo_r13 as R13
from pop2d_potoo_r13 import R6, R7, C, catmull, hexc, erode, ferode, X0, X1, Y0, Y1, SS, MIRX, EYE, EYE_R

C.update(R13.PURPLE)
C.update(mwall='#A391DC', mfloor='#B9AAE8', tongue='#CBBEF0', tgroove='#7E6CCB', mroof='#8A78D2',
         lipsh='#D7C3DE', lipin='#5A49AA')

SCR = '/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/279ed44b-aa1d-54e2-8396-02fa8e081036/scratchpad'
BT14 = os.path.join(SCR, 'bt14')
_ORIG_HEAD, _ORIG_BARK = R13.draw_head, R13.bark_pattern
_REC = []


def smooth(t):
    t = min(1.0, max(0.0, t)); return t * t * (3 - 2 * t)


def offset_line(pts, wfun, inward, every=3, away=False):
    """Gladde curve op afstand wfun(i, n) van pts (dichte puntenlijst), naar binnen (naar `inward`) of naar buiten."""
    P = np.array(pts, float); n = len(P); out = []
    for i in range(n):
        t = P[min(i + 1, n - 1)] - P[max(i - 1, 0)]; t = t / (np.linalg.norm(t) + 1e-9)
        nr = np.array((-t[1], t[0]))
        if ((np.array(inward) - P[i]) @ nr < 0) != away:
            nr = -nr
        out.append(tuple(P[i] + nr * wfun(i, n)))
    dec = out[::every] + ([out[-1]] if (n - 1) % every else [])
    return catmull(dec, closed=False, n=6)


def mouth_parts(cv, px):
    mouth_pts = R7.L_GAPE[:-1] + [(504, 252), (510, 256)] + R7.L_FAR[::-1][1:] + R7.L_NEAR[::-1][1:-1]
    mouth = cv.mask(mouth_pts)
    low = catmull(R7.L_NEAR + R7.L_FAR[1:], closed=False, n=8)          # onderrand: mondhoek -> punt -> voorhoek
    return mouth_pts, mouth, low


def lip_w(i, n):
    """Lipdikte langs de onderrand (leidraadpixels): dik bij de mondhoek en onderin, dun naar de punt en de voorkant."""
    s = i / (n - 1)
    k = [(0.0, 23.0), (0.07, 19.0), (0.25, 17.0), (0.40, 14.0), (0.50, 9.0), (0.58, 7.5), (0.78, 5.5), (1.0, 3.5)]
    xs, ys = zip(*k)
    return float(np.interp(s, xs, ys))


def draw_head(cv, px):
    head = cv.mask(R7.L_HEAD + R7.L_FAR[::-1][1:] + R7.L_JAWOUT[::-1][1:-1])
    mouth_pts, mouth, low = mouth_parts(cv, px)
    jaw = ImageChops.subtract(cv.mask(R7.L_JAWOUT + R7.L_FAR[::-1][1:-1] + [(510, 256)] + R7.L_GAPE[::-1][1:-1]), mouth)
    sil = ImageChops.lighter(head, mouth)
    # ruige kopomtrek (ronde 13, ongewijzigd)
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
        back = np.array((-out[1], out[0]))
        if back[0] > 0:
            back = -back
        q = [tuple(p - back * 11 - out * 2), tuple(p - back * 4 + out * 2.5), tuple(p + back * 3 + out * 4),
             tuple(p + back * 8 + out * 3.2), tuple(p + back * 7 - out * 2)]
        td.polygon(cv.P(catmull(q, closed=True, n=6)), fill=255)
    sil = ImageChops.lighter(sil, tufts)
    body_alpha = cv.im.split()[3].copy()                 # wat er al ligt (lijf, vleugel): voor de slagschaduw van de kin
    cv.fill(sil, C['fur']); cv.shade(sil, C['shade'], 16 * px)

    # ---- kin: bevederde onderkant van de kop, van de mondhoek langs de onderkaak om de punt, terug naar de keel
    mc = (416.0, 335.0)
    nlow = len(low)
    ys = np.array([p[1] for p in low])
    itip = int(np.argmax(ys))
    def chin_w(i, n):
        y = low[i][1]
        if i <= itip:                                   # nabije kant: smal bij de mondhoek, breed onderin
            return 9.0 + 19.0 * smooth((y - 330) / (low[itip][1] - 330))
        return 28.0 * smooth((y - 392) / (low[itip][1] - 392))   # verre kant: loopt vóór de punt weer dicht
    chin_out = offset_line(low, chin_w, mc, every=4, away=True)
    chin_out = [p for p in chin_out]
    chin_raw = cv.mask(chin_out + low[::-1], smooth=False)
    chin = ImageChops.subtract(chin_raw, mouth)
    sil = ImageChops.lighter(sil, chin_raw.filter(ImageFilter.MaxFilter(3)))   # geen naad/gaatje tussen kin en muil
    jaw = ImageChops.lighter(jaw, chin)
    cv.fill(jaw, C['jawfur'])
    # onderkant van de kin in de schaduwtoon (sikkel), slagschaduw van de kop op de borst eronder
    chin_all = ImageChops.lighter(chin, jaw)
    under = ImageChops.subtract(chin_all, ImageChops.offset(chin_all, int(3 * px), -int(11 * px)))
    under = ImageChops.multiply(under, cv.mask([(300, 360), (560, 360), (560, 520), (300, 520)], smooth=False))
    cv.fill(under, C['shade'])
    cast = ImageChops.subtract(ImageChops.offset(chin_all, -int(2 * px), int(10 * px)), sil)
    cast = ImageChops.multiply(cast, body_alpha.point(lambda v: 255 if v > 0 else 0))
    cv.fill(cast.filter(ImageFilter.GaussianBlur(2 * px)).point(lambda v: 255 if v > 110 else 0), C['shade'])

    # ---- muil: lip (licht) en holte
    cv.fill(mouth, C['lip'])
    lip_in = offset_line(low, lip_w, mc, every=4)
    lowlip = ImageChops.multiply(cv.mask(lip_in + low[::-1], smooth=False), mouth)
    c0 = R7.L_GAPE[0]                                   # mondhoek: lip rondt de hoek af en loopt in de bovenlip
    rc = [(c0[0] + 16 + 15 * math.cos(a), c0[1] + 4 + 13 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 28)]
    lowlip = ImageChops.lighter(lowlip, ImageChops.multiply(cv.mask(rc), mouth))
    inner = ImageChops.subtract(erode(mouth, 3.5 * px), lowlip)          # bovenlip blijft dun (3,5)
    cav = inner
    cv.fill(cav, C['mroof'])
    soft = lambda m, r: ImageChops.multiply(m.filter(ImageFilter.GaussianBlur(r * px)), cav)
    # binnenwand van de verre kaak: eigen, iets lichtere toon langs de voorrand
    far = [p for p in lip_in if p[0] > 412 and p[1] < 446]
    farw = [(x - 22 * math.sin(math.pi * min(1.0, max(0.0, (446 - y) / 190.0))) ** 0.7, y) for x, y in far]
    cv.fill(soft(cv.mask(far + farw[::-1], smooth=False), 2.5), C['mwall'])
    # kaakbodem: lichter, onderin (rug van de kom naar de keel toe hoger in het midden)
    floor = [(336, 392), (360, 380), (392, 374), (424, 376), (452, 386), (470, 400), (468, 470), (330, 470)]
    cv.fill(soft(cv.mask(floor), 3), C['mfloor'])
    # keel: donkere opening achter de tongwortel, tussen gehemelte en bodem
    throat = [(358, 354), (378, 346), (400, 346), (424, 352), (434, 362), (416, 364), (394, 362), (372, 366)]
    cv.fill(soft(cv.mask(throat), 4), C['mdeep2'])
    # tong in de kaakbodem, met groef in het midden
    tng = [(386, 380), (398, 372), (414, 374), (424, 386), (424, 408), (418, 426), (410, 436), (402, 434), (394, 420),
           (386, 402)]
    tmask = ImageChops.multiply(cv.mask(tng), cav)
    tmask = tmask.filter(ImageFilter.GaussianBlur(1.2 * px)); cv.fill(tmask, C['tongue'])
    cv.fill(ImageChops.subtract(tmask, ImageChops.offset(tmask, int(5 * px), -int(4 * px))), C['mfloor'])
    cv.line([(404, 382), (406, 398), (407, 414), (406, 426)], 2.2 * px, closed=False, col='tgroove')
    # gehemelte: donkere V-spleet (breed bovenaan, spits naar beneden) en een klein gaatje ervoor
    v = [(377, 296), (387, 293), (398, 294), (394, 310), (391, 326), (390, 344), (386, 326), (382, 310)]
    cv.fill(soft(cv.mask(v), 1.0), C['slit2'])
    # slagschaduw onder de bovenkaak: indigo band bovenin, dik in het midden, dun naar mondhoek en voorkant
    gd = [p for p in catmull(R7.L_GAPE, closed=False, n=10) if 326 <= p[0] <= 506]
    def gsh(x):
        return 5 + 19 * math.sin(math.pi * (x - 326) / 180.0) ** 0.8
    shb = [(x, y - 4) for x, y in gd] + [(x - 2, y + gsh(x)) for x, y in gd[::-1]]
    cv.fill(soft(cv.mask(shb, smooth=False), 1.6), C['mdeep1'])
    cv.fill(soft(cv.mask([(x, y - 4) for x, y in gd] + [(x, y + 0.55 * gsh(x)) for x, y in gd[::-1]], smooth=False), 2.5), C['mdeep2'])
    # donkere binnenrand langs de onderlip (vorm over vorm), taps naar de uiteinden
    rimline = lip_in[2:-3]
    for j in range(len(rimline) - 1):
        s = j / (len(rimline) - 1)
        w = 2.6 * min(1.0, s / 0.12, (1 - s) / 0.25)
        if w > 0.4:
            cv.d.line(cv.P([rimline[j], rimline[j + 1]]), fill=hexc(C['lipin']), width=max(1, int(w * px)))
    # lip met één schaduwtoon aan de binnen-onderkant (volume), lichte kant naar boven
    lipsh = ImageChops.subtract(lowlip, ImageChops.offset(lowlip, -int(2 * px), -int(5 * px)))
    cv.fill(ImageChops.multiply(lipsh, cv.mask([(300, 300), (560, 300), (560, 520), (300, 520)], smooth=False)), C['lipsh'])
    # hoorntip van de onderkaak (donker, zoals ronde 13)
    tip = R7.L_NEAR[-1]
    rim = ImageChops.subtract(ImageChops.lighter(mouth, jaw), cav)
    for col, r in ((C['b0'], 15), (C['b1'], 8)):
        cm = cv.mask([(tip[0] + 6 + math.cos(a) * r, tip[1] - 2 + math.sin(a) * r * 0.8) for a in np.linspace(0, 2 * math.pi, 24)])
        cv.fill(ImageChops.multiply(cm.filter(ImageFilter.GaussianBlur(2 * px)).point(lambda v: 255 if v > 128 else 0), lowlip), col)

    # ---- bovensnavel (ronde 13, ongewijzigd): hoornstuk vóóraan dat in de haak eindigt
    gg = [p for p in catmull(R7.L_GAPE, closed=False) if 428 <= p[0] <= 476]
    sliver = [(x, y - 7 * (x - 428) / 48) for x, y in gg] + [(x, y + 2) for x, y in gg[::-1]]
    bill = ImageChops.lighter(cv.mask(R7.L_BILL), cv.mask(sliver, smooth=False))
    A, B = np.array(R7.L_BILL_BASE, float), np.array(R7.L_BILL_TIP, float)
    cols = [hexc(C[c]) for c in ('b0', 'b1', 'b2', 'b3')]
    grad = Image.new('RGBA', cv.size); gdr = ImageDraw.Draw(grad)
    vv = B - A; u = vv / np.linalg.norm(vv); nrm = np.array((-u[1], u[0]))
    for i in range(60):
        t0, t1 = i / 60, (i + 1) / 60
        t = (t0 + t1) / 2; k = min(int(t * 3), 2); f = t * 3 - k
        col = tuple(int(cols[k][j] + (cols[k + 1][j] - cols[k][j]) * f) for j in range(3)) + (255,)
        p0, p1 = A + vv * (t0 * 1.3 - 0.15), A + vv * (t1 * 1.3 - 0.15)
        gdr.polygon(cv.P([tuple(p0 + nrm * 200), tuple(p1 + nrm * 200), tuple(p1 - nrm * 200), tuple(p0 - nrm * 200)]), fill=col)
    cv.im.paste(grad, (0, 0), bill)
    for (x, y) in ((442, 210), (454, 218), (466, 227), (476, 236),
                   (446, 228), (458, 236), (469, 243),
                   (450, 198), (462, 207)):
        cv.line([(x - 5, y - 7), (x + 2, y - 3), (x + 4, y + 1), (x - 1, y + 6)], 1.7 * px, closed=False, col='brush')
    r = EYE_R * px
    cv.ellipse(EYE, r, r, 'eye', 'line', 3.2 * px)

    # ---- lijnen
    co = [p for p in chin_out if p[1] > 368 and p[0] < 470]
    for j in range(len(co) - 1):          # onderrand van de kin: van de keel (taps) om de punt, taps naar de voorkant
        s_ = j / (len(co) - 1); w = 4.5 * min(1.0, s_ / 0.25, (1 - s_) / 0.15)
        if w > 0.6:
            cv.d.line(cv.P([co[j], co[j + 1]]), fill=hexc(C['line']), width=max(1, int(w * px)))
    cv.line(mouth_pts, 3.6 * px)
    cv.im.paste(grad, (0, 0), bill)
    cv.line([sliver[0]] + sliver[len(gg) // 2:len(gg)] + R7.L_BILL[2:-1], 3.6 * px, closed=False)
    # gezichtsveren hangen een fractie over de bovenlip (ronde 13)
    gl = [p for p in catmull(R7.L_GAPE, closed=False, n=12) if 342 <= p[0] <= 455]
    wav = [(x, y + 3.2 * max(0.0, math.sin(math.pi * (x - 330) / 25.0))) for x, y in gl]
    cv.fill(cv.mask([(x, y - 6) for x, y in gl] + wav[::-1], smooth=False), C['fur'])
    cv.line(wav[::2], 3.6 * px, closed=False)

    # ---- mondhoek als scharnier: vlezige lip-lob waar boven- en onderkaak samenkomen, plooi + schaduw de wang in
    wedge = [(c0[0] + 2, c0[1] - 6), (c0[0] - 12, c0[1] - 1), (c0[0] - 26, c0[1] + 8), (c0[0] - 30, c0[1] + 16),
             (c0[0] - 20, c0[1] + 16), (c0[0] - 8, c0[1] + 10), (c0[0] - 1, c0[1] + 8)]
    cv.fill(cv.mask(wedge), C['shade'])
    lob = [(c0[0] + 18, c0[1] - 5), (c0[0] + 6, c0[1] - 7), (c0[0] - 5, c0[1] - 3), (c0[0] - 9, c0[1] + 6),
           (c0[0] - 4, c0[1] + 16), (c0[0] + 8, c0[1] + 22), (c0[0] + 18, c0[1] + 20)]
    lobm = Image.new('L', cv.size, 0)
    # naad kaak/mantel: veerpuntjes van de wang over de mantel (ronde 13)
    for (x, y) in ((312, 324), (316, 346), (323, 366)):
        tuft = [(x + 3, y - 9), (x - 6, y - 4), (x - 11, y + 4), (x - 5, y + 8), (x + 3, y + 7)]
        cv.fill(cv.mask(tuft), C['jawfur'])
        cv.line([(x - 6, y - 4), (x - 11, y + 4), (x - 5, y + 8)], 1.8 * px, closed=False, col='fline')
    fold = catmull([c0, (c0[0] - 10, c0[1] + 3), (c0[0] - 19, c0[1] + 7), (c0[0] - 27, c0[1] + 12)], closed=False, n=8)
    for j in range(len(fold) - 1):                                          # plooi: de gaplijn loopt taps door, de wang in
        s_ = j / (len(fold) - 1); w = 3.2 * (1 - s_) + 0.9
        cv.d.line(cv.P([fold[j], fold[j + 1]]), fill=hexc(C['line' if s_ < 0.3 else 'jt']), width=max(1, int(w * px)))
    cv.line([(c0[0] + 22, c0[1] - 1), (c0[0] + 12, c0[1] + 1), (c0[0] + 3, c0[1] + 2)], 2.4 * px, closed=False, col='lipin')
    zone = ImageChops.lighter(ImageChops.lighter(mouth, chin_all), ImageChops.lighter(lobm, cv.mask(wedge)))
    cv.zone = zone
    return ImageChops.lighter(ImageChops.lighter(sil, jaw), bill), mouth, bill


def record_streak(cv, a, b, w, col):
    _REC.append((a, b, w, col)); R13._orig_streak(cv, a, b, w, col)


def bark_replay(cv, full, skip, px, seed=9):
    """Zelfde streepjes als ronde 13; alleen die in de nieuwe muil/kin vallen weg."""
    sk = ImageChops.lighter(skip, getattr(cv, 'zone', skip)).resize((cv.size[0] // 4, cv.size[1] // 4), Image.BOX)
    ska = np.asarray(sk) > 0
    for a, b, w, col in _REC:
        X, Y = cv.tf(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
        if ska[min(int(Y / 4), ska.shape[0] - 1), min(int(X / 4), ska.shape[1] - 1)]:
            continue
        R13._orig_streak(cv, a, b, w, col)


def render():
    """Ronde 13 (met opname van het patroon) en ronde 14; buiten de opdrachtzone wordt ronde 13 overgenomen."""
    import pickle
    R13._orig_streak = R13.streak
    cache = os.path.join(SCR, 'w14', 'r13_cache.pkl')
    if os.path.exists(cache):
        r13, rec = pickle.load(open(cache, 'rb')); _REC[:] = rec
    else:
        R13.streak = record_streak
        _REC.clear()
        r13 = R13.draw_full()
        R13.streak = R13._orig_streak
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        pickle.dump((r13, list(_REC)), open(cache, 'wb'))
    zone_holder = {}
    def dh(cv, px):
        res = draw_head(cv, px); zone_holder['z'] = cv.zone; return res
    R13.draw_head, R13.bark_pattern = dh, bark_replay
    r14 = R13.draw_full()
    R13.draw_head, R13.bark_pattern = _ORIG_HEAD, _ORIG_BARK
    z = zone_holder['z'].filter(ImageFilter.MaxFilter(2 * int(14 * SS) + 1))
    out = Image.composite(r14, r13, z)
    return r13, out, z


def head_crop(img, box=(270, 90, 545, 500), k=1.0):
    hp = img.crop((int((X1 - box[2]) * SS), int((box[1] - Y0) * SS), int((X1 - box[0]) * SS), int((box[3] - Y0) * SS)))
    hp = hp.resize((int((box[2] - box[0]) * k), int((box[3] - box[1]) * k)), Image.LANCZOS)
    hb = Image.new('RGB', hp.size, 'white'); hb.paste(hp, (0, 0), hp)
    return hb


def vel(r13, pop):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    W, H = 1640, 1060
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    lab = lambda x, y, t: d.text((x, y), t, font=F, fill=(60, 60, 60))
    d.text((12, 8), 'Great potoo ronde 14: alleen muil/kaken (mondhoek als scharnier, dikke lip, holte met diepte, kin naar de keel)',
           font=FB, fill=(30, 30, 30))
    big = R6.fit(pop, 560)
    im.paste(big, (10, 36)); lab(14, 600, '(a) ronde 14, spritehoek')
    hk = head_crop(pop, k=1.45)
    im.paste(hk, (580, 36)); lab(584, 36 + hk.height + 4, '(b) kop groot')
    cl = Image.open(R6.CLOSE).convert('RGB').crop((120, 300, 880, 1260))
    cl = cl.resize((int(cl.width * hk.height / cl.height), hk.height), Image.LANCZOS)
    xc = 580 + hk.width + 12
    im.paste(cl, (xc, 36)); lab(xc + 4, 36 + hk.height + 4, '(c) close-up bek open')
    lf = Image.open(R6.LEID).convert('RGB').crop((270, 90, 545, 500)).transpose(Image.FLIP_LEFT_RIGHT)
    lf = lf.resize((int(lf.width * 0.62 * 1.45), int(lf.height * 0.62 * 1.45)), Image.LANCZOS)
    y2 = 36 + hk.height + 30
    im.paste(lf, (580, y2)); lab(584, y2 + lf.height + 4, '(d) leidraad (gespiegeld)')
    h13 = head_crop(r13, k=0.62 * 1.45)
    im.paste(h13, (580 + lf.width + 12, y2)); lab(584 + lf.width + 12, y2 + h13.height + 4, '(e) ronde 13, kop')
    s13 = R6.fit(r13, 180)
    xs = 580 + lf.width + h13.width + 24
    im.paste(s13, (xs, y2)); lab(xs + 4, y2 + 184, '(f) ronde 13')
    s64 = R6.fit(pop, 64, pad=0.03)
    im.paste(s64, (10, 640)); im.paste(s64.resize((192, 192), Image.NEAREST), (84, 640)); lab(10, 836, '(g) 64 px: 1x en 3x')
    im.save(os.path.join(HERE, 'vel_ronde14.png'))
    big.save(os.path.join(HERE, 'ronde14_spritehoek.png'))
    os.makedirs(BT14, exist_ok=True)
    big.save(os.path.join(BT14, 'y.png'))


def preview(name='prev.png'):
    """Snel: alleen lijf-vlak + kop, zonder patroon (om de muil te bekijken)."""
    k = 1.0; px = SS * k
    size = (int((X1 - X0) * SS * k), int((Y1 - Y0) * SS * k))
    T = lambda p: ((MIRX - p[0]) * px - (MIRX - X1) * px, (p[1] - Y0) * px)
    cv = R7.Canvas(size, T)
    body = cv.mask(R13.BODY); cv.fill(body, C['fur'])
    cv.fill(cv.mask(R13.COVERTS), C['wing'])
    draw_head(cv, px)
    box = (270, 180, 545, 500)
    c = cv.im.crop((int((X1 - box[2]) * SS), int((box[1] - Y0) * SS), int((X1 - box[0]) * SS), int((box[3] - Y0) * SS)))
    bg = Image.new('RGB', c.size, 'white'); bg.paste(c, (0, 0), c)
    bg.resize((c.width * 3 // 5, c.height * 3 // 5), Image.LANCZOS).save(os.path.join(SCR, 'w14', name))


if __name__ == '__main__' and len(sys.argv) > 1:
    preview(sys.argv[1])
elif __name__ == '__main__':
    r13, pop, z = render()
    a, b = np.asarray(r13).astype(int), np.asarray(pop).astype(int)
    outside = np.asarray(z) == 0
    print('pixeldiff buiten de zone:', int((np.abs(a - b).sum(axis=2)[outside] > 0).sum()))
    pop.save(os.path.join(SCR, 'w14', 'r14full.png'))
    vel(r13, pop)
