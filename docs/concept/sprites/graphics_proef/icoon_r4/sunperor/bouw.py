"""r4: onderlaag Sunperor met kroon en kop APART geschaald (reparatie van r3, waar kroon+kop als één groep x1,2/x1,45 gingen).
 kop (masker+snavel+ogen) 1,25xS breed / 1,45xS hoog rond het halsgewricht (28,31) (vogel-kopfactor);
 kroon KR x S (1,0-1,1) rond zijn aanhechting op de kruin (28,19), die de kop-transformatie volgt -> kroon blijft boven de kop;
 overige groepen als r3 (romp 1,0; vleugel 0,95; poten 0,75 lang; staf 1,55/0,78; kroonpunt 0,6 aan de kroon).
 Vaste plaatsing TR = r3 (-5,2): romp, staf, hand, vleugel en poten liggen pixel voor pixel waar r3 ze had.
 Lijfkleur: bruinzwart (front 2,3) -> 14 (98,98,90, zoals Honchkrow/Noctowl het lijf vullen) i.p.v. grijs 1.
python3 bouw.py naam [KR drempel] -> <naam>.png (32x32, pal5)"""
import sys,os,numpy as np
from collections import Counter
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,H); import delen as Dl
ROOT=H+'../../../../../../'
a=sys.argv
naam=a[1]; KR=float(a[2]) if len(a)>2 else 1.05; DREMPEL=float(a[3]) if len(a)>3 else 0.45
S=0.36; KB,KH,PL=1.25,1.45,0.75
fr=np.array(Image.open(Dl.FRONT))[:64]; lab=np.load(H+'delen.npy'); names=[d[0] for d in Dl.DELEN]
NEK=np.array([28.0,31.0]); KRUIN=np.array([28.0,19.0])
G={'romp':(np.zeros(2),None,S,S),
   'kop':(NEK,'romp',KB*S,KH*S),'kroon':(KRUIN,'kop',KR*S,KR*S),
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
MAP={2:14,3:14,4:6,5:10,6:10,7:13,8:11,9:12,10:6,11:8,12:9,13:1,14:3,15:6}
IP=np.array([[int(v) for v in l.split()[:3]] for l in open(ROOT+'graphics/pokemon/icon_palettes/pal5.pal').read().split('\n')[3:19]])
OFF=np.array([10.0,6.0]); TR=np.array([-5,2])
def naar_icoon(x,y,n): return OFF+T((x,y),n)+TR
def laag(groepen):
    out=np.zeros((32,32),np.uint8)
    for n in groepen:
        ids=[i for i,m in enumerate(names) if m==n]; pm=np.isin(lab,ids)
        for Y in range(32):
            for X in range(32):
                (sx,sy),k=Tinv(np.array([X,Y],float)-OFF-TR,n)
                x0,y0=int(np.floor(sx)),int(np.floor(sy)); x1,y1=int(np.ceil(sx+k[0])),int(np.ceil(sy+k[1]))
                if x1<=0 or y1<=0 or x0>=64 or y0>=64: continue
                x0,y0=max(0,x0),max(0,y0); x1,y1=min(64,x1),min(64,y1)
                sel=pm[y0:y1,x0:x1]
                if sel.size==0 or sel.mean()<DREMPEL: continue
                v=fr[y0:y1,x0:x1][sel]; dk=np.isin(v,list(DONKER))
                out[Y,X]=15 if dk.mean()>0.5 else MAP[Counter(v[~dk].tolist()).most_common(1)[0][0]]
    return out
res=laag(['kroon','kroonpunt','vleugel','poten','romp','staf','hand','kop'])
mm=res>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
res[edge]=15
if __name__=='__main__':
    im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()); im.save(H+f'{naam}.png',transparency=0)
    ys,xs=np.nonzero(res); print(naam,'KR',KR,'maat',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'rijen',ys.min(),ys.max())
    for p,n in [((22,19),'kop'),((34,27),'kop'),((24,23),'kop'),((29,23),'kop'),((6,0),'kroon'),((51,22),'kroon'),((28,0),'kroon')]: print(p,n,naar_icoon(*p,n).round(1))
