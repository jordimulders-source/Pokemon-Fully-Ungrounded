"""Nachtaap fase 3: kop (muriqui-gezicht) en achtervoeten 2D overschilderd op de Blender-render.
Buiten Blender (Jordi 5 nov). Bron: ../blender/render_snel.png (pose en massa bevroren).
Coordinaten in render-pixels (560x560); getekend op 4x en verkleind (anti-aliasing).
Uitvoer: model.png (1120, = 2x), model_kop.png (close-up), model_voeten.png.
"""
import os, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

HIER = os.path.dirname(os.path.abspath(__file__))
K = 4
SRC = Image.open(os.path.join(HIER, '../blender/render_snel.png')).convert('RGBA')
W = SRC.size[0] * K
img = np.asarray(SRC.resize((W, W), Image.LANCZOS)).astype(np.float32) / 255.0

LIJN = (77, 62, 96)
VACHT = [(36, 40, 78), (62, 70, 122), (104, 112, 176), (128, 138, 192), (156, 166, 212)]
GEZICHT = [(26, 22, 42), (38, 32, 60), (52, 44, 80), (70, 60, 102)]
SNUIT = [(122, 100, 140), (158, 134, 170), (188, 166, 200), (212, 194, 224)]
TEEN = [(30, 32, 64), (52, 56, 104), (84, 90, 150), (110, 118, 178)]

def c(rgb): return np.array(rgb, np.float32) / 255.0

def catmull(pts, n=24, closed=True):
    p = [np.array(q, float) for q in pts]
    if closed: p = [p[-1]] + p + [p[0], p[1]]
    else: p = [p[0]] + p + [p[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i-1], p[i], p[i+1], p[i+2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2*p1) + (-p0+p2)*t + (2*p0-5*p1+4*p2-p3)*t*t + (-p0+3*p1-3*p2+p3)*t**3))
    if not closed: out.append(p[-2])
    return [(float(x) * K, float(y) * K) for x, y in out]

def masker_poly(pts, closed=True, smooth=True):
    m = Image.new('L', (W, W), 0)
    d = ImageDraw.Draw(m)
    d.polygon(catmull(pts) if smooth else [(x*K, y*K) for x, y in pts], fill=255)
    return np.asarray(m) > 127

def masker_ellips(cx, cy, rx, ry):
    yy, xx = np.mgrid[0:W, 0:W]
    return ((xx/K - cx)/rx)**2 + ((yy/K - cy)/ry)**2 <= 1

def lijnmasker(pts, breedte, closed=False):
    m = Image.new('L', (W, W), 0)
    d = ImageDraw.Draw(m)
    q = catmull(pts, closed=closed) if len(pts) > 2 else [(x*K, y*K) for x, y in pts]
    d.line(q, fill=255, width=int(breedte*K), joint='curve')
    for x, y in (q[0], q[-1]):
        r = breedte*K/2; d.ellipse([x-r, y-r, x+r, y+r], fill=255)
    return np.asarray(m) > 127

def verf(mask, kleur, alpha=1.0):
    global img
    a = mask.astype(np.float32)[..., None] * alpha
    img[..., :3] = img[..., :3] * (1 - a) + c(kleur) * a
    img[..., 3:] = np.maximum(img[..., 3:], a)

def bol(mask, ramp, R=12.0, licht=(-0.55, -0.65, 0.55), extra=None):
    """Volume-shading uit de afstand tot de rand (zoals een opgeblazen vorm), licht linksboven."""
    d = nd.distance_transform_edt(mask) / K
    h = np.sqrt(np.clip(R*R - (R - np.minimum(d, R))**2, 0, None))
    if extra is not None: h = h + extra
    h = nd.gaussian_filter(h, 1.2*K)
    gy, gx = np.gradient(h)
    gx *= K; gy *= K
    n = np.dstack([-gx, -gy, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    L = np.array(licht); L /= np.linalg.norm(L)
    I = np.clip((n @ L) * 0.9 + 0.25, 0, 1)
    stops = np.linspace(0, 1, len(ramp))
    cols = np.array([c(k) for k in ramp])
    out = np.zeros((W, W, 3), np.float32)
    for ch in range(3): out[..., ch] = np.interp(I, stops, cols[:, ch])
    a = mask.astype(np.float32)[..., None]
    img[..., :3] = img[..., :3] * (1 - a) + out * a
    img[..., 3:] = np.maximum(img[..., 3:], a)

def omlijn(mask, dikte=4.6, niet=None):
    dd = nd.distance_transform_edt(~mask) / K
    ring = (dd > 0) & (dd <= dikte)
    if niet is not None: ring &= ~niet
    verf(ring, LIJN)

def gum(mask):
    img[mask] = 0

# ------------------------------------------------------------------ voeten
# Muriqui-voet (Jordi/SPEC 5 nov): lange behaarde zool, vier tenen samen als gekrulde want, grote teen los.
# Bovenste voet: grijpt een onzichtbare tak boven de enkel (vuist, geen gat); onderste voet: slap, tenen licht gekruld.

# bovenste voet: slanke lange voet omhoog, vier tenen als want over de (onzichtbare) tak, grote teen ervoor
ALPHA0 = np.asarray(SRC.resize((W, W)))[..., 3] > 0
gum(masker_poly([(200, 30), (300, 30), (300, 101), (200, 101)], smooth=False))
enkel1 = masker_ellips(237, 113, 24, 9)
# haak: lange zool omhoog, tenen als één gekrulde want over de tak, open greep (tak) tussen tenen en grote teen
voet1 = masker_poly([(223, 112), (222, 92), (226, 74), (233, 60), (243, 51), (256, 47), (268, 51), (276, 61),
                      (278, 74), (275, 85), (268, 92), (262, 89), (263, 78), (261, 69), (256, 64), (253, 71),
                      (252, 86), (253, 98), (251, 112)])
omlijn(voet1, niet=enkel1 & ALPHA0)
bol(voet1, VACHT, R=12)
tenen1 = masker_poly([(243, 51), (256, 47), (268, 51), (276, 61), (278, 74), (275, 85), (268, 92), (262, 89),
                       (263, 78), (261, 69), (256, 64), (249, 58)])
bol(tenen1, TEEN, R=6, licht=(-0.45, -0.75, 0.5))
verf(lijnmasker([(243, 52), (250, 58), (256, 64)], 2.4), LIJN)
grote1 = masker_poly([(251, 104), (250, 97), (253, 92), (259, 90), (263, 94), (260, 100), (255, 104)])
omlijn(grote1, dikte=2.6)
bol(grote1, TEEN, R=4, licht=(-0.45, -0.75, 0.5))

# onderste voet: hangt slap in het verlengde van het scheenbeen, knikt iets omlaag, tenen licht gekruld
yy0, xx0 = np.mgrid[0:W, 0:W] / K
dvec = np.array([0.864, 0.504])
gum(((xx0 - 452) * dvec[0] + (yy0 - 422) * dvec[1] > 0) & (yy0 > 380) & (xx0 > 430))
enkel2 = ((xx0 - 452) * dvec[0] + (yy0 - 422) * dvec[1] <= 0.5) & ALPHA0
voet2 = masker_poly([(440, 410), (455, 404), (465, 412), (474, 423), (482, 436), (488, 450), (490, 463), (486, 473),
                      (478, 475), (472, 467), (466, 458), (457, 451), (447, 449), (440, 443), (434, 428)])
omlijn(voet2, niet=enkel2)
bol(voet2, VACHT, R=12)
tenen2 = masker_poly([(480, 442), (486, 450), (490, 463), (486, 473), (478, 475), (472, 467), (472, 455)])
bol(tenen2, TEEN, R=6, licht=(-0.45, -0.75, 0.5))
verf(lijnmasker([(482, 440), (472, 452), (472, 466)], 2.3), LIJN)
grote2 = masker_poly([(458, 452), (466, 455), (468, 463), (463, 471), (456, 470), (454, 461)])
omlijn(grote2, dikte=2.4)
bol(grote2, TEEN, R=4, licht=(-0.45, -0.75, 0.5))
verf(lijnmasker([(458, 409), (448, 423), (444, 440)], 2.0), LIJN)
knie = (xx0 > 395) & (xx0 < 452) & (yy0 > 395) & (yy0 < 450) & (img[..., :3].sum(axis=2) < 0.42) & (img[..., 3] > 0.5) & ~voet2
img[knie, :3] = img[knie, :3] * 0.4 + c(VACHT[1]) * 0.6

# ------------------------------------------------------------------ kop
# Muriqui-kop naar foto 4/5: ronde schedel zonder oren, groot donker gezichtsschild met rechte wenkbrauwlijn,
# kleine ogen dicht bij elkaar, lichte neusrug die breder wordt naar een lange snuit, neusgaten bovenaan,
# brede rechte mond, donkere kin; kleine maansikkel; vacht omlijst het gezicht. Geen koptelefoon-wangen.
# Spritemaat: het hele model wordt ±0,12x (64 px breed). Daarom kop 1,3x (Pokemon-verhouding) en elk gezichtsdeel
# op pixels gedimensioneerd: oog >= 2 px, snuit >= 4 px breed, schild ±10 px (zie model_64.png).
S = 1.3
NX, NY = 96, 312          # nieuw kopmidden (groeit naar linksboven, nek blijft aan de romp)
def T(x, y): return (NX + (x - 107) * S, NY + (y - 322) * S)
def TP(pts): return [T(x, y) for x, y in pts]
def E(x, y, rx, ry): X, Y = T(x, y); return masker_ellips(X, Y, rx * S, ry * S)
FX = 101
SRC4 = np.asarray(SRC.resize((W, W), Image.LANCZOS)).astype(np.float32) / 255.0
licht = SRC4[..., :3].sum(axis=2) > 2.2
yy, xx = np.mgrid[0:W, 0:W] / K
handzone = (yy > 388) & (xx < 175) & (xx > 70)
hand = handzone & (nd.distance_transform_edt(~(licht & handzone)) / K <= 5.0) & (SRC4[..., 3] > 0.5)

kop = E(107, 320, 52, 56) | masker_poly(TP([(80, 350), (122, 350), (121, 375), (110, 385), (92, 385), (81, 375)]))
omlijn(kop)
bol(kop, VACHT, R=36)
# 1 spritepixel = ±6,4 eenheden hier (render 8,3 px / S); alle gezichtsdelen >= 1,5-2 px
schild = masker_poly(TP([(72, 315), (80, 309), (101, 308), (122, 309), (130, 315), (133, 328), (131, 344), (126, 360),
                         (118, 372), (108, 379), (101, 380), (94, 379), (84, 372), (76, 360), (71, 344), (69, 328)]))
bol(schild, GEZICHT, R=13)
richel = masker_poly(TP([(78, 314.5), (124, 314.5), (124, 318), (78, 318)]), smooth=True) & schild
verf(richel, GEZICHT[0], 0.75)
# ogen: donkere oogkas, lichtblauwe iris (±2 px), één glansje; rechte wenkbrauw snijdt de bovenkant iets af (streng)
for ox in (FX - 9.5, FX + 9.5):
    verf(E(ox, 325, 6.4, 5.8), GEZICHT[0])
    bol(E(ox, 325.4, 5.0, 4.8), [(84, 140, 200), (140, 190, 234), (190, 222, 246)], R=4)
    verf(E(ox + 0.6, 326.0, 2.0, 2.3), (20, 28, 58))
    verf(E(ox - 1.8, 324.0, 1.2, 1.2), (255, 255, 255))
verf(masker_poly(TP([(80, 317.5), (122, 317.5), (122, 321.2), (80, 321.2)]), smooth=False) & schild, GEZICHT[0])
# lichte neusrug -> brede snuit met lippen (foto 4); neusgaten klein en schuin bovenaan de snuit; mond erin; donkere kin
snuit = masker_poly(TP([(FX - 3, 332), (FX + 3, 332), (FX + 6, 341), (FX + 12, 349), (FX + 16, 357), (FX + 16, 364),
                        (FX + 11, 370), (FX, 372), (FX - 11, 370), (FX - 16, 364), (FX - 16, 357), (FX - 12, 349), (FX - 6, 341)]))
bol(snuit, SNUIT, R=8)
for nx, k in ((FX - 4, -1), (FX + 4, 1)):
    verf(masker_poly(TP([(nx - 2.6*k, 349.5), (nx + 0.8*k, 346.5), (nx + 2.4*k, 348.5), (nx + 0.4*k, 351.5)])), (52, 34, 64))
verf(lijnmasker(TP([(FX - 12, 362.5), (FX - 4, 363.2), (FX + 4, 363.2), (FX + 12, 362.5)]), 3.4), (34, 24, 46))
# maansikkel: kort, ±2 px dik
m1 = E(FX + 1, 299, 12, 9); X, Y = T(FX + 1, 307); m2 = masker_ellips(X, Y, 13 * S, 9 * S)
verf(m1 & ~m2 & (yy < T(0, 304)[1]), (236, 236, 246))
# healerhand ligt vóór de kop
a_ = hand.astype(np.float32)[..., None]
img[:] = img * (1 - a_) + SRC4 * a_

# naadjes (1 px gaten tussen oude en nieuwe omlijning) dichten met lijnkleur
A = img[..., 3] > 0.5
dicht = nd.binary_closing(A, structure=np.ones((7, 7))) & ~A
img[dicht] = np.r_[c(LIJN), 1.0]
out = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8), 'RGBA')
model = out.resize((1120, 1120), Image.LANCZOS)
model.save(os.path.join(HIER, 'model.png'))
def opwit(im):
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); return bg
opwit(out.crop((20*K, 220*K, 190*K, 410*K))).resize((612, 684), Image.LANCZOS).save(os.path.join(HIER, 'model_kop.png'))
v = Image.new('RGBA', (900, 440), (255, 255, 255, 255))
v.paste(opwit(out.crop((195*K, 35*K, 300*K, 125*K))).resize((420, 360), Image.LANCZOS), (0, 40))
v.paste(opwit(out.crop((400*K, 400*K, 510*K, 490*K))).resize((440, 360), Image.LANCZOS), (450, 40))
v.save(os.path.join(HIER, 'model_voeten.png'))
# spritemaat-controle: 64 px breed, 50 %-dekking en verkleinde kleur, 1x en 8x
bb = model.getchannel('A').point(lambda v: 255 if v > 128 else 0).getbbox()
m = model.crop(bb); sc = 64 / max(m.size)
k = m.resize((round(m.size[0]*sc), round(m.size[1]*sc)), Image.BOX)
a = np.asarray(k)[..., 3] > 127
print('64-maat', k.size, 'px', int(a.sum()))
kk = np.asarray(k).copy(); kk[..., 3] = np.where(a, 255, 0)
k = Image.fromarray(kk, 'RGBA')
vel = Image.new('RGBA', (64*8 + 20 + 64*2, 64*8), (255, 255, 255, 255))
vel.paste(opwit(k).resize((k.size[0]*8, k.size[1]*8), Image.NEAREST), (0, 0))
vel.paste(opwit(k), (64*8 + 10, 10)); vel.paste(opwit(k).resize((k.size[0]*2, k.size[1]*2), Image.NEAREST), (64*8 + 10, 90))
vel.save(os.path.join(HIER, 'model_64.png'))
# vel voor Jordi: model | kop naast foto 4/5 | voeten naast foto 2/3 | spritemaat
R = os.path.join(HIER, '../referenties/')
vel = Image.new('RGB', (1500, 1130), 'white'); d = ImageDraw.Draw(vel)
vel.paste(opwit(model).convert('RGB').resize((700, 700), Image.LANCZOS), (0, 30)); d.text((10, 8), 'model (2D-overschildering op render_snel)', fill='black')
def foto(p, box, size): return Image.open(R + p).convert('RGB').crop(box).resize(size, Image.LANCZOS)
vel.paste(opwit(out.crop((20*K, 220*K, 190*K, 410*K))).convert('RGB').resize((340, 380), Image.LANCZOS), (720, 30))
vel.paste(foto('foto4_moeder_met_jong.jpg', (520, 120, 880, 520), (340, 378)), (1070, 30))
vel.paste(foto('foto5_zittend_hand_op_kop.jpg', (280, 110, 440, 290), (200, 225)), (1290, 420))
d.text((720, 8), 'kop (1,3x, Pokemon-verhouding)  |  foto 4 en 5', fill='black')
vel.paste(opwit(out.crop((205*K, 40*K, 290*K, 125*K))).convert('RGB').resize((260, 260), Image.LANCZOS), (720, 440))
vel.paste(opwit(out.crop((420*K, 395*K, 505*K, 480*K))).convert('RGB').resize((260, 260), Image.LANCZOS), (990, 440))
d.text((720, 418), 'bovenste voet (grijpt)  |  onderste voet (slap)', fill='black')
vel.paste(foto('foto2_hangend_lange_armen.jpg', (180, 400, 330, 560), (180, 192)), (720, 720))
vel.paste(foto('foto3_klimmend_tak.jpg', (60, 200, 200, 324), (200, 177)), (920, 720))
d.text((720, 700), 'foto 2 / 3 (voeten)', fill='black')
k8 = Image.open(os.path.join(HIER, 'model_64.png')).convert('RGB')
vel.paste(k8.crop((0, 0, 512, 512)).resize((400, 400), Image.NEAREST), (0, 730))
vel.paste(k8.crop((522, 0, 660, 512)).resize((138, 512)).crop((0, 0, 138, 200)), (420, 760))
d.text((10, 735 - 18), 'spritemaat: 64 px breed, verkleind (8x en 1x/2x)', fill='black')
vel.save(os.path.join(HIER, 'vel_model.png'))
print('ok')
