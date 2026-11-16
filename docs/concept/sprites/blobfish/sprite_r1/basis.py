# Blobfish r1 onderlaag: model verkleinen met oppervlak-middeling (methode hauntflare/basis/basis.py)
# en kwantiseren naar kleuren die echt in het model staan. Niets getekend.
# Het model heeft een raster van ~4 px (natief ~200x118 voor de vis); 52 px breed = ~3,9x verkleining,
# daarom oppervlak-middeling i.p.v. 2x-reductie (GEMINI.md: schrappen/2x alleen bij kleine verkleining).
# Gebruik: python3 basis.py [breedte=52] [alpha=0.5] [kleuren=14]
import sys; from PIL import Image; import numpy as np
W=int(sys.argv[1]) if len(sys.argv)>1 else 52
T=float(sys.argv[2]) if len(sys.argv)>2 else 0.5
K=int(sys.argv[3]) if len(sys.argv)>3 else 14
ONDER=54   # bodemlijn (onderste rij), zie NOTITIES.md
a=np.asarray(Image.open('../model/model.png').convert('RGB')).astype(float)
wit=a.min(2)>=0xe0
ys,xs=np.where(~wit); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
crop=a[y0:y1,x0:x1]; al=(~wit[y0:y1,x0:x1]).astype(float)
s=(x1-x0)/W; H=int(round((y1-y0)/s))
def area(arr):
    big=np.kron(arr,np.ones((4,4)))
    return np.asarray(Image.fromarray(big.astype('float32')).resize((W,H),Image.BOX))
A=area(al); C=np.stack([area(crop[...,k]*al) for k in range(3)],2)/np.maximum(A,1e-6)[...,None]
# palet: k-means op de modelpixels, elk centrum daarna op de dichtstbijzijnde echte modelkleur gezet
px=crop[al>0].reshape(-1,3); rng=np.random.default_rng(1); smp=px[rng.choice(len(px),40000,replace=False)]
# start: helderheidskwantielen, zodat donkere lijn en glans een eigen centrum krijgen
lum=smp@[0.299,0.587,0.114]; cen=np.array([smp[np.argsort(lum)[int(q*(len(smp)-1))]] for q in np.linspace(0.005,0.995,K)])
for _ in range(40):
    d=((smp[:,None,:]-cen[None])**2).sum(2); lab=d.argmin(1)
    cen=np.array([smp[lab==k].mean(0) if (lab==k).any() else cen[k] for k in range(K)])
uniq=np.unique(px.astype(int),axis=0)
cen=np.array([uniq[((uniq-c)**2).sum(1).argmin()] for c in cen])
cen=cen[np.argsort(cen@[0.299,0.587,0.114])]
out=np.zeros((64,64),int); ox=(64-W)//2; oy=ONDER+1-H
for y in range(H):
    for x in range(W):
        if A[y,x]>=T: out[oy+y,ox+x]=1+((cen-C[y,x])**2).sum(1).argmin()
# gaten dicht (achtergrond die niet aan de rand hangt)
from collections import deque
bg=np.zeros((64,64),bool); q=deque([(0,0)]); bg[0,0]=1
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<64 and 0<=xx<64 and out[yy,xx]==0 and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
gat=(out==0)&~bg
for y,x in zip(*np.where(gat)): out[y,x]=1+((cen-C[y-oy,x-ox])**2).sum(1).argmin()
pal=[(255,0,255)]+[tuple(int(v) for v in c) for c in cen]
p=Image.fromarray(out.astype('uint8'),'P'); p.putpalette([v for c in pal for v in c]+[0]*(768-3*len(pal))); p.save('basis.png',transparency=0)
np.save('basis_C.npy',C); open('basis_geo.txt','w').write(f'{x0} {y0} {s} {ox} {oy} {W} {H}\n')
print('maat',W,H,'px',(out>0).sum(),'pos',ox,oy,'gaten',gat.sum()); print('palet',pal[1:])
