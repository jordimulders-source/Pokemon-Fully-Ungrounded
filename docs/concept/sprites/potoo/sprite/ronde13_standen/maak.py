"""Ronde 13: standen van ronde 12 met het lijf FK x zo groot (FK=0.90/0.85/0.80/0.75).\nRonde 12: als 11, lijf ineengedoken (kop voorover), staart korter, kop groter op de sprite.\nRonde 11: kop = Jordi's omtrek, lijf en staart overgetrokken van de foto op de tak (op het oog geschaald).\nRonde 9: Jordi's omtrek (vorm vast) + lijf van ronde 3 in de juiste verhouding.
Alles in J-coördinaten (pixels van jordi_overtrek/overtrek_v1.webp): de kop is zijn lijn (lijn_J.npy + gaatjes),
het lijf is de omtrek van ronde 3 (rijen 28-62), uniform geschaald zodat kaakpunt (x19) en rug (x46) van ronde 3
op zijn kaakpunt (360,925) en rug (1095) vallen. Daarna alles samen naar 64x64 (1 spritepixel = K J-pixels)."""
import json, numpy as np
from PIL import Image, ImageDraw
from collections import deque, Counter
from scipy import ndimage as nd
from skimage.morphology import skeletonize
LIJN=np.load('../../jordi_overtrek/lijn_J.npy')
H,W=3200,1400
GATEN=[[(638,83),(720,111)],[(825,150),(861,200)],[(1031,404),(1036,452)],[(400,457),(437,470)],[(1120,707),(1115,753)],
       [(454,751),(433,781)],[(1118,799),(1110,850),(1095,940)],[(229,107),(223,114)],[(156,234),(153,243)],[(93,310),(88,313)],
       [(204,375),(231,375)],[(91,400),(88,403)]]
D=json.load(open('../../jordi_overtrek/omtrek_cellen.json')); HALS=[tuple(p) for p in D['hals_J']]
kop=Image.new('L',(W,H),0); kop.paste(Image.fromarray((LIJN*255).astype(np.uint8)),(0,0)); d=ImageDraw.Draw(kop)
for g in GATEN: d.line(g,fill=255,width=3)
hals=Image.new('L',(W,H),0); ImageDraw.Draw(hals).line(HALS,fill=255,width=5)
# lijf + staart overgetrokken van referenties/jordi_great_potoo_tak_bek_open_volledig.png (gespiegeld, 3x),
# geschaald op het oog (24 px op de foto = 145 J): J = oog_J + (X - oog_foto)/s
s3=24/145*3; ex3,ey3=(335-188)*3,176*3
# Jordi 6 nov: lijf iets kleiner zodat de bek groot wordt; zit op de tak als op die foto, maar ineengedoken met de kop
# voorover (referenties/jordi_great_potoo_bek_open_ineengedoken.png: oog -> zitplek 6,9 oog). Onder de kaakpunt (Y 820)
# wordt het lijf samengedrukt tot de tak op oog + 7,0 oog; staart onder de tak 0,73x (6,7 -> 4,9 oog); 0,5 oog naar achteren.
def yv(Y):
    if Y<=820: return Y
    if Y<=1290: return 820+(Y-820)*0.45
    return 820+470*0.45+(Y-1290)*0.73
J0=lambda X,Y:(427.9+(X-ex3)/s3, 327+(Y-ey3)/s3)
import os
FK=float(os.environ.get('FK','1.0'))   # lijf FK x zo groot (Jordi 6 nov: 10-25% kleiner t.o.v. kop en mond)
AY=925.0; AX=735.0; BOT0=J0(0,yv(1775))[1]
def krimp(p):
    x,y=p
    if y<=AY: return p
    t=(y-AY)/(BOT0-AY); fx=1-(1-FK)*t
    return (AX+(x-AX)*fx, AY+(y-AY)*FK)
J=lambda X,Y:krimp(J0(X+(36 if Y>760 else 0),yv(Y)))
VOOR=[(320,720),(300,800),(298,900),(302,1000),(322,1100),(360,1200),(400,1270),(470,1340),(540,1450),(570,1600),(600,1720),(640,1775)]
RUG=[(780,750),(790,800),(815,900),(835,1000),(845,1100),(835,1200),(815,1300),(800,1400),(790,1500),(760,1600),(720,1700),(680,1775)]
VLEUGEL=[(720,620),(745,800),(765,1000),(785,1200),(790,1300)]
le=[J(*p) for p in VOOR]; re=[J(*p) for p in RUG]
lijf=Image.new('L',(W,H),0); d=ImageDraw.Draw(lijf)
d.line(le,fill=255,width=3); d.line(re,fill=255,width=3); d.line([(1095,940),re[0]],fill=255,width=3); d.line([le[-1],re[-1]],fill=255,width=3)
vl=Image.new('L',(W,H),0); ImageDraw.Draw(vl).line([J(*p) for p in VLEUGEL],fill=255,width=3)
# naar spritepixels
Y0=33; K=(le[-1][1]-Y0)/62.0; X0=32-(min(p[0] for p in le)+max(p[0] for p in re))/2/K
def cel(x,y): return int(np.floor(x/K+X0)), int(np.floor((y-Y0)/K))+1
def rast(img,dil=2):
    a=np.array(img)>0; a=skeletonize(nd.binary_dilation(a,iterations=dil)); ys,xs=np.nonzero(a)
    c=Counter(cel(x,y) for x,y in zip(xs,ys)); return {k for k,v in c.items() if v>=2}
KOP,HL,LF,VL=rast(kop),rast(hals),rast(lijf),rast(vl)
ox,oy=(261.67*2-181)*1.25,(223.33*2-185)*1.25; rx,ry=29*2.5/K,27*2.5/K; ex,ey=ox/K+X0,(oy-Y0)/K+1
OOG={(x,y) for x in range(64) for y in range(64) if ((x+.5-ex)/rx)**2+((y+.5-ey)/ry)**2<=1}
def dun(S):
    a=np.zeros((64,64),bool)
    for x,y in S:
        if 0<=x<64 and 0<=y<64: a[y,x]=True
    a=skeletonize(a); return {(x,y) for y,x in zip(*np.nonzero(a))}
KOP,HL,LF,VL=dun(KOP),dun(HL),dun(LF),dun(VL)
L=KOP|HL|LF
G=[['.']*64 for _ in range(64)]
out=set(); q=deque([(0,0)])
while q:
    x,y=q.popleft()
    if (x,y) in out or not(0<=x<64 and 0<=y<64) or (x,y) in L: continue
    out.add((x,y)); q.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
mx,my=cel(250,600); mond=set(); q=deque([(mx,my)])
while q:
    x,y=q.popleft()
    if (x,y) in mond or (x,y) in L or (x,y) in out: continue
    mond.add((x,y)); q.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
assert len(mond)<500,'muil lekt'
ty=cel(360,925)[1]          # rij van de kaakpunt: daaronder het lijf van ronde 3
my_=[y for x,y in mond]; m0,m1=min(my_),max(my_)
def hx(y):
    xs=[x for x,yy in HL if yy==y]; return max(xs) if xs else None
for y in range(64):
    for x in range(64):
        if (x,y) in out or (x,y) in L: continue
        if (x,y) in mond:
            t=(y-m0)/max(1,m1-m0); G[y][x]='9' if t<.2 else 'A' if t<.55 else 'B' if t<.85 else 'C'
        elif y>ty:
            v=[xx for xx,yy in VL if yy==y]
            G[y][x]='4' if (v and x>max(v)) else ('3' if y>cel(0,J(0,1295)[1])[1] else '5')
        else:
            h=hx(y); G[y][x]='4' if (h is not None and x>h) else ('6' if y<6 else '5')
for x,y in L:
    if 0<=x<64 and 0<=y<64: G[y][x]='2' if (x,y) in HL and (x,y) not in KOP else '1'
for x,y in VL:
    if G[y][x] not in '.1': G[y][x]='2'
for x,y in OOG: G[y][x]='8'
open(os.environ.get('OUT','raster.txt'),'w').write('\n'.join(''.join(r) for r in G)+'\n')
print('K',round(K,1),'kaakpunt rij',ty,'muil',len(mond))
