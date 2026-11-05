"""Great potoo ronde 6: kop + snavel + muil als één 2D-tekening, direct uit de overgetrokken leidraad
(TRACES['leidraad'] in pop3d_potoo_ronde5.py, linkerhelft van jordi_great_potoo_bek_open_duo.webp), gespiegeld zodat
de vogel naar links kijkt. Geplakt op het lijf (lijf, vleugels, staart) van het 3D-poppetje van ronde 5 in de spritehoek.
Zelfde stijl: vlakke kleuren (C2), één schaduwtoon (licht linksboven), donkere lijn.
Draaien vanuit de repo-root: python3 docs/concept/sprites/potoo/poppetje/pop2d_kop.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d_potoo_ronde5 as P3

REF = os.path.join(HERE, '../referenties')
FOTO = os.path.join(REF, 'jordi_great_potoo_bek_open_duo.webp')
MX = 820          # spiegelas: x' = MX - x (fotopixels)
SS = 4            # supersampling: 4 tekenpixels per fotopixel
BOX = (250, 90, 560, 470)   # tekenvlak in fotopixels (ongespiegeld)

TR = P3.TRACES['leidraad']
EYE, ER = TR['eye'], TR['r']
# omtrek kop + kaak (rood) en mondrand (oranje), overgenomen van de foto; de bovenrand van de muil is opnieuw
# op de foto gelegd (licht gebogen gaplijn) en de rechterkant (haakje) iets verfijnd
OUTLINE = TR['outline']
GAPE = [(322, 292), (345, 285), (370, 280), (400, 274), (430, 267), (460, 259), (490, 251), (508, 246)]   # bovenrand muil
LOWER = [(508, 246), (513, 262), (510, 284), (500, 312), (470, 370), (440, 412), (405, 448), (370, 415), (345, 375),
         (330, 335), (322, 292)]                                                                         # onderkaakrand (U)
HOOK = [(500, 243, 6.5), (510, 244, 6.5), (517, 251, 6.0), (520, 262, 5.0), (518, 274, 3.8), (513, 285, 2.4), (507, 292, 1.0)]
SLITS = [((384, 312), (5, 16)), ((391, 357), (4, 13))]   # donkere spleetjes in gehemelte/keel (foto)
BRUSH = [((452, 214), (486, 236)), ((458, 202), (494, 226)), ((470, 232), (498, 244)), ((448, 228), (476, 246)),
         ((466, 192), (500, 216)), ((440, 240), (466, 254))]   # korte borstelveertjes voor/tussen de ogen, naar de snavel

C = dict(fur='#F1EFF6', shade='#C9C3D6', line='#28223A', lip='#F2EADF', lipd='#D6CABF',
         m0='#C9B8F0', m1='#A08CE6', m2='#7563CF', m3='#4C3E9C', slit='#231B52', hk1='#B3A9BC', hk2='#7A7085',
         hk3='#544A60', hook='#3A3346', eye='#09080D', lid='#D3CCE2', brush='#9A8FB0', jt='#6E6484')
EYE_K = 1.12      # stilering: oog iets groter
MOUTH_K = 1.05    # stilering: muil iets groter (om de mondhoek)


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def tp(pt):
    """Foto -> tekenvlak (gespiegeld, supersampled)."""
    x, y = pt
    return ((MX - x - (MX - BOX[2])) * SS, (y - BOX[1]) * SS)


def catmull(pts, closed=True, n=12):
    pts = [np.array(p, float) for p in pts]
    if closed and np.allclose(pts[0], pts[-1]):
        pts = pts[:-1]
    out = []
    N = len(pts)
    rng = range(N) if closed else range(N - 1)
    for i in rng:
        p0 = pts[(i - 1) % N] if closed else pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[(i + 1) % N]
        p3 = pts[(i + 2) % N] if closed else pts[min(i + 2, N - 1)]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(pts[-1])
    return [tuple(p) for p in out]


def mask(size, poly):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return m


def erode(m, px):
    return m.filter(ImageFilter.MinFilter(2 * px + 1)) if px > 0 else m


def scale_about(pts, c, k):
    return [(c[0] + (x - c[0]) * k, c[1] + (y - c[1]) * k) for x, y in pts]


def draw_head():
    W, H = (BOX[2] - BOX[0]) * SS, (BOX[3] - BOX[1]) * SS
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    corner = GAPE[0]
    mouth_ph = scale_about(GAPE + LOWER[1:], corner, MOUTH_K)
    outline_ph = OUTLINE
    head = catmull([tp(p) for p in outline_ph])
    mouthp = catmull([tp(p) for p in mouth_ph])
    mh = mask((W, H), head)
    mm = mask((W, H), mouthp)
    mh = ImageChops.lighter(mh, mm)                       # de muil valt altijd binnen de kop
    # vacht + één schaduwtoon (sikkel rechtsonder: licht van linksboven)
    fur = Image.new('RGBA', (W, H), hexc(C['fur']) + (255,))
    im.paste(fur, (0, 0), mh)
    d = 18 * SS
    shifted = ImageChops.offset(mh, -d // 2, -d)
    sh = ImageChops.subtract(mh, shifted)
    im.paste(Image.new('RGBA', (W, H), hexc(C['shade']) + (255,)), (0, 0), sh)
    # muil: lippen (dik bij de mondhoek, dun naar de punt), dan de kom licht -> donker naar de keel achterin
    im.paste(Image.new('RGBA', (W, H), hexc(C['lip']) + (255,)), (0, 0), mm)
    cx, cy = tp(corner)
    inner = erode(mm, 4 * SS)
    # lippen breder bij de mondhoek: extra lipvlak rond de mondhoek
    lipc = mask((W, H), [(cx + dx * 11 * SS, cy + dy * 9 * SS) for dx, dy in
                         [(math.cos(a), math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40)]])
    inner = ImageChops.subtract(inner, lipc)
    im.paste(Image.new('RGBA', (W, H), hexc(C['m0']) + (255,)), (0, 0), inner)
    # dieper = verder van de rand en dichter bij de keel (bovenmidden van de muil, foto)
    keel = tp((392, 318))
    for k, (col, r) in enumerate(((C['m1'], 92), (C['m2'], 64), (C['m3'], 34))):
        e = mask((W, H), [(keel[0] + math.cos(a) * r * 0.62 * SS, keel[1] + math.sin(a) * r * SS * 0.95 - (k * 3 * SS))
                          for a in np.linspace(0, 2 * math.pi, 60)])
        e = ImageChops.multiply(e, erode(inner, (6 + 6 * k) * SS))
        im.paste(Image.new('RGBA', (W, H), hexc(col) + (255,)), (0, 0), e)
    # vage tong / middenrichel onderin (lichter)
    tng = [tp((396, 372)), tp((404, 372)), tp((408, 420)), tp((400, 436)), tp((392, 420))]
    tm = ImageChops.multiply(mask((W, H), catmull(tng)), erode(inner, 6 * SS))
    im.paste(Image.new('RGBA', (W, H), hexc(C['m1']) + (255,)), (0, 0), tm)
    # donkere spleetjes in gehemelte/keel
    dd = ImageDraw.Draw(im)
    for (x, y), (rx, ry) in SLITS:
        X, Y = tp((x, y))
        dd.ellipse((X - rx * SS, Y - ry * SS, X + rx * SS, Y + ry * SS), fill=hexc(C['slit']))
    # kaakpunt: de lip wordt zelf donkerder naar de punt (geen kapje)
    tipp = tp(LOWER[6])
    for col, r in ((C['lipd'], 34), (C['jt'], 16)):
        cm = mask((W, H), [(tipp[0] + math.cos(a) * r * SS, tipp[1] + math.sin(a) * r * SS) for a in np.linspace(0, 2 * math.pi, 40)])
        cm = ImageChops.multiply(cm, ImageChops.subtract(mm, inner))
        im.paste(Image.new('RGBA', (W, H), hexc(col) + (255,)), (0, 0), cm)
    # bovensnavel: één hoornvorm langs de hele bovenrand van de muil (snijrand ±0,3 r_e), vóóraan dikker,
    # zonder onderbreking door in het haakje dat omlaag krult; kleur verloopt van hoorngrijs naar donker
    gape = catmull([tp(p) for p in scale_about(GAPE, corner, MOUTH_K)], closed=False, n=8)
    hook = [(tp((x, y)), w) for x, y, w in HOOK]
    path = [(p, 0.28 * ER + (0.5 * ER - 0.28 * ER) * (i / (len(gape) - 1)) ** 2) for i, p in enumerate(gape)]
    path += [(p, w) for p, w in hook[1:]]
    cols = [hexc(C[c]) for c in ('hk1', 'hk2', 'hk3', 'hook')]
    total = len(path)
    for i in range(total - 1):
        (p0, w0), (p1, w1) = path[i], path[i + 1]
        t = i / (total - 1)
        k = min(int(t * 3.2), 2)
        f = t * 3.2 - k
        col = tuple(int(cols[k][j] + (cols[k + 1][j] - cols[k][j]) * min(f, 1)) for j in range(3))
        v = np.array(p1) - np.array(p0)
        nrm = np.array((v[1], -v[0])) / (np.linalg.norm(v) + 1e-9)    # naar boven (gezicht)
        up = 1.0 if i < len(gape) - 1 else 0.5                         # langs de gaplijn ligt de hoorn boven de rand
        a0 = np.array(p0) + nrm * w0 * SS * up; b0 = np.array(p0) - nrm * w0 * SS * (1 - up)
        a1 = np.array(p1) + nrm * w1 * SS * up; b1 = np.array(p1) - nrm * w1 * SS * (1 - up)
        dd.polygon([tuple(a0), tuple(a1), tuple(b1), tuple(b0)], fill=col)
        dd.ellipse((p1[0] - w1 * SS * 0.5, p1[1] - w1 * SS * 0.5, p1[0] + w1 * SS * 0.5, p1[1] + w1 * SS * 0.5), fill=col)
    # borstelveertjes: korte tapse streepjes voor/tussen de ogen, naar de snavel
    for a, b in BRUSH:
        A, B = np.array(tp(a)), np.array(tp(b))
        v = B - A; n_ = np.array((v[1], -v[0])) / np.linalg.norm(v)
        dd.polygon([tuple(A + n_ * 2.2 * SS), tuple(B), tuple(A - n_ * 2.2 * SS)], fill=hexc(C['brush']))
    # oog: plek en grootte van de foto (iets groter), pikzwart zonder glans, smal licht ooglidrandje
    ex, ey = tp(EYE)
    r = ER * EYE_K * SS
    dd.ellipse((ex - r - 4 * SS, ey - r - 1 * SS, ex + r + 4 * SS, ey + r + 6 * SS), fill=hexc(C['lid']))
    dd.ellipse((ex - r, ey - r, ex + r, ey + r), fill=hexc(C['eye']))
    # lijnen: omtrek kop, mondrand, ooglid, haakje
    lw = 4 * SS
    dd.line(head + [head[0]], fill=hexc(C['line']), width=lw, joint='curve')
    dd.line(mouthp + [mouthp[0]], fill=hexc(C['line']), width=int(lw * 0.8), joint='curve')
    dd.ellipse((ex - r - 4 * SS, ey - r - 1 * SS, ex + r + 4 * SS, ey + r + 6 * SS), outline=hexc(C['line']), width=int(lw * 0.7))
    hk_out = [p for p, w in hook]
    # buitenrand van het haakje (voorkant van de snavel) als lijn
    dd.line([(p[0] - w * SS * 0.5, p[1]) for p, w in hook], fill=hexc(C['line']), width=int(lw * 0.6), joint='curve')
    im.putalpha(ImageChops.lighter(mh, Image.new('L', (W, H), 0)))
    return im


def head_overlay_on_photo():
    """(b) 2D-kop half doorzichtig over de gespiegelde foto, met dezelfde lijnen."""
    foto = Image.open(FOTO).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT)
    x0, x1 = MX - BOX[2], MX - BOX[0]
    foto = foto.crop((x0, BOX[1], x1, BOX[3])).resize(((BOX[2] - BOX[0]) * SS, (BOX[3] - BOX[1]) * SS))
    h = draw_head()
    a = h.split()[3].point(lambda v: int(v * 0.62))
    out = foto.copy(); out.paste(h.convert('RGB'), (0, 0), a)
    lines_on(out)
    return out


def lines_on(im):
    d = ImageDraw.Draw(im)
    d.line(catmull([tp(p) for p in OUTLINE]) + [tp(OUTLINE[0])], fill=(230, 40, 40), width=2 * SS)
    d.line([tp(p) for p in TR['rim']], fill=(255, 150, 0), width=2 * SS)


def traced_photo():
    foto = Image.open(FOTO).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT)
    x0, x1 = MX - BOX[2], MX - BOX[0]
    foto = foto.crop((x0, BOX[1], x1, BOX[3])).resize(((BOX[2] - BOX[0]) * SS, (BOX[3] - BOX[1]) * SS))
    lines_on(foto)
    return foto


def full_sprite(yaw=48, pitch=4):
    """(c) Lijf/vleugels/staart van ronde 5 (3D) + de 2D-kop, op de plek en grootte van de 3D-kop van ronde 5."""
    m = P3.potoo()
    nh = len(P3.potoo(body=0))
    head3, body3 = m[:nh], m[nh:]
    pts, rs = P3.extent(m, yaw, pitch)
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    R = P3.R
    scale = R * (236 / 256) / max(x1 - x0, y1 - y0)
    ctr = ((x0 + x1) / 2, (y0 + y1) / 2)
    body = P3.shade(*P3.render(body3, yaw, pitch, scale, ctr), out=R).convert('RGB')
    _, gh, _ = P3.render(head3, yaw, pitch, scale, ctr)
    ys, xs = np.where(gh >= 0)
    hx0, hx1, hy0, hy1 = xs.min(), xs.max(), ys.min(), ys.max()
    h = draw_head()
    bb = h.split()[3].getbbox()
    h = h.crop(bb)
    k = (hx1 - hx0) / h.width * 1.0
    h = h.resize((int(h.width * k), int(h.height * k)), Image.LANCZOS)
    # bovenkant van de kop gelijk, horizontaal gecentreerd op de 3D-kop
    px = int((hx0 + hx1) / 2 - h.width / 2)
    py = int(hy0)
    body.paste(h.convert('RGB'), (px, py), h.split()[3])
    return body


def vel():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    W, Hh = 1340, 470
    im = Image.new('RGB', (W, Hh), 'white')
    d = ImageDraw.Draw(im)
    lab = lambda x, y, t: d.text((x, y), t, font=F, fill=(60, 60, 60))
    d.text((12, 8), 'Great potoo ronde 6: kop + snavel + muil als 2D-tekening uit de overgetrokken leidraad, op het lijf van ronde 5', font=FB, fill=(30, 30, 30))
    sz = (300, 368)
    im.paste(traced_photo().resize(sz, Image.LANCZOS), (10, 40)); lab(14, 412, '(a) leidraad gespiegeld + overtrek')
    im.paste(head_overlay_on_photo().resize(sz, Image.LANCZOS), (320, 40)); lab(324, 412, '(b) 2D-kop over de foto (zelfde lijnen)')
    full = full_sprite()
    im.paste(full.resize((400, 400), Image.LANCZOS), (630, 30)); lab(634, 432, '(c) volledig poppetje, spritehoek')
    s64 = full.resize((64, 64), Image.LANCZOS)
    im.paste(s64, (1045, 50)); im.paste(s64.resize((192, 192), Image.NEAREST), (1125, 50)); lab(1045, 246, '(d) 64 px 1x en 3x')
    try:
        r5 = Image.open(os.path.join(HERE, 'vel_ronde5.png')).crop((10, 34, 410, 434)).resize((160, 160), Image.LANCZOS)
        im.paste(r5, (1100, 275)); lab(1060, 440, '(e) ronde 5')
    except FileNotFoundError:
        pass
    im.save(os.path.join(HERE, 'vel_ronde6.png'))
    full.save(os.path.join(HERE, 'ronde6_spritehoek.png'))


if __name__ == '__main__':
    vel()
