# Stap 4: technisch opschonen van de kale reductie (basis_<VAR>.npy). Telt elke gewijzigde pixel per zone.
import sys; from PIL import Image; import numpy as np
VAR=sys.argv[1]; o=np.load(f'basis_{VAR}.npy'); b=o.copy()
log={}
def mark(why,y,x,v):
    if o[y,x]!=v: o[y,x]=v; log[why]=log.get(why,0)+1
# 1. groen terug naar 3 tinten + donkere selout: #3f6036 (6) -> #467e4b (5) (beide modelkleuren, bijna gelijk)
for y,x in zip(*np.where(o==6)): mark('6->5 tintreductie',y,x,5)
# 2. losse 1-px-tintvlekjes binnen een vlak (niet omlijning/neon): alle 4 buren delen 1 andere kleur van dezelfde groep
GROUP={1:'O',2:'G',3:'G',4:'G',5:'G',7:'N',8:'W',9:'W',10:'W',11:'W',12:'S',13:'S',14:'S'}
for it in range(2):
    c=o.copy()
    for y in range(1,63):
        for x in range(1,63):
            v=c[y,x]
            if v in (0,1,7): continue
            nb=[c[y-1,x],c[y+1,x],c[y,x-1],c[y,x+1]]
            if len(set(nb))==1 and nb[0]!=v and nb[0] in GROUP and GROUP[nb[0]]==GROUP[v]: mark('losse tintpixel',y,x,nb[0])
# 3. losse omlijningspixel midden in een vlak zonder lijnbuur (rivet-ruis): alle 8 buren geen lijn
for y in range(1,63):
    for x in range(1,63):
        if o[y,x]==1:
            nb=o[y-1:y+2,x-1:x+2].ravel(); nb=np.delete(nb,4)
            if (nb>0).all() and not np.isin(nb,[1,5,10,14]).any():
                u,uc=np.unique(nb,return_counts=True); mark('losse lijnpixel (bout/ruis)',y,x,u[uc.argmax()])
np.save(f'post_{VAR}.npy',o)
print('afwijkend van kale reductie:',(o!=b).sum(),log)
