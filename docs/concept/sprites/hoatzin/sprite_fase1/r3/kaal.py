# Stap 2: kale reductie van natief_bewerkt.png naar 44 px hoog (vlakgemiddelde, lijn wint bij >=34% lijnpixels),
# daarna dichtstbijzijnde paletkleur. Geen handwerk.
import numpy as np
from PIL import Image
from gemeen import PAL, nearest, H
nat=np.array(Image.open('natief_bewerkt.png')).astype(float)
m=nat[...,3]>0
ys,xs=np.nonzero(m); nat=nat[ys.min():ys.max()+1, xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
Hn,Wn=m.shape; W=round(Wn*H/Hn)
# 8x oversampling voor eerlijke vlakgewichten
up=8; N=np.repeat(np.repeat(nat,up,0),up,1); M=np.repeat(np.repeat(m,up,0),up,1)
out=np.zeros((H,W),np.uint8); frac=np.zeros((H,W)); meanc=np.zeros((H,W,3))
for y in range(H):
  for x in range(W):
    y0,y1=round(y*Hn*up/H),round((y+1)*Hn*up/H); x0,x1=round(x*Wn*up/W),round((x+1)*Wn*up/W)
    mm=M[y0:y1,x0:x1]
    if mm.mean()<0.45: continue
    blk=N[y0:y1,x0:x1][mm][:,:3]; L=blk.mean(1)
    line=L<20; frac[y,x]=line.mean(); meanc[y,x]=blk[~line].mean(0) if (~line).any() else 0
    if line.mean()>=0.34: out[y,x]=1; continue
    c=blk[~line].mean(0)
    out[y,x]=nearest(c)
np.save('kaal.npy',out); np.save('frac.npy',frac); np.save('meanc.npy',meanc)
print('kaal',W,'x',H,'px',(out>0).sum())
