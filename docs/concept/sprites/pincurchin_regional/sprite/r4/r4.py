# r4: linkeroog (c3) — R1 1 px naar rechts, mond voor het oog; R2 idem, oog voor de mond; R3 oog op x13-16, kolom x13 weer lijfrand.
import numpy as np
from PIL import Image
from toon import save
from mond import maak
pin=np.array(Image.open('../../../../../../graphics/pokemon/pincurchin/anim_front.png'))[:64].astype(int)
MAP={3:0,10:8,9:9,7:10,5:11,8:12,11:13}
OOG=pin[39:44,27:32]; C3=np.delete(OOG,3,1)
A2=np.load('../r2/A.npy'); B2=np.load('../r2/B.npy'); kaal=np.load('../r1/schoon.npy')
R3B=np.load('../r3/B115_c3.npy')
def zet(A,oog,y0,x0):
    m=np.zeros((64,64),bool)
    for j in range(oog.shape[0]):
        for i in range(oog.shape[1]):
            v=oog[j,i]
            if v in MAP: A[y0+j,x0+i]=MAP[v]; m[y0+j,x0+i]=True
    return m
ozone=np.zeros((64,64),bool); ozone[39:44,13:18]=True; ozone[39:45,28:33]=True
def bouw(lx,oog_voor):
    A=A2.copy(); A[ozone]=kaal[ozone]
    ml=zet(A,C3,39,lx); mr=zet(A,OOG,40,28)
    Bb=B2.copy(); Bb[ozone]=A[ozone]
    B,niet,over,vak=maak(A,Bb,(ml|mr) if oog_voor else mr,1.15)
    return B,niet
reg=np.zeros((64,64),bool); reg[37:47,12:21]=True
uit={}
uit['R1'],n1=bouw(14,False); uit['R2'],n2=bouw(14,True)
# losse mondlijnpixel (17,39) boven het oog: alleen het oog als buur -> lijf (zoals de losse pixel in r3)
for k in ('R1','R2'): uit[k][39,17]=kaal[39,17]
n1+=1; n2+=1
R3=R3B.copy()
for y in (40,41,42): R3[y,13]=kaal[y,13]
uit['R3']=R3
print('controle: r3-opbouw opnieuw (x13) == r3/B115_c3:',(bouw(13,True)[0]==R3B).all())
for k,B in uit.items():
    np.save(k+'.npy',B); save(B,k+'.png')
    print(k,'diff t.o.v. r3 B115_c3:',(B!=R3B).sum(),'| buiten x12-20,y37-46:',((B!=R3B)&~reg).sum())
print('px niet uit geschaalde mond: R1',n1,'R2',n2)
