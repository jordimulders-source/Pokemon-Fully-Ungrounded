# r10 = r9 + G: buitenlijn volgens Gen 3 (licht linksboven): randpixel met achtergrond rechts of onder = zwart (1),
#   anders (alleen boven/links open) = donkerrood selout (2). Daarna geen om-en-om: een randpixel waarvan beide
#   rand-buren (8-buren op de rand) het andere type zijn, neemt dat type over. Gelogd.
from PIL import Image; import numpy as np, sys
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']')
L=np.load(D+'r9/idx.npy').copy(); H,W=L.shape; F=L>0
rim=F&~ndimage.binary_erosion(F)
def bg(y,x): return not(0<=y<H and 0<=x<W) or not F[y,x]
log=open(D+'r10/log.txt','w')
T=np.zeros((H,W),int)
for y,x in zip(*np.where(rim)):
    T[y,x]=1 if (bg(y,x+1) or bg(y+1,x) or bg(y+1,x+1)) else 2
for it in range(3):
    for y,x in zip(*np.where(rim)):
        nb=[T[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W and rim[y+dy,x+dx]]
        if len(nb)>=2 and all(v!=T[y,x] for v in nb): T[y,x]=nb[0]
for y,x in zip(*np.where(rim)):
    if L[y,x]!=T[y,x]: log.write(f'({x},{y}) {L[y,x]}->{T[y,x]} G buitenlijn\n'); L[y,x]=T[y,x]
r=L[rim]; print('rand zwart',(r==1).sum(),'selout',(r==2).sum())
np.save(D+'r10/idx.npy',L); save_p64(L,PAL,D+'r10/sprite.png'); save_idx(L,PAL,D+'r10/r10_10x.png',10)
