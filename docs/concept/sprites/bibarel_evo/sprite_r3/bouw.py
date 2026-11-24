# bouw.py ronde 3: start r1 (sprite_r1/sprite.png). Zones: neus (r2), broek (crème als r1, 3 tinten relatief naar modelhelderheid),
# bovenlichaam (alleen donkere vlekjes zonder model weg). Kraag = r1. Daarbuiten pixeldiff 0 (bewezen onderaan).
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from scipy import ndimage
r1=laad('sprite_r1/sprite.png'); vs=np.load('sprite_r1/voor_selout.npy')
T=np.load('sprite_r1/toon.npy'); F=np.load('sprite_r1/lijnfrac.npy')
AANDEEL=[float(a) for a in (sys.argv[1:4] if len(sys.argv)>3 else (0.50,0.33,0.17))]   # licht/midden/donker
naam=sys.argv[4] if len(sys.argv)>4 else 'sprite'
o=r1.copy(); log=[]
fg=r1>0; P=np.pad(fg,1); rand=fg&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
GEZ=np.zeros((64,64),bool); GEZ[14:28,20:35]=True
KRAAG=np.zeros((64,64),bool); KRAAG[15:28,35:42]=True; KRAAG[15:28,18:21]=True; KRAAG[27:31,19:39]=True; KRAAG&=~GEZ
def zet(x,y,v,z):
    if o[y,x]!=v: o[y,x]=v; log.append((x,y,z))
# 1. neus (r2): rood driehoekje op de modelplek
NEUS=np.zeros((64,64),bool)
for x,y in ((23,19),(24,19),(25,19),(24,20)): zet(x,y,12,'neus'); NEUS[y,x]=True
# 2. broek: r1-broek + taille als boog (zoals r2); tinten relatief: rangorde van de modelhelderheid binnen de broek
def taille(x): return 42-int(round(0.021*(x-28)**2))
BROEK=np.zeros((64,64),bool)
for y in range(36,64):
    for x in range(64):
        if not fg[y,x]: continue
        if (y<42 and x>=38) or (y==42 and x>=43) or (43<=y<47 and 43<=x<49): continue
        ok=y>=taille(x) if (x<=22 or 33<=x<=37) else y>=42
        if ok and (vs[y,x] in (2,3,4,5) or r1[y,x] in (6,7,15)) and not (r1[y,x]==7 and y<42): BROEK[y,x]=True
BROEK&=~rand
lijn=BROEK&(vs==2)&(F>=0.4)                          # crème-donker als binnenlijn alleen waar het model een lijn heeft
vlak=BROEK&~lijn
t=T[vlak]; q_l=np.quantile(t,1-AANDEEL[0]); q_d=np.quantile(t,AANDEEL[2])
for y,x in zip(*np.where(vlak)):
    zet(x,y,7 if T[y,x]>=q_l else (6 if T[y,x]>=q_d else 15),'broek')
for y,x in zip(*np.where(lijn)): zet(x,y,15,'broek lijn')
# tintvlekjes <3 px in de broek -> meest voorkomende crème-buurtint (geen vlakken middelen, alleen 1-2 px losse pixels)
for k in (7,6,15):
    lab,n=ndimage.label((o==k)&vlak)
    for i in range(1,n+1):
        pts=np.argwhere(lab==i)
        if len(pts)>=3: continue
        nb={}
        for yy,xx in pts:
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                Y,X=yy+dy,xx+dx
                if BROEK[Y,X] and lab[Y,X]!=i and o[Y,X] in (6,7,15): nb[o[Y,X]]=nb.get(o[Y,X],0)+1
        if nb:
            q=max(nb,key=nb.get)
            for yy,xx in pts: zet(xx,yy,q,'broek vlekje')
# 3. bovenlichaam: alleen donkere vlekjes (zwart/lijn, clusters <3 px) waar het model GEEN lijn heeft -> modeltint; rest r1-patroon
VACHT=np.isin(r1,(1,2))&fg&~rand&~GEZ&~KRAAG&~BROEK; VACHT[:15,:]=False
lab,n=ndimage.label(np.isin(o,(1,2))&~rand,structure=np.ones((3,3)))
for i in range(1,n+1):
    pts=np.argwhere(lab==i)
    if len(pts)>=3 or not all(VACHT[y,x] for y,x in pts): continue
    if any(F[y,x]>=0.2 for y,x in pts): continue        # model heeft daar (iets van) een lijn: laten staan
    P2=np.pad(o,1)
    if any(P2[y+1+dy,x+1+dx] in (8,9,10) for y,x in pts for dy in (-1,0,1) for dx in (-1,0,1)): continue
    for y,x in pts: zet(x,y,5 if T[y,x]>=150 else (4 if T[y,x]>=120 else 3),'vacht vlekje zonder model')
opslaan(o,f'sprite_r3/{naam}.png',8)
d=r1!=o; toeg=NEUS|BROEK|VACHT
print(naam,'aandeel',AANDEEL,'| gewijzigd t.o.v. r1:',d.sum(),'| buiten de zones:',(d&~toeg).sum())
for nm,m in (('neus',NEUS),('broek',BROEK),('bovenlichaam',VACHT),('kraag',KRAAG)): print('  %-13s %d px'%(nm,(d&m).sum()))
import collections; print('  broek tinten',collections.Counter(o[BROEK].tolist()))
