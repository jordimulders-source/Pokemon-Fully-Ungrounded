# Lijnbewarende oppervlakreductie (S=1.6): per spritecel de dekking per modelklasse;
# volgorde: achtergrond (>=0,55) > paars (>=0,22) > koper (>=0,25) > omlijning (>=0,35) > meeste dekking van de overige.
import numpy as np; import sys
from PIL import Image; from collections import deque
from reduce_pal import PAL
a=np.asarray(Image.open('natief.png')).astype(int)
# achtergrond = neutraal wit (alle kanalen >=248, max-min<=6), floodfill vanaf de rand (vleugels zijn blauwig wit)
wit=(a.min(2)>=248)&((a.max(2)-a.min(2))<=6); bg=np.zeros(wit.shape,bool)
q=deque([(y,x) for y in range(100) for x in (0,99)]+[(y,x) for x in range(100) for y in (0,99)])
while q:
    y,x=q.popleft()
    if 0<=y<100 and 0<=x<100 and wit[y,x] and not bg[y,x]: bg[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
cen=np.array(PAL[1:]); d=((a[:,:,None,:]-cen[None,None])**2).sum(-1); cl=d.argmin(-1)+1; cl[bg]=0
np.save('nat_cls.npy',cl)
S=1.6; X0,Y0,X1,Y1=17,20,84,82
W=int(np.ceil((X1-X0)/S)); H=int(np.ceil((Y1-Y0)/S))
o=np.zeros((H,W),int)
for j in range(H):
  for i in range(W):
    x0=X0+i*S; x1=x0+S; y0=Y0+j*S; y1=y0+S; v=np.zeros(16)
    for y in range(int(y0),int(np.ceil(y1))):
      wy=min(y+1,y1)-max(y,y0)
      for x in range(int(x0),int(np.ceil(x1))):
        wx=min(x+1,x1)-max(x,x0); v[cl[y,x]]+=wx*wy
    v/=S*S
    if v[0]>=0.55: continue
    if v[13]>=0.22: o[j,i]=13; continue
    if v[14]+v[15]>=0.25: o[j,i]=14 if v[14]>=v[15] else 15; continue
    if v[1]>=0.35: o[j,i]=1; continue
    r=v.copy(); r[0]=0; r[1]=0; r[13]=0; o[j,i]=r.argmax() if r.max()>0 else 1
np.savetxt('kaal.txt',o,fmt='%2d'); print(W,H,(o>0).sum())
