# Aders in de vleugels uit het model: donkere natieve pixels (helderheid < 140, grijze groep) binnen de vleugels,
# niet grenzend aan zwart/lucht (dan is het de buitenlijn), als 8-samenhangende component >= MINLEN natieve px.
# Spritecel = ader als hij >= 2 aderpixels bevat. Uitvoer: lijst cellen.
import numpy as np,sys; from PIL import Image
from lab import label
nat=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); grp=np.load('ngrp.npy'); L=nat.mean(-1)
X0,Y0,fx,fy,OX,OY=21,12,109/56,123/63,4,1
H,W=grp.shape
sx=lambda i:int((i-X0)/fx+OX); sy=lambda j:int((j-Y0)/fy+OY)
src=open('zones.py').read(); exec(src[src.index('def zone'):src.index('from collections')])
def aders(MINLEN=12):
    wing=np.zeros((H,W),bool)
    for j in range(H):
        for i in range(W):
            if grp[j,i] in ('k','y') and zone(sx(i),sy(j))=='vleugels': wing[j,i]=True
    dark=wing&(grp=='k')&(L<140)
    # buitenlijn-buren eruit: pixel met zwart of lucht binnen 1 px
    edge=np.zeros_like(dark)
    for j in range(H):
        for i in range(W):
            if dark[j,i]:
                n=grp[max(0,j-1):j+2,max(0,i-1):i+2]
                if (n=='#').any() or (n=='.').any(): edge[j,i]=True
    v=dark&~edge
    lab,n=label(v)
    keep=np.zeros_like(v)
    for k in range(1,n+1):
        if (lab==k).sum()>=MINLEN: keep|=lab==k
    from collections import Counter
    c=Counter((sx(i),sy(j)) for j,i in zip(*np.where(keep)))
    return sorted(p for p,v in c.items() if v>=2)

if __name__=='__main__': print(aders(int(sys.argv[1]) if len(sys.argv)>1 else 12))
