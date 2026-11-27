# Ronde 2: grijs.npy (vleugels/staart/dij/poten opnieuw uit het model) -> spikkels, lijf-kleurronde, geel, oog, buitenlijn, haren.
import numpy as np
from collections import Counter
from gemeen import *
k=np.load('kaal.npy'); s=np.load('grijs.npy'); zone=np.load('zone.npy'); mc=np.load('meanc.npy'); geel=np.load('geel.npy')
Hh,Ww=s.shape; Y,X=np.mgrid[0:Hh,0:Ww]; kop=(Y<=11)&(X<=16)
GR={5,8,9,10}; LIJF={2,3,4,6,7}
log={}
def zet(y,x,v,why):
    if s[y,x]!=v: s[y,x]=v; log.setdefault(why,[]).append((x,y))
inb=lambda y,x: 0<=y<Hh and 0<=x<Ww
# 1. spikkels: zwarte binnenpixel in de grijze zone met <=1 zwarte 8-buur en geen transparante buur -> grijze buurtint
s0=s.copy()
for y,x in zip(*np.nonzero(zone&(s0==1))):
    nb=s0[max(y-1,0):y+2,max(x-1,0):x+2]
    if (nb==0).any() or (y in (0,Hh-1)) or x in (0,Ww-1): continue
    if (nb==1).sum()-1<=1:
        g=[v for v in nb.flatten() if v in GR]
        if g: zet(y,x,Counter(g).most_common(1)[0][0],'spikkel')
# 2. lijf: 3 tinten (2 schaduw, 3 midden, 4 licht), licht linksboven; toon = modelhelderheid + afstand tot de rand linksboven/rechtsonder
body=np.isin(s,list(LIJF))&~kop
lum=mc.mean(2)
def rand(y,x,dy,dx,n):
    for i in range(1,n+1):
        yy,xx=y+dy*i,x+dx*i
        if not inb(yy,xx) or not body[yy,xx]: return i
    return n+1
for y,x in zip(*np.nonzero(body)):
    ul=min(rand(y,x,-1,0,3),rand(y,x,0,-1,3),rand(y,x,-1,-1,3))
    dr=min(rand(y,x,1,0,3),rand(y,x,0,1,3),rand(y,x,1,1,3))
    sc=(lum[y,x]-40)/10            # modelhelderheid (lijf ±37, lichter dons ±50-60)
    sc+= {1:1.6,2:0.8}.get(ul,0) - {1:1.2,2:0.4}.get(dr,0)
    v=4 if sc>=1.0 else 2 if sc<=-0.6 else 3
    zet(y,x,v,'lijf toon')
# 3. geel: plukjes waar het model geel heeft (>=2 gele natieve px = licht geel 7, aangrenzend 1 = 6), alleen in het dons
for y,x in zip(*np.nonzero(body)):
    if geel[y,x]>=2: zet(y,x,7,'geel')
for y,x in zip(*np.nonzero(body)):
    if geel[y,x]==1 and s[y,x] not in (7,) and any(inb(y+dy,x+dx) and geel[y+dy,x+dx]>=2 for dy in (-1,0,1) for dx in (-1,0,1)):
        zet(y,x,6,'geel')
# 4. oog (r1): grijze ring om een donkere kern
OOG=[[4,9,9,4],[9,1,1,9],[9,1,1,9],[4,9,9,4]]
for dy,r in enumerate(OOG):
    for dx,v in enumerate(r): zet(4+dy,8+dx,v,'oog')
# 5. ruis en buitenlijn kop/lijf (zoals r1; de grijze zone kreeg zijn lijn al in grijs.py)
for y in range(1,Hh-1):
    for x in range(1,Ww-1):
        v=s[y,x]; nb=[s[y-1,x],s[y+1,x],s[y,x-1],s[y,x+1]]
        if v>1 and len(set(nb))==1 and nb[0]>1 and nb[0]!=v and not (4<=y<=7 and 8<=x<=11) and v not in (6,7):
            zet(y,x,nb[0],'ruis')
t=lambda y,x: (not inb(y,x) or s[y,x]==0)
for y in range(Hh):
    for x in range(Ww):
        v=s[y,x]
        if v in (0,1) or zone[y,x] or (4<=y<=7 and 8<=x<=11): continue
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            if t(y+dy,x+dx) and not t(y-dy,x-dx) and not t(y-2*dy,x-2*dx) and s[y-dy,x-dx]!=1:
                zet(y,x,1,'buitenlijn'); break
# 6. gemeten modellijnen/tonen staart-dij (natief -> sprite x,y * 0,571):
#    staartonderrand natief (50-53, 51-52) '##' -> (28..30,29); donkere toonkolom natief x44 r45-50 ('o') -> (25,26..28)
for x,v in ((28,5),(29,1),(30,1)): zet(29,x,v,'staart/dij')
for y in (26,27,28): zet(y,25,5,'staart/dij')
# 7. tenen naar het model: rechtertoon linkervoet natief (32-36,63-64) grijs met lijn eronder; rechtervoet linkerteen
#    natief (35-46,67-68) doorlopend grijs tot in de poot, onderlijn eronder
for (x,y),v in {(19,36):8,(20,36):1,(21,38):8,(22,38):8,(23,38):8,(23,39):1}.items(): zet(y,x,v,'tenen')
# 8. Gen 3-belijning in de grijze delen (zwart-aandeel was 41 % tegen 10-18 % bij Taillow/Murkrow/Doduo):
#    binnenlijn tussen grijs en grijs -> donkerste grijs (5); buitenlijn aan de lichtkant (transparant boven/links, grijs binnen) -> 5
s0=s.copy()
for y in range(Hh):
    for x in range(Ww):
        if s0[y,x]!=1 or kop[y,x]: continue
        n4={(dy,dx):(s0[y+dy,x+dx] if inb(y+dy,x+dx) else 0) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))}
        vals=list(n4.values())
        if 0 not in vals:
            if sum(v in GR for v in vals)>=2 and not any(v in LIJF for v in vals): zet(y,x,5,'binnenlijn grijs')
        else:
            lichtkant=(n4[(-1,0)]==0 or n4[(0,-1)]==0) and n4[(1,0)]!=0 and n4[(0,1)]!=0
            if lichtkant and (n4[(1,0)] in (8,9,10) or n4[(0,1)] in (8,9,10)) and not any(v in LIJF for v in vals):
                zet(y,x,5,'selout lichtkant')
np.save('schoon.npy',s)
np.save('schoon.npy',s)
