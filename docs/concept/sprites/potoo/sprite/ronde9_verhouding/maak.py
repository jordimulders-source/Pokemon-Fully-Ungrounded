"""Ronde 9: Jordi's omtrek (vorm vast) + lijf van ronde 3 in de juiste verhouding.
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
# lijf van ronde 3
R3=[l.rstrip('\n').ljust(64,'.') for l in open('../ronde3/raster.txt')][:64]
# verhouding uit Jordi's foto's (tak_bek_open_volledig: oog 24 px, oogmidden->staartpunt 414 px = 17,3 oog; lijf max 185 px = 7,7 oog;
# leidraad: oog 58 fotopx = 145 J-px): lijf onder de kaakpunt tot 327+17,3*145 J, breedste punt 7,7*145 J.
import sys
EYE=145; BOT=327+17.3*EYE; WMAX=7.7*EYE
r3w=max((lambda xs:(max(xs)-min(xs)+1) if xs else 0)([i for i,c in enumerate(R3[y]) if c!='.']) for y in range(29,63))
FV=(BOT-925)/(62-28); FH=WMAX/r3w
J=lambda x,y:(1095-(46-x)*FH, 925+(y-28)*FV)
F=FH
le,re=[],[]
for y in range(29,63):
    xs=[i for i,c in enumerate(R3[y]) if c!='.']
    if xs: le.append(J(min(xs),y+.5)); re.append(J(max(xs)+1,y+.5))
lijf=Image.new('L',(W,H),0); d=ImageDraw.Draw(lijf)
d.line([(360,925),le[0]]+le,fill=255,width=3); d.line([(1095,940)]+re,fill=255,width=3); d.line([le[-1],re[-1]],fill=255,width=3)
# naar spritepixels
Y0=33; K=(le[-1][1]-Y0)/62.0; X0=32-(min(min(p[0] for p in le),55)+1120)/2/K
def cel(x,y): return int(np.floor(x/K+X0)), int(np.floor((y-Y0)/K))+1
def rast(img,dil=2):
    a=np.array(img)>0; a=skeletonize(nd.binary_dilation(a,iterations=dil)); ys,xs=np.nonzero(a)
    c=Counter(cel(x,y) for x,y in zip(xs,ys)); return {k for k,v in c.items() if v>=2}
KOP,HL,LF=rast(kop),rast(hals),rast(lijf)
ox,oy=(261.67*2-181)*1.25,(223.33*2-185)*1.25; rx,ry=29*2.5/K,27*2.5/K; ex,ey=ox/K+X0,(oy-Y0)/K+1
OOG={(x,y) for x in range(64) for y in range(64) if ((x+.5-ex)/rx)**2+((y+.5-ey)/ry)**2<=1}
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
            # kleur van ronde 3 op de overeenkomstige plek
            Jx,Jy=(x+.5-X0)*K,(y-.5)*K+Y0; rx3=int(46-(1095-Jx)/FH); ry3=int(28+(Jy-925)/FV)
            c=R3[min(62,ry3)][min(63,max(0,rx3))] if 0<=ry3<64 else '.'
            G[y][x]=c if c not in '.1' else '4'
        else:
            h=hx(y); G[y][x]='4' if (h is not None and x>h) else ('6' if y<6 else '5')
for x,y in L:
    if 0<=x<64 and 0<=y<64: G[y][x]='2' if (x,y) in HL and (x,y) not in KOP else '1'
for x,y in OOG: G[y][x]='8'
open('raster.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
print('K',round(K,1),'kaakpunt rij',ty,'muil',len(mond))
