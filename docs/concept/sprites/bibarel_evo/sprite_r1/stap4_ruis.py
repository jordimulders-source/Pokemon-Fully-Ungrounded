# Stap 4: ruis weg (Krassault-recept): tintclusters < 3 px (4-buren) nemen de meest voorkomende buurtint over, liefst binnen
# dezelfde kleurgroep. Omlijning (1), silhouet en het gezicht (wordt per pixel gerepareerd) blijven buiten het filter.
import numpy as np, sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from scipy import ndimage
o=laad('sprite_r1/basis.png').copy()
GROEP={3:'b',4:'b',5:'b',6:'c',7:"c",9:'d',10:'d',11:'o',12:'o',13:'w',14:'w'}
for ronde in range(3):
    n_ver=0
    for k in GROEP:
        lab,n=ndimage.label(o==k)
        for i in range(1,n+1):
            pts=np.argwhere(lab==i)
            if len(pts)>=3: continue
            nb={}
            for y,x in pts:
                for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                    Y,X=y+dy,x+dx
                    if 0<=Y<64 and 0<=X<64 and lab[Y,X]!=i and o[Y,X] not in (0,1):
                        nb[o[Y,X]]=nb.get(o[Y,X],0)+1
            if not nb: continue
            zelf={q:v for q,v in nb.items() if GROEP.get(q)==GROEP[k]}
            kies=max(zelf or nb,key=lambda q:(zelf or nb)[q])
            for y,x in pts: o[y,x]=kies
            n_ver+=len(pts)
    print('ronde',ronde,'gewijzigd',n_ver)
opslaan(o,'sprite_r1/ontruist.png',8)
