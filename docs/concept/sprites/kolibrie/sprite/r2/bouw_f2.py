# Frame 2: onderlaag_f2 (geschrapt natief raster) -> frame2.png, log per zone
import json,os,numpy as np; from PIL import Image
from schoon import *
from bron import bron
a0,lum,_=bron('f2')
Y,X=np.mgrid[0:64,0:64]
Z={'kop+oog+snavel':(X<=20)&(Y>=24),'kuif':(X>=9)&(X<=19)&(Y>=15)&(Y<=23),
   'vleugels':np.isin(a0,[4,11,12,13,14])&(Y<=30)&(X>=19)&(X<=50),
   'zielvlammen':np.isin(a0,[4,11,12,13,14])&(X>=51)&(Y<=32)}
Z['lijf+schouder']=(a0>0)&(X>=19)&(X<=40)&(Y>=17)&~Z['vleugels']&~Z['kop+oog+snavel']
Z['staart']=(a0>0)&(X>=41)&~Z['vleugels']&~Z['zielvlammen']
a=a0.copy()
ver=Z['vleugels']&(X<=29); nabij=Z['vleugels']&~ver
a=vleugeldrempel(a,lum,ver,[(150,4),(170,12),(999,13)])
a=vleugeldrempel(a,lum,nabij,[(150,4),(168,12),(212,13),(999,14)])
a=randlijn(a,Z['vleugels']|Z['zielvlammen'])
krul=Z['staart']&np.isin(a,[1,2,3,5,6,7,8,11,15])&(Y<=36)
a=toonband(a,lum,krul,[(30,1),(52,2),(85,5),(999,7)],glad=False)
besch=np.zeros((64,64),bool); besch[(X<=8)&(Y>=38)]=1
a=spikkels(a,Z['vleugels']|Z['lijf+schouder']|Z['zielvlammen'],besch)
a[(Z['lijf+schouder']|Z['kop+oog+snavel'])&(a==6)]=5   # lijfgroep max 3 tinten (5/7/8); 6 alleen in de staartslierten
lijnzone=((Z['lijf+schouder']|Z['kop+oog+snavel'])&np.isin(a,[3,5,6,7,8,9,11,15]) | Z['staart']&np.isin(a,[7,8]))&~besch
a=buitenlijn(a,lijnzone,schaduwkant=((1,0),(1,1)))
FIX=json.load(open('fix_f2.json')) if os.path.exists('fix_f2.json') else []
for x,y,old,new,why in FIX:
    assert a[y,x]==old,(x,y,a[y,x],old,why); a[y,x]=new
save(a,'frame2.png'); print(zones_log(a0,a,Z))
