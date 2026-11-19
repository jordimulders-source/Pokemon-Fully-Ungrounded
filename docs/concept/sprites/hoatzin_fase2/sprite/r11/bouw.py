# r10 bouw: lagen achter -> voor, per onderdeel Gen 3-schaduw; geometrie in geom.py (afgelezen op MODEL.png).
# Uitvoer: basis.npy / basis.png (zonder handwerk aan de kop); kop.py zet daarna kop + oog met de hand.
import numpy as np
from PIL import Image
from geom import *

ORDER = ['verre', 'staart', 'lijf', 'buik', 'vleugel', 'poot_v', 'poot_n', 'kuif']
part = np.full((64,64), -1)

def zet(mask, nm):
    part[mask] = ORDER.index(nm)

# ---------------- poten (model, legs.png) ----------------
def poot(segs):
    m = np.zeros((64,64), bool); tips = []
    for pts, w0, w1, tip in segs:
        m |= capsule(pts, w0, w1)
        if tip: tips.append(pts[-1])
    return m, tips
POOT_V = [([(26.6,49.6),(25.4,52.2),(24.4,54.8)], 1.25, 1.05, False),
          ([(24.4,55.6),(20.5,56.6),(17.2,57.4)], 1.05, 0.55, True),
          ([(24.2,56.0),(24.0,58.4),(23.8,60.4)], 0.95, 0.55, True),
          ([(25.0,55.8),(27.0,56.4),(28.6,57.0)], 0.85, 0.55, True)]
POOT_N = [([(33.4,49.6),(33.0,52.4),(32.6,55.2)], 1.35, 1.1, False),
          ([(32.4,56.0),(31.2,59.4),(30.4,62.6)], 1.05, 0.6, True),
          ([(33.2,55.8),(35.0,57.0),(36.6,58.2)], 0.95, 0.55, True),
          ([(31.8,56.0),(30.2,56.6),(28.9,57.2)], 0.85, 0.55, True)]
pv, tips_v = poot(POOT_V); pn, tips_n = poot(POOT_N)

# ---------------- kuif: plukken (model, kop.png) ----------------
KUIF = [   # (naam, middellijn basis -> punt, breedte basis, max (op 35%), punt); afgelezen op kopm.png (model 30x)
 ('K1', [(9.8,19.6),(8.4,14.6),(6.4,9.0)], 1.6, 1.9, 0.5),
 ('K2', [(11.2,19.6),(11.0,14.5),(10.9,10.0)], 1.6, 1.9, 0.5),
 ('K3', [(12.6,19.6),(14.4,14.0),(16.4,10.0)], 1.6, 1.9, 0.5),
 ('K4', [(13.8,19.6),(18.0,13.4),(21.0,9.4),(23.2,7.4)], 1.6, 1.9, 0.5),
 ('K5', [(14.8,19.8),(20.0,14.8),(26.4,12.3)], 1.6, 1.9, 0.5),
 ('K6', [(15.8,20.4),(21.0,16.4),(25.4,16.6),(29.6,19.4)], 1.6, 1.9, 0.5),
]
def wprof(t, a, b, c):
    return np.where(t < 0.35, a+(b-a)*t/0.35, b+(c-b)*(t-0.35)/0.65)
kuifm = np.zeros((64,64), bool); kuif_own = np.full((64,64), -1)
for i, (nm, pts, a_, b_, c_) in enumerate(KUIF):
    d, t, dx, dy = segdist(PX, PY, pts); m = d <= wprof(t, a_, b_, c_)
    kuifm |= m; kuif_own[m] = i

KUIF_AUTO = False
if not KUIF_AUTO: kuifm[:] = False
alles = fill2 | fill | pv | pn | kuifm
# lagen
zet(verre & alles, 'verre'); zet(staart, 'staart'); zet(lijf, 'lijf'); zet(buikfill, 'buik'); zet(vleugel, 'vleugel')
# r9-poten weg (onder de buik), modelpoten erin
oudpoot = alles & (YY >= 49) & ~staart & ~buikfill & ~vleugel
part[oudpoot] = -1
zet(pv, 'poot_v'); zet(pn, 'poot_n'); zet(kuifm, 'kuif')
# vulling = alles met een onderdeel
vul = part >= 0

out = np.zeros((64,64), int)
ROL = np.full((64,64), -1)
TT = np.zeros((64,64))
def kleur_pennen(zone, pens, tonen, lichtdeel=1.0, schaal=1.0):
    ds = []; dirs = []
    for nm, pts, *_ in pens:
        d, t, dx, dy = segdist(PX, PY, pts); ds.append(d); dirs.append((dx, dy, t))
    ds = np.array(ds); k = ds.argmin(0); own = np.where(zone, k, -1)
    def lid(yy, xx): return own[yy, xx] if (0 <= yy < 64 and 0 <= xx < 64) else -1
    for i in range(len(pens)):
        lt, md, dk = tonen[i][:3]; ls = tonen[i][3] if len(tonen[i]) > 3 else 0.0; dx, dy, t = dirs[i]
        nx, ny = dy, -dx; flip = (-nx-ny) < 0; nx = np.where(flip, -nx, nx); ny = np.where(flip, -ny, ny)
        for y, x in zip(*np.nonzero(own == i)):
            ox, oy = int(round(nx[y,x])), int(round(ny[y,x]))
            up = lid(y+oy, x+ox); dn = lid(y-oy, x-ox)
            c = 1
            if dn != i and dn >= 0: c = 2
            elif up != i and t[y,x] >= ls: c = 0
            ROL[y, x] = c; TT[y, x] = t[y, x]
    return own

Z = {nm: part == ORDER.index(nm) for nm in ORDER}
# lijf: pseudo-3D
Hh = blur(Z['lijf'] | Z['buik'] | Z['vleugel'], 2.2)
gx = np.gradient(Hh, axis=1); gy = np.gradient(Hh, axis=0); lam = (gx*0.7 + gy*0.7)
MC = np.load('modelcel.npy').mean(2); MCs = blur(MC, 0.7)
# nek: lichter mauve dan de vleugel (Jordi: nek moet zich onderscheiden), donkere nekband achter de kop
out[Z['lijf']] = L5
out[Z['lijf'] & (lam < 0.0)] = M4
out[Z['lijf'] & (MCs < 70)] = D3
out[Z['lijf'] & (MCs < 40)] = D2
# streepjes uit het model als enkele doorlopende lijnen: licht in de donkere nekband, donker in de lichte hals
def lijn(pts, kleur, alleen):
    d, t, _, _ = segdist(PX, PY, pts); m = (d < 0.5) & Z['lijf'] & np.isin(out, alleen); out[m] = kleur
lijn([(17.5,24.5),(20.0,29.0),(22.5,33.5)], M4, [D2, D3])
lijn([(20.5,23.0),(23.0,27.5),(24.8,31.0)], M4, [D2, D3])
lijn([(14.5,27.5),(16.5,31.5),(18.5,35.0)], M4, [M4, L5])
lijn([(17.0,30.0),(19.5,34.5),(21.0,37.0)], M4, [L5])
# buik
Hb = blur(Z['buik'] | Z['lijf'], 1.8); gx = np.gradient(Hb, axis=1); gy = np.gradient(Hb, axis=0); lb = gx*0.7+gy*0.7
out[Z['buik']] = BU12
hl = ((PX-20.8)/3.0)**2 + ((PY-40.3)/2.3)**2 <= 1
out[Z['buik'] & hl] = BU13
out[Z['buik'] & (lb < -0.085)] = BU11
zb = Z['buik']; dn = np.zeros_like(zb); dn[:-1] = ~zb[1:]; rt = np.zeros_like(zb); rt[:, :-1] = ~zb[:, 1:]
out[zb & (dn | rt) & (YY > 41)] = BU11
# pennen
MLb = blur(np.load('modelcel.npy').mean(2), 1.2)
TAB = {2: (L5, M4, D3), 1: (M4, D3, D2), 0: (D3, D2, LINE)}
def macro(z, hoog=95, laag=60):
    lv = np.where(MLb >= hoog, 2, np.where(MLb >= laag, 1, 0)); return lv
own_f = kleur_pennen(Z['verre'], FV, [(0,0,0,0.3)]*len(FV))
own_t = kleur_pennen(Z['staart'], TAIL, [(0,0,0,0.0)]*len(TAIL))
own_w = kleur_pennen(Z['vleugel'], PENS, [p[2] for p in PENS])
# niveau per pen (gemiddelde modelhelderheid per pen, zie NOTITIES): 2 licht, 1 midden, 0 donker
NIV = {'P1':2,'P2':2,'P3':2,'P4':2,'P5':2,'P6':2,'P7':2,'P8':1,'C1':0,'C2':0,'C3':0,'C4':0,
       'I1':1,'I2':2,'I3':2,'A1':1,'A2':1,'A3':1}
LV = np.zeros((64,64), int)
for i, p in enumerate(PENS):
    LV[Z['vleugel'] & (own_w == i)] = NIV[p[0]]
LV[Z['verre']] = 1; LV[Z['staart']] = 0
for zn in ('verre', 'staart', 'vleugel'):
    for y, x in zip(*np.nonzero(Z[zn] & (ROL >= 0))):
        c = TAB[LV[y, x]][ROL[y, x]]
        if c == LINE and TT[y, x] < 0.45: c = D2
        out[y, x] = c
# poten: licht links/boven, donker rechts/onder
for zm, segs, (lt, md, dk) in ((Z['poot_v'], POOT_V, (G14, D3, D2)), (Z['poot_n'], POOT_N, (G15, G14, D2))):
    Hp = blur(zm, 0.8); gx = np.gradient(Hp, axis=1); gy = np.gradient(Hp, axis=0); l = gx*0.75+gy*0.65
    out[zm] = md; out[zm & (l > 0.05)] = lt; out[zm & (l < -0.06)] = dk
KS = 0.45
# kuif: binnenste deel = kruin als één massa (licht linksboven, sikkel onder), buitenste deel = losse plukken
kz = Z['kuif']
Hk = blur(kz, 1.3); gx = np.gradient(Hk, axis=1); gy = np.gradient(Hk, axis=0); lk = gx*0.7+gy*0.7
out[kz] = BR6
out[kz & (lk > 0.07)] = BR7
out[kz & (lk < -0.08)] = D2
KT = np.zeros((64,64)); OFF = np.zeros((64,64)); WL = np.zeros((64,64))
for i, (nm, pts, a_, b_, c_) in enumerate(KUIF):
    m = kz & (kuif_own == i)
    best = np.full((64,64), 1e9); off = np.zeros((64,64)); tt = np.zeros((64,64))
    L = [np.hypot(pts[j+1][0]-pts[j][0], pts[j+1][1]-pts[j][1]) for j in range(len(pts)-1)]; tot = sum(L); acc = 0
    for j in range(len(pts)-1):
        (x0,y0),(x1,y1) = pts[j],pts[j+1]; vx,vy = x1-x0,y1-y0; l2 = vx*vx+vy*vy
        u = np.clip(((PX-x0)*vx+(PY-y0)*vy)/l2,0,1); qx = x0+u*vx; qy = y0+u*vy; dd = np.hypot(PX-qx,PY-qy)
        n_x,n_y = vy/np.sqrt(l2),-vx/np.sqrt(l2)
        if -n_x-n_y < 0: n_x,n_y = -n_x,-n_y
        mm = dd < best; best[mm] = dd[mm]; off[mm] = ((PX-qx)*n_x+(PY-qy)*n_y)[mm]; tt[mm] = (acc+u[mm]*L[j])/tot
        acc += L[j]
    KT[m] = tt[m]; OFF[m] = off[m]; WL[m] = wprof(tt, a_, b_, c_)[m]
buiten = kz & (KT > KS)
out[buiten] = BR6
out[buiten & (OFF > np.maximum(WL-1.0, 0.0))] = BR7
out[buiten & (OFF < -(WL-0.9)) & (WL > 1.1)] = D2
# scheiding: achterste pluk krijgt een donkere lijn langs de voorste (buitenste deel)
ko = kuif_own
for y, x in zip(*np.nonzero(kz)):
    for a, b in ((0,1),(0,-1),(1,0),(-1,0)):
        yy, xx = y+a, x+b
        if 0 <= yy < 64 and 0 <= xx < 64 and kz[yy, xx] and ko[yy, xx] > ko[y, x] and KT[y, x] > KS:
            out[y, x] = D2; break

# ---------------- binnenlijnen: vorm over vorm -> onderliggende pixel donker ----------------
CAST = {'verre': D2, 'staart': LINE, 'lijf': D3, 'buik': BU11, 'vleugel': D3}
pp = part.copy()
for y in range(64):
    for x in range(64):
        p = pp[y, x]
        if p < 0: continue
        nm = ORDER[p]
        if nm not in CAST: continue
        for dy_, dx_ in ((0,1),(0,-1),(1,0),(-1,0)):
            yy, xx = y+dy_, x+dx_
            if 0 <= yy < 64 and 0 <= xx < 64 and pp[yy, xx] > p:
                voor = ORDER[pp[yy, xx]]
                if nm == 'lijf' and voor == 'buik': continue
                if nm == 'buik' and voor.startswith('poot'): continue
                if nm in ('lijf','buik') and voor == 'vleugel': out[y, x] = D2 if nm == 'lijf' else BU11; break
                out[y, x] = CAST[nm]; break

# ---------------- buitenlijn ----------------
ring = nb4(vul) & ~vul
# ook diagonale hoeken van dunne delen niet nodig: 4-ring
Hv = blur(vul, 1.4); gx = np.gradient(Hv, axis=1); gy = np.gradient(Hv, axis=0)
SEL = {'verre': D2, 'staart': D2, 'lijf': D3, 'buik': BU11, 'vleugel': D3, 'poot_v': D2, 'poot_n': G14, 'kuif': D2}
for y, x in zip(*np.nonzero(ring)):
    # naar welk onderdeel grenst de ring
    nbp = [part[y+a, x+b] for a, b in ((0,1),(0,-1),(1,0),(-1,0)) if 0 <= y+a < 64 and 0 <= x+b < 64 and part[y+a, x+b] >= 0]
    nm = ORDER[max(nbp)]
    # buitennormaal = -gradient; lichtkant als normaal naar linksboven wijst
    licht = (gx[y, x]*0.7 + gy[y, x]*0.7) > 0.035
    out[y, x] = SEL[nm] if licht else LINE
out[vul] = np.where(out[vul] == 0, M4, out[vul])

np.save('basis.npy', out); np.save('part.npy', part)
im = Image.fromarray(out.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('basis.png', transparency=0)
