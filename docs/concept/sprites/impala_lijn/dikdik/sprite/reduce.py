# Kale reductie: natief raster (72x89 figuur) -> HOOGTE px hoog.
# Per spritecel: vlakgemiddelde over het 1024-model (alleen voorgrond), dan dichtstbijzijnde modelpaletkleur
# (k-means op het natieve raster). Alpha = aandeel voorgrond >= 0.45.
# Uit: kaal.png, kaal_lab.npy (labels, -1 = transparant), model_pal.npy, kaal_mode.png (variant: meest voorkomende kleur)
import sys, numpy as np
from PIL import Image
HOOGTE=int(sys.argv[1]) if len(sys.argv)>1 else 52
a=np.asarray(Image.open('../referenties/model_r3b.png').convert('RGB')).astype(float)
nat=np.asarray(Image.open('natief.png').convert('RGB')).reshape(-1,3).astype(float)
nat=nat[nat.min(axis=1)<225]
rng=np.random.default_rng(3); K=16
C=nat[rng.choice(len(nat),K,replace=False)]
for _ in range(80):
    lab=((nat[:,None,:]-C[None])**2).sum(2).argmin(1)
    C=np.array([nat[lab==k].mean(0) if (lab==k).any() else C[k] for k in range(K)])
C=C[np.argsort(C.sum(1))]
fg=a.min(axis=2)<225
labm=((a.reshape(-1,1,3)-C[None])**2).sum(2).argmin(1).reshape(a.shape[:2])
ys,xs=np.nonzero(fg); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
p=(y1-y0)/HOOGTE; W=int(np.ceil((x1-x0)/p))
out=-np.ones((HOOGTE,W),int); mode=-np.ones((HOOGTE,W),int)
for j in range(HOOGTE):
    for i in range(W):
        xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p)); ya,yb=int(round(y0+j*p)),int(round(y0+(j+1)*p))
        f=fg[ya:yb,xa:xb]
        if f.size==0 or f.mean()<0.45: continue
        m=a[ya:yb,xa:xb][f].mean(0)
        out[j,i]=((C-m)**2).sum(1).argmin()
        mode[j,i]=np.bincount(labm[ya:yb,xa:xb][f],minlength=K).argmax()
np.save('kaal_lab.npy',out); np.save('kaal_mode_lab.npy',mode); np.save('model_pal.npy',C)
for L,n in [(out,'kaal'),(mode,'kaal_mode')]:
    img=np.zeros((HOOGTE,W,4),'uint8')
    for j in range(HOOGTE):
        for i in range(W):
            if L[j,i]>=0: img[j,i,:3]=C[L[j,i]]; img[j,i,3]=255
    Image.fromarray(img).save(n+'.png'); Image.fromarray(img).resize((W*10,HOOGTE*10),Image.NEAREST).save(n+'_10x.png')
print('pitch',p,'W',W,'px',(out>=0).sum()); [print(k,C[k].astype(int)) for k in range(K)]
