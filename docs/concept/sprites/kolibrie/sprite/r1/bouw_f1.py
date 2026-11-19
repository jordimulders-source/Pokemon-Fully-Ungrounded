# Frame 1: onderlaag_f1 -> frame1.png (opschonen + per-pixel reparaties), log per zone
import json,numpy as np; from PIL import Image
from schoon import *
P=json.load(open('plaats.json'))
from bron import bron
a0,lum,_=bron('f1')
Y,X=np.mgrid[0:64,0:64]
Z={'kop+oog+snavel':(X<=20)&(Y>=20)&(Y<=37),'kuif':(X>=12)&(X<=23)&(Y>=11)&(Y<=21),
   'vleugels':(X>=27)&(Y<=30)&(Y>=5)&~((Y>=24)&(X<=36)), 'lijf+schouder':(X>=6)&(Y>=21)&(Y<=41)&(X<=49),
   'staart':(X>=40)&(Y>=36), 'zielvlammen':(Y>=42)&np.isin(a0,[11,12,13,14])}
Z['lijf+schouder']&=~Z['vleugels']&~Z['kop+oog+snavel']; Z['staart']&=~Z['zielvlammen']
a=a0.copy()
ver=Z['vleugels']&(X< 41-(Y-18)*1.15)&(Y<=30); nabij=Z['vleugels']&~ver
a=vleugeldrempel(a,lum,ver,[(150,4),(170,12),(999,13)])
a=vleugeldrempel(a,lum,nabij,[(150,4),(168,12),(212,13),(999,14)])
a=randlijn(a,Z['vleugels']|Z['zielvlammen'])
besch=np.zeros((64,64),bool)
for x,y in [(12,27),(12,28),(13,28)]: besch[y,x]=1            # oog (glans + iris)
besch[(X<=8)&(Y>=28)]=1                                          # snavel
a=spikkels(a,Z['vleugels']|Z['lijf+schouder']|Z['zielvlammen'],besch)
# --- per-pixel reparaties (x,y,oud,nieuw,reden) ---
a[(Z['lijf+schouder']|Z['kop+oog+snavel'])&(a==6)]=5   # lijfgroep max 3 tinten (5/7/8); 6 alleen in de staartslierten
lijnzone=((Z['lijf+schouder']|Z['kop+oog+snavel'])&np.isin(a,[3,5,6,7,8,9,11,15]) | Z['staart']&np.isin(a,[7,8]))&~besch
a=buitenlijn(a,lijnzone,schaduwkant=((1,0),(1,1)))
FIX=json.load(open('fix_f1.json')) if __import__('os').path.exists('fix_f1.json') else []
for x,y,old,new,why in FIX:
    assert a[y,x]==old,(x,y,a[y,x],old,why); a[y,x]=new
save(a,'frame1.png'); print(zones_log(a0,a,Z))
