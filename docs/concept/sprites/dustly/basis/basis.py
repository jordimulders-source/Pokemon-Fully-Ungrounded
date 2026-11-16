# Kale reductie Dustly: natief (100x100, cloud 67x63) -> factor 2/3 met vlakgemiddelde (BOX) over de dekkende
# pixels, alpha >= T, kleur = dichtstbijzijnde modelkleur (k-means 16 op het natieve model). Niets getekend.
import sys; from PIL import Image; import numpy as np
T=float(sys.argv[1]) if len(sys.argv)>1 else 0.5
a=np.asarray(Image.open('basis/natief.png').convert('RGB')).astype(float)
bg=a.min(2)>=200                      # bijna-wit = achtergrond (Gemini-ruis weg)
X0,Y0=17,18; Wn,Hn=69,63              # natieve uitsnede, veelvoud van 3
crop=a[Y0:Y0+Hn,X0:X0+Wn].copy(); al=(~bg[Y0:Y0+Hn,X0:X0+Wn]).astype(float)
assert not (~bg)[:,:X0].any() and not (~bg)[:,X0+Wn:].any() and not (~bg)[:Y0].any() and not (~bg)[Y0+Hn:].any()
# modelpalet
px=crop[al>0]; np.random.seed(1); k=16
C=px[np.linspace(0,len(px)-1,k).astype(int)]
for it in range(60):
    l=((px[:,None]-C[None])**2).sum(2).argmin(1)
    C=np.array([px[l==i].mean(0) if (l==i).any() else C[i] for i in range(k)])
C=C[np.argsort(C@[.299,.587,.114])]
np.save('basis/modelpalet.npy',C)
W,H=Wn*2//3,Hn*2//3
big=lambda x: np.kron(x,np.ones((2,2)))
def box(x): return np.asarray(Image.fromarray(big(x).astype('float32')).resize((W,H),Image.BOX))
A=box(al); Cc=np.stack([box(crop[...,c]*al) for c in range(3)],2)/np.maximum(A,1e-6)[...,None]
idx=np.zeros((H,W),int)-1
for y in range(H):
    for x in range(W):
        if A[y,x]>=T: idx[y,x]=((C-Cc[y,x])**2).sum(1).argmin()
np.save('basis/kaal_idx.npy',idx)
out=np.zeros((64,64,4),'uint8'); ox=(64-W)//2; oy=64-H-3
for y in range(H):
    for x in range(W):
        if idx[y,x]>=0: out[oy+y,ox+x,:3]=C[idx[y,x]]; out[oy+y,ox+x,3]=255
Image.fromarray(out).save('basis/kaal_64.png'); print('maat',W,H,'pos',ox,oy,'px',(idx>=0).sum())
for c in C: print(c.astype(int),int(c@[.299,.587,.114]))
