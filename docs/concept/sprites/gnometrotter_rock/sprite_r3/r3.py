# r3.py: Gnometrotter Rock ronde 3 = r2 + de 8 keurpunten (keuring_r2/KEURING.md), alles uit de modelmeting (meet.py:
# donker-aandeel en helderheid per spritepixel). Baard, riem/gesp, stok, zolen, neus, hand R, rugkamvorm, silhouet: r2.
import sys, numpy as np; from scipy import ndimage as nd
sys.path.insert(0,'../sprite')
from gemeen import *
R2='../sprite_r2/'
o=lees(R2+'gnometrotter_rock.png'); zone=np.load(R2+'zone.npy'); naad2=np.load(R2+'naad.npy'); fac=np.load(R2+'fac.npy')
m=np.load('meet.npz'); donk,hel=m['donk'],m['hel']
fg=o>0; r2=o.copy(); LOG={}
def log(k,X,Y): LOG.setdefault(k,[]).append((int(X),int(Y)))
OUT=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    if any(not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): OUT[Y,X]=True
def nms(Y,X,drempel):
    c=donk[Y,X]
    if c<drempel: return False
    g=lambda y,x: donk[y,x] if 0<=y<64 and 0<=x<64 else 0
    return (c>=g(Y,X-1) and c>=g(Y,X+1)) or (c>=g(Y-1,X) and c>=g(Y+1,X))
def binnen(z): return (zone==z)&~OUT
# 4. haar R op modelmaat: lichte modelpixels (hel >= 165, geen lijn) in het vak x32-40, y15-18 horen bij het plukje
for Y in range(15,19):
    for X in range(32,41):
        if fg[Y,X] and not OUT[Y,X] and hel[Y,X]>=165 and donk[Y,X]<0.35 and zone[Y,X] in (1,3,6):
            if zone[Y,X]!=3: log('haar R erbij',X,Y)
            zone[Y,X]=3
# tinten uit de modelhelderheid
def toon(z,Y,X):
    h=hel[Y,X]
    if z==6:  return 15 if h>=197 else (8 if h>=162 else 7)       # lijf: 7 / 8 / 15 (lichtste modelplek)
    if z==12: return 11 if h>=150 else 10                          # broek/benen: 10 / 11 (9 = lijn)
    if z==1:  return 5 if h>=145 else (4 if h>=112 else 3)        # muts/rugkam
    if z in (2,3): return 13 if h>=180 else 12                     # haar
for z in (6,12,1,2,3):
    for Y,X in zip(*np.where(binnen(z))):
        if z==1 and o[Y,X]==3 and Y in (16,17,18,19) and 24<=X<=31: continue   # dichte oogstrook (Jordi) blijft
        o[Y,X]=toon(z,Y,X)
# grote vlakken: meerderheidsfilter 3x3 binnen hetzelfde onderdeel (muts 5x5) tegen dambord
for z,r in ((1,2),(12,1),(6,1),(2,1),(3,1)):
    o2=o.copy()
    for Y,X in zip(*np.where(binnen(z))):
        t=[o[y,x] for y in range(Y-r,Y+r+1) for x in range(X-r,X+r+1) if 0<=y<64 and 0<=x<64 and zone[y,x]==z and not OUT[y,x]]
        c=np.bincount(t,minlength=16); o2[Y,X]=c.argmax() if c.max()>c[o[Y,X]] else o[Y,X]
    o=o2
# lijnen uit het model: donker-aandeel >= 0,35 en lokaal maximum (1 px), in muts (2), broek (9), lijf (6, naast de r2-facetnaden)
for z,b,dr in ((1,2,0.35),(12,9,0.22),(6,6,0.5)):
    for Y,X in zip(*np.where(binnen(z))):
        if nms(Y,X,dr): o[Y,X]=b
for Y,X in zip(*np.where(naad2&(zone==6))): o[Y,X]=6
# modellijn die naast de buitenlijn loopt = dubbele lijn: in de broek weg (buurtint)
for Y,X in zip(*np.where(binnen(12)&(o==9))):
    if sum(OUT[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))>=1 and sum(o[Y+dy,X+dx]==9 and not OUT[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)==0:
        o[Y,X]=toon(12,Y,X); log('dubbele lijn broek weg',X,Y)
# 3. schouderovaal rechts: eigen onderdeel = het r2-facet onder (45,24); lijn 6 rondom (ook de onderrand), vulling uit het model
ov=(fac==fac[24,45])&(zone==6)
rand=ov&nd.binary_dilation(~ov,structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))
bin_ov=list(zip(*np.where(ov&~rand&~OUT)))
for Y,X in bin_ov: o[Y,X]=8
for _,Y,X in sorted(((hel[Y,X],Y,X) for Y,X in bin_ov),reverse=True)[:4]: o[Y,X]=15   # glans op de 4 lichtste modelpixels
# 7. hooglicht lijf: op de lichtste modelplek buiten het ovaal (4 lichtste vlakpixels, aaneengesloten rond de lichtste)
kand=(zone==6)&~ov&~OUT&(o==8)
ys,xs=np.where(kand); i0=np.argmax(hel[ys,xs]); Y0,X0=ys[i0],xs[i0]
buurt=[(hel[Y,X],Y,X) for Y,X in zip(ys,xs) if abs(Y-Y0)<=1 and abs(X-X0)<=2]
for _,Y,X in sorted(buurt,reverse=True)[:4]: o[Y,X]=15; log('hooglicht lijf (lichtste modelplek)',X,Y)
for Y,X in zip(*np.where(rand)):
    if not OUT[Y,X]: o[Y,X]=6
# 8./4. haar: lijn 2 op de buitenrand (al outline), plukje R: rand naar de muts op de mutskant als het model daar donker is
hr=zone==3
for Y,X in zip(*np.where(nd.binary_dilation(hr)&~hr&(zone==1))):
    if donk[Y,X]>=0.15 and o[Y,X]!=2: o[Y,X]=2; log('lijn om haar R (mutskant)',X,Y)
for Y,X in zip(*np.where(hr&~OUT)):
    if any(zone[Y+dy,X+dx] in (6,) for dy,dx in ((1,0),(0,1),(0,-1))): o[Y,X]=2      # onderrand plukje tegen het gezicht
# 5. linkerarm (x11-17, y31-33) zonder dambord: bovenrij lijn 6, midden 8, onderrij 7, scheiding vuist|arm op x10
for X in range(11,18):
    for Y,k in ((31,6),(32,8),(33,7)):
        if zone[Y,X]==7 and not OUT[Y,X]: o[Y,X]=k
for Y in range(31,34):
    if zone[Y,10]==7 and not OUT[Y,10]: o[Y,10]=6
for X,Y in ((5,30),(4,31),(15,31)): o[Y,X]=6                      # outline highlight op de vuist weg (las als dambord)
if zone[32,8]==7: o[32,8]=8
# losse lijnstipjes (1 px, raken geen andere lijn/buitenrand) in broek/muts/lijf weg -> buurtint
for z,b in ((12,9),(1,2),(6,6)):
    for Y,X in zip(*np.where(binnen(z)&(o==b))):
        nb=[(Y+dy,X+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
        if not any(o[y,x] in (1,b) for y,x in nb if fg[y,x]):
            t=[o[y,x] for y,x in nb if zone[y,x]==z and o[y,x] not in (1,b)]
            if t: o[Y,X]=max(set(t),key=t.count)
# tintvlekjes < 3 px in de herkleurde onderdelen -> buurtint (glans 15 >= 3 px, anders 8)
for z in (6,12,1,2,3):
    for k in set(o[binnen(z)].ravel())-{1,2,6,9,15}:
        lab,n=nd.label((o==k)&binnen(z),structure=np.ones((3,3)))
        for i in range(1,n+1):
            mm=lab==i
            if mm.sum()>=3: continue
            r=nd.binary_dilation(mm,structure=np.ones((3,3)))&~mm&(zone==z)&~OUT; t=o[r]; t=t[(t!=k)&~np.isin(t,[1,2,6,9])]
            if len(t): o[mm]=np.bincount(t).argmax()
for Y,X in zip(*np.where((o==15)&(zone==6))):          # glanspixel zonder glansbuur -> 8
    if not ((o[Y-1:Y+2,X-1:X+2]==15).sum()-1): o[Y,X]=8
np.save('zone.npy',zone)
opslaan(o,'gnometrotter_rock.png')
for k,v in LOG.items(): print(k,len(v),v)
print('15 in lijf:',((o==15)&(zone==6)).sum())
