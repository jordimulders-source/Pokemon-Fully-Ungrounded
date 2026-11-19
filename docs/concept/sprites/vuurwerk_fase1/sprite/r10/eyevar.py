# varianten nabij oog (rij 14-17, kol 22-24) naar het Mudkip-oog (Gen 3: zwarte ring, glans binnenin); model: oog kol 22.4-24.6, rij 14.3-16.6
import numpy as np, sys; from PIL import Image, ImageDraw
from txt import CH; from reduce2 import PAL
I={c:i for i,c in enumerate(CH)}
A=np.load('sprite_A.npy')
V={'nu':"",
 'V1 k-hoeken':"14,22=k 14,23=E 14,24=k 15,22=E 15,23=w 15,24=E 16,22=k 16,23=E 16,24=k",
 'V2 b-hoeken':"14,22=b 14,23=E 14,24=b 15,22=E 15,23=w 15,24=E 16,22=b 16,23=E 16,24=b",
 'V4 3x4 (Mudkip)':"14,22=k 14,23=E 14,24=k 15,22=E 15,23=w 15,24=E 16,22=E 16,23=E 16,24=E 17,22=k 17,23=E 17,24=k"}
def var(sp):
    a=A.copy()
    for t in sp.split():
        rc,v=t.split('='); r,c=map(int,rc.split(',')); a[r,c]=I[v]
    return a
def rgb(a,r0,r1,c0,c1,Z):
    x=PAL[a[r0:r1,c0:c1]].astype('uint8'); x[a[r0:r1,c0:c1]==0]=255
    return Image.fromarray(x).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
ims=[]
for k,sp in V.items():
    a=var(sp); np.save('eye_'+k.split()[0]+'.npy',a); ims.append((k,[rgb(a,3,23,12,30,10),rgb(a,0,30,0,30,2)]))
W=sum(i.width+i2.width+20 for _,(i,i2) in ims); H=max(i.height for _,(i,_) in ims)+16
o=Image.new('RGB',(W,H),(225,225,225)); d=ImageDraw.Draw(o); x=0
for k,(i,i2) in ims:
    d.text((x,0),k,fill=0); o.paste(i,(x,14)); o.paste(i2,(x+i.width+4,14)); x+=i.width+i2.width+20
o.save(sys.argv[1])
