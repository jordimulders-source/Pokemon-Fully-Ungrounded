# r10: Gen 3-kleurronde per onderdeel op het r9-silhouet; geometrie (pennen, plukken, poten) afgelezen op MODEL.png
# via modelgrid.py (spritecoordinaten, continu: pixel x beslaat [x,x+1)). Uitvoer: basis.npy (indexen) + basis.png
import numpy as np, json, sys
from PIL import Image
R9 = np.array(Image.open('../r9/hoatzin.png'))
H, W = 64, 64
YY, XX = np.mgrid[0:64, 0:64]; PX = XX + 0.5; PY = YY + 0.5

PAL = [(152,208,160),(28,16,30),(60,36,58),(100,68,94),(146,112,138),(188,154,178),
       (118,60,40),(170,98,58),(46,56,138),(98,124,218),(216,50,74),
       (76,40,96),(124,68,152),(180,124,214),(98,96,122),(150,148,174)]
LINE, D2, D3, M4, L5, BR6, BR7, BL8, BL9, RED, BU11, BU12, BU13, G14, G15 = range(1,16)

def blur(a, s=1.6):
    r = int(3*s)+1; k = np.exp(-np.arange(-r, r+1)**2/(2*s*s)); k /= k.sum()
    b = np.pad(a.astype(float), r, mode='constant')
    b = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 0, b)
    b = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 1, b)
    return b[r:-r, r:-r]

def nb4(m):
    o = np.zeros_like(m)
    o[1:] |= m[:-1]; o[:-1] |= m[1:]; o[:, 1:] |= m[:, :-1]; o[:, :-1] |= m[:, 1:]
    return o

def segdist(px, py, pts):
    """afstand tot polyline + parameter t (0..1 langs de lijn) + richting van het dichtstbijzijnde segment"""
    best = np.full(px.shape, 1e9); tt = np.zeros(px.shape); dx = np.zeros(px.shape); dy = np.zeros(px.shape)
    L = [np.hypot(pts[i+1][0]-pts[i][0], pts[i+1][1]-pts[i][1]) for i in range(len(pts)-1)]; tot = sum(L); acc = 0
    for i in range(len(pts)-1):
        (x0, y0), (x1, y1) = pts[i], pts[i+1]
        vx, vy = x1-x0, y1-y0; l2 = vx*vx+vy*vy
        u = np.clip(((px-x0)*vx+(py-y0)*vy)/l2, 0, 1)
        d = np.hypot(px-(x0+u*vx), py-(y0+u*vy))
        m = d < best
        best[m] = d[m]; tt[m] = (acc+u[m]*L[i])/tot; dx[m] = vx/np.sqrt(l2); dy[m] = vy/np.sqrt(l2)
        acc += L[i]
    return best, tt, dx, dy

def capsule(pts, w0, w1):
    d, t, _, _ = segdist(PX, PY, pts)
    return d <= w0+(w1-w0)*t

# ---------------- basis: vulling = r9-masker min de buitenring ----------------
m9 = R9 > 0
fill = m9 & ~nb4(~m9)

# ---------------- onderdelen ----------------
# leading edge (voorrand nabije vleugel), van boven naar beneden; rechts ervan = vleugel
LE = [(36.8,8.0),(33.2,14),(29.8,21.5),(27.2,27.5),(25.4,32.5),(25.2,37),(26.8,41),(29.5,44.5),(33.5,47.5)]
def rechts_van(pts):
    d, t, dx, dy = segdist(PX, PY, pts)
    # kruisproduct richting x (p - dichtstbij): >0 = rechts van de lijn (y omlaag)
    best = np.full(PX.shape, 1e9); s = np.zeros(PX.shape)
    for i in range(len(pts)-1):
        (x0, y0), (x1, y1) = pts[i], pts[i+1]; vx, vy = x1-x0, y1-y0; l2 = vx*vx+vy*vy
        u = np.clip(((PX-x0)*vx+(PY-y0)*vy)/l2, 0, 1); dd = np.hypot(PX-(x0+u*vx), PY-(y0+u*vy))
        cr = vx*(PY-y0)-vy*(PX-x0)
        m = dd < best; best[m] = dd[m]; s[m] = cr[m]
    return s < 0   # lijn loopt omlaag; links-hand: cr<0 = rechts (oost) van de lijn
buik = np.isin(R9, [11,12,13])
buikfill = (buik | (fill & nb4(buik) & (YY > 36) & (XX < 36) & ~rechts_van(LE))) & fill
wingside = rechts_van(LE) & (YY < 50)
staart = fill & (PY > 47.0-0.75*(PX-33.5)) & (XX >= 33) & (YY >= 40)
vleugel = fill & wingside & ~staart & ~buikfill
verre = fill & ~vleugel & ~staart & ~buikfill & (YY <= 20) & (XX <= 30) & ~((XX <= 16) & (YY >= 18))

# ---------------- pennen nabije vleugel (afgelezen op het model) ----------------
# (naam, centerline, halve breedte, tonen licht/midden/scheiding)
FAN = (L5, M4, D3, 0.4); COV = (M4, D3, D2, 0.55); INN = (L5, M4, D3, 0.0); ARM = (M4, D3, D2, 0.15); EDGE = (L5, M4, D3, 0.0)
PENS = [
 ('P1', [(37.0,13.0),(40.0,7.0),(42.9,1.7)], FAN),
 ('P2', [(39.6,13.6),(44.0,8.0),(48.3,3.0)], FAN),
 ('P3', [(41.2,14.6),(47.0,9.4),(52.3,5.6)], FAN),
 ('P4', [(42.3,15.7),(48.5,12.0),(54.6,9.2)], FAN),
 ('P5', [(42.8,17.3),(49.5,15.2),(55.9,13.2)], FAN),
 ('P6', [(42.0,19.3),(49.5,17.9),(55.9,16.9)], FAN),
 ('P7', [(41.0,21.6),(48.0,21.4),(54.4,21.7)], FAN),
 ('P8', [(39.5,24.0),(46.0,24.2),(52.0,25.3)], FAN),
 ('C1', [(36.5,27.0),(43.5,27.4),(50.5,28.2)], COV),
 ('C2', [(35.5,30.0),(42.0,30.4),(48.5,31.4)], COV),
 ('C3', [(34.5,33.0),(40.0,33.4),(45.5,34.6)], COV),
 ('C4', [(33.5,36.0),(37.5,36.4),(41.0,37.6)], COV),
 ('I1', [(28.6,26.0),(31.0,20.0),(34.0,13.5),(37.6,8.6)], EDGE),
 ('I2', [(32.2,26.0),(35.0,20.0),(38.6,14.4)], INN),
 ('I3', [(36.0,25.5),(38.6,21.0),(41.0,17.5)], INN),
 ('A1', [(26.6,29.5),(26.4,35.0),(28.0,40.0),(31.5,44.5)], EDGE),
 ('A2', [(30.4,29.0),(31.8,35.0),(34.2,40.5),(37.0,45.0)], ARM),
 ('A3', [(34.4,29.5),(36.4,34.5),(38.8,39.5)], ARM),
]
# fan-silhouet uit pencapsules (tips en inkepingen uit het model) in het buitengebied
fanbuiten = (XX >= 38) & (YY <= 25)
penunion = np.zeros((64,64), bool)
for nm, pts, _ in PENS:
    if nm[0] in 'P': penunion |= capsule(pts, 1.9, 1.45)
rand9 = blur(m9.astype(float), 1.0) < 0.75   # dicht bij de r9-buitenrand
fill2 = fill.copy()
weg = fanbuiten & fill & ~penunion & rand9
bij = fanbuiten & penunion & ~fill
fill2[weg] = False; fill2[bij] = True
fill = fill2.copy()
vleugel = (vleugel & ~weg) | bij

# ---------------- verre vleugel achter de kop ----------------
FV = [
 ('F1', [(10.5,16.0),(9.6,9.0),(9.1,3.7)]),
 ('F2', [(13.2,16.0),(13.2,9.0),(13.1,4.0)]),
 ('F3', [(15.6,16.0),(16.4,10.0),(16.8,5.3)]),
 ('F4', [(18.0,16.0),(19.6,11.0),(20.6,8.0)]),
 ('F5', [(19.5,17.5),(22.4,13.0),(24.0,11.2)]),
]
lobes = np.zeros((64,64), bool)
for nm, pts in FV: lobes |= capsule(pts, 1.75, 1.45)
regio = (YY <= 13) & (XX <= 25)
weg2 = regio & fill & ~lobes & rand9
bij2 = regio & lobes & ~fill
fill[weg2] = False; fill[bij2] = True; fill2[weg2] = False; fill2[bij2] = True
verre = (verre & ~weg2) | bij2

# ---------------- staart ----------------
TAIL = [
 ('T1', [(40.5,42.0),(47.0,51.5),(52.5,61.0)]),
 ('T2', [(37.5,45.0),(43.0,53.0),(48.0,62.0)]),
 ('T3', [(34.5,48.0),(39.0,54.0),(43.5,61.0)]),
]

oudkuif = np.isin(R9, [6,7]) & (YY < 20) & ~lobes
fill[oudkuif] = False; fill2[oudkuif] = False; verre &= fill; vleugel &= fill
lijf = fill & ~vleugel & ~staart & ~buikfill & ~verre
