# Ledian-evolutie r1: model OVERNEMEN. natief.png (natief.py) -> palet -> gaten -> schrappen -> kaal.png
# Daarna alleen technische reparaties (lijst REPARATIES), elk met reden -> ledian_evo_r1.png
import numpy as np, sys
from PIL import Image
from collections import deque
D='docs/concept/sprites/ledian_evo/sprite_r1/'
a=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(int)[15:81,17:83]   # bbox 66x66
PAL=[(0,0,0),            # 0 transparant
 (16,16,16),             # 1 omlijning zwart
 (0x2a,0x29,0x29),       # 2 donkergrijs (sprieten, gewrichten, lijnen)
 (0x64,0x64,0x64),       # 3 grijs
 (0xa0,0xa1,0xa2),       # 4 vuist schaduw
 (0xc3,0xc4,0xc5),       # 5 vuist midden
 (0xf8,0xf8,0xf8),       # 6 wit (vuist, oogglans)
 (0x8d,0x19,0x22),       # 7 donkerrood (selout/lijn op rood)
 (0xb0,0x27,0x2e),       # 8 rood schaduw
 (0xe5,0x44,0x44),       # 9 rood
 (0xf4,0x73,0x71),       # 10 rood licht
 (0xfa,0xe3,0x75),       # 11 geel licht
 (0xd5,0xae,0x36)]       # 12 goud
H=W=66
nw=(a>=0xe0).all(2)
bg=np.zeros((H,W),bool); q=deque()
for y in range(H):
    for x in range(W):
        if (y in(0,H-1) or x in(0,W-1)) and nw[y,x]: bg[y,x]=1; q.append((y,x))
while q:
    y,x=q.popleft()
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        Y,X=y+dy,x+dx
        if 0<=Y<H and 0<=X<W and nw[Y,X] and not bg[Y,X]: bg[Y,X]=1; q.append((Y,X))
C=np.array(PAL[1:]); idx=((a[:,:,None,:]-C[None,None])**2).sum(3).argmin(2)+1
idx[bg]=0
# ingesloten achtergrond (in het model wit = achtergrond die door een gat schijnt): transparant
for y,x in [(29,9),(51,40)]:     # zaadpunt: spleet arm/hoofd, spleet tussen de benen
    st=[(y,x)]; assert idx[y,x]==6
    while st:
        Y,X=st.pop()
        if 0<=Y<H and 0<=X<W and idx[Y,X]==6:
            idx[Y,X]=0; st+= [(Y+1,X),(Y-1,X),(Y,X+1),(Y,X-1)]
ROWS=[54,57]; COLS=[61,63]       # benen (recht stuk) en vleugel (recht stuk vóór de punt)
k=np.delete(np.delete(idx,ROWS,0),COLS,1)
assert k.shape==(64,64)
def save(arr,fn):
    im=Image.fromarray(arr.astype('uint8'),'P'); flat=[c for p in PAL for c in p]; flat+=[0]*(768-len(flat))
    im.putpalette(flat); im.save(D+fn,transparency=0)
save(k,'kaal.png')
s=k.copy()
# REPARATIES (y,x,nieuwe index,reden) op 64x64-coordinaten
REPARATIES=[]
exec(open(D+'reparaties.py').read()) if len(sys.argv)<2 else None
for y,x,v,why in REPARATIES: s[y,x]=v
save(s,'ledian_evo_r1.png')
print('kleuren',len(set(s.flatten())),'afwijkend t.o.v. kaal',int((s!=k).sum()))
