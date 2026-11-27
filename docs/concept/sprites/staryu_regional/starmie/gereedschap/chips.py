# chips.py: kiest plekken voor chocoladechips (2 px) op elke achterste punt; schrijft sprite_r1/chips.json.
# Alleen plaatsing (geen vorm): op vulpixels (koek S/O/M/L) waarvan de 4 buren ook vulling zijn, zo ver
# mogelijk uit elkaar (eerste chip het dichtst bij het zwaartepunt van de punt). Model r3/r4: chips op alle punten.
import sys, json; sys.path.insert(0,'gereedschap'); from gemeen import *
from kaal import voorste
o=np.asarray(Image.open(sys.argv[1])).astype(int); FILL=(3,4,5,6); _,fm=voorste()
def binnen(x,y): return all(o[y+dy,x+dx] in FILL and not fm[y+dy,x+dx] for dy,dx in ((0,0),(-1,0),(1,0),(0,-1),(0,1)))
out=[]
for n in SETB:
    pts=[(x,y) for y,x in zip(*np.where(o>0)) if punt_van(x,y)==n and o[y,x] in FILL and not fm[y,x]]
    cx=np.mean([p[0] for p in pts]); cy=np.mean([p[1] for p in pts])
    kand=[]
    for x,y in pts:
        if not binnen(x,y): continue
        if binnen(x+1,y): kand.append((x,y,1,0))
        elif binnen(x,y+1): kand.append((x,y,0,1))
    nchip=3 if len(kand)>=20 else 2
    gek=[]
    if kand:
        gek.append(min(kand,key=lambda c:(c[0]+c[2]/2-cx)**2+(c[1]+c[3]/2-cy)**2))
        while len(gek)<nchip:
            ok=[c for c in kand if all(max(abs(c[0]-g[0]),abs(c[1]-g[1]))>=3 for g in gek)]
            if not ok: break
            gek.append(max(ok,key=lambda c:min(max(abs(c[0]-g[0]),abs(c[1]-g[1])) for g in gek)))
    print(n,len(pts),'kandidaten',len(kand),'chips',gek); out+= [list(map(int,c)) for c in gek]
json.dump(out,open('sprite_r1/chips.json','w'))
