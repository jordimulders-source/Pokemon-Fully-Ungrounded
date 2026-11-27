# r3: onderlaag r3/v1 (natief 5,12 -> 2x met lijnregel -> geschrapt), verder als r2 (familiepalet, losse pixels, buitenlijn).
# (rood/oranje/geel/doorschijnend), per pixel alleen kleuren uit de eigen familie (tint blijft zoals het model).
# Daarna: losse 1-px-vlekjes in vulling -> meest voorkomende buurkleur binnen dezelfde familie. Buitenlijn als r1.
from PIL import Image; import numpy as np, sys, colorsys
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D)
from toon import save_idx, save_p64
B=np.asarray(Image.open(D+'r3/v1/geschrapt.png').convert('RGB')).astype(float)
F=np.load(D+'r3/v1/fig.npy')
PAL=[(0,0,0),
 (36,18,16),(104,40,34),          #1 lijn, 2 donkerrood
 (160,48,40),(208,68,50),(236,104,64), #3-5 rood
 (240,140,76),(246,176,100),       #6-7 oranje
 (250,214,130),(252,240,168),(255,255,240), #8-10 geel/wit
 (240,152,128),                    #11 roze glans
 (128,104,96),(204,176,160),(240,224,204)] #12-14 doorschijnend
FAM={'line':[1,2],'red':[2,3,4,5,11],'orange':[5,6,7],'yellow':[7,8,9,10],'desat':[12,13,14,10]}
P=np.array(PAL,float)
H,W,_=B.shape
def fam(c):
    l=c.mean()
    if l<70: return 'line'
    h,s,v=colorsys.rgb_to_hsv(*(c/255)); h*=360
    if s<0.25: return 'desat'
    if h<20 or h>340: return 'red'
    if h<35: return 'orange'
    return 'yellow'
Fm=np.empty((H,W),object); L=np.zeros((H,W),int)
for y in range(H):
    for x in range(W):
        if not F[y,x]: continue
        f=fam(B[y,x]); Fm[y,x]=f
        ks=FAM[f]; d=[((P[k]-B[y,x])**2).sum() for k in ks]
        L[y,x]=ks[int(np.argmin(d))]
def rand(y,x):
    return any(not(0<=y+dy<H and 0<=x+dx<W) or not F[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
# losse pixels
n=0
L2=L.copy()
for y in range(H):
    for x in range(W):
        if not F[y,x] or rand(y,x) or L[y,x] in (1,10): continue
        nb=[L[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
        if L[y,x] not in nb:
            ok=[k for k in nb if k in FAM[Fm[y,x]] and k!=1]
            if ok:
                L2[y,x]=max(set(ok),key=ok.count); n+=1
L=L2
lum=B.mean(2)
for y in range(H):
    for x in range(W):
        if F[y,x] and rand(y,x):
            sch=(y+1>=H or not F[y+1,x]) or (x+1>=W or not F[y,x+1])
            L[y,x]=1 if (lum[y,x]<70 or sch) else 2
print('losse',n)
np.save(D+'r3/idx.npy',L); np.save(D+'r3/fam.npy',Fm)
save_p64(L,PAL,D+'r3/sprite.png'); save_idx(L,PAL,D+'r3/r2_10x.png',10)
