"""Icoon-onderlaag Sunperor uit onderdelen van de front, met vaste factoren per groep
(kopie van viscacha/icoon/onderdelen/bouw.py, aangepast aan REGELS_PER_BOUW.md 'Rechtop vogel'):
 kopgroep (kroon + kop) KB x S breed / KH x S hoog rond het halsgewricht; romp 1,0 x S; vleugel 0,95 x S aan de schouder;
 poten S breed / PL x S lang aan de heup (stompjes >= 2 px); staf dikker (1,55 x S) en korter (0,78 x S) aan de hand;
 lange veerpunt van de kroon 0,6 x S aan zijn aanhechting op de kroon.
python3 bouw.py naam S [KB KH PL drempel] -> <naam>.png (32x32, pal5, ruwe onderlaag)
Kleur per icoonpixel = meest voorkomende frontkleur in het bronvak (les 27 nov), via MAP naar pal5 (zie pal.txt)."""
import sys,os,numpy as np
from collections import Counter
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,H); import delen as Dl
ROOT=H+'../../../../../../'
a=sys.argv
naam,S=a[1],float(a[2]); KB=float(a[3]) if len(a)>3 else 1.2; KH=float(a[4]) if len(a)>4 else 1.45
PL=float(a[5]) if len(a)>5 else 0.75; DREMPEL=float(a[6]) if len(a)>6 else 0.45
fr=np.array(Image.open(Dl.FRONT))[:64]; lab=np.load(H+'delen.npy'); names=[d[0] for d in Dl.DELEN]
NEK=np.array([28.0,31.0])   # halsgewricht: onderkant masker, midden van de nek
# groep: (anker, oudergroep, sx, sy) ; anker volgt de transformatie van de ouder
G={'romp':(np.zeros(2),None,S,S),
   'kop':(NEK,'romp',KB*S,KH*S),'kroon':(NEK,'romp',KB*S,KH*S),
   'kroonpunt':(np.array([10.0,23.0]),'kroon',0.6*S,0.6*S),
   'vleugel':(np.array([37.0,30.0]),'romp',0.95*S,0.95*S),
   'poten':(np.array([29.0,53.0]),'romp',S,PL*S),
   'staf':(np.array([16.0,43.0]),'hand',1.55*S,0.78*S),
   'hand':(np.array([20.0,43.0]),'romp',S,S)}
def T(p,n):
    A,ouder,sx,sy=G[n]; p=np.asarray(p,float)
    if ouder is None: return p*np.array([sx,sy])
    return T(A,ouder)+(p-A)*np.array([sx,sy])
def Tinv(q,n):
    A,ouder,sx,sy=G[n]; s=np.array([sx,sy])
    if ouder is None: return q/s, 1/s
    return A+(q-T(A,ouder))/s, 1/s
DONKER={1}
MAP={2:1,3:1,4:6,5:10,6:10,7:13,8:11,9:12,10:6,11:8,12:9,13:1,14:3,15:6}   # dichtstbijzijnde in pal5 (bruinzwart -> grijs zoals Honchkrow; lichtbruin -> bruin)
IP=np.array([[int(v) for v in l.split()[:3]] for l in open(ROOT+'graphics/pokemon/icon_palettes/pal5.pal').read().split('\n')[3:19]])
OFF=np.array([10.0,6.0])
out=np.zeros((48,48),np.uint8)
ORDE=['kroon','kroonpunt','vleugel','poten','romp','staf','hand','kop']
for n in ORDE:
    ids=[i for i,m in enumerate(names) if m==n]; pm=np.isin(lab,ids)
    for Y in range(48):
        for X in range(48):
            (sx,sy),k=Tinv(np.array([X,Y],float)-OFF,n)
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
def naar_icoon(x,y,n): return OFF+T((x,y),n)+TR
mm=res>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)): res[y,x]=15 if y<mid else 14
if __name__=='__main__':
    im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()); im.save(H+f'{naam}.png',transparency=0)
    print(naam,'S',S,'kop',KB,KH,'poten',PL,'drempel',DREMPEL,'maat',w,'x',h)
