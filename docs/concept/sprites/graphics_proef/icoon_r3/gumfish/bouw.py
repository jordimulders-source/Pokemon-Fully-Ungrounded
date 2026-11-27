"""Icoon-onderlaag Gumfish uit onderdelen van de front, met vaste factoren per groep
(kopie van viscacha/icoon/onderdelen/bouw.py, aangepast aan REGELS_PER_BOUW.md 'Vis / zwemmer':
 lijf 1,3xS in de lengte en 1,0xS in de hoogte, kop 1,3-1,5xS vast aan de voorkant, vinnen/staart 1,0xS aan hun aanhechting).
python3 bouw.py naam S kop [lijflengte staart]  -> <naam>.png (32x32, pal0, ruwe onderlaag)
Kleur per icoonpixel = meest voorkomende frontkleur in het bronvak (les 27 nov), via MAP naar pal0 (zie pal.txt)."""
import sys,os,numpy as np
from collections import Counter
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,H); import delen as Dl
ROOT=H+'../../../../../../'
naam,S,KF=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
LL=float(sys.argv[4]) if len(sys.argv)>4 else 1.3   # lijf in de lengte (meting 1,16-1,34)
ST=float(sys.argv[5]) if len(sys.argv)>5 else 1.0
DREMPEL=float(sys.argv[6]) if len(sys.argv)>6 else 0.45   # minimale dekking van een onderdeel in het bronvak   # staartvin; minimum staart 3,0+0,32xf (f=12 -> 6,8 px) vraagt ±1,2
fr=np.array(Image.open(Dl.FRONT))[:64]; lab=np.load(H+'delen.npy')
names=[d[0] for d in Dl.DELEN]
LIJF=np.array([LL*S,1.0*S])     # romp: langer, niet hoger
# groep: (anker in de front, schaal x, schaal y); anker ligt op het lijf en volgt de romptransformatie
GROEP={'kop':(np.array([24.0,42.0]),KF*S,KF*S),         # halsgewricht vis: grens kop/romp, midden flank
       'staartvin':(np.array([46.0,34.0]),ST*S,ST*S),          # aanhechting staart op de rug
       'borstvin':(np.array([30.0,41.0]),S,S)}           # aanhechting borstvin (voorrand)
DONKER={1,2}
MAP={4:6,6:6,9:10,10:10,11:11,13:3}
IP=np.array([[int(v) for v in l.split()[:3]] for l in open(ROOT+'graphics/pokemon/icon_palettes/pal0.pal').read().split('\n')[3:19]])
OFF=np.array([4.0,8.0])
def doel(x,y,n):
    p=np.array([x,y],float)
    if n in GROEP: A,sx,sy=GROEP[n]; return OFF+A*LIJF+(p-A)*np.array([sx,sy])
    return OFF+p*LIJF
def bron(X,Y,n):
    q=np.array([X,Y],float)-OFF
    if n in GROEP: A,sx,sy=GROEP[n]; s=np.array([sx,sy]); return A+(q-A*LIJF)/s, 1/s
    return q/LIJF, 1/LIJF
out=np.zeros((48,64),np.uint8)
ORDE=['staartvin','romp','borstvin','kop']
for n in ORDE:
    ids=[i for i,m in enumerate(names) if m==n]; pm=np.isin(lab,ids)
    for Y in range(48):
        for X in range(64):
            (sx,sy),k=bron(X,Y,n)
            x0,y0=int(np.floor(sx)),int(np.floor(sy)); x1,y1=int(np.ceil(sx+k[0])),int(np.ceil(sy+k[1]))
            if x1<=0 or y1<=0 or x0>=64 or y0>=64: continue
            x0,y0=max(0,x0),max(0,y0); x1,y1=min(64,x1),min(64,y1)
            sel=pm[y0:y1,x0:x1]
            if sel.size==0 or sel.mean()<DREMPEL: continue
            v=fr[y0:y1,x0:x1][sel]; dk=np.isin(v,list(DONKER))
            if dk.mean()>0.5: out[Y,X]=15
            else: out[Y,X]=MAP[Counter(v[~dk].tolist()).most_common(1)[0][0]]
ys,xs=np.nonzero(out); c=out[ys.min():ys.max()+1,xs.min():xs.max()+1]
h,w=c.shape; res=np.zeros((32,32),np.uint8); oy=30-h; ox=16-w//2
for y in range(h):
    for x in range(w):
        if 0<=oy+y<32 and 0<=ox+x<32 and c[y,x]: res[oy+y,ox+x]=c[y,x]
TR=np.array([ox-xs.min(),oy-ys.min()])
def naar_icoon(x,y,n): return doel(x,y,n)+TR
def bron_icoon(X,Y,n): return bron(X-TR[0],Y-TR[1],n)
mm=res>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)): res[y,x]=15 if y<mid else 14
if __name__=='__main__':
    im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()); im.save(H+f'{naam}.png',transparency=0)
    print(naam,'S',S,'kop',KF,'lijf',LL,'staart',ST,'maat',w,'x',h)
