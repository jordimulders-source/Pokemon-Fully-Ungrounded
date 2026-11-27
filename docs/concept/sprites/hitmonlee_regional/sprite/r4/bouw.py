# r4: onderlaag r3/v1. Palet van 15 (gemeten op k-means in Lab van het model + Gen 3-stappen),
# per pixel dichtstbijzijnde kleur in Lab (geen familiebeperking, zodat de doorschijnende bleke delen blijven).
# Losse 1-px-vlekjes -> meest voorkomende buurkleur als die in Lab dichtbij ligt (dE<30). Buitenlijn: 1 aan de schaduwkant
# (buiten rechts/onder) of waar het model donker is, anders 2.
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D)
from toon import save_idx, save_p64, lab
B=np.asarray(Image.open(D+'r3/v1/geschrapt.png').convert('RGB')).astype(float)
F=np.load(D+'r3/v1/fig.npy')
PAL=[(0,0,0),
 (32,16,12),(96,32,24),                       #1 lijn, 2 donkerrood
 (160,48,40),(216,72,48),(240,108,64),        #3-5 rood
 (248,148,80),(250,186,104),                  #6-7 oranje
 (252,224,144),(254,246,216),(255,255,255),   #8 geel, 9 kern, 10 glans
 (232,140,112),(244,196,172),                 #11-12 zalm/bleekroze (glas)
 (120,84,68),(204,156,128),(236,216,184)]     #13-15 doorschijnend donker/tan/creme
PL=lab(np.array(PAL[1:],float))
H,W,_=B.shape
BL=lab(B)
L=np.zeros((H,W),int)
d=((BL[...,None,:]-PL[None,None])**2).sum(-1); L=d.argmin(-1)+1; L[~F]=0
def rand(y,x,M):
    return any(not(0<=y+dy<H and 0<=x+dx<W) or not M[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
n=0; L2=L.copy()
for y in range(H):
    for x in range(W):
        if not F[y,x] or rand(y,x,F) or L[y,x] in (1,10): continue
        nb=[L[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
        if L[y,x] not in nb:
            k=max(set(nb),key=nb.count)
            if k!=0 and np.sqrt(((PL[k-1]-PL[L[y,x]-1])**2).sum())<30: L2[y,x]=k; n+=1
L=L2
lum=B.mean(2)
for y in range(H):
    for x in range(W):
        if F[y,x] and rand(y,x,F):
            sch=(y+1>=H or not F[y+1,x]) or (x+1>=W or not F[y,x+1])
            L[y,x]=1 if (lum[y,x]<60 or sch) else 2
print('losse',n,'kleuren',len(set(L.ravel())))
np.save(D+'r4/idx.npy',L)
save_p64(L,PAL,D+'r4/sprite.png'); save_idx(L,PAL,D+'r4/r4_10x.png',10)
