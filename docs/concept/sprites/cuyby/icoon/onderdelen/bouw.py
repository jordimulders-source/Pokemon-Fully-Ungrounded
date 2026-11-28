"""Cuyby-icoon: onderlaag uit onderdelen van de front (aangepast van viscacha/icoon/onderdelen/bouw.py + delen.py).
Verschil met de viscacha: kleur per vak = meerderheid van de gemapte frontindices (geen gemiddelde -> geen blur).
python3 bouw.py naam pal s_lijf s_kop s_oren   (vanuit de repo-root) -> onderdelen/<naam>.png (32x32)"""
import sys,numpy as np
from PIL import Image,ImageDraw
D='docs/concept/sprites/cuyby/'
naam,PAL=sys.argv[1],int(sys.argv[2]); s_l,s_k,s_o=map(float,sys.argv[3:6])
fr=np.array(Image.open(D+'ronde4/anim_front.png'))[:64]
DELEN=[  # naam, polygoon (x,y); eerste match wint
 ('oor zwart',[(18,14),(26,14),(26,20),(18,20)]),
 ('oor oranje',[(38,15),(45,15),(45,19),(41,20),(38,19)]),
 ('onderlijf',[(0,37),(63,37),(63,63),(0,63)]),
 ('kop',[(0,0),(63,0),(63,37),(0,37)]),
]
lab=np.zeros((64,64),np.int8)-1
for i,(n,poly) in reversed(list(enumerate(DELEN))):
    m=Image.new('L',(64,64),0); ImageDraw.Draw(m).polygon(poly,fill=1,outline=1); lab[(np.array(m)>0)&(fr>0)]=i
# frontindex -> icoonindex (per icoonpalet; donker = 1 omlijning, 14 oogzwart -> 15)
MAP={0:{2:3,3:3,4:2,5:2,6:7,7:7,8:6,9:6,10:1,11:14,12:11,13:10,15:6},
     3:{2:3,3:11,4:12,5:12,6:13,7:13,8:8,9:8,10:1,11:14,12:7,13:7,15:8}}[PAL]
IP=np.array([[int(v) for v in l.split()[:3]] for l in open(f'graphics/pokemon/icon_palettes/pal{PAL}.pal').read().split('\n')[3:19]])
NEK=np.array([31.0,37.0]); off=np.array([8.0,8.0])
S={'oor zwart':s_o,'oor oranje':s_o,'kop':s_k,'onderlijf':s_l}
out=np.zeros((48,48),np.uint8)
for i,(n,_) in enumerate(DELEN[::-1]):
    i=len(DELEN)-1-i; pm=lab==i; s=S[n]
    for Y in range(48):
        for X in range(48):
            q=np.array([X,Y],float)-off
            sx,sy=NEK+(q-NEK*s_l)/s; k=1/s
            x0,y0=int(np.floor(sx)),int(np.floor(sy)); x1,y1=int(np.ceil(sx+k)),int(np.ceil(sy+k))
            x0,y0=max(0,x0),max(0,y0); x1,y1=min(64,x1),min(64,y1)
            if x1<=x0 or y1<=y0: continue
            sel=pm[y0:y1,x0:x1]
            if sel.size==0 or sel.mean()<0.45: continue
            v=fr[y0:y1,x0:x1][sel]
            if np.isin(v,[1,14]).mean()>0.5: out[Y,X]=15; continue
            mv=[MAP[int(t)] for t in v if t not in (1,14)]
            out[Y,X]=max(set(mv),key=mv.count)
ys,xs=np.nonzero(out); c=out[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=c.shape
res=np.zeros((32,32),np.uint8); oy=29-h+1; ox=16-w//2
res[oy:oy+h,ox:ox+w]=c
mm=res>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)): res[y,x]=15 if y<mid else 14
im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()); im.save(D+f'icoon/onderdelen/{naam}.png')
print(naam,'maat',w,'x',h)
for y in range(32):
    r=''.join('.' if v==0 else '%x'%v for v in res[y])
    if r.strip('.'): print('%2d '%y+r)
