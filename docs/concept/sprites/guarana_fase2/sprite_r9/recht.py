# recht.py SPRITE: rechte stukken buitenrand (>= 3 px op één rij/kolom met de achtergrond aan dezelfde kant) in de trossen
import sys; sys.path.insert(0,'sprite_r9'); import numpy as np; from PIL import Image; from hulp import *
o=np.array(Image.open(sys.argv[1])).astype(int)
BOX=[(4,20,22,42),(40,20,62,41),(16,8,38,30)]
def tros(x,y): return o[y,x] in (1,2,3,4,5,10,11) and any(a<=x<c and b<=y<d for a,b,c,d in BOX) and any(ok(y+dy,x+dx) and o[y+dy,x+dx] in (2,3,4,5,10,11) for dy,dx in N8)
def bgd(x,y,d): yy,xx=y+d[0],x+d[1]; return not ok(yy,xx) or o[yy,xx]==0
uit=[]
for d in ((0,-1),(0,1),(-1,0),(1,0)):
    ly,lx=(1,0) if d[0]==0 else (0,1)
    for y in range(64):
        for x in range(64):
            if not (tros(x,y) and bgd(x,y,d)): continue
            if ok(y-ly,x-lx) and tros(x-lx,y-ly) and bgd(x-lx,y-ly,d): continue
            run=[]; cy,cx=y,x
            while ok(cy,cx) and tros(cx,cy) and bgd(cx,cy,d): run.append((cx,cy)); cy,cx=cy+ly,cx+lx
            if len(run)>=3: uit.append(({(0,-1):'links',(0,1):'rechts',(-1,0):'boven',(1,0):'onder'}[d],run[0],run[-1],len(run)))
for u in uit: print(u)
