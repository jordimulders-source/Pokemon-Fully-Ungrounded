# Segmenten op het natieve raster: lijnpixels (k-means 0 zwart, 1/3 donkergroen, 2/8 donkergeel, 4 donkerroze) scheiden de vlakken;
# 4-samenhangende vulvlakken = onderdelen (veer, kop, band ...). Kleine vlakjes (<8 natieve px) en lijnpixels krijgen het dichtstbijzijnde segment (BFS).
# -> seg_natief.npy (segment per natieve pixel, -1 = achtergrond), lijn_natief.npy (bool)
import numpy as np
from collections import deque
lab=np.load('km_lab.npy'); H,W=lab.shape
bg=lab<0; L=np.isin(lab,[0,1,2,3,4,8]) & ~bg; F=~bg & ~L
seg=-np.ones((H,W),int); n=0; size={}
for y in range(H):
    for x in range(W):
        if F[y,x] and seg[y,x]<0:
            q=deque([(y,x)]); seg[y,x]=n; c=0
            while q:
                a,b=q.popleft(); c+=1
                for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                    yy,xx=a+dy,b+dx
                    if 0<=yy<H and 0<=xx<W and F[yy,xx] and seg[yy,xx]<0: seg[yy,xx]=n; q.append((yy,xx))
            size[n]=c; n+=1
klein=[k for k,c in size.items() if c<8]
for k in klein: seg[seg==k]=-1
# BFS-uitbreiding over dekkende pixels
q=deque(zip(*np.where(seg>=0)))
while q:
    a,b=q.popleft()
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=a+dy,b+dx
        if 0<=yy<H and 0<=xx<W and not bg[yy,xx] and seg[yy,xx]<0: seg[yy,xx]=seg[a,b]; q.append((yy,xx))
np.save('seg_natief.npy',seg); np.save('lijn_natief.npy',L)
print('segmenten',n,'klein',len(klein),'groot',sum(1 for c in size.values() if c>=8))
