import numpy as np
from PIL import Image
from collections import deque
si=np.array(Image.open('sprite_r3/sprite.png')); S=si>0
kaal=np.load('sprite_r1/kaal.npy')>0
def edges(m):
    P=[]
    for y in range(16,53): P.append(('L',y,int(np.where(m[y,:30])[0].min())))
    for x in list(range(2,13))+list(range(27,30)): P.append(('T',int(16+np.where(m[16:40,x])[0].min()),x))
    for x in range(2,29): P.append(('B',int(np.where(m[30:60,x])[0].max()+30),x))
    for y in list(range(25,34))+list(range(39,44)):
        r=m[y,20:]; P.append(('R',y,int(20+np.argmin(r)-1)))
    return P
def fit(P):
    pts=np.array([(x+0.5,y+0.5) for _,y,x in P],float)
    A=np.c_[2*pts,np.ones(len(pts))]; b=(pts**2).sum(1)
    cx,cy,c=np.linalg.lstsq(A,b,rcond=None)[0]; r=np.sqrt(c+cx*cx+cy*cy)
    return cx,cy,r,pts
for nm,m in (('sprite',S),('kaal model',kaal)):
    P=edges(m); cx,cy,r,pts=fit(P)
    d=np.hypot(pts[:,0]-cx,pts[:,1]-cy)-r
    print(f'{nm}: centrum ({cx:.1f},{cy:.1f}) r={r:.2f}')
    for q,cond in (('linksboven',(pts[:,0]<cx)&(pts[:,1]<cy)),('linksonder',(pts[:,0]<cx)&(pts[:,1]>=cy)),('rechtsboven',(pts[:,0]>=cx)&(pts[:,1]<cy)),('rechtsonder',(pts[:,0]>=cx)&(pts[:,1]>=cy))):
        dd=d[cond]; i=np.argmax(np.abs(dd)); p=pts[cond][i]
        print(f'  {q}: max afwijking {dd[i]:+.2f} px bij (x{int(p[0])},y{int(p[1])}), rms {np.sqrt((dd**2).mean()):.2f}')
    big=[(k,y,x,round(float(dv),2)) for (k,y,x),dv in zip(P,d) if abs(dv)>0.7]
    print('  punten >0.7 px:',big)
def seq(m):
    L=[int(np.where(m[y,:30])[0].min()) for y in range(16,53)]
    B=[int(np.where(m[30:60,x])[0].max()+30) for x in range(2,29)]
    T=[int(16+np.where(m[16:40,x])[0].min()) for x in range(2,31)]
    def rl(v):
        out=[];c=1
        for a,b in zip(v,v[1:]):
            if a==b:c+=1
            else: out.append(c);c=1
        out.append(c);return out
    return L,rl(L),T,rl(T),B,rl(B)
for nm,m in (('sprite',S),('kaal',kaal)):
    L,rL,T,rT,B,rB=seq(m)
    print(nm,'links x per rij 16-52',L,'\n   trappen (rijen per x)',rL)
    print('   boven y per kol 2-30',T,'\n   trappen (kol per y)',rT)
    print('   onder y per kol 2-28',B,'\n   trappen (kol per y)',rB)
