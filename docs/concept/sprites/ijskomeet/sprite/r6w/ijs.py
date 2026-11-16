# r6 ijslijf: vulling = mediaan lichte modelpixels, naden = projectie van modellijnen (1 natieve px -> 1 spritepixel), dun gemaakt.
import sys; sys.path.insert(0,'r6w')
import numpy as np; from PIL import Image
from p6 import CH,PAL,to_txt,save,from_txt
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); lum=n.mean(2)
m=np.load('mask_r1.npy'); ox,oy=11,-4
P=np.array(PAL,float); I={c:i for i,c in enumerate(CH)}
POLY=[(0.5,40),(1.2,36),(2.5,32),(4.5,28.5),(7,26.5),(9.5,24.8),(12,23.2),(15,22.6),(17.5,22.8),(20,23.6),(22,24.5),(22.2,39.4),
      (25,39.2),(30,38.8),(31,41.2),(34.6,42.6),(35.6,44),(35.6,52),(34.5,54.5),(34,57.5),(30.5,59.6),(25.5,61),(15.5,61),(11.5,59.6),(7.5,57),(4.5,54),(2.5,50),(1,46)]
def inpoly(px,py,P=POLY):
    c=False; k=len(P)
    for a in range(k):
        x1,y1=P[a]; x2,y2=P[(a+1)%k]
        if (y1>py)!=(y2>py) and px< x1+(py-y1)*(x2-x1)/(y2-y1): c=not c
    return c
ice=np.zeros((64,64),bool)
for j in range(64):
  for i in range(64):
    ice[j,i]=m[j,i] and inpoly(i+0.5,j+0.5)
np.save('r6w/ice.npy',ice)
dark=np.zeros((64,64),int); midl=np.zeros((64,64),int); fill=np.full((64,64),-1)
for j in range(64):
  for i in range(64):
    if not ice[j,i]: continue
    y=3*j+oy; x=3*i+ox
    px=n[y:y+3,x:x+3].reshape(-1,3); l=lum[y:y+3,x:x+3].ravel()
    dark[j,i]=(l<70).sum()
    hi=np.sort(l)[-3:].mean()
    midl[j,i]=((l>=70)&(l<hi-40)).sum()
    keep=l>=hi-30
    med=np.median(px[keep],0)
    cand='WLMD'
    fill[j,i]=I[cand[int(np.argmin([((med-P[I[c]])**2).sum() for c in cand]))]]
seam=(dark>=1)&ice
# dun maken: L-hoeken weg
def thin(s):
    ch=True
    while ch:
        ch=False
        for j in range(1,63):
            for i in range(1,63):
                if not s[j,i]: continue
                nb=[s[j-1,i],s[j,i+1],s[j+1,i],s[j,i-1]]
                if sum(nb)!=2: continue
                # twee loodrechte buren -> hoekpixel
                if (nb[0] and nb[2]) or (nb[1] and nb[3]): continue
                a=(j-1,i) if nb[0] else (j+1,i); b=(j,i+1) if nb[1] else (j,i-1)
                diag=(a[0],b[1])
                # alleen weg als de diagonale tegenhoek leeg is en geen andere 8-buren afhangen
                if s[diag]: continue
                s[j,i]=False; ch=True
    return s
seam=thin(seam.copy())
o=fill.copy()
o[seam]=I['S']
mid=(midl>=3)&~seam&ice&(dark==0)
o[mid & np.isin(fill,[I['W'],I['L']])]=I['D']
np.save('r6w/seam.npy',seam)
to_txt(o,'r6w/ijs.txt')
for j in range(20,62): print('%2d '%j+''.join('.' if o[j,i]<0 else CH[o[j,i]] for i in range(0,38)))
