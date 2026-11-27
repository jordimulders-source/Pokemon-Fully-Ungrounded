# Ronde 3: keurderpunten 2-8 op schoon.npy (= r2 zonder haren), daarna nieuwe haren (punt 1).
# Coördinaten van de keurder zijn 64x64; sprite = (X-12, Y-20). Letters: K=1 d=2 D=3 m=4 M=5 g=8 G=9 l=10.
import numpy as np
from gemeen import *
s=np.load('schoon.npy'); r2=s.copy(); Hh,Ww=s.shape
K,d,D,m,M,g,G,l=1,2,3,4,5,8,9,10
cnt={}
def zet(X,Y,v,p,oud=None):
    x,y=X-12,Y-20
    if oud is not None: assert s[y,x] in (oud if isinstance(oud,tuple) else (oud,)),(p,X,Y,s[y,x])
    if s[y,x]!=v: s[y,x]=v; cnt[p]=cnt.get(p,0)+1
# 2. buikonderkant: onderste rij doorlopende 1-px lijn (staat er al), daarboven D/d; verre vleugel onderrand 1 px
for X in range(27,35): zet(X,43,D,'2 buik')            # rij 43 binnen
for X in (28,29,30,31,33,34): zet(X,44,d,'2 buik')      # rij 44 binnen ((27,44) en (32,44) grenzen aan transparant: lijn)
for X,Y in ((18,43),(19,43),(20,43),(21,43),(22,43),(18,44),(19,44),(20,44)): zet(X,Y,M,'2 verre vleugel')
# 3. zwarte binnenlijnen -> d
for X,Y in ((30,36),(30,37),(30,38),(36,36),(37,36),(38,36),(31,38),(33,38),(34,38),(23,38),(24,38),(25,38),(23,37),(24,37)):
    zet(X,Y,d,'3 binnenlijn',oud=K)
# 5. kop: stippen -> m
for X,Y in ((21,23),(18,24),(18,25)): zet(X,Y,m,'5 kop',oud=D)
# 6. snavel bovenrug -> G
for X in range(15,19): zet(X,27,G,'6 snavel',oud=g)
# 4. dij: lichtvlak l/G met M-sikkel rechts; staart: G met M-veerlijnen die uit de dij waaieren
#    (veerlijnen natief_bewerkt r47-52; op 4 spriterijen passen er twee met G ertussen: vanaf de M-sikkel van de dij omhoog naar (45,45) en omlaag naar (46,49))
GRY=(5,8,9,10)
for Y in range(46,53):
    xs=[X for X in range(35,40) if s[Y-20,X-12] in GRY]
    if not xs: continue
    for X in xs:
        v=M if X==max(xs) and len(xs)>=3 else (l if X-min(xs)<2 else G)
        zet(X,Y,v,'4 dij')
for Y in range(45,50):
    for X in range(40,48):
        if s[Y-20,X-12] in GRY+(4,): zet(X,Y,G,'4 staart')
def lijn(x0,y0,x1,y1):
    n=max(abs(x1-x0),abs(y1-y0)); return sorted({(round(x0+(x1-x0)*t/n),round(y0+(y1-y0)*t/n)) for t in range(n+1)})
for a in (lijn(40,46,45,45),lijn(40,48,46,49)):   # twee veerlijnen die vanaf de dij uitwaaieren (G ertussen)
    for X,Y in a:
        if s[Y-20,X-12] in GRY: zet(X,Y,M,'4 veerlijn')
# 7. verre voet: 1 px tussenruimte tussen teenpunt en klauw (natief x19-21 r67-68 transparant)
zet(23,58,0,'7 voet',oud=K)
# 8. lichte randpixels
zet(37,56,M,'8 rand',oud=G); zet(34,62,g,'8 rand',oud=l)
np.save('schoon3.npy',s)
for k_,v in cnt.items(): print(k_,v)
a=(s>0)!=(r2>0); print('alpha-diff t.o.v. r2 (zonder haren):',int(a.sum()))
# 1. haren: 2-px streepjes vast aan de buitenlijn (eerste pixel 4-buur van de lijn), los van elkaar
HAAR={'A':[[(8,26),(8,27)],[(10,25),(10,26)],[(7,29),(8,30)],
           [(31,16),(32,17)],[(31,19),(32,20)],[(32,22),(33,23)]],
      'B':[[(8,26),(8,27)],[(10,25),(10,26)],[(12,24),(13,25)],[(7,29),(8,30)],
           [(31,15),(32,16)],[(31,18),(32,19)],[(31,21),(32,21)],[(34,24),(35,23)]]}
for var,strokes in HAAR.items():
    v=s.copy(); allp=[p for st in strokes for p in st]
    for i,st in enumerate(strokes):
        x,y=st[0]; assert any(v[y+dy,x+dx]>0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))),('niet vast',var,st)
        for x,y in st: assert v[y,x]==0,(var,x,y)
        for j,o in enumerate(strokes):
            if j!=i: assert all(max(abs(a[0]-b[0]),abs(a[1]-b[1]))>1 for a in st for b in o),('raakt',var,st,o)
    for x,y in allp: v[y,x]=1
    # geen ingesloten gaatjes
    for y in range(1,Hh-1):
        for x in range(1,Ww-1):
            if v[y,x]==0 and not all(s[y+dy,x+dx]>0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))) and all(v[y+dy,x+dx]>0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): raise SystemExit(f'gat {var} {x},{y}')
    np.save(f'haar_{var}.npy',v); print('haren',var,len(strokes),'streepjes',len(allp),'px','zwart %',round((v==1).sum()/(v>0).sum()*100,1))
