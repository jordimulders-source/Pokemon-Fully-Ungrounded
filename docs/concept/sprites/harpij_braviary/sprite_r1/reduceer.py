# Stap 2: kale reductie. Natief model (bbox x24-81, y3-94) -> factor F met vlakgemiddelde (exacte oppervlakte-gewichten)
# en dichtstbijzijnde modelkleur (modelpalet uit kwant.py + oogkleuren gemeten). Regel: donker (lijn) wint als >= DARK van het vak.
import numpy as np, sys; from PIL import Image
F=float(sys.argv[1]) if len(sys.argv)>1 else 0.66
DARK=float(sys.argv[2]) if len(sys.argv)>2 else 0.34
a=np.asarray(Image.open('../model/model_natief.png').convert('RGB')).astype(float)
o=np.load('model_idx.npy'); pal=np.load('model_pal.npy')
x0,x1,y0,y1=24,82,3,95
A=a[y0:y1,x0:x1]; M=(o[y0:y1,x0:x1]>0).astype(float)
dark=(A.mean(2)<36).astype(float)*M
h,w=M.shape; H=int(round(h*F)); W=int(round(w*F))
def wmat(n,N):
    # gewichten: doelpixel j bedekt bron [j/F,(j+1)/F)
    m=np.zeros((N,n)); s=n/N
    for j in range(N):
        a0,a1=j*s,(j+1)*s
        for i in range(int(a0),min(n,int(np.ceil(a1)))):
            m[j,i]=max(0,min(a1,i+1)-max(a0,i))
    return m
Ry=wmat(h,H); Rx=wmat(w,W)
def red(img): return np.einsum('yi,ijc,xj->yxc',Ry,img,Rx) if img.ndim==3 else Ry@img@Rx.T
area=Ry.sum(1)[:,None]*Rx.sum(1)[None]
cov=red(M)/area; dk=red(dark)/area
avg=red(A*M[:,:,None])/np.maximum(red(M),1e-6)[:,:,None]
C=np.vstack([pal,[[121,96,64],[151,131,88]]])   # + oog (amber donker/licht, gemeten)
d=((avg[:,:,None]-C[None,None])**2).sum(-1); idx=d.argmin(-1)+1
idx[dk>=DARK]=1
idx[cov<0.5]=0
np.save('kaal.npy',idx); np.save('kaal_pal.npy',C)
P=[(255,255,255)]+[tuple(int(v) for v in c) for c in C]
im=Image.fromarray(idx.astype('uint8'),'P'); im.putpalette([v for t in P for v in t]+[0]*(768-3*len(P)))
im.save('kaal.png'); im.convert('RGB').resize((W*10,H*10),Image.NEAREST).save('kaal_10x.png')
print(W,H)
