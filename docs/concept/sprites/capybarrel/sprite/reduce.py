# Kale reductie van het 1024-model naar BREEDTE px figuurbreedte:
# modelpixels -> dichtstbijzijnde modelpaletkleur (k-means op het natieve raster),
# per spritecel wint de meest voorkomende paletkleur (geen gemiddelde = geen blur),
# alpha = aandeel voorgrond >= 0.45. Uit: kaal.png (RGBA) + kaal_lab.npy (labels, -1 = transparant)
import sys, numpy as np
from PIL import Image
BREEDTE=int(sys.argv[1]) if len(sys.argv)>1 else 46
FASE=float(sys.argv[2]) if len(sys.argv)>2 else 0.0
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
a=np.asarray(Image.open(R+'referenties/model_r3.png').convert('RGB')).astype(float)
nat=np.asarray(Image.open(R+'oog/r3_natief.png').convert('RGB')).reshape(-1,3).astype(float)
nat=nat[nat.min(axis=1)<225]
rng=np.random.default_rng(1); K=14
C=nat[rng.choice(len(nat),K,replace=False)]
for _ in range(60):
    lab=((nat[:,None,:]-C[None])**2).sum(2).argmin(1)
    C=np.array([nat[lab==k].mean(0) if (lab==k).any() else C[k] for k in range(K)])
C=C[np.argsort(C.sum(1))]
fg=a.min(axis=2)<225
lab=((a.reshape(-1,1,3)-C[None])**2).sum(2).argmin(1).reshape(a.shape[:2])
ys,xs=np.nonzero(fg); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
p=(x1-x0)/BREEDTE; H=int(np.ceil((y1-y0)/p))
out=-np.ones((H,BREEDTE),int)
for j in range(H):
    for i in range(BREEDTE):
        xa,xb=int(round(x0+(i+FASE)*p-FASE*p)),int(round(x0+(i+1)*p))
        ya,yb=int(round(y1-(H-j)*p)),int(round(y1-(H-j-1)*p))
        ya=max(ya,0)
        f=fg[ya:yb,xa:xb]
        if f.size==0 or f.mean()<0.45: continue
        l=lab[ya:yb,xa:xb][f]
        out[j,i]=np.bincount(l,minlength=K).argmax()
np.save(R+'sprite/kaal_lab.npy',out); np.save(R+'sprite/model_pal.npy',C)
img=np.zeros((H,BREEDTE,4),'uint8')
for j in range(H):
    for i in range(BREEDTE):
        if out[j,i]>=0: img[j,i,:3]=C[out[j,i]]; img[j,i,3]=255
Image.fromarray(img).save(R+'sprite/kaal.png')
Image.fromarray(img).resize((BREEDTE*12,H*12),Image.NEAREST).save(R+'sprite/kaal_12x.png')
print('pitch',p,'H',H,'pal'); [print(k,C[k].astype(int)) for k in range(K)]
