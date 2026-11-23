import os,sys,numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
for p in ('..','../r2','../r3','../r5'): sys.path.insert(0,os.path.join(H,p))
from veld import licht,tint,yy,xx
from r2 import LIJF
R5=np.array(Image.open(os.path.join(H,'../r5/claydol_r10kop_r5.png'))).astype(int)
VAST6=[(22,44),(23,44),(24,44),(24,45),(24,46),(25,46),(26,46),(33,44),(34,44),(35,44),(31,45),(33,45),(31,46),(32,46),(33,46),(31,47),
 (21,43),(20,43),(22,42),(21,44),(21,45),(21,46),(21,47),(18,47),(19,48),(20,49),(47,47),(46,48),(46,49),(45,50),
 (39,40),(39,41),(40,42),(40,43),(41,44),(40,45),(39,46),(39,47),(42,49),(42,50),(42,51),(41,52),(39,53),(40,53),(41,53),(42,53),
 (36,51),(37,51),(23,54),(24,54),(25,54),(26,54),(29,56),(30,56),(30,57)]
NAAD={40:39,41:39,42:40,43:40,44:41,45:40,46:39,47:39,48:40,49:42,50:42,51:42,52:41}
def delen():
    vul=LIJF&(yy>=40)&~np.isin(R5,(7,8,9))
    for x,y in VAST6: vul[y,x]=False
    D=np.zeros((64,64),'U5')
    for y,x in zip(*np.where(vul)):
        if y<=50 and (x<=20 or (x<=22 and y<=42)): D[y,x]='armL'
        elif y in NAAD and x>NAAD[y]: D[y,x]='armR'
        elif y<=42: D[y,x]='hals'
        elif y<=54: D[y,x]='romp'
        elif x<=30: D[y,x]='voetL'
        else: D[y,x]='voetR'
    return D
DR=[(0.60,2),(0.32,3),(0.02,5),(-0.45,10),(-9,6)]
def schets(reflectie=False):
    D=delen(); S=R5.copy()
    for x,y in VAST6: S[y,x]=6
    S[np.isin(R5,(8,))]=9
    G=licht(30,50,20,14)
    loc={'romp':licht(30,48,11,8.5),'armL':licht(17.5,46,4.5,4.5),'armR':licht(45.5,47,5.5,5.5),
         'hals':licht(31,44,10,5),'voetL':licht(26.5,55.5,5,3),'voetR':licht(37.5,56.5,6.5,3.5)}
    w={'romp':0.5,'armL':0.5,'armR':0.5,'hals':0.3,'voetL':0.45,'voetR':0.45}
    for k,Lk in loc.items():
        L=(1-w[k])*G+w[k]*Lk
        if k=='hals': L=L-0.45           # schaduw van de kop
        m=D==k; T=tint(L,DR); S[m]=T[m]
    if reflectie:
        for y,x in zip(*np.where((D=='romp')|(D=='voetR')|(D=='voetL')|(D=='armR'))):
            if S[y,x] in (6,10) and R5[y+1,x]==7 and xx[y,x]>=27: S[y,x]={6:10,10:5}[S[y,x]]
    return S,D
def txt(S):
    H_='0123456789A'
    return {y:''.join(H_[S[y,x]] if (LIJF[y,x] and y>=40) else (H_[R5[y,x]] if R5[y,x] else '.') for x in range(13,52)) for y in range(40,61)}
if __name__=='__main__':
    for r in (0,1):
        S,D=schets(r); 
        for y,s in txt(S).items(): print(y,s)
        print()
        im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(Image.open(os.path.join(H,'../r5/claydol_r10kop_r5.png')).getpalette()); im.save(os.path.join(H,'schets%d.png'%r),transparency=0)
