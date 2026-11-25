# Kale reductie (hybride, alles uit het model): per spritecel
#  - lijn (modelpalet 0) als >= DREMPEL van de voorgrond in die cel modellijn is;
#  - anders vlakgemiddelde van de niet-lijnpixels -> dichtstbijzijnde modelpaletkleur (zonder 0).
# Silhouet: aandeel voorgrond >= 0.45. Uit: kaal_lab.npy, kaal.png, kaal_10x.png
import sys, numpy as np
from PIL import Image
DREMPEL=float(sys.argv[1]) if len(sys.argv)>1 else 0.30
HOOGTE=52
a=np.asarray(Image.open('../referenties/model_r3b.png').convert('RGB')).astype(float)
C=np.load('model_pal.npy')
fg=a.min(axis=2)<225
labm=((a.reshape(-1,1,3)-C[None])**2).sum(2).argmin(1).reshape(a.shape[:2])
ys,xs=np.nonzero(fg); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
p=(y1-y0)/HOOGTE; W=int(np.ceil((x1-x0)/p))
out=-np.ones((HOOGTE,W),int)
for j in range(HOOGTE):
    for i in range(W):
        xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p)); ya,yb=int(round(y0+j*p)),int(round(y0+(j+1)*p))
        f=fg[ya:yb,xa:xb]
        if f.size==0 or f.mean()<0.45: continue
        l=labm[ya:yb,xa:xb][f]; px=a[ya:yb,xa:xb][f]
        if (l==0).mean()>=DREMPEL: out[j,i]=0; continue
        m=px[l!=0].mean(0)
        out[j,i]=1+((C[1:]-m)**2).sum(1).argmin()
np.save('kaal_lab.npy',out)
img=np.zeros((HOOGTE,W,4),'uint8')
for j in range(HOOGTE):
    for i in range(W):
        if out[j,i]>=0: img[j,i,:3]=C[out[j,i]]; img[j,i,3]=255
Image.fromarray(img).save('kaal.png'); Image.fromarray(img).resize((W*10,HOOGTE*10),Image.NEAREST).save('kaal_10x.png')
print('W',W,'px',(out>=0).sum(),'lijn',(out==0).sum())
# --- extra: gemiddelde modelkleur (zonder lijnpixels) en lijnaandeel per cel, voor het omkleuren per zone ---
avg=np.zeros((HOOGTE,W,3)); lf=np.zeros((HOOGTE,W))
for j in range(HOOGTE):
    for i in range(W):
        xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p)); ya,yb=int(round(y0+j*p)),int(round(y0+(j+1)*p))
        f=fg[ya:yb,xa:xb]
        if f.size==0 or not f.any(): continue
        l=labm[ya:yb,xa:xb][f]; px=a[ya:yb,xa:xb][f]; lf[j,i]=(l==0).mean()
        if (l!=0).any(): avg[j,i]=px[l!=0].mean(0)
np.save('kaal_avg.npy',avg); np.save('kaal_lf.npy',lf)
