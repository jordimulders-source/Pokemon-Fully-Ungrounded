"""Icoon-onderlaag Gumfish uit onderdelen van de front, met vaste factoren per groep (kopie van viscacha bouw.py).
python3 bouw.py naam s_lijf s_kop [s_staart]  -> <naam>.png (32x32, pal0, ruwe onderlaag)
Kleur per icoonpixel = meest voorkomende frontkleur in het bronvak (les 27 nov), via MAP naar pal0."""
import sys,os,numpy as np
from collections import Counter
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,H); import delen as Dl
ROOT=H+'../../../../../../'
naam,s_l,s_k=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
s_t=float(sys.argv[4]) if len(sys.argv)>4 else s_l
fr=np.array(Image.open(Dl.FRONT))[:64]; lab=np.load(H+'delen.npy')
names=[d[0] for d in Dl.DELEN]
KOP={'kop'}
NEK=np.array([24.0,42.0])        # 'halsgewricht' vis: grens kop/romp, midden van de flank
DONKER={1,2}                     # omlijning in de front
# front-index -> pal0-index (dichtstbijzijnde kleurtoon in pal0, toonvolgorde licht/midden behouden; zie pal.txt)
MAP={4:6,6:6,9:10,10:10,11:11,13:3}
IP=np.array([[int(v) for v in l.split()[:3]] for l in open(ROOT+'graphics/pokemon/icon_palettes/pal0.pal').read().split('\n')[3:19]])
OFF=np.array([10.0,10.0])
def bron(X,Y,n):
    q=np.array([X,Y],float)-OFF
    if n in KOP: return NEK+(q-NEK*s_l)/s_k, 1/s_k
    if n=='staartvin':  # staart schaalt rond zijn aanhechting (46,34) op de romp
        A=np.array([46.0,34.0]); return A+(q-A*s_l)/s_t, 1/s_t
    return q/s_l, 1/s_l
def doel(x,y,n):
    p=np.array([x,y],float)
    if n in KOP: return OFF+NEK*s_l+(p-NEK)*s_k
    if n=='staartvin': A=np.array([46.0,34.0]); return OFF+A*s_l+(p-A)*s_t
    return OFF+p*s_l
out=np.zeros((48,56),np.uint8)
ORDE=['staartvin','romp','borstvin','kop']
for n in ORDE:
    ids=[i for i,m in enumerate(names) if m==n]; pm=np.isin(lab,ids)
    for Y in range(48):
        for X in range(56):
            (sx,sy),k=bron(X,Y,n)
            x0,y0=int(np.floor(sx)),int(np.floor(sy)); x1,y1=int(np.ceil(sx+k)),int(np.ceil(sy+k))
            if x1<=0 or y1<=0 or x0>=64 or y0>=64: continue
            x0,y0=max(0,x0),max(0,y0); x1,y1=min(64,x1),min(64,y1)
            sel=pm[y0:y1,x0:x1]
            if sel.size==0 or sel.mean()<0.45: continue
            v=fr[y0:y1,x0:x1][sel]; dk=np.isin(v,list(DONKER))
            if dk.mean()>0.5: out[Y,X]=15
            else: out[Y,X]=MAP[Counter(v[~dk].tolist()).most_common(1)[0][0]]
ys,xs=np.nonzero(out); c=out[ys.min():ys.max()+1,xs.min():xs.max()+1]
h,w=c.shape; res=np.zeros((32,32),np.uint8); oy=30-h; ox=16-w//2
for y in range(h):
    for x in range(w):
        if 0<=oy+y<32 and 0<=ox+x<32 and c[y,x]: res[oy+y,ox+x]=c[y,x]
TR=np.array([ox-xs.min(),oy-ys.min()])   # canvas -> 32x32
def naar_icoon(x,y,n): return doel(x,y,n)+TR
mm=res>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)): res[y,x]=15 if y<mid else 14
if __name__=='__main__':
    im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()); im.save(H+f'{naam}.png',transparency=0)
    np.save(H+f'{naam}_tr.npy',np.array([s_l,s_k,s_t,*TR]))
    print(naam,'maat',w,'x',h,'TR',TR)
