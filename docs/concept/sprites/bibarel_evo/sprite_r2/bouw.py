# bouw.py ronde 2: r1 (sprite_r1/sprite.png) -> sprite_r2/sprite.png. Alleen: kraag (Bibarel), tuinbroek (tinten naar model),
# bruine vacht/romp (donkere vlekken terug naar modeltint), neus. Daarbuiten pixeldiff 0 (bewezen onderaan).
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); sys.path.insert(0,'sprite_r2'); from gemeen import *
from scipy import ndimage
from kraag import kraag, ZONE as KRAAG
r1=laad('sprite_r1/sprite.png'); vs=np.load('sprite_r1/voor_selout.npy')
T=np.load('sprite_r1/toon.npy'); F=np.load('sprite_r1/lijnfrac.npy')
o=r1.copy(); log=[]
fg=r1>0; P=np.pad(fg,1); rand=fg&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
GEZ=np.zeros((64,64),bool); GEZ[14:28,20:35]=True
def zet(x,y,v,z):
    if o[y,x]!=v: o[y,x]=v; log.append((x,y,z))
# ---- 1. kraag: Bibarel-wangen/kinvacht (kraag.py)
kl=[]; o=kraag(o,kl); log+=kl
# ---- 2. tuinbroek: zone = r1-broek + taille als ronde boog (U, evenwijdig aan de U-onderkant van het borststuk uit het model)
def taille(x): return 42-int(round(0.021*(x-28)**2))
BROEK=np.zeros((64,64),bool)
for y in range(36,64):
    for x in range(64):
        if not fg[y,x]: continue
        if (y<42 and x>=38) or (y==42 and x>=43): continue   # onderarm/hand
        if 43<=y<47 and 43<=x<49: continue          # hand + pols
        if x<=22 or 33<=x<=37: ok=y>=taille(x)
        else: ok=y>=42
        if ok and (vs[y,x] in (2,3,4,5) or r1[y,x] in (6,7,15)) and not (r1[y,x]==7 and y<42): BROEK[y,x]=True
BROEK&=~rand                                         # buitenlijn/selout blijft van r1
for y,x in zip(*np.where(BROEK)):
    if vs[y,x]==2 and F[y,x]>=0.4: v=15              # binnenlijn alleen waar het model een lijn heeft
    elif T[y,x]>=150: v=7
    elif T[y,x]>=120: v=6
    else: v=15
    zet(x,y,v,'tuinbroek')
# ---- 3. bruine vacht (romp/armen/schouders/benen-boven): donkere vlekken zonder modellijn -> modeltint; lijnstukjes <3 px weg
VACHT=np.isin(o,(1,2,3,4,5))&fg&~rand&~GEZ&~KRAAG&~BROEK; VACHT[:15,:]=False
def tint(y,x): return 5 if T[y,x]>=150 else (4 if T[y,x]>=120 else 3)
P2=np.pad(o,1)
for y,x in zip(*np.where(VACHT)):
    v=o[y,x]
    if v==1 and any(P2[y+1+dy,x+1+dx] in (8,9,10) for dy in (-1,0,1) for dx in (-1,0,1)): continue  # rand van hand/stam
    if v in (1,2):
        zet(x,y,2 if F[y,x]>=0.4 else tint(y,x),'vacht lijn')
    elif v==3 and tint(y,x)>3 and F[y,x]<0.25:
        zet(x,y,tint(y,x),'vacht donkere vlek')
lab,n=ndimage.label(o==2,structure=np.ones((3,3)))
for i in range(1,n+1):
    pts=np.argwhere(lab==i)
    if len(pts)<3 and all(VACHT[y,x] for y,x in pts):
        for y,x in pts: zet(x,y,tint(y,x),'vacht lijnfragment')
# ---- 4. neus: rood (oranje-donker = modelneus d04b31), driehoek 3+1 px op de modelplek
for x,y in ((23,19),(24,19),(25,19),(24,20)): zet(x,y,12,'neus')
# ---- 5. losse zwarte pixels (geen zwart/achtergrond in de 8 buren) binnen de zones -> donkere eigen tint
NEUS0=np.zeros((64,64),bool); NEUS0[19:21,23:26]=True
Z0=KRAAG|BROEK|VACHT
P3=np.pad(o,1)
for y,x in zip(*np.where((o==1)&Z0)):
    nb=[P3[y+1+dy,x+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
    if any(v in (0,1) for v in nb): continue
    zet(x,y,15 if sum(v in (6,7,15) for v in nb)>sum(v in (2,3,4,5) for v in nb) else 2,'losse zwarte pixel')
opslaan(o,'sprite_r2/sprite.png',8)
# ---- bewijs: diff buiten de zones
NEUS=np.zeros((64,64),bool); NEUS[19:21,23:26]=True
ROMP=VACHT|np.isin(r1,(1,2,3,4,5))&~rand&~GEZ&~KRAAG&~BROEK  # vachtzone zoals hierboven gedefinieerd
ROMP[:15,:]=False
toegestaan=KRAAG|BROEK|ROMP|NEUS
d=r1!=o
print('gewijzigd t.o.v. r1:',d.sum(),'| buiten de zones:',(d&~toegestaan).sum())
import collections; print(collections.Counter(z for _,_,z in log))
for naam,m in (('kraag',KRAAG),('tuinbroek',BROEK),('vacht/romp',ROMP&~KRAAG&~BROEK),('neus',NEUS)): print('  %-11s %d px'%(naam,(d&m).sum()))
np.save('sprite_r2/zones.npy',np.stack([KRAAG,BROEK,ROMP,NEUS]))
