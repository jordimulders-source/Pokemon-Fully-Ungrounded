# natief -> 2x2-blokreductie. Elke spritepixel komt uit zijn eigen 2x2-blok modelpixels (niets getekend):
#  >=3 achtergrond -> transparant; zwarte modelpixel in het blok -> O; anders donkergroene lijnpixel -> L;
#  anders gemiddelde kleur van de vulpixels -> dichtstbijzijnde modelvulkleur. Gebruik: python3 reduce.py OY OX [geel]
import sys, numpy as np
from PIL import Image
from palet import KM, I, MODEL, FILL
lab=np.load('km_lab.npy'); H,W=lab.shape
rgb=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
cl=np.zeros(lab.shape,int)
for k,v in KM.items(): cl[lab==k]=I[v]
OY,OX=int(sys.argv[1]),int(sys.argv[2]); MODE=sys.argv[3] if len(sys.argv)>3 else ''
F=np.array([MODEL[n] for n in FILL],float); FI=[I[n] for n in FILL]
h,w=(H-OY)//2,(W-OX)//2; o=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2)); b=cl[sl].ravel()
        if (b==0).sum()>=3: continue
        if (b==I['O']).any(): o[j,i]=I['O']; continue
        if (b==I['L']).any(): o[j,i]=I['L']; continue
        if MODE=='geel' and (b==I['Y1']).any(): o[j,i]=I['Y1']; continue   # gele bogen zijn 1 modelpixel breed: geel wint, zoals de lijnen
        m=np.isin(b,FI); c=rgb[sl].reshape(-1,3)[m].mean(0)
        o[j,i]=FI[int(((F-c)**2).sum(1).argmin())]
np.save('kaal_%d%d%s.npy'%(OY,OX,MODE),o)
ys,xs=np.where(o>0); print(OY,OX,'bbox',xs.max()-xs.min()+1,ys.max()-ys.min()+1,'px',(o>0).sum())
