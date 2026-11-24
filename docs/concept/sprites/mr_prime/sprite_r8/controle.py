# controle r7: losse pixels (geen 4-buur met dezelfde tint, niet op de buitenrand, buiten ogen/stok), tintclusters < 3 px
import numpy as np; from PIL import Image; from collections import deque
P=np.asarray(Image.open('mr_prime.png')).astype(int); H,W=P.shape
print('kleuren incl. transparant:',len(np.unique(P)),'| palet-index 0 transparant:',Image.open('mr_prime.png').info.get('transparency'))
def rand(y,x): return any(not(0<=y+dy<H and 0<=x+dx<W) or P[y+dy,x+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
los=[];klein=[];seen=np.zeros_like(P,bool)
for y in range(H):
    for x in range(W):
        v=P[y,x]
        if v==0 or seen[y,x]: continue
        q=deque([(y,x)]); seen[y,x]=1; comp=[(y,x)]
        while q:
            a,b=q.popleft()
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=a+dy,b+dx
                if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and P[yy,xx]==v: seen[yy,xx]=1; q.append((yy,xx)); comp.append((yy,xx))
        if len(comp)<3 and v!=1: klein.append((v,comp))
print('tintclusters < 3 px (excl. zwart):',len(klein))
for v,c in klein: print('  tint',v,c)
