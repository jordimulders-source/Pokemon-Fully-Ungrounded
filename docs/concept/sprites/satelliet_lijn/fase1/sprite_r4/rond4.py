# rond4.py: cirkelfit op de buitenlijn van de bol (zonder voetjes/antennes) + trappen. python3 rond4.py [npy]
import numpy as np, sys
m=np.load(sys.argv[1] if len(sys.argv)>1 else 'sprite.npy')>0
P=[]
for y in range(23,49): P.append(('L',y,int(np.where(m[y,:30])[0].min())))
for x in range(9,19): P.append(('T',int(np.where(m[20:40,x])[0].min()+20),x))
for x in range(9,30): P.append(('B',int(np.where(m[36:60,x])[0].max()+36),x))
for y in list(range(29,36))+list(range(40,43)): r=m[y,25:]; P.append(("R",y,int(25+np.argmin(r)-1)))
pts=np.array([(x+0.5,y+0.5) for _,y,x in P],float)
A=np.c_[2*pts,np.ones(len(pts))]; b=(pts**2).sum(1); cx,cy,c=np.linalg.lstsq(A,b,rcond=None)[0]; r=np.sqrt(c+cx*cx+cy*cy)
d=np.hypot(pts[:,0]-cx,pts[:,1]-cy)-r
print(f'centrum ({cx:.1f},{cy:.1f}) r={r:.2f}')
for q,cond in (('linksboven',(pts[:,0]<cx)&(pts[:,1]<cy)),('linksonder',(pts[:,0]<cx)&(pts[:,1]>=cy)),('rechtsboven',(pts[:,0]>=cx)&(pts[:,1]<cy)),('rechtsonder',(pts[:,0]>=cx)&(pts[:,1]>=cy))):
    dd=d[cond]; i=np.argmax(np.abs(dd)); p=pts[cond][i]
    print(f'  {q}: max {dd[i]:+.2f} px bij (x{int(p[0])},y{int(p[1])}), rms {np.sqrt((dd**2).mean()):.2f}')
def rl(v):
    out=[];c=1
    for a,b2 in zip(v,v[1:]):
        if a==b2:c+=1
        else: out.append(c);c=1
    return out+[c]
L=[int(np.where(m[y,:30])[0].min()) for y in range(22,50)]
B=[int(np.where(m[36:60,x])[0].max()+36) for x in range(9,30)]
print('links x per rij 22-49',L,'\n  trappen (rijen per x)',rl(L))
print('onder y per kol 9-29',B,'\n  trappen (kol per y)',rl(B))
