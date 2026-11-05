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

def bol(mask, ramp, R=12.0, licht=(-0.55, -0.65, 0.55), extra=None, gewicht=None):
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
    if gewicht is not None: a = a * gewicht[..., None]
    img[..., :3] = img[..., :3] * (1 - a) + out * a
    img[..., 3:] = np.maximum(img[..., 3:], a)

def omlijn(mask, dikte=4.6, niet=None):
    dd = nd.distance_transform_edt(~mask) / K
    ring = (dd > 0) & (dd <= dikte)
    if niet is not None: ring &= ~niet
    verf(ring, LIJN)

def gum(mask):
    img[mask] = 0

# ------------------------------------------------------------------ staart
# Jordi 5 nov: "de staart iets minder recht, iets meer vanuit een hoek" -> spiraal gekanteld (verkort 0,72 langs de
# as van de staartwortel naar het spiraalmidden); de wortel blijft vast aan het lijf.
yyS, xxS = np.mgrid[0:W, 0:W] / K
ANK = np.array([378.0, 300.0]); AS = np.array([455.0, 262.0]) - ANK; AS /= np.linalg.norm(AS)
VERK = 0.72
STAP2 = True
zone = (xxS > 335) & (yyS < 368)
rel = np.dstack([xxS - ANK[0], yyS - ANK[1]])
para = rel @ AS
alfa = np.clip(para / 40.0, 0, 1) * zone   # geleidelijk vanaf de wortel: geen naad
src = rel + (alfa * (para / VERK - para))[..., None] * AS
sx = (src[..., 0] + ANK[0]) * K; sy = (src[..., 1] + ANK[1]) * K
nieuw = np.zeros_like(img)
for ch in range(4):
    nieuw[..., ch] = nd.map_coordinates(img[..., ch], [sy, sx], order=1, mode='constant')
img[zone] = nieuw[zone]

# ------------------------------------------------------------------ voeten
# Muriqui-voet (Jordi/SPEC 5 nov): lange behaarde zool, vier tenen samen als gekrulde want, grote teen los.
# Bovenste voet: grijpt een onzichtbare tak boven de enkel (vuist, geen gat); onderste voet: slap, tenen licht gekruld.

# bovenste voet: slanke lange voet omhoog, vier tenen als want over de (onzichtbare) tak, grote teen ervoor
ALPHA0 = np.asarray(SRC.resize((W, W)))[..., 3] > 0
gum(masker_poly([(200, 30), (300, 30), (300, 101), (200, 101)], smooth=False))
# Jordi 5 nov: "Bovenste poot lijkt wel los te zitten" -> onderbeen + voet één vorm (geen knieknik, geen enkelnaad),
# zacht overgevloeid in de dij.
onderbeen = masker_poly([(198, 276), (198, 260), (198, 244), (199, 228), (202, 212), (206, 196), (210, 172),
                          (214, 140), (218, 112), (216, 98), (214, 84), (217, 70), (226, 59), (240, 53), (256, 54),
                          (269, 61), (277, 73), (276, 87), (268, 97), (257, 102), (253, 112), (255, 135),
                          (257, 162), (254, 186), (251, 208), (254, 228), (261, 237), (269, 245), (276, 252), (286, 264), (300, 280)])
yb, xb = np.mgrid[0:W, 0:W] / K
onderbeen &= ~((yb > 248) & ~ALPHA0)
gum((yb < 251) & (xb > 185) & (xb < 300) & ~onderbeen)
# schaduw = de eigen doorsnede van de render (dij, rij 230) langs het nieuwe been getrokken: naadloos met de dij
SRC4 = np.asarray(SRC.resize((W, W), Image.LANCZOS)).astype(np.float32) / 255.0
rij = 230 * K
r_a = SRC4[rij, :, 3] > 0.5
r_rgb = SRC4[rij, :, :3]
binnen = [x for x in range(196 * K, 262 * K) if r_a[x] and r_rgb[x].sum() > 0.9]
prof = r_rgb[binnen[0] + 3 * K:binnen[-1] + 1 - 3 * K]
tp = np.linspace(0, 1, len(prof))
kleur = np.zeros((W, W, 3), np.float32)
rijen = np.where(onderbeen.any(axis=1))[0]
for y in rijen:
    xs = np.where(onderbeen[y])[0]
    L, R_ = xs[0], xs[-1]
    t = (np.arange(L, R_ + 1) - L) / max(R_ - L, 1)
    for ch in range(3): kleur[y, L:R_ + 1, ch] = np.interp(t, tp, prof[:, ch])
mw = nd.gaussian_filter(onderbeen.astype(np.float32), (2 * K, 0.5 * K))[..., None]
kleur = nd.gaussian_filter(kleur, (2 * K, 0.5 * K, 0)) / np.maximum(mw, 1e-3)
w = (onderbeen * np.clip((256 - yb) / 20, 0, 1)).astype(np.float32)[..., None]
img[..., :3] = img[..., :3] * (1 - w) + kleur * w
img[..., 3:] = np.maximum(img[..., 3:], w)
# omlijning: overal boven de dij, en verder alleen waar nu een gat zit (geen lijnen over arm/romp)
dd = nd.distance_transform_edt(~onderbeen) / K
ring = (dd > 0) & (dd <= 4.6) & (yb < 254) & ((yb < 236) | (img[..., 3] < 0.5))
verf(ring, LIJN)
# tenen als gesloten want om de tak, grote teen ervoor (binnen de omtrek)
# voet als want (foto Jordi 5 nov, muriqui aan een touw): bovenkant behaard, tenen samen naar onder gekruld,
# ronde hiel, donkere kale zool zichtbaar waar de voet kantelt; geen losse vingers/grote teen
# bovenste: alleen de behaarde buitenkant van de want; één vouwlijn waar de tenen omkrullen
verf(lijnmasker([(256, 66), (265, 78), (264, 92)], 2.2), LIJN)

# onderste been (knie -> voet) in één stuk, schaduw = doorsnede van de render (x=380, licht boven -> donker onder,
# donkerste tint opgehaald), zacht overgevloeid in de dij; voet hangt slap, tenen licht gekruld, grote teen los
yb, xb = np.mgrid[0:W, 0:W] / K
been2 = masker_poly([(350, 398), (356, 389), (366, 384), (380, 382), (398, 381), (418, 385), (438, 392), (455, 402), (466, 411), (478, 420),
                      (489, 433), (496, 447), (499, 462), (494, 476), (483, 481), (472, 476), (465, 463), (456, 454),
                      (447, 449), (440, 440), (425, 431), (410, 424), (396, 421), (382, 424), (366, 430), (352, 428)])
gum((((xb > 372) & (yb > 360)) | ((xb > 357) & (yb > 377) & (yb < 392))) & (yb < 495) & ~been2)
SRC4b = np.asarray(SRC.resize((W, W), Image.LANCZOS)).astype(np.float32) / 255.0
prof = SRC4b[385 * K:420 * K, 380 * K, :3]
prof = np.maximum(prof, c(VACHT[1]) * 0.95)
tp = np.linspace(0, 1, len(prof))
d2 = np.array([0.864, 0.504]); n2 = np.array([-d2[1], d2[0]]); P0 = np.array([380.0, 405.0])
u = (xb - P0[0]) * d2[0] + (yb - P0[1]) * d2[1]
sv = (xb - P0[0]) * n2[0] + (yb - P0[1]) * n2[1]
ub = np.round(u).astype(int)
kleur = np.zeros((W, W, 3), np.float32)
idx = np.where(been2)
for b_ in np.unique(ub[idx]):
    sel = been2 & (ub == b_)
    ss = sv[sel]; lo, hi = ss.min(), ss.max()
    t = (ss - lo) / max(hi - lo, 1e-3)
    for ch in range(3): kleur[..., ch][sel] = np.interp(t, tp, prof[:, ch])
mw = nd.gaussian_filter(been2.astype(np.float32), 1.5 * K)[..., None]
kleur = nd.gaussian_filter(kleur, (1.5 * K, 1.5 * K, 0)) / np.maximum(mw, 1e-3)
w = (been2 * np.clip((xb - 356) / 40, 0, 1)).astype(np.float32)[..., None]
img[..., :3] = img[..., :3] * (1 - w) + kleur * w
img[..., 3:] = np.maximum(img[..., 3:], w)
dd = nd.distance_transform_edt(~been2) / K
verf((dd > 0) & (dd <= 4.6) & ((xb > 372) | (img[..., 3] < 0.5)), LIJN)
zool2 = masker_poly([(446, 440), (456, 441), (466, 448), (474, 458), (483, 465), (493, 462), (499, 470),
                      (490, 482), (479, 483), (469, 476), (463, 464), (454, 456), (444, 451)]) & been2
bol(zool2, GEZICHT, R=4, licht=(-0.3, -0.9, 0.4))
verf(lijnmasker([(488, 440), (493, 455), (490, 468)], 2.2), LIJN)

# ------------------------------------------------------------------ rugpatroon
# Jordi 5 nov: "verder gaan met het patroon op de rug, wat misschien nu wel een typisch zuid amerikaans patroon kan zijn".
# Fase 2 had drie lichte tapse wiggen vanaf de ruggengraat; fase 3: dezelfde wiggen, nu getrapt (Andes-trapmotief,
# chakana/tocapu). Grote vlakken (op 64: basis ±3 px, treden ±1 px), geen dunne lijnen (afgekeurd).
LILA = np.array([200, 194, 236], np.float32) / 255
yR, xR = np.mgrid[0:W, 0:W] / K
binnen = nd.distance_transform_edt(img[..., 3] > 0.5) / K > 5.0
# Jordi: "die moeten mee bewegen met het perspectief, houd er rekening mee dat het een pose is" -> wiggen op een
# cilinder om de romp (as langs de rug, kop-kant naar de kijker gekanteld), terug geprojecteerd naar beeld.
d_ = np.array([0.85, 0.53]); n_ = np.array([0.53, -0.85]); P0 = np.array([240.0, 238.0])
A = (xR - P0[0]) * d_[0] + (yR - P0[1]) * d_[1]; C = (xR - P0[0]) * n_[0] + (yR - P0[1]) * n_[1]
romp = (img[..., 3] > 0.5) & (A > -10) & (A < 125) & (C > -95) & (C < 40)
bins = np.arange(-10, 126)
cmax = np.full(len(bins), np.nan)
Ai = np.round(A).astype(int)
for i, b_ in enumerate(bins):
    sel = romp & (Ai == b_)
    if sel.any(): cmax[i] = C[sel].max()
cmax = nd.median_filter(np.nan_to_num(cmax, nan=np.nanmedian(cmax)), 15)
RR = 44.0; TILT = np.radians(28)
rug = np.interp(A, bins, cmax)                      # rugrand per positie langs de as
phi = np.arcsin(np.clip((C - (rug - RR)) / RR, -1, 1))  # 90 graden = rug, 0 = naar de kijker
a_opp = (A - RR * np.cos(phi) * np.sin(TILT)) / np.cos(TILT)   # positie op het oppervlak langs de as
wig = np.zeros((W, W), bool)
graden = np.degrees(phi)
treden = [(52, 12.0), (20, 8.0), (-10, 4.5), (-32, 1.6)]  # tot welke hoek (vanaf de rug) welke halve breedte
for a0, sch in ((40, 1.0), (68, 1.0), (96, 0.9)):
    hb = np.zeros_like(graden)
    vorige = 95
    for g, h in treden:
        hb = np.where((graden <= vorige) & (graden > g), h * sch, hb)
        vorige = g
    wig |= (np.abs(a_opp - a0) <= hb) & romp
wig &= binnen
lum = img[..., :3].mean(axis=2); ref = np.median(lum[binnen])
fac = np.clip(lum / ref, 0.55, 1.25) ** 0.7
img[wig, :3] = np.clip(LILA * fac[wig][:, None], 0, 1)

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
zilver = handzone & (SRC4[..., 2] - SRC4[..., 0] < 0.12) & (SRC4[..., :3].mean(axis=2) > 0.42) & (SRC4[..., 3] > 0.5)
zilver = nd.binary_opening(zilver, structure=np.ones((5, 5)))
lab, nlab = nd.label(zilver); grootste = np.argmax(np.bincount(lab.ravel())[1:]) + 1
zilver = nd.binary_fill_holes(lab == grootste)
hand = (nd.distance_transform_edt(~zilver) / K <= 5.0) & (SRC4[..., 3] > 0.5) & ~((xx < 103) & (yy < 397) & (yy > 376))

# Stap 3 (Jordi 5 nov): "Het hoofd mag iets meer in driekwart, het gezicht mag een 20% meer van het totale hoofd in
# gebruik nemen en de maan mag daar nog boven, die mag echt wel 2 tot 3 keer zo groot."
# Gezicht frontaal ontworpen (midden x=107) en over de bol van de kop gedraaid (yaw 22 graden naar links);
# snuit steekt uit (grotere straal), dus verschuift verder. Gezicht 1,2x (lineair), maan 2,5x.
YAW = np.radians(18); RB = 54.0; FS = 1.2
def M(x, y, r=1.0):
    dx, dy = x - 107, y - 320
    lat = np.arcsin(np.clip(dy / (RB * r), -0.99, 0.99)); cl = np.cos(lat)
    lon = np.arcsin(np.clip(dx / (RB * r * cl), -0.99, 0.99))
    return T(107 + RB * r * cl * np.sin(lon - YAW), 320 + dy)
def F(x, y, r=1.0): return M(107 + (x - 101) * FS, 370 + (y - 370) * FS, r)  # groeit vanaf de kin omhoog
def FP(pts, r=1.0): return [F(x, y, r) for x, y in pts]
def FE(cx, cy, rx, ry, r=1.0, n=40):
    return masker_poly([F(cx + rx*np.cos(t), cy + ry*np.sin(t), r) for t in np.linspace(0, 2*np.pi, n, endpoint=False)], smooth=False)
def ME(cx, cy, rx, ry, n=48):
    return masker_poly([M(cx + rx*np.cos(t), cy + ry*np.sin(t)) for t in np.linspace(0, 2*np.pi, n, endpoint=False)], smooth=False)

kop = E(107, 320, 52, 56) | masker_poly(FP([(84, 352), (118, 352), (117, 372), (108, 380), (94, 380), (85, 372)]))
schild = masker_poly(FP([(72, 315), (80, 309), (101, 308), (122, 309), (130, 315), (133, 328), (131, 344), (126, 360),
                         (118, 372), (108, 379), (101, 380), (94, 379), (84, 372), (76, 360), (71, 344), (69, 328)]))
snuit = masker_poly(FP([(FX - 3, 332), (FX + 3, 332), (FX + 6, 341), (FX + 12, 349), (FX + 16, 357), (FX + 16, 364),
                        (FX + 11, 370), (FX, 372), (FX - 11, 370), (FX - 16, 364), (FX - 16, 357), (FX - 12, 349), (FX - 6, 341)], 1.12))
# in driekwart steekt de snuit (en de kin eronder) over de kopomtrek: één omtrek om kop + gezicht + snuit
kin = masker_poly(FP([(FX - 15, 360), (FX + 15, 360), (FX + 12, 374), (FX, 380), (FX - 12, 374)], 1.06))
kop = nd.binary_closing(kop | schild | snuit | kin, structure=np.ones((9, 9)))
omlijn(kop)
bol(kop, VACHT, R=36)
schild = (schild | kin) & kop
bol(schild, GEZICHT, R=13)
verf(masker_poly(FP([(78, 314.5), (124, 314.5), (124, 318), (78, 318)])) & schild, GEZICHT[0], 0.75)
for ox in (FX - 9.5, FX + 9.5):
    verf(FE(ox, 325, 6.4, 5.8), GEZICHT[0])
    bol(FE(ox, 325.4, 5.0, 4.8), [(84, 140, 200), (140, 190, 234), (190, 222, 246)], R=4)
    verf(FE(ox + 0.6, 326.0, 2.0, 2.3), (20, 28, 58))
    verf(FE(ox - 1.8, 324.0, 1.2, 1.2), (255, 255, 255))
verf(masker_poly(FP([(80, 317.5), (122, 317.5), (122, 321.2), (80, 321.2)]), smooth=False) & schild, GEZICHT[0])
bol(snuit, SNUIT, R=8)
for nx, k in ((FX - 4, -1), (FX + 4, 1)):
    verf(masker_poly(FP([(nx - 2.6*k, 349.5), (nx + 0.8*k, 346.5), (nx + 2.4*k, 348.5), (nx + 0.4*k, 351.5)], 1.14)), (52, 34, 64))
verf(lijnmasker(FP([(FX - 12, 362.5), (FX - 4, 363.2), (FX + 4, 363.2), (FX + 12, 362.5)], 1.1), 3.4), (34, 24, 46))
# maan boven het gezicht, 2,5x: brede sikkel (hoorns omlaag), ±2 px dik op 64
maan = ME(107, 284, 29, 15) & ~ME(107, 292, 31, 14)
verf(maan & kop, (236, 236, 246))
# healerhand ligt vóór de kop
a_ = hand.astype(np.float32)[..., None]
img[:] = img * (1 - a_) + SRC4 * a_

# restje oude kin tussen nieuwe kin en hand weg
yk, xk = np.mgrid[0:W, 0:W] / K
img[(xk > 84) & (xk < 112) & (yk > 378) & (yk < 398) & ~kop & ~hand] = 0
# gloed om de healerhand (Jordi 5 nov: "een lichtblauwe gloed graag om de hand heen"); als vlakke banden met eigen
# omlijning (Reuniclus/Duosion), zodat hij in de sprite werkt; niet over het gezicht
yh, xh = np.mgrid[0:W, 0:W] / K
handvol = nd.binary_fill_holes(hand)
hl = handvol & (nd.distance_transform_edt(handvol) / K > 4.5)
dg = nd.distance_transform_edt(~handvol) / K
vrij = ~kop
g1 = (dg > 0) & (dg <= 4.5) & vrij; g2 = (dg > 4.5) & (dg <= 9.5) & vrij; gl = (dg > 9.5) & (dg <= 11.8) & vrij
verf(gl, (78, 126, 192)); verf(g2, (186, 222, 250)); verf(g1, (140, 196, 242))
# zweem blauw in de palm
verf(hl, (170, 214, 248), 0.22)
# heup rechts: uitsteeksels in de omtrek wegslijpen (opening in een klein vak)
yv, xv = np.mgrid[0:W, 0:W] / K
vak = ((yv > 240) & (yv < 270) & (xv > 255) & (xv < 305))
A = img[..., 3] > 0.5
weg = vak & A & ~nd.binary_opening(A, structure=np.ones((13, 13)))
img[weg] = 0
img[(yv > 368) & (yv < 378.6) & (xv > 362) & (xv < 376)] = 0  # restje oude knie-omlijning
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
