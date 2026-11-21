# r2 opbouwen: lijf/kop/oog/snavel/poten (P) = r1 pixel voor pixel; daaromheen de overgetrokken veren (veren.py) gerasterd
# (4x4 deelpunten, >= 50% dekking), per veer 2 tinten gesplitst langs de veeras (lichtkant linksboven), 1 px donkergroene lijn
# op de achterste veer waar twee veren elkaar raken, zwarte buitenrand met gekleurde selout aan de lichtkant.
# Gebruik: python3 bouw.py [A|B|0]  (A/B = keuze gele veren)
import sys, json, numpy as np
from collections import Counter
from palet import I
from veren import VEREN
GEEL=sys.argv[1] if len(sys.argv)>1 else 'A'
GEELSET={'A':{'FL2','FRF3'},'B':{'FT0','FT2','FRF2'},'0':set()}[GEEL]
r1=np.load('r1_kls.npy'); H,W=r1.shape
LINE={I['O'],I['L']}; PINK={I['K0'],I['K1'],I['K2'],I['K3']}
P=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if r1[y,x] and (y>=47 or (19<=x<=34 and y>=22) or (35<=x<=40 and y>=36) or r1[y,x] in PINK): P[y,x]=True
def inpoly(px,py,pts):
    c=False; n=len(pts)
    for i in range(n):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%n]
        if (y1>py)!=(y2>py) and px<(x2-x1)*(py-y1)/(y2-y1)+x1: c=not c
    return c
SUB=[(i+0.5)/4 for i in range(4)]
cov=np.zeros((len(VEREN),H,W))
for k,(nm,soort,pts) in enumerate(VEREN):
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    for y in range(int(min(ys)),int(max(ys))+1):
        for x in range(int(min(xs)),int(max(xs))+1):
            cov[k,y,x]=sum(inpoly(x+a,y+b,pts) for a in SUB for b in SUB)/16
own=-np.ones((H,W),int)
for y in range(H):
    for x in range(W):
        if P[y,x]: continue
        tot=min(1,cov[:,y,x].sum())
        if tot<0.5: continue
        front=[k for k in range(len(VEREN)) if cov[k,y,x]>=0.5]
        own[y,x]=front[-1] if front else int(cov[:,y,x].argmax())
# tinten: lichtkant van de veeras (top -> zwaartepunt) = lichte tint
S=np.load('model64.npy'); MY=(S[...,0]>150)&(S[...,0]-S[...,2]>60); ML=S@[.299,.587,.114]
out=np.where(P,r1,0)
for k,(nm,soort,pts) in enumerate(VEREN):
    tx,ty=pts[0]; cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
    ax,ay=cx-tx,cy-ty; nx,ny=-ay,ax          # normaal op de as
    if nx*(-1)+ny*(-1)<0: nx,ny=-nx,-ny      # normaal wijst naar linksboven = lichtkant
    if soort=='W': lt,dk=I['G1'],I['G2']
    elif soort=='C': lt,dk=I['G1'],I['G2']
    elif nm in GEELSET: lt,dk=I['Y1'],I['Y2']
    else: lt,dk=I['G4'],I['G5']
    for y,x in zip(*np.where(own==k)):
        s=(x+0.5-tx)*nx+(y+0.5-ty)*ny
        out[y,x]=lt if s>0 else dk
        if soort=='C':   # kuif: tinten en gele bogen uit het model
            out[y,x]=I['Y1'] if MY[y,x] else (I['G1'] if ML[y,x]>=150 else I['G2'])
# lijnen tussen veren: pixel van de achterste veer naast een voorste veer -> L
lijn=[]
for y in range(H):
    for x in range(W):
        k=own[y,x]
        if k<0: continue
        for a,b in((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
            if 0<=a<H and 0<=b<W and own[a,b]>k: lijn.append((y,x)); break
for y,x in lijn: out[y,x]=I['L']
# kuifbogen: de gele bogen over de twee kuifveren, overgetrokken van het model (g2-vel); 1 px, Y1
BOGEN=[[(24.6,19.8),(25.0,17.6),(25.8,16.2),(27.0,15.4),(28.4,15.6),(29.2,16.6)],[(30.0,19.2),(30.8,18.2),(32.0,17.9),(33.2,18.4),(33.8,19.4)]]
kuif=[k for k,v in enumerate(VEREN) if v[1]=='C'][0]
for y,x in zip(*np.where(own==kuif)):
    if out[y,x]==I['Y1']: out[y,x]=I['G1'] if ML[y,x]>=150 else I['G2']   # losse modelgeel-stipjes eruit, de bogen komen ervoor in de plaats
nb=0
for boog in BOGEN:
    for (x1,y1),(x2,y2) in zip(boog,boog[1:]):
        for t in np.linspace(0,1,12):
            x=int(x1+(x2-x1)*t); y=int(y1+(y2-y1)*t)
            if own[y,x]==kuif and out[y,x]!=I['Y1']: out[y,x]=I['Y1']; nb+=1
# binnenlijnen dunner: een lijnpixel die alleen een hoekje maakt tussen twee loodrechte lijnburen (trapje van 2 px) -> tint van zijn veer
def isl(a,b): return 0<=a<H and 0<=b<W and out[a,b]==I['L'] and own[a,b]>=0
nh=0
for y,x in lijn:
    N,S_,Wn,E=isl(y-1,x),isl(y+1,x),isl(y,x-1),isl(y,x+1)
    if sum((N,S_,Wn,E))==2 and ((N and E) or (N and Wn) or (S_ and E) or (S_ and Wn)) and not (N and S_) and not (Wn and E):
        # alleen als de diagonaal de lijn heel houdt
        dy=-1 if N else 1; dx=1 if E else -1
        if not isl(y+dy,x+dx):
            k=own[y,x]; c=Counter(out[a,b] for a,b in((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if 0<=a<H and 0<=b<W and own[a,b]==k and out[a,b]!=I['L'])
            if c: out[y,x]=c.most_common(1)[0][0]; nh+=1
# buitenrand
def op(a,b): return 0<=a<H and 0<=b<W and out[a,b]>0
rand=[(y,x) for y in range(H) for x in range(W) if own[y,x]>=0 and any(not op(a,b) for a,b in((y-1,x),(y+1,x),(y,x-1),(y,x+1)))]
for y,x in rand: out[y,x]=I['O']
sel=0
for y,x in rand:
    up=not op(y-1,x); lf=not op(y,x-1); dn=not op(y+1,x); rt=not op(y,x+1)
    if (up or lf) and not (dn or rt):
        inn=[out[a,b] for a,b in((y+1,x),(y,x+1)) if op(a,b) and out[a,b] not in LINE]
        out[y,x]=I['Y2'] if inn and inn[0] in (I['Y1'],I['Y2']) else I['L']; sel+=1
np.save('r2_%s_kls.npy'%GEEL,out); np.save('own.npy',own)
log={'kuifboog_px':nb,'lijnhoekjes':nh,'geel':GEEL,'veren':len(VEREN),'binnenlijnen':len(lijn),'buitenrand':len(rand),'selout':sel,'diff_in_P':int(((out!=r1)&P).sum()),
     'kleuren':len(set(out.ravel()))-1}
print(json.dumps(log))
