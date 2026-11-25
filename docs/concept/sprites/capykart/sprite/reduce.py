# Kale reductie van model_r5 (1024) naar BREEDTE px: modelpixels -> k-means modelpalet,
# per spritecel wint de meest voorkomende paletkleur (geen gemiddelde = geen blur), alpha = aandeel voorgrond >= 0.45.
# Uit: kaal_lab.npy (labels, -1 = transparant), model_pal.npy, kaal.png, kaal_12x.png
import sys, numpy as np
from PIL import Image
BREEDTE=int(sys.argv[1]) if len(sys.argv)>1 else 62
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/'
a=np.asarray(Image.open(R+'referenties/model_r5.png').convert('RGB')).astype(float)
fg=a.min(axis=2)<225
pix=a[fg]; rng=np.random.default_rng(1); K=int(sys.argv[2]) if len(sys.argv)>2 else 18
S=pix[rng.choice(len(pix),40000,replace=False)]
C=S[rng.choice(len(S),K,replace=False)]
for _ in range(60):
    lab=((S[:,None,:]-C[None])**2).sum(2).argmin(1)
    C=np.array([S[lab==k].mean(0) if (lab==k).any() else C[k] for k in range(K)])
C=C[np.argsort(C.sum(1))]
lab=np.zeros(a.shape[:2],int)
flat=a.reshape(-1,3)
for s in range(0,len(flat),65536):
    lab.reshape(-1)[s:s+65536]=((flat[s:s+65536,None,:]-C[None])**2).sum(2).argmin(1)
ys,xs=np.nonzero(fg); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
p=(x1-x0)/BREEDTE; H=int(np.ceil((y1-y0)/p))
out=-np.ones((H,BREEDTE),int)
for j in range(H):
    for i in range(BREEDTE):
        xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p))
        ya,yb=max(int(round(y1-(H-j)*p)),0),int(round(y1-(H-j-1)*p))
        f=fg[ya:yb,xa:xb]
        if f.size==0 or f.mean()<0.45: continue
        out[j,i]=np.bincount(lab[ya:yb,xa:xb][f],minlength=K).argmax()
np.save(R+'sprite/kaal_lab.npy',out); np.save(R+'sprite/model_pal.npy',C)
img=np.zeros((H,BREEDTE,4),'uint8')
m=out>=0; img[m,:3]=C[out[m]]; img[m,3]=255
Image.fromarray(img).save(R+'sprite/kaal.png')
Image.fromarray(img).resize((BREEDTE*12,H*12),Image.NEAREST).save(R+'sprite/kaal_12x.png')
print('bbox',x0,x1,y0,y1,'pitch',p,'H',H)
for k in range(K): print(k,C[k].astype(int),(out==k).sum())
