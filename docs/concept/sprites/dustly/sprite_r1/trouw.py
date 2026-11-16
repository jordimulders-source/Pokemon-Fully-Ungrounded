# Trouwe sprite: auto-reductie + technische opschoning + gezicht per pixel naar het model.
import sys; sys.path.insert(0,'sprite_r1'); sys.path.insert(0,'basis'); import numpy as np; from lab import label
o=np.load('sprite_r1/auto_idx.npy').copy(); auto=o.copy(); log={}
def put(zone,pts,v):
    for x,y in pts:
        if o[y,x]!=v: o[y,x]=v; log[zone]=log.get(zone,0)+1
fig=o>0
# 1. gezicht (zone 'gezicht'): ogen/mond/tanden naar natieve modelpixels (zie mapping in rapport)
F={}
for x in range(11,27):
    for y in range(26,37): F[(x,y)]=o[y,x]
face=dict(F)
# rechteroog: pupil 2 hoog links in het wit, lijn rond (model: K rondom, rechts K)
for p,v in {(21,30):1,(21,31):9,(20,30):9,(20,31):1,(26,30):1,(26,27):1,(20,32):1,(21,32):9,(22,32):9,(23,32):1,(24,32):3,(16,30):1}.items(): face[p]=v
# mond: rij 34 x12-16, dip rij 35 x17-19, rij 34 x20-23, mondhoek rechts (24,33); tanden (15,35) en (22,35)
for x in range(11,27):
    for y in (33,34,35,36):
        if face[(x,y)] in (1,2,9): face[(x,y)]=3
for x in list(range(12,17))+list(range(20,24)): face[(x,34)]=1
for x in (17,18,19): face[(x,35)]=1
face[(24,33)]=1; face[(11,35)]=1; face[(21,33)]=1; face[(22,33)]=1
face[(15,35)]=9; face[(22,35)]=9; face[(21,35)]=1; face[(23,35)]=1; face[(22,36)]=1
for (x,y),v in face.items():
    if fig[y,x]: put('gezicht',[(x,y)],v)
# 2. lichtrand (zone 'rand'): roze selout op de buitenrand linksboven, perzik er direct binnen waar het model perzik heeft
def edge(m):
    e=np.zeros_like(m)
    for y in range(64):
        for x in range(64):
            if m[y,x] and any(not(0<=y+dy<64 and 0<=x+dx<64) or not m[y+dy,x+dx] for dy,dx in ((0,1),(1,0),(0,-1),(-1,0))): e[y,x]=True
    return e
E=edge(fig)
from PIL import Image; from bgmask import bgmask
_a=np.asarray(Image.open('basis/natief.png').convert('RGB')).astype(float); _l=_a@[.299,.587,.114]
RIMI=((_a[...,0]-_a[...,1])>=25)&(_l>=150)&~bgmask()
rimzone=lambda x,y: (y<=24 and x<=30) or (x<=11 and y<=33) or (y<=12 and x<=34)
# 3. ruis: tintvlakjes < 3 px (3/4/5) nemen de meest voorkomende buurtint aan (behalve rand/gezicht)
def clean(skip=None):
    for t in (3,4,5,6):
        lab,n=label(o==t,4)
        for i in range(1,n+1):
            ys,xs=np.where(lab==i)
            if len(ys)>=3: continue
            for y,x in zip(ys,xs):
                if 26<=y<=36 and 11<=x<=26: continue
                if skip is not None and skip[y,x]: continue
                nb=[o[y+dy,x+dx] for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)) if 0<=y+dy<64 and 0<=x+dx<64 and o[y+dy,x+dx] in (3,4,5,6)]
                if nb: put('ruis',[(x,y)],max(set(nb),key=nb.count))
clean(); clean()
# bultlijnen uit het model (dunne donkere bogen, ribbels.py) -> één tint donkerder dan het vlak, alleen ketens
from ribbels import ridges
rg,_=ridges(); BL=np.zeros((64,64),bool)
for ny,nx in zip(*np.where(rg)):
    sx=9+int((nx-17+0.5)/1.5); sy=8+int((ny-18+0.5)/1.5)
    if 0<=sx<64 and 0<=sy<64 and fig[sy,sx] and not E[sy,sx] and not (25<=sy<=37 and 10<=sx<=27) and o[sy,sx] in (3,4,5,6): BL[sy,sx]=True
for y,x in zip(*np.where(BL)):
    if sum(BL[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1))>=2:
        put('bultlijnen',[(x,y)],{3:2,4:3,5:4,6:5}[o[y,x]])
# losse lijnpixels (2) zonder lijnburen in het lijf -> vlaktint
for y,x in zip(*np.where(o==2)):
    if E[y,x] or BL[y,x] or (26<=y<=36 and 11<=x<=26): continue
    if not any(o[y+dy,x+dx] in (1,2) for dy in (-1,0,1) for dx in (-1,0,1) if (dy,dx)!=(0,0)):
        nb=[o[y+dy,x+dx] for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)) if o[y+dy,x+dx] in (3,4,5,6)]
        if nb: put('ruis',[(x,y)],max(set(nb),key=nb.count))
# 4. buitenlijn 1 px binnen het silhouet: lichtkant roze (7), schaduwkant links/onder donker (1), rechts/slierten (2)
labf,nf=label(fig,4); size={i:(labf==i).sum() for i in range(1,nf+1)}
main=max(size,key=size.get)
for y,x in zip(*np.where(E)):
    if (26<=y<=36 and 11<=x<=26) and o[y,x] in (9,): continue
    # dunne slierten (geen binnenpixel ernaast) en losse wolkjes houden hun vulling, zoals de gaswolk van Gastly
    if labf[y,x]!=main: continue
    if y>=41 and x>=26 and auto[y,x] in (4,5,6): continue
    if not any(fig[y+dy,x+dx] and not E[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1)): continue
    # gekleurde selout: lijnkleur volgt de modeltint van de rand (donker vlak -> donkerste lijn, licht gas -> donkere gastint)
    if rimzone(x,y): v=7
    else: v={1:1,2:1,3:1,4:2,5:3,6:3}.get(auto[y,x],1)
    put('buitenlijn',[(x,y)],v)
# perzik binnen de roze rand waar het model hem heeft (auto 8 of 7 binnenin) -> 8
for y in range(64):
    for x in range(64):
        if fig[y,x] and not E[y,x] and rimzone(x,y) and o[y,x]!=7 and any(E[y+dy,x+dx] and o[y+dy,x+dx]==7 for dy in (-1,0,1) for dx in (-1,0,1)):
            by,bx=int(18+(y-8)*1.5),int(17+(x-9)*1.5)
            if RIMI[by:by+3,bx:bx+3].any() or auto[y,x] in (7,8): put('rand',[(x,y)],8)
clean(BL|E); clean(BL|E)
# perzik-lichtrand: elke natieve perzikpixel naar zijn spritepixel; valt hij op de roze buitenlijn, dan één stap naar binnen (rechtsonder)
for ny,nx in zip(*np.where(RIMI)):
    sx=9+int((nx-17+0.5)/1.5); sy=8+int((ny-18+0.5)/1.5)
    for cx,cy in ((sx,sy),(sx+1,sy+1),(sx+1,sy),(sx,sy+1)):
        if fig[cy,cx] and not E[cy,cx] and o[cy,cx] not in (7,9,1):
            put('rand',[(cx,cy)],8); break
np.save('sprite_r1/trouw_idx.npy',o)
d=(o!=auto)&fig; print('afwijkend van auto:',d.sum(),log,'px',(o>0).sum(),{i:int((o==i).sum()) for i in range(1,11)})
