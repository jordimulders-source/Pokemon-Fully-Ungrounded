# Onderlaag: natief (165x146 modelpixels) -> 46 breed (factor 3,59), dekking >= 0,45 = silhouet, kleur = gemiddelde voorgrond -> dichtstbijzijnde paletkleur.
# Alleen startpunt; de sprite wordt daarna met de hand op het tekstraster opgeschoond.
import numpy as np; from PIL import Image; from palet import PAL,CH
a=np.asarray(Image.open('natief.png')).astype(float)
x0,x1,y0,y1=18,183,37,183; W=46; s=(x1-x0)/W; H=int(np.ceil((y1-y0)/s))
fg=a.min(2)<225; pal=np.array(PAL[1:],float)
out=np.zeros((64,64),int); top=63-H; left=(64-W)//2
for j in range(H):
  for i in range(W):
    ya,yb=y0+j*s,y0+(j+1)*s; xa,xb=x0+i*s,x0+(i+1)*s
    ys=slice(int(ya),int(np.ceil(yb))); xs=slice(int(xa),int(np.ceil(xb)))
    f=fg[ys,xs]
    if f.mean()<0.45: continue
    c=a[ys,xs][f].mean(0)
    out[top+j,left+i]=1+int(np.argmin(((pal-c)**2).sum(1)))
# buitenrand = omlijning
m=out>0; p=np.pad(m,1); edge=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
out[edge]=1
print('H',H,'px',m.sum())
open('onderlaag.txt','w').write('\n'.join(''.join(CH[v] for v in r) for r in out)+'\n')
