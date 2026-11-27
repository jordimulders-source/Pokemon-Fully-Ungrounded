# r1: kale reductie (geschrapt model) -> eigen glaspalet (dichtstbijzijnde kleur, gewogen op helderheid)
# -> buitenrand = lijn (zwart aan de schaduwkant, donkerrood aan de lichtkant), AA-randpixels buiten de modellijn weg.
from PIL import Image; import numpy as np, sys
sys.path.insert(0,'docs/concept/sprites/hitmonlee_regional/sprite')
from toon import save_idx
D='docs/concept/sprites/hitmonlee_regional/sprite/'
B=np.asarray(Image.open(D+'r1/geschrapt.png').convert('RGB')).astype(float)
F=np.load(D+'r1/fig.npy').copy()
PAL=[(0,0,0),
 (44,20,16),    #1 lijn zwartbruin
 (112,40,32),   #2 donkerrood (lijn lichtkant / ringlijn)
 (168,52,40),   #3 rood donker
 (216,80,48),   #4 rood
 (240,120,56),  #5 oranjerood
 (248,160,80),  #6 oranje
 (250,200,112), #7 licht oranjegeel
 (252,236,168), #8 bleekgeel
 (255,255,255), #9 wit
 (236,168,148), #10 roze glans op rood
 (140,92,76),   #11 doorschijnend donker (ring/been)
 (188,144,120), #12 doorschijnend midden
 (228,204,184), #13 doorschijnend licht
]
P=np.array(PAL,float)
def near(c):
    d=((P[1:]-c)**2*np.array([1,1.3,0.8])).sum(1)
    return int(d.argmin())+1
H,W,_=B.shape
L=np.zeros((H,W),int)
for y in range(H):
    for x in range(W):
        if F[y,x]: L[y,x]=near(B[y,x])
lum=B.mean(2)
def isrand(y,x,M):
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if not(0<=yy<H and 0<=xx<W) or not M[yy,xx]: return True
    return False
# AA buiten de modellijn weg
weg=[]
for y in range(H):
    for x in range(W):
        if F[y,x] and isrand(y,x,F) and lum[y,x]>=150:
            inn=[lum[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W and F[y+dy,x+dx]]
            if inn and min(inn)<90: weg.append((y,x))
for y,x in weg: F[y,x]=False; L[y,x]=0
np.save(D+'r1/fig_r1.npy',F)
# buitenlijn
nzw=nrood=0
for y in range(H):
    for x in range(W):
        if F[y,x] and isrand(y,x,F):
            # schaduwkant = buiten ligt rechts of onder
            sch = (y+1>=H or not F[y+1,x]) or (x+1>=W or not F[y,x+1])
            if lum[y,x]<70 or sch: L[y,x]=1; nzw+=1
            else: L[y,x]=2; nrood+=1
print('AA weg',len(weg),'lijn zwart',nzw,'donkerrood',nrood)
np.save(D+'r1/idx.npy',L)
save_idx(L,PAL,D+'r1/r1_10x.png',10)
from toon import save_p64
save_p64(L,PAL,D+'r1/sprite.png')
