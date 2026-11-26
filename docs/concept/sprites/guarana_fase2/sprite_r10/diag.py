# diag.py SPRITE: schuine rechte trappen (rand per rij springt steeds precies 1 px dezelfde kant op, >= 4 stappen) aan de buitenrand van de trossen
import sys; sys.path.insert(0,'sprite_r9'); import numpy as np; from PIL import Image
o=np.array(Image.open(sys.argv[1])).astype(int)
BOX=[('links',4,20,23,42),('rechts',40,20,62,41),('midden',16,8,38,30)]
for n,x0,y0,x1,y1 in BOX:
    for kant in ('L','R'):
        xs=[]
        for y in range(y0,y1):
            r=[x for x in range(x0,x1) if o[y,x] in (1,2,3,4,5,10,11) and ((x-1>=0 and o[y,x-1]==0) if kant=='L' else (x+1<64 and o[y,x+1]==0))]
            xs.append((y,(min(r) if kant=='L' else max(r)) if r else None))
        run=[]
        for (ya,a),(yb,b) in zip(xs,xs[1:]):
            if a is not None and b is not None and abs(b-a)==1 and (not run or b-a==run[-1][1]): run.append((yb,b-a))
            else:
                if len(run)>=4: print(n,kant,'trap tot rij',run[-1][0],len(run),'stappen')
                run=[(yb,b-a)] if a is not None and b is not None and abs(b-a)==1 else []
        if len(run)>=4: print(n,kant,'trap tot rij',run[-1][0],len(run))
