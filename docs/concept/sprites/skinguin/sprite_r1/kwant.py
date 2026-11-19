# geschrapt.png -> index-raster met de dichtstbijzijnde modelkleur (clustercentra gemeten op het model); achtergrond = floodfill vanaf de rand
import numpy as np; from PIL import Image; from collections import deque
a=np.asarray(Image.open('geschrapt.png')).astype(int); H,W=a.shape[:2]
C={1:(24,16,28),2:(66,48,48),3:(152,38,38),4:(214,52,50),5:(230,100,90),6:(234,238,248),7:(184,188,204),8:(100,100,122),9:(244,214,96),10:(188,150,50),11:(220,184,64)}
light=a.min(2)>=245
bg=np.zeros((H,W),bool); q=deque([(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)])
while q:
    y,x=q.popleft()
    if 0<=y<H and 0<=x<W and light[y,x] and not bg[y,x]:
        bg[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
keys=list(C); cen=np.array([C[k] for k in keys])
d=((a[:,:,None,:]-cen[None,None])**2).sum(-1); o=np.array(keys)[d.argmin(-1)]
o[bg]=0
np.savetxt('kaal.txt',o,fmt='%d')
pal=[(255,0,255)]+[C[k] for k in range(1,12)]
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in pal for v in c]+[0]*(768-3*len(pal)))
im.save('kaal.png',transparency=0); im.convert('RGB').resize((W*8,H*8),Image.NEAREST).save('kaal_8x.png')
from collections import Counter; print(Counter(o.ravel()))
