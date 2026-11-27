# r7 = r6 + D: binnenlijnen alleen waar het model ze heeft (Krassault/Abra-regel): een lijnpixel (1/2) binnen het silhouet
#   (niet aan de buitenrand, niet in oog/ringzones die al per pixel gezet zijn) waarvan het 2x2-blok < 2 natieve lijnpixels
#   heeft, krijgt de modelkleur zonder lijn (M_zonderlijn). Gelogd in r7/log.txt.
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']')
L6=np.load(D+'r6/idx.npy'); L=L6.copy(); H,W=L.shape
Mz=np.load(D+'M_zonderlijn.npy'); ND=np.load(D+'N_donker.npy')
F=L>0
log=open(D+'r7/log.txt','w')
def rand(y,x): return any(not(0<=y+dy<H and 0<=x+dx<W) or not F[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
VAST=np.zeros((H,W),bool)
VAST[11:23,30:50]=True; VAST[44:54,46:59]=True   # ringen (r6 A/C)
VAST[24:34,16:30]=True                           # ogen (r6 B)
n=0
for y in range(H):
    for x in range(W):
        if F[y,x] and L[y,x] in (1,2) and not rand(y,x) and not VAST[y,x] and ND[y,x]<2 and Mz[y,x] not in (1,2):
            log.write(f'({x},{y}) {L[y,x]}->{Mz[y,x]} D geen modellijn\n'); L[y,x]=Mz[y,x]; n+=1
print('D',n)
np.save(D+'r7/idx.npy',L); save_p64(L,PAL,D+'r7/sprite.png'); save_idx(L,PAL,D+'r7/r7_10x.png',10)
