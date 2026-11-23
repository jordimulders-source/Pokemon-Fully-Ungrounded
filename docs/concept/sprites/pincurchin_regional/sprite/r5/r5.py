# r5: linkeroog 3 breed (ring|pupil|ring: kolom 1 van het c3-oog geschrapt), evt. 6 hoog (ringrij 1 herhaald);
# 115%-mond verschoven (dx,dy) zodat er lijf tussen oog en mond zit. Basis = opbouw r4/R2 (oog voor mond).
import numpy as np
from PIL import Image
from toon import save
from mond import maak
pin=np.array(Image.open('../../../../../../graphics/pokemon/pincurchin/anim_front.png'))[:64].astype(int)
MAP={3:0,10:8,9:9,7:10,5:11,8:12,11:13}
OOG=pin[39:44,27:32]; C3=np.delete(OOG,3,1); O35=np.delete(C3,1,1); O36=np.insert(O35,1,O35[1],0)
A2=np.load('../r2/A.npy'); B2=np.load('../r2/B.npy'); kaal=np.load('../r1/schoon.npy'); R2=np.load('../r4/R2.npy')
def zet(A,oog,y0,x0):
    m=np.zeros((64,64),bool)
    for j in range(oog.shape[0]):
        for i in range(oog.shape[1]):
            v=oog[j,i]
            if v in MAP: A[y0+j,x0+i]=MAP[v]; m[y0+j,x0+i]=True
    return m
ozone=np.zeros((64,64),bool); ozone[38:44,13:18]=True; ozone[39:45,28:33]=True
def bouw(oog,y0,dx,dy):
    A=A2.copy(); A[ozone]=kaal[ozone]
    ml=zet(A,oog,y0,14); mr=zet(A,OOG,40,28)
    Bb=B2.copy(); Bb[ozone]=A[ozone]
    B,niet,over,vak=maak(A,Bb,ml|mr,1.15,dx,dy)
    # oog-mond-afstand: kleinste afstand (Chebyshev) tussen linkeroog en mond
    mond=np.isin(B,[12,13])|((B==0)&(B!=A)); mond&=~(ml|mr)
    my,mx=np.where(mond); ey,ex=np.where(ml)
    gap=min(max(abs(a-c),abs(b-d)) for a,b in zip(my,mx) for c,d in zip(ey,ex))-1
    return B,niet,over,gap,mond
reg=np.zeros((64,64),bool); reg[36:52,12:31]=True   # oog- en mondgebied
VAR={'V1_oog3x5_mond+1+1':(O35,39,1,1),'V2_oog3x5_mond+2+1':(O35,39,2,1),'V3_oog3x6_mond+1+1':(O36,38,1,1)}
for k,(o,y0,dx,dy) in VAR.items():
    B,niet,over,gap,mond=bouw(o,y0,dx,dy)
    my,mx=np.where(mond)
    np.save(k+'.npy',B); save(B,k+'.png')
    print(k,'| lijf tussen oog en mond:',gap,'px | mond x',mx.min(),mx.max(),'y',my.min(),my.max(),
          '| niet uit geschaalde mond',niet,'| oogpx onder mond',over,'| diff buiten oog/mond (x12-30,y36-51) t.o.v. R2:',((B!=R2)&~reg).sum())
for o in (O35,O36): print('\n'.join(''.join({10:'A',9:'9',7:'7',5:'5'}.get(v,'.') for v in r) for r in o)); print()
