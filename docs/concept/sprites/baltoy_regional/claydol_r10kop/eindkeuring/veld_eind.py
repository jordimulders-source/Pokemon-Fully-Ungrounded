# Eindkeuring: SCHETS van één lichtveld voor het hele lijf (alleen als hulp; het eindraster staat als tekst in eind.py)
import os,sys,numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
for p in ('../r6','..','../r2','../r3','../r5'): sys.path.insert(0,os.path.join(H,p))
from schets import delen, VAST6
yy,xx=np.mgrid[0:64,0:64]
R6=np.array(Image.open(os.path.join(H,'../r6/claydol_r10kop_r6.png'))).astype(int)
LD=np.array([-0.55,-0.6,0.58]); LD/=np.linalg.norm(LD)
def bol(cx,cy,rx,ry):
    u=(xx+0.5-cx)/rx; v=(yy+0.5-cy)/ry; r2=np.clip(u*u+v*v,0,0.97)
    n=np.stack([u,v,np.sqrt(1-r2)]); return (n*LD[:,None,None]).sum(0)
def veld():
    D=delen()
    G=bol(31.5,50,13,12)                       # één ton: hals+romp+onderlijf
    L=G.copy()
    loc={'armL':bol(17,46.5,5,4.5),'armR':bol(45,46.5,6,5),'voetL':bol(27,55,6,4),'voetR':bol(36,56,8,5)}
    for k,Lk in loc.items():
        m=D==k; L[m]=0.45*G[m]+0.55*Lk[m]
    # slagschaduw van de kop: rand loopt van linksboven (rij 41) schuin naar rechtsonder (rij 47 bij x 40), gebogen
    ys=41.0+6.5*np.clip((xx-21)/19,0,1)**1.4
    L=np.where(yy+0.5<ys, np.minimum(L, -0.05-0.25*np.clip((xx-24)/14,0,1)), L)
    return L,D
DR=[(0.62,2),(0.38,3),(0.08,5),(-0.25,10),(-9,6)]
def tint(L):
    T=np.full(L.shape,DR[-1][1])
    for g,t in reversed(DR[:-1]): T[L>=g]=t
    return T
if __name__=='__main__':
    L,D=veld(); T=tint(L)
    for y in range(38,62):
        print('%2d '%y+''.join(('%X'%T[y,x] if D[y,x] else ('%X'%R6[y,x] if R6[y,x] else '.')) for x in range(12,53)))
