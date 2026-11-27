# Modellijnen naar het spriteraster: binnenlijnen van het natieve model (L<20, niet aan de buitenrand),
# per 8-verbonden component; component >= MIN natieve px = echte lijn, kleiner = spikkel.
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from gemeen import H
nat=np.array(Image.open('natief_bewerkt.png')).astype(float)
m=nat[...,3]>0; ys,xs=np.nonzero(m); nat=nat[ys.min():ys.max()+1, xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
Hn,Wn=m.shape; W=round(Wn*H/Hn)
L=nat[...,:3].mean(2); line=(L<20)&m
rand=line & nd.binary_dilation(~m)          # buitenomlijning
inner=line&~rand
lab,n=nd.label(inner,np.ones((3,3)))
sz=nd.sum(inner,lab,range(1,n+1))
MIN=5
echt=np.isin(lab,1+np.nonzero(sz>=MIN)[0])
hit=np.zeros((H,W),int)
for y,x in zip(*np.nonzero(echt)):
    hit[min(H-1,int((y+0.5)*H/Hn)),min(W-1,int((x+0.5)*W/Wn))]+=1
np.save('lijnhit.npy',hit)
print('binnenlijn-componenten',n,'echt',int((sz>=MIN).sum()),'natief px echt',int(echt.sum()),'spikkel',int(inner.sum()-echt.sum()))
