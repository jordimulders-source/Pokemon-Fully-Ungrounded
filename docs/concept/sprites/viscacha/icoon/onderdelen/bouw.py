"""Icoon-onderlaag uit onderdelen van de front, met vaste factoren per groep (geen vrije vormen).
python3 bouw.py naam s_lijf s_kop   -> onderdelen/<naam>.png (32x32, pal2, ruwe onderlaag)"""
import sys,numpy as np
from PIL import Image
sys.path.insert(0,'docs/concept/sprites/viscacha/icoon/onderdelen'); import delen as Dl
D='docs/concept/sprites/viscacha/'
naam,s_l,s_k=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
fr=np.array(Image.open(D+'af/viscacha.png'))[:64]; L=open(D+'af/normal.pal').read().split('\n'); FP=np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(16)])
rgb=FP[fr].astype(float); lab=np.load(D+'icoon/onderdelen/delen.npy')
names=[d[0] for d in Dl.DELEN]
KOP={'kop','verre oor','nabije oor','elektrisch motief'}
NEK=np.array([21.0,38.0])        # halsgewricht (x,y) in de front: kop draait/schaalt hieromheen
lum=FP.mean(1); donker=lum[fr]<70
IP=np.array([[int(v) for v in l.split()[:3]] for l in open('graphics/pokemon/icon_palettes/pal2.pal').read().split('\n')[3:19]])
# doelpositie: lichaam geschaald met s_l rond (0,0); kopgroep met s_k rond NEK, NEK zelf met s_l
def doel(x,y,kop):
    off=np.array([12.0,8.0])
    if kop: return off+NEK*s_l+(np.array([x,y])-NEK)*s_k
    return off+np.array([x,y])*s_l
out=np.zeros((40,48),np.uint8)
def bron(X,Y,kop):
    off=np.array([12.0,8.0]); q=np.array([X,Y],float)-off
    if kop: return NEK+(q-NEK*s_l)/s_k, 1/s_k
    return q/s_l, 1/s_l
ORDE=['verre achterpoot','romp','dij en achtervoet','voorpoot','bef','opgeheven poot','verre oor','kop','elektrisch motief','nabije oor']
for n in ORDE:
    ids=[i for i,m in enumerate(names) if m==n]; pm=np.isin(lab,ids); kop=n in KOP
    for Y in range(40):
        for X in range(48):
            (sx,sy),k=bron(X,Y,kop)
            x0,y0=int(np.floor(sx)),int(np.floor(sy)); x1,y1=int(np.ceil(sx+k)),int(np.ceil(sy+k))
            if x1<=0 or y1<=0 or x0>=64 or y0>=64: continue
            x0,y0=max(0,x0),max(0,y0); x1,y1=min(64,x1),min(64,y1)
            sel=pm[y0:y1,x0:x1]
            if sel.size==0 or sel.mean()<0.45: continue
            c=rgb[y0:y1,x0:x1][sel]; dkk=donker[y0:y1,x0:x1][sel].mean()
            if dkk>0.5: out[Y,X]=15
            else:
                cc=rgb[y0:y1,x0:x1][sel & ~donker[y0:y1,x0:x1]].mean(0)
                out[Y,X]=((IP[1:14]-cc)**2).sum(1).argmin()+1
v8=np.array(Image.open(D+'icoon/maker/icon_v8.png'))[:32]
# staart uit v8 pixel voor pixel (x>=22, y<=22 in v8 frame 1), aanzet tegen de rugrand van het samengestelde lijf
T=[(x,y,v8[y,x]) for y in range(0,23) for x in range(22,32) if v8[y,x]]
yt=int(round(8+44*s_l)); row=np.nonzero(out[yt])[0]
xr=row.max() if len(row) else int(48*s_l)
dx=xr-22-1; dy=yt-22
for x,y,v in T:
    X,Y=x+dx,y+dy
    if 0<=Y<40 and 0<=X<48 and out[Y,X]==0: out[Y,X]=v
# bijsnijden en in 32x32 zetten (onderkant y29, midden 16)
ys,xs=np.nonzero(out); c=out[ys.min():ys.max()+1,xs.min():xs.max()+1]
h,w=c.shape; res=np.zeros((32,32),np.uint8)
oy=30-h; ox=16-w//2
for y in range(h):
    for x in range(w):
        if 0<=oy+y<32 and 0<=ox+x<32 and c[y,x]: res[oy+y,ox+x]=c[y,x]
# buitenrand donker (boven 15, onder 14)
mm=res>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)):
    if res[y,x] not in (8,9): res[y,x]=15 if y<mid else 14
im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()); im.save(D+f'icoon/onderdelen/{naam}.png')
print(naam,'maat',w,'x',h)
