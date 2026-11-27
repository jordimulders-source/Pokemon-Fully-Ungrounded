# strepen.py SPRITE: horizontale rijen >= 3 px donker (zwart, lijnrood, diep rood, groene lijn) die (deels) binnen het silhouet liggen en
# over een vrucht/oog lopen; per streep welke onderdelen (vrucht-eigenaar, oog, groen) en hoeveel pixels op de buitenrand
import sys; sys.path.insert(0,'sprite_r6'); import numpy as np; from PIL import Image; from hulp import *
o=np.array(Image.open(sys.argv[1])).astype(int); own=np.load('sprite_r6/own.npy'); fg=o>0
RAND=np.array([[fg[y,x] and any(not ok(y+dy,x+dx) or not fg[y+dy,x+dx] for dy,dx in N4) for x in range(64)] for y in range(64)])
D={1,2,14,6}; uit=[]
for y in range(64):
    x=0
    while x<64:
        if o[y,x] in D:
            x0=x
            while x<64 and o[y,x] in D: x+=1
            seg=range(x0,x)
            rood=any(o[y,i] in (1,2,14) and not RAND[y,i] for i in seg)
            if x-x0>=3 and rood and sum(not RAND[y,i] for i in seg)>=3:
                uit.append((y,x0,x-1,''.join({1:'K',2:'L',14:'$',6:'l'}[o[y,i]] for i in seg),sum(RAND[y,i] for i in seg)))
        else: x+=1
for u in uit: print('rij %d x%d-%d %s (buitenrand %d)'%u)
print(len(uit),'strepen')
