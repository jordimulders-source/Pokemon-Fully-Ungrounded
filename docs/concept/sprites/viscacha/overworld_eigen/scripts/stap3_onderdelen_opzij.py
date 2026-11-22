"""Stap 3: onderlaag opzij uit de onderdelen van de front (zelfde polygonen als het icoon: icoon/onderdelen/delen.py),
met vaste factoren per groep uit de OW-meetstudie (RESULTAAT.md):
 - lijf: hoogte 0,39 x front (figuur opzij), lengte x1,17 -> sx 0,45, sy 0,39
 - kopgroep (kop + wangmotief) rond het halsgewricht: kop wordt +-9 x 9 px (front-kop 22 x 14 zonder snorharen) -> sx 0,43, sy 0,60
 - oren: 3-4 px boven de kop -> 0,40 (oor 1,9 + 0,19 x front)
 - opgeheven poot vervalt (OW-opzij: 2 poten op de grond, wordt in stap 4 met de hand neergezet)
Kleur per doelpixel = meest voorkomende frontkleur in de bronvlek (geen gemiddelde -> geen blur), donker wint bij >45%.
Gebruik: python3 stap3_onderdelen_opzij.py [sx_l sy_l sx_k sy_k s_o] -> werk/opzij_onderdelen.txt"""
import sys,os,numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H); from ow_pal import *
R=os.path.abspath(os.path.join(H,'../../../../../..')); D=R+'/docs/concept/sprites/viscacha/'
sys.path.insert(0,D+'icoon/onderdelen'); import delen as Dl
v=[float(x) for x in sys.argv[1:6]] if len(sys.argv)>5 else [0.45,0.39,0.43,0.60,0.40]
sxl,syl,sxk,syk,so=v
fr=np.array(Image.open(D+'af/viscacha.png'))[:64]; lab=np.load(D+'icoon/onderdelen/delen.npy'); names=[d[0] for d in Dl.DELEN]
# frontindex -> OW-index (zelfde kleur; omlijning 1 -> 2)
F2O={1:2,2:3,3:4,4:5,5:6,6:8,7:9,8:10,9:11,10:12,11:7,12:13,13:14,14:4,15:15}
NEK=np.array([24.0,36.0])
G={'kop':'k','elektrisch motief':'k','verre oor':'o','nabije oor':'o'}
ORDE=['verre achterpoot','romp','dij en achtervoet','voorpoot','bef','staart','verre oor','kop','elektrisch motief','nabije oor']
out=np.zeros((48,48),np.uint8)
def tf(g):
    if g=='k': return sxk,syk
    if g=='o': return so,so
    return sxl,syl
for n in ORDE:
    ids=[i for i,m in enumerate(names) if m==n]; pm=np.isin(lab,ids); g=G.get(n,'l'); sx,sy=tf(g)
    for Y in range(48):
        for X in range(48):
            # doel = off + NEK*s_lijf + (bron-NEK)*s_groep
            bx=NEK[0]+(X-8-NEK[0]*sxl)/sx; by=NEK[1]+(Y-8-NEK[1]*syl)/sy
            x0,y0=int(np.floor(bx)),int(np.floor(by)); x1,y1=int(np.ceil(bx+1/sx)),int(np.ceil(by+1/sy))
            x0,y0=max(0,x0),max(0,y0); x1,y1=min(64,x1),min(64,y1)
            if x1<=x0 or y1<=y0: continue
            sel=pm[y0:y1,x0:x1]
            if sel.mean()<0.45: continue
            c=fr[y0:y1,x0:x1][sel]
            if (c==1).mean()>0.45: out[Y,X]=2; continue
            c=c[c!=1]; vals,cnt=np.unique(c,return_counts=True); out[Y,X]=F2O[int(vals[cnt.argmax()])]
ys,xs=np.nonzero(out); c=out[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=c.shape
res=np.zeros((32,32),np.uint8); oy=30-h; ox=16-w//2
for y in range(h):
    for x in range(w):
        if 0<=oy+y<32 and 0<=ox+x<32 and c[y,x]: res[oy+y,ox+x]=c[y,x]
open(H+'/../werk/opzij_onderdelen.txt','w').write(totext(res)+'\n'); print('maat',w,'x',h); print(totext(res))
