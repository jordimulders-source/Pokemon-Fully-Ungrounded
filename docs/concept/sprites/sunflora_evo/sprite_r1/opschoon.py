# Technisch opschonen van de kop: tintvlekjes < 3 px (4-buren, zelfde index) buiten het gezicht en
# niet de buitenlijn -> meest voorkomende buurkleur (8-buren) uit dezelfde kop. Lijf en gezicht onaangeroerd.
import numpy as np; from PIL import Image; from scipy import ndimage; from pal import PAL
C=np.load('samen.npy'); O=C.copy()
FACE0=np.zeros_like(C,bool); FACE0[19:40,15:39]=True
na=((C==10)&~FACE0).sum(); C[(C==10)&~FACE0]=5; print('tongkleur buiten gezicht -> oranje',na)
FACE=np.zeros_like(C,bool); FACE[19:40,15:39]=True
EDGE=ndimage.binary_dilation(C==0)&(C>0)   # buitenlijn/selout niet aanraken
FACE|=EDGE
n_tot=0
for it in range(3):
    ch=0
    for k in range(2,11):
        lab,n=ndimage.label(C==k)
        for l in range(1,n+1):
            ys,xs=np.where(lab==l)
            if len(ys)>=3: continue
            keep=FACE[ys,xs]; ys,xs=ys[~keep],xs[~keep]
            for y,x in zip(ys,xs):
                nb=[C[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if (yy,xx)!=(y,x) and 0<=yy<64 and 0<=xx<64 and C[yy,xx] in range(2,11) and C[yy,xx]!=k]
                if nb: C[y,x]=max(set(nb),key=nb.count); ch+=1
    n_tot+=ch
    if not ch: break
print('opgeschoonde vlekpixels',n_tot,'| gewijzigd t.o.v. kaal:',(C!=O).sum())
np.save('r1_schoon.npy',C)
# Lijf: lichte groene pixels op de buitenrand -> lijn (b aan de lichtkant boven/links, zwart onder/rechts)
nl=0
for y,x in zip(*np.where(np.isin(C,[12,13,14]))):
    up=y==0 or C[y-1,x]==0; lf=x==0 or C[y,x-1]==0
    dn=y==63 or C[y+1,x]==0; rt=x==63 or C[y,x+1]==0
    if dn or rt: C[y,x]=1; nl+=1
    elif up or lf: C[y,x]=11; nl+=1
print('lijf-randpixels naar lijn',nl)
np.save('r1_schoon.npy',C)
