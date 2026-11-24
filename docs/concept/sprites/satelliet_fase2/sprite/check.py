# Controle: losse pixels (geen 4-buur van dezelfde klasse; lijnklassen 1/11/15 en glans uitgezonderd),
# lichte pixels op de buitenrand (grenzen aan transparant), kleuren, bbox.
import numpy as np, sys; from PIL import Image
im=Image.open(sys.argv[1]); o=np.array(im); H,W=o.shape
ys,xs=np.where(o>0); print('bbox x %d-%d y %d-%d (%dx%d)'%(xs.min(),xs.max(),ys.min(),ys.max(),xs.max()-xs.min()+1,ys.max()-ys.min()+1),'kleuren',len(set(o.ravel()))-1,'(+transparant)')
nb=lambda j,i:[(j+dy,i+dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=j+dy<H and 0<=i+dx<W]
los=[];rand=[]
for j,i in zip(ys,xs):
    v=o[j,i]; n=[o[q] for q in nb(j,i)]
    if v not in (1,11,15) and v not in n and not (j,i)==(29,21): los.append((i,j,int(v)))
    if 0 in n and v not in (1,8,9,7): rand.append((i,j,int(v)))
    if v==1 and all(q!=0 for q in n) and sum(q==1 for q in n)==0: los.append((i,j,'1-los'))
print('losse pixels',len(los),los[:60]); print('lichte buitenrand',len(rand),rand[:60])
