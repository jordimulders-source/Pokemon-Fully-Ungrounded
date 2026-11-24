# bouw.py ronde 7 (vanaf r6): 1) bandjes zoals Gemini r5: 3 px (licht 7,7 + tan rand 6 aan de schaduwkant) vanaf de bovenhoeken van het
# borststuk omhoog over de schouders tot achter de kraag (kraagzone wijkt alleen onder het bandje); 2) volume in het crème zoals r5:
# licht linksboven, middentint als brede sikkel rechts en langs de onderrand/heupen, donker alleen in de diepste hoeken.
# Schaduw uit de vorm van het crème zelf (hoogteveld uit de afstand tot de rand, licht van linksboven); geen kleurmiddeling.
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from scipy import ndimage
r6=laad('sprite_r6/sprite.png'); r5=laad('sprite_r5/sprite.png')
o=r6.copy(); zone={}
fg=r6>0; P=np.pad(fg,1); RAND=fg&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
C,S,D=7,6,15
def z(n,x,y,v):
    assert fg[y,x] and not RAND[y,x],(n,x,y)
    o[y,x]=v; zone[(x,y)]=n
# ---- 1. bandjes ----
RB={33:(35,36,37),32:(36,37,38),31:(36,37,38),30:(37,38,39),29:(38,39,40),28:(39,40,41),27:(39,40,41)}
LB={33:(21,22,23),32:(21,22,23),31:(22,23,24),30:(22,23,24),29:(22,23,24)}
NIEUW=set()
for B in (RB,LB):
    for y,(a,b,c) in B.items():
        for x,v in ((a,C),(b,C),(c,S)): z('bandjes',x,y,v); NIEUW.add((x,y))
# oude bandjespixels die nu buiten het bandje vallen -> vacht van r5 (schouder)
for y in range(27,34):
    for x in list(range(19,26))+list(range(33,44)):
        if (x,y) not in NIEUW and r6[y,x] in (C,S) and r5[y,x] not in (C,S,D): z('bandjes oud',x,y,r5[y,x])
        elif (x,y) not in NIEUW and r6[y,x] in (C,S): z('bandjes oud',x,y,4)
# ---- 2. volume in het crème ----
CRA=np.isin(r6,(C,S,D))&fg; CRA[:34]=False; CRA[:,:19]=False
lab,n=ndimage.label(CRA); CRA=lab==(np.argmax(ndimage.sum(CRA,lab,range(1,n+1)))+1)
ZAK=np.zeros((64,64),bool); ZAK[37:45,22:34]=True           # naad r37 + zak r38-44 (r6) blijven zoals ze zijn
REGIO=CRA&~ZAK&~RAND
d=ndimage.distance_transform_edt(np.pad(CRA,1))[1:-1,1:-1]
h=np.sqrt(np.minimum(d,6.0)); h=ndimage.gaussian_filter(h,0.8)
gy,gx=np.gradient(h); nrm=np.dstack([-gx,-gy,np.full_like(h,0.55)]); nrm/=np.linalg.norm(nrm,axis=2,keepdims=True)
L=np.array([-1.0,-1.1,0.9]); L/=np.linalg.norm(L)
sh=nrm@L
v=sh[REGIO]; q_mid=np.quantile(v,0.50); q_dk=np.quantile(v,0.08)
for y,x in zip(*np.where(REGIO)):
    t=C if sh[y,x]>=q_mid else (D if (sh[y,x]<q_dk and d[y,x]<=1.5) else S)
    z('crème volume',x,y,t)
# donker (F) alleen in de diepste hoek: aan de rand, rechtsonder; elders middentint
for y,x in zip(*np.where(REGIO&(o==D))):
    rand=any(not CRA[y+dy,x+dx] for dy,dx in ((1,0),(0,1),(1,1)))
    if not (rand and x>=28 and y>=45): z('crème volume',x,y,S)
# sikkel langs de rechterrand van borststuk/buik (schaduwkant): binnen 2 px van de rechterrand -> middentint
for y in range(34,46):
    xs=[x for x in range(19,45) if CRA[y,x]]
    if not xs: continue
    xr=max(xs); w=1 if y<38 else 2
    for x in range(xr-w+1,xr+1):
        if REGIO[y,x] and o[y,x]==C: z('crème volume',x,y,S)
# vlakjes <3 px -> buurtint (geen middeling)
for k in (C,S,D):
    lab,nn=ndimage.label((o==k)&REGIO)
    for i in range(1,nn+1):
        pts=np.argwhere(lab==i)
        if len(pts)>=3: continue
        nb={}
        for yy,xx in pts:
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                Y,X=yy+dy,xx+dx
                if REGIO[Y,X] and lab[Y,X]!=i: nb[o[Y,X]]=nb.get(o[Y,X],0)+1
        if nb:
            qq=max(nb,key=nb.get)
            for yy,xx in pts: z('crème volume',xx,yy,qq)
opslaan(o,'sprite_r7/sprite.png',8)
import collections
KR=np.zeros((64,64),bool); KR[15:28,35:42]=True; KR[15:28,18:21]=True; KR[27:31,19:39]=True
dd=o!=r6; print('gewijzigd t.o.v. r6:',dd.sum(),'| buiten zones:',sum(1 for y,x in zip(*np.where(dd)) if (x,y) not in zone),'| kraagzone:',[(int(x),int(y)) for y,x in np.argwhere(dd&KR)])
print(dict(collections.Counter(zone[(x,y)].split(' ')[0] for y,x in zip(*np.where(dd)))))
print('crème tinten in regio:',{k:int(((o==k)&REGIO).sum()) for k in (C,S,D)},'| silhouet gelijk:',((o>0)==(r6>0)).all())
