# Natief raster -> dichtstbijzijnde kleur uit het 15-kleurenpalet (modelkleuren), per natieve pixel.
# Achtergrond = bijna-wit (min-kanaal >= BG) dat vanaf de rand bereikbaar is (flood fill); ingesloten licht = wit/creme van de kop.
import numpy as np; from PIL import Image; from collections import deque
from reduce2 import PAL, n, save
BG=236
cand=n.min(2)>=BG; H,W=cand.shape; bg=np.zeros_like(cand); dq=deque()
for y in range(H):
    for x in (0,W-1): dq.append((y,x))
for x in range(W):
    for y in (0,H-1): dq.append((y,x))
while dq:
    y,x=dq.popleft()
    if not(0<=y<H and 0<=x<W) or bg[y,x] or not cand[y,x]: continue
    bg[y,x]=True; dq.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
d=((n[:,:,None,:]-PAL[None,None,1:,:])**2).sum(3); q=(d.argmin(2)+1).astype('uint8'); q[bg]=0
np.save('natief_q.npy',q); save(q,'natief_q.png'); print('opaak',(q>0).sum())
