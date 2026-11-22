"""Route 'chibi op 64, dan exact 2x':
1) chibi op frontschaal: de KOP (kop, oren, elektrisch motief) blijft 1:1 (geen hersampling!);
   lijf/poten/staart worden met nearest-neighbour verkleind (factor s_lijf/0.5) rond de hals.
2) exact 2x2-reductie met regels: glans wint, donkere lijn bij >=2 donkere pixels, geel bij >=2 geel, anders meest voorkomende tint.
Het gezicht gaat dus alleen door een exacte halvering met regels.
python3 chibi2x.py naam s_lijf"""
import sys,numpy as np
from PIL import Image
sys.path.insert(0,'docs/concept/sprites/viscacha/icoon/onderdelen'); import delen as Dl
D='docs/concept/sprites/viscacha/'
naam=sys.argv[1]; s_l=float(sys.argv[2]); f=s_l/0.5
fr=np.array(Image.open(D+'af/viscacha.png'))[:64]; lab=np.load(D+'icoon/onderdelen/delen.npy'); names=[d[0] for d in Dl.DELEN]
KOP={'kop','verre oor','nabije oor','elektrisch motief'}
kopm=np.isin(lab,[i for i,n in enumerate(names) if n in KOP])
NEK=np.array([21,38]); H=W=96; O=np.array([20,20])
c=np.zeros((H,W),np.uint8)
# lijf eerst (nearest, rond NEK), dan kop 1:1 erover
for Y in range(H):
    for X in range(W):
        sx,sy=NEK+(np.array([X,Y])-O-NEK)/f
        sx,sy=int(np.floor(sx)),int(np.floor(sy))
        if 0<=sx<64 and 0<=sy<64 and fr[sy,sx] and not kopm[sy,sx]: c[Y,X]=fr[sy,sx]
ys,xs=np.nonzero(kopm&(fr>0))
for y,x in zip(ys,xs): c[y+O[1],x+O[0]]=fr[y,x]
Image.fromarray(c,'P').save(D+f'icoon/onderdelen/{naam}_64.png')
# exacte 2x2-reductie met regels (frontindexen)
DONKER={1}; GEEL={8,9,10,11}; WIT={13}
h=w=H//2; o=np.zeros((h,w),np.uint8)
L=open(D+'af/normal.pal').read().split('\n'); FP=np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(16)])
IP=np.array([[int(v) for v in l.split()[:3]] for l in open('graphics/pokemon/icon_palettes/pal2.pal').read().split('\n')[3:19]])
def naar_icoon(k):
    if k in GEEL: return 9 if FP[k].mean()>170 else 8
    return int(((IP[1:14]-FP[k])**2).sum(1).argmin()+1)
for j in range(h):
    for i in range(w):
        b=c[2*j:2*j+2,2*i:2*i+2].ravel(); b=b[b>0]
        if len(b)<2: continue
        s=set(b.tolist())
        if s&WIT: o[j,i]=3; continue
        if sum(v in DONKER for v in b)>=2: o[j,i]=15; continue
        g=[v for v in b if v in GEEL]
        if len(g)>=2: o[j,i]=naar_icoon(max(set(g),key=g.count)); continue
        r=[v for v in b if v not in DONKER] or list(b)
        o[j,i]=naar_icoon(max(set(r),key=r.count))
ys,xs=np.nonzero(o); cc=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; hh,ww=cc.shape
res=np.zeros((32,32),np.uint8); oy,ox=30-hh,16-ww//2
res[max(0,oy):oy+hh,max(0,ox):ox+ww]=cc[max(0,-oy):,max(0,-ox):][:32-max(0,oy),:32-max(0,ox)]
mm=res>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)):
    if res[y,x] not in (8,9,3): res[y,x]=15 if y<mid else 14
im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()); im.save(D+f'icoon/onderdelen/{naam}.png'); print(naam,ww,'x',hh)
